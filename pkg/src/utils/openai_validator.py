import openai


def openai_apikey_valid(API_KEY: str):
    openai.api_key = API_KEY

    # Test if the API key is valid. If it is not, it will throw an error.
    # If it is valid, it will return True.
    try:
        openai.Completion.create(
            engine="davinci-codex",
            prompt="This is a test of the OpenAI API. What is the meaning of life?",
            max_tokens=5,
        )
    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors (e.g., invalid API key)
        print(f"Error: {e}")
        return False
    else:
        # The API key is valid if the request succeeds
        return True
