# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import asyncio
import random
import time
import os

import gradio.blocks
import agent
import tempfile
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import RunConfig
from google.adk.agents.run_config import StreamingMode
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
from loguru import logger
from typing import List
from tools.message_validate import test_message

import gradio as gr
import agent.root_agent
import litellm
import uuid


tempfile.tempdir = "logs/"

load_dotenv(override=True)

# logger.info(f"openai  api key loaded {os.getenv('OPENAI_API_KEY')}")

app_name = "content_reviewer"

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()
runner = Runner(
    app_name=app_name,
    agent=agent.root_agent.root_agent,
    artifact_service=artifact_service,
    session_service=session_service,
)
user_id_1 = "user"

# litellm._turn_on_debug()

run_configs = RunConfig(streaming_mode=StreamingMode.SSE, support_cfc=False)


async def run_prompt(session: Session, new_message: str):
    content = types.Content(role="user", parts=[types.Part(text=new_message)])
    print("** User says:", new_message)
    # logger.infO()

    final_response = ""

    async for event in runner.run_async(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
        run_config=run_configs,
    ):
        # print(f"** Assistant says:{event}")
        # if event.content and event.content.parts:
        #     for part in event.content.parts:
        #         print(f"Potential final response from [{event.author}]: {part.text}")

        if (
            event.is_final_response()
            and event.content
            and event.content.parts
            and event.author == "merge_agent"
        ):
            print(f"len event.content.parts[{len(event.content.parts)}")

            final_response = f"{event.content.parts[0].text            }" + "\n"
            yield gr.ChatMessage(content=final_response, role="assistant")

    # return


def demo():
    with gr.Blocks(fill_height=True, fill_width=True) as demo_:
        session_id = str(uuid.uuid1())
        print(session_id)
        session_11 = session_service.create_session_sync(
            user_id=user_id_1, session_id=session_id, app_name="content_reviewer"
        )

        chatbot = gr.Chatbot(type="messages")
        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])

        async def submit(message, chat_history: List[gr.ChatMessage]):
            if not message:
                return "", chat_history

            if not test_message(message):
                chat_history.append(
                    gr.ChatMessage(
                        content="Invalid message, it content apperate content",
                        role="assistant",
                    )
                )
                return "Invalid message, it content apperate content", chat_history

            chat_history.append(gr.ChatMessage(content=message, role="user"))
            # response =  asyncio.run()
            async for item in run_prompt(session=session_11, new_message=message):

                chat_history.append(item)
            return "", chat_history

        def submit_sync(message, chat_history: List[gr.ChatMessage]):
            return asyncio.run(submit(message, chat_history))

        msg.submit(submit_sync, [msg, chatbot], [msg, chatbot])
        return demo_


if __name__ == "__main__":
    demo_ = demo()
    demo_.launch(server_name="0.0.0.0")
    # run_prompt()
