from dff.script import Message
from dff.utils.testing import is_interactive_mode

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from dialog_graph.pipeline import pipeline


app = FastAPI()


class Output(BaseModel):
    user_id: str
    response: Message


@app.post("/chat/", response_model=Output)
async def respond(
    user_id: str,
    user_message: Message,
):
    context = await pipeline._run_pipeline(user_message, user_id) 
    return {"user_id": user_id, "response": context.last_response}


if __name__ == "__main__":
    if is_interactive_mode():
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
        )
