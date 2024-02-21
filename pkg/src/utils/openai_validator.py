import openai


def openai_apikey_valid(api_key: str):
    """
    A function to set the OpenAI API key and test its validity.
    Takes in a string api_key and returns True if the key is valid, False otherwise.
    """

    openai.api_key = api_key

    # Test if the API key is valid. If it is not, it will throw an error.
    # If it is valid, it will return True.
    try:
        openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, how are you?"}],
        )

    except openai.OpenAIError as e:
        # Handle OpenAI API errors (e.g., invalid API key)
        print(f"Error: {e}")
        return False
    # The API key is valid if the request succeeds
    return True
