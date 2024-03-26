[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![Pull Request](https://github.com/intelops/compage-llm-backend/actions/workflows/ci.yml/badge.svg) ![CodeQL](https://github.com/intelops/compage-llm-backend/actions/workflows/github-code-scanning/codeql/badge.svg) ![Python](https://img.shields.io/badge/python-3.8-blue.svg)

# Compage LLM Backend

This compage llm backend project is a FastAPI application that provides functionality for code generation, token management, unit test generation for compageGPT

## Overview

This project is built using the FastAPI framework in Python. It provides functionality for code generation using langchain and openAI, token management, and more. The project structure is organized as follows:

```bash
root
|---- main.py
|---- venv
|---- pkg
|     |---- src
|           |---- routes
|           |---- middlewares
|           |---- configs
|           |---- models
|           |---- schemas
|           |---- store
|           |---- __init__.py
|
| ---- Dockerfile
|---- requirements.txt
|---- Makefile
|----.gitignore
... many more
```

## Features

- **Health:** The project provides an API endpoint `/api/health` that returns a simple "ok" response. This can be used to check if the server is up and running.

- **Validate OpenAI API key:** The project provides an API endpoint `/api/validate_openai` that validates the OpenAI API key. It offers OpenAI Validation, explanation as responses.

- **Unit Test Generation:** The project provides an API endpoint `/api/unit_test_generate` that utilizes LangChain and OpenAI to generate Unit Test Cases. It offers Unit Test Generation, explanation as responses.

- **Documentation Generation:** The project provides an API endpoint `/api/doc_generate` that utilizes LangChain and OpenAI to generate documentation. It offers Documentation Generation, explanation as responses.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/intelops/compage-llm-backend
   ```

2. Navigate to the project directory:

   ```bash
   cd compage-llm-backend
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
   ```bash
   # run the database setup using docker
   docker run --name cassandra-backend-llm -p 9042:9042 cassandra:latest

   # execute the docker bash
   docker exec -it cassandra-backend-llm bash

   # enter the database
   cqlsh

   # create the keyspace
   CREATE KEYSPACE IF NOT EXISTS backend_llm WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
   
   ```

## Usage

1. Run the FastAPI application:

   ```python
   python main.py
   ```

2. Access the API at `http://localhost:8000`.

3. Checkout the swagger documentation at [docs](http://localhost:8000/docs).

## API Endpoints

- `/api/health`: Health check endpoint. Returns a simple "ok" response.
- `/api/unit_test_generate`: Generate code using LangChain and OpenAI. Receive unit test flow and explanation as responses.
- `/api/doc_generate`: Generate documentation using LangChain and OpenAI. Receive documentation flow and explanation as responses.
- `/api/validate_openai`: Validate the OpenAI API key. Receive OpenAI Validation, explanation as responses.


## Dockerization

You can use the included Dockerfile to containerize the application. Build the Docker image and run it in a container.

```bash
docker build -t backend_llm .
docker run -p 8000:8000 backend_llm
```

## Contributing

Contributions are welcome! If you find any issues or want to enhance the project, feel free to submit a pull request.
