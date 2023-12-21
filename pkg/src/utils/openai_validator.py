import openai

def openai_apikey_valid(API_KEY: str):
    openai.api_key = API_KEY

    # Test if the API key is valid. If it is not, it will throw an error.
    # If it is valid, it will return True.
    try:
        openai.Completion.create(
            engine="davinci",
            prompt="This is a test of the OpenAI API. What is the meaning of life?",
            max_tokens=5,
        )
    except Exception as e:
        raise e
    else:
        return True
