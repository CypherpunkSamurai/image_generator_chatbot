# Langchain DALLE Chatbot Server

A FastAPI Server Chatbot with Langchain integration to generate images based on the text input.

## How to run

1. Install Requirements

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the server

```shell
# edit .env file with contents of .env.example
uvicorn app:app --reload
```

3. Make a HTTP Request

```shell
curl -X 'POST' \
    'http://localhost:8000/api/v1/chat' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "message": "hello",
    "model": "deepseek-r1-distill-qwen-32b",
    "stream": false
}'
```

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)

- [Langchain](https://python.langchain.com/)
