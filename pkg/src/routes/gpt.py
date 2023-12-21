import json
import os
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pkg.src.config.database import get_session
from pkg.src.middleware.jwt_middleware import JWTBearer, get_current_username
from pkg.src.models.openAI_Token import OpenAI_Token
from pkg.src.schemas.gpt import GPTRequest

# Langchain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import SequentialChain, LLMChain
from pkg.src.store.cassandra_chat_history import chat_history_store

router = APIRouter()
session = get_session()


@router.post("/code_generate")
async def code_generate(request_body: GPTRequest, token: str = Depends(JWTBearer())):
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

    # main gpt logic begins here
    os.environ["OPENAI_API_KEY"] = res["api_key"]

    # prompt template for the code generation
    code_template = PromptTemplate(
        input_variables=["lang", "top"],
        template="{top}"
        + " using {lang} language with proper inline comments. The code should be in markdown code format.",
    )

    # code_explain_template = PromptTemplate(
    #     input_variables=["top"],
    #     template="Explain in detail the working of the generated code and algorithm "
    #     + " for {top}"
    #     + " in proper markdown format",
    # )
    # code_flow_template = PromptTemplate(
    #     input_variables=["top"],
    #     template="Generate the diagram flow "
    #     + "for {top} in proper markdown format in mermaid code block",
    # )

    # code_testcase_template = PromptTemplate(
    #     input_variables=["lang", "top"],
    #     template="Generate the unit test cases and codes "
    #     + "and integration test cases with codes  "
    #     + "in  {lang}"
    #     + " for {top} in proper  markdown formats",
    # )

    # use memory for the conversation
    code_memory = ConversationBufferMemory(input_key="top", memory_key="chat_history")
    explain_memory = ConversationBufferMemory(
        input_key="top", memory_key="chat_history"
    )
    flow_memory = ConversationBufferMemory(input_key="top", memory_key="chat_history")
    testcase_memory = ConversationBufferMemory(
        input_key="top", memory_key="chat_history"
    )

    # create the  OpenAI LLM model
    open_ai_llm = OpenAI(temperature=0.7, max_tokens=1000)

    # create a chain to generate the code
    code_chain = LLMChain(
        llm=open_ai_llm,
        prompt=code_template,
        output_key="code",
        memory=code_memory,
        verbose=True,
    )
    #  create another chain to explain the code
    # code_explain_chain = LLMChain(
    #     llm=open_ai_llm,
    #     prompt=code_explain_template,
    #     output_key="code_explain",
    #     memory=explain_memory,
    #     verbose=True,
    # )

    # #  create another chain to generate the code flow if needed
    # code_flow_chain = LLMChain(
    #     llm=open_ai_llm,
    #     prompt=code_flow_template,
    #     output_key="code_flow",
    #     memory=flow_memory,
    #     verbose=True,
    # )

    # #  create another chain to generate the code flow if needed
    # code_testcase_chain = LLMChain(
    #     llm=open_ai_llm,
    #     prompt=code_testcase_template,
    #     output_key="code_unit_test",
    #     memory=testcase_memory,
    #     verbose=True,
    # )

    # create a sequential chain to combine both chains
    sequential_chain = SequentialChain(
        # chains=[code_chain, code_explain_chain, code_flow_chain, code_testcase_chain],
        chains=[code_chain],
        input_variables=["lang", "top"],
        # output_variables=["code", "code_explain", "code_flow", "code_unit_test"],
        output_variables=["code"],
    )

    try:
        response = sequential_chain(
            {"lang": request_body.language, "top": request_body.prompt}
        )

        chat_history.add_user_message(request_body.prompt)
        chat_history.add_ai_message(json.dumps(response))
        return {
            "status": "success",
            "code": 200,
            "message": "Code generated successfully!",
            "data": {
                "code": response["code"],
                # "code_explain": response["code_explain"],
                # "code_flow": response["code_flow"],
                # "code_unit_test": response["code_unit_test"],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={"message": "Error in generating code!", "error": str(e)},
        )


