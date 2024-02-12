from fastapi import Header
from typing_extensions import Annotated
from fastapi.responses import JSONResponse


from chainlit.auth import create_jwt
from chainlit.server import app
import chainlit as cl

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@app.get("/custom-auth")
async def custom_auth(identifier: Annotated[str | None, Header()] = None):
    # Verify the user's identity with custom logic.
    token = create_jwt(cl.User(identifier=identifier,metadata={"auth":"custom"}))
    return JSONResponse({"token": token})

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )
    user_data = cl.user_session.get("user")
    await cl.Message(content=f"Connected to Chainlit! {user_data}").send()


@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Hello!")
    await msg.send()
