from Chatbot import Chatbot
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json

app = FastAPI()


class GenerateRequest(BaseModel):
    settings: dict
    messages: list


class GenerateResponse(BaseModel):
    status: str
    content: dict


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    # Example processing logic
    print(request)
    if not request.settings or not request.messages:
        # print(f"Request: {request}")
        raise HTTPException(status_code=400, detail="Missing arguments")
    if not isinstance(request.settings, dict) or not isinstance(request.messages, list):
        raise HTTPException(status_code=400, detail="Invalid payload received")

    settings = {
        "response_length": request.settings.get("response_length"),
        "temperature": request.settings.get("temperature"),
        "system_prompt": request.settings.get("system_prompt"),
        "precaution": request.settings.get("precaution"),
    }

    chatbot = Chatbot(settings)
    payload = request.messages
    print(payload)

    response = chatbot.get_response(payload)
    print(response["content"])
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["content"])
    return GenerateResponse(status="success", content=response["content"])


@app.post("/api/stream")
async def stream_text(request: GenerateRequest):
    if not request.settings or not request.messages:
        raise HTTPException(status_code=400, detail="Missing arguments")
    if not isinstance(request.settings, dict) or not isinstance(request.messages, list):
        raise HTTPException(status_code=400, detail="Invalid payload received")

    settings = {
        "response_length": request.settings.get("response_length"),
        "temperature": request.settings.get("temperature"),
        "system_prompt": request.settings.get("system_prompt"),
        "precaution": request.settings.get("precaution"),
        "stream": True,  # Ensure streaming is enabled
    }

    chatbot = Chatbot(settings)
    payload = request.messages

    def event_stream():
        for response in chatbot.get_streaming_response(payload):
            yield json.dumps(response) + "\n"

    return StreamingResponse(event_stream(), media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
