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
    custom_theme = gr.themes.Base(
        primary_hue="blue",
        secondary_hue="indigo",
        neutral_hue="slate",
        font=["'Segoe UI'", "Arial", "sans-serif"],
        radius_size="lg",
        spacing_size="md",
        text_size="lg",
        font_mono=["'Fira Mono'", "monospace"],
    )

    with gr.Blocks(
        fill_height=True,
        fill_width=True,
        theme=custom_theme,
        css="""
        body {
            background: linear-gradient(135deg, #e0e7ff 0%, #f0fdfa 100%);
        }
        .gradio-container {
            max-width: 900px !important;
            margin: 40px auto !important;
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(60,60,120,0.12);
            background: rgba(255,255,255,0.95);
        }
        .gr-chatbot {
            background: #f8fafc !important;
            border-radius: 18px !important;
            box-shadow: 0 2px 8px rgba(60,60,120,0.06);
        }
        .gr-button {
            font-size: 1.1em !important;
            border-radius: 12px !important;
            padding: 0.7em 2em !important;
        }
        .gr-textbox textarea {
            border-radius: 12px !important;
            font-size: 1.1em !important;
            background: #f1f5f9 !important;
        }
        """
    ) as demo_:
        gr.HTML(
            """
            <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px;">
                <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f6e1.svg" width="48" />
                <div>
                    <h1 style="margin:0;font-size:2.2em;font-weight:800;letter-spacing:1px;color:#334155;">🛡️ 内容审核智能助手</h1>
                    <div style="color:#64748b;font-size:1.1em;">AI驱动的文案合规与优化建议</div>
                </div>
            </div>
            """
        )
        gr.Markdown(
            """
            <span style="color:#6366f1;font-weight:bold;">请输入需要审核的文案，系统将自动检测合规性、敏感词、表达方式等问题，并给出优化建议。</span>
            """,
            elem_id="desc"
        )
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    type="messages",
                    label="审核对话历史",
                    bubble_full_width=False,
                    show_copy_button=True,
                    height=420,
                    avatar_images=["https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f464.svg", "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f916.svg"],
                    render_markdown=True,
                )
                msg = gr.Textbox(
                    label="输入待审核内容",
                    placeholder="请输入需要审核的文案...",
                    lines=4,
                    autofocus=True,
                )
                submit_btn = gr.Button("🚀 提交审核", variant="primary")
                clear = gr.ClearButton([msg, chatbot], value="🧹 清空历史")
            with gr.Column(scale=1):
                gr.Markdown(
                    """
                    <div style="background:#f1f5f9;border-radius:12px;padding:18px 16px;box-shadow:0 1px 4px rgba(60,60,120,0.04);">
                    <b>使用说明：</b>
                    <ul style="margin:0 0 0 1em;padding:0;color:#334155;">
                        <li>支持多轮对话，自动保存历史</li>
                        <li>请勿输入违法违规内容</li>
                        <li>审核建议仅供参考，最终以平台政策为准</li>
                    </ul>
                    </div>
                    """,
                    elem_id="usage"
                )

        # ...existing code...
        session_id = str(uuid.uuid1())
        session_11 = session_service.create_session_sync(
            user_id=user_id_1, session_id=session_id, app_name="content_reviewer"
        )

        async def submit(message, chat_history: List[gr.ChatMessage]):
            if not message:
                return "", chat_history

            if not test_message(message):
                chat_history.append(
                    gr.ChatMessage(
                        content="❌ 文案不合规，请检查内容后重试。",
                        role="assistant",
                    )
                )
                return "❌ 文案不合规，请检查内容后重试。", chat_history

            chat_history.append(gr.ChatMessage(content=message, role="user"))
            async for item in run_prompt(session=session_11, new_message=message):
                chat_history.append(item)
            return "", chat_history

        def submit_sync(message, chat_history: List[gr.ChatMessage]):
            return asyncio.run(submit(message, chat_history))

        submit_btn.click(submit_sync, [msg, chatbot], [msg, chatbot])
        msg.submit(submit_sync, [msg, chatbot], [msg, chatbot])

        return demo_


if __name__ == "__main__":
    demo_ = demo()
    demo_.launch(server_name="0.0.0.0")
    # run_prompt()
