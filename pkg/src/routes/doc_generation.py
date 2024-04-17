"""
This module provides a function to generate documentation using OpenAI's GPT-3.5-Turbo-Instruct model.
"""

import os

from fastapi import APIRouter, HTTPException
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Langchain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import OpenAI

from pkg.src.config.database import get_session
from pkg.src.schemas.gpt import GPTRequest, validate_gpt_request

router = APIRouter()
session = get_session()


@router.post("/doc_generate")
async def doc_generate(request_body: GPTRequest):
    """
    A function to generate documentation using OpenAI's GPT-3.5-Turbo-Instruct model.
    """
    try:
        validate_gpt_request(request_body)

        # set the OpenAI API key
        os.environ["OPENAI_API_KEY"] = request_body.openai_api_key

        # create the OpenAI LLM model
        open_ai_llm = OpenAI(
            temperature=0.7,
            max_tokens=2048,
            model="gpt-3.5-turbo-instruct",
        )

        # prompt template for the documentation generation
        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template="Generate documentation for the following code snippet in markdown code format: {prompt}",
        )

        # Tokenize the prompt into chunks
        prompt_chunks = tokenize_prompt(request_body.prompt)

        # Initialize memory and response
        doc_memory = ConversationBufferMemory(
            input_key="prompt",
            memory_key="chat_history",
        )

        full_response = ""

        # Iterate through prompt chunks and make sequential calls
        for chunk in prompt_chunks:
            chain = LLMChain(
                llm=open_ai_llm,
                prompt=prompt_template,
                memory=doc_memory,
                output_key="docs",
                verbose=True,
            )

            response = chain({"prompt": chunk})
            full_response += response["docs"]

            # Update memory for context
            doc_memory.save_context({"prompt": chunk}, outputs={"docs": response["docs"]})

        return {
            "status": "success",
            "code": 200,
            "message": "Documentation generated successfully",
            "data": {"docs": full_response},
        }

    except HTTPException as e:
        raise e from e


# Helper function for prompt tokenization
def tokenize_prompt(prompt, chunk_size=1000, chunk_overlap=200):
    """
    tokenizes the prompt into chunks
    """
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    prompt_chunks = text_splitter.split_text(prompt)
    return prompt_chunks
