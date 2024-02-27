import os

from fastapi import APIRouter, Depends, HTTPException
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Langchain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import OpenAI

from pkg.src.config.database import get_session
from pkg.src.middleware.jwt_middleware import JWTBearer, get_current_username
from pkg.src.models.openAI_Token import OpenAI_Token
from pkg.src.schemas.gpt import GPTRequest
from pkg.src.store.cassandra_chat_history import chat_history_store

router = APIRouter()
session = get_session()


@router.post("/code_generate")
async def code_generate(request_body: GPTRequest, token: str = Depends(JWTBearer())):
    """
    A function to generate code using OpenAI's GPT-3.5-Turbo-Instruct model.
    It takes a request body with GPTRequest type and a JWT token as parameters, and returns the generated code in the specified language, along with a success status message.
    It also handles authentication and error scenarios using HTTPException.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if request_body.prompt == "":
        raise HTTPException(status_code=400, detail="prompt cannot be empty")
    if request_body.language == "":
        raise HTTPException(status_code=400, detail="language cannot be empty")

    # decode token for username
    username = get_current_username(token)

    chat_history = chat_history_store(username=username, session=session)

    # query to get api_key
    query = OpenAI_Token.objects.filter(username=username).allow_filtering()

    # get api-key from the store
    res = query.first()

    if query.count() < 1:
        raise HTTPException(status_code=401, detail="api-key not found!")

    os.environ["OPENAI_API_KEY"] = res["api_key"]

    # create the OPENAI Template for the code generation

    code_template = PromptTemplate(
        input_variables=["lang", "top"],
        template="{top}"
        + " using {lang} language with proper inline comments. The code and code explanation document should be in markdown code format.",
    )

    # use memory for the conversation
    code_memory = ConversationBufferMemory(input_key="top", memory_key="chat_history")

    # create the OpenAI LLM model
    open_ai_llm = OpenAI(
        temperature=0.7, max_tokens=2048, model="gpt-3.5-turbo-instruct"
    )

    # create the LLM chain
    code_chain = LLMChain(
        llm=open_ai_llm,
        prompt=code_template,
        memory=code_memory,
        verbose=True,
        output_key="code",
    )

    try:
        response = code_chain(
            {"lang": request_body.language, "top": request_body.prompt}
        )
        chat_history.add_user_message(request_body.prompt)
        chat_history.add_ai_message(response["code"])
        return {
            "status": "success",
            "data": {
                "code": response["code"],
            },
            "code": 200,
            "message": "Code generated successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={"message": "Error in generating code!", "error": str(e)},
        ) from e


@router.post("/doc_generate")
async def doc_generate(request_body: GPTRequest, token: str = Depends(JWTBearer())):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if request_body.prompt == "":
        raise HTTPException(status_code=400, detail="prompt cannot be empty")

    if request_body.language == "":
        raise HTTPException(status_code=400, detail="language cannot be empty")

    # decode token for username
    username = get_current_username(token)

    # query to get api_key
    query = OpenAI_Token.objects.filter(username=username).allow_filtering()

    # get api-key from the store
    res = query.first()

    if query.count() < 1:
        raise HTTPException(status_code=401, detail="api-key not found!")

    # main gpt logic begins here
    os.environ["OPENAI_API_KEY"] = res["api_key"]

    # create the OpenAI LLM model
    open_ai_llm = OpenAI(
        temperature=0.7, max_tokens=2048, model="gpt-3.5-turbo-instruct"
    )

    # prompt template for the code generation
    prompt_template = PromptTemplate(
        input_variables=["top"],
        template="{top} \n The documentation should be generated within 2048 tokens.",
    )

    # Tokenize the prompt into chunks
    prompt_chunks = tokenize_prompt(request_body.prompt)

    # Initialize memory and response
    documentation_memory = ConversationBufferMemory(
        input_key="top", memory_key="chat_history"
    )
    full_response = ""

    # Iterate through prompt chunks and make sequential calls
    for chunk in prompt_chunks:
        chain = LLMChain(
            llm=open_ai_llm,
            prompt=prompt_template,
            memory=documentation_memory,
            output_key="docs",
            verbose=True,
        )

        try:
            response = chain({"top": chunk})
            full_response += response["docs"]
            print(response)
            # Update memory for context
            documentation_memory.save_context(
                {"top": chunk}, outputs={"docs": response["docs"]}
            )

        except Exception as e:
            # Handle errors gracefully
            raise HTTPException(
                status_code=404,
                detail={"message": "Error generating documentation!", "error": str(e)},
            ) from e

    # Return the complete generated documentation
    return {
        "status": "success",
        "code": 200,
        "message": "Documentation generated successfully!",
        "data": {"docs": full_response},
    }


# Helper function for prompt tokenization
def tokenize_prompt(prompt, chunk_size=1000, chunk_overlap=200):
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    prompt_chunks = text_splitter.split_text(prompt)
    return prompt_chunks
