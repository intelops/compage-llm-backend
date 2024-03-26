import os
from fastapi import APIRouter, HTTPException

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import OpenAI

from pkg.src.schemas.gpt import GPTRequest, validate_gpt_request
from pkg.src.config.database import get_session
from pkg.src.store.cassandra_chat_history import chat_history_store

router = APIRouter()
session = get_session()


@router.post("/unit_test_generate")
async def unit_test_generate(request_body: GPTRequest):
    """
    A function to generate code using OpenAI's GPT-3.5-Turbo-Instruct model.
    It takes a request body with GPTRequest type as parameters and returns the generated code in the specified language, along with a success status message.
    """
    try:

        validate_gpt_request(request_body)
        # Invoke chat history store
        chat_store = chat_history_store(session=session)

        # Set the OpenAI API key
        os.environ["OPENAI_API_KEY"] = request_body.openai_api_key

        # create the OPENAI Template for the code generation
        unit_test_template = PromptTemplate(
            input_variables=["prompt"],
            template="{prompt} \nThe code should be generated in markdown format.",
        )

        # use store for the conversation
        unit_test_memory = ConversationBufferMemory(
            input_key="prompt",
            memory_key="chat_history",
        )

        # create the OpenAI LLM model
        unit_test_llm = OpenAI(
            temperature=0.7,
            max_tokens=2048,
            model_name="gpt-3.5-turbo-instruct",
        )

        # create the LLM Chain
        unit_test_chain = LLMChain(
            llm=unit_test_llm,
            prompt=unit_test_template,
            memory=unit_test_memory,
            verbose=True,
            output_key="code",
        )

        response = unit_test_chain({"prompt": request_body.prompt})
        chat_store.add_user_message(request_body.prompt)
        chat_store.add_ai_message(response["code"])
        return {
            "status": "success",
            "data": {"code": response["code"]},
            "message": "Unit test generated successfully",
            "code": 200,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
