# LLM Backend

This llm_backend project is a FastAPI application that provides functionality for code generation, token management for compageGPT

## Overview

This project is built using the FastAPI framework in Python. It provides functionality for code generation using langchain and openAI, token management, and more. The project structure is organized as follows:

```bash
root
|---- main.py
|---- venv
|---- connect_bundle
|---- pkg
|     |---- src
|           |---- routes
|           |---- middlewares
|           |---- configs
|           |---- models
|           |---- schemas
|           |---- utils
|           |---- store
|           |---- __init__.py
|
|---- tests
|      |----- test_ping.py
| ---- Dockerfile
|---- requirements.txt
|----.gitignore
|----.env
|----.env.example
... many more
```

## Features

- **Token Management:** The project includes token management using JSON Web Tokens (JWT). Users can add their openAI api-keys and generate tokens for secure API access.

- **Code Generation:** The project provides an API endpoint `/api/code_generate` that utilizes LangChain and OpenAI to generate code. It offers code flow and explanation as responses.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MrAzharuddin/backend_llm
   ```

2. Navigate to the project directory:

   ```bash
   cd compage/backend_llm
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python3.8 -m venv venv
   source venv/bin/activate
   ```

4. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Setup the database:
   [Follow these steps Datastax Docs](https://docs.datastax.com/en/astra/astra-db-vector/databases/python-driver.html)

6. Create an environment variable (.env.development) for your Database credentials and JWT setup:

   ```shell
      JWT_SECRET=GENERATE_YOUR_SECRET_HERE
      JWT_ALGORITHM=HS256
      ENVIRONMENT=development


      ASTRADB_KEYSPACE=compage_gpt
      ASTRADB_CLIENT_SECRET=
      ASTRADB_CLIENT_ID=
      ASTRADB_TOKEN=
   ```

## Usage

1. Run the FastAPI application:

   ```python
   python3 main.py
   ```

2. Access the API at `http://localhost:8000`.

## API Endpoints

- `/api/create-token`: Generate a JWT token by providing valid credentials.
- `/api/code_generate`: Generate code using LangChain and OpenAI. Receive code flow and explanation as responses.

## Testing

To run tests, use the following command from the project root directory:

```bash
pytest .
```

## Dockerization

You can use the included Dockerfile to containerize the application. Build the Docker image and run it in a container.

```bash
docker build -t backend_llm .
docker run -p 8000:8000 backend_llm
```

## Contributing

Contributions are welcome! If you find any issues or want to enhance the project, feel free to submit a pull request.
