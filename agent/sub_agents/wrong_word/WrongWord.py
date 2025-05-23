import os
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# from travel_concierge.sub_agents.booking import prompt


_promopt = """
 你是一个负责审核文案是否包含错别字agent，请检查输入的文案是否包含错别字，
 如果包含错别字，请返回相应错别字，并解释相关内容，如果没有则返回"无错别字"
"""
qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    extra_body={"enable_thinking": True, "stream": False},
    stream=False,
)


wrong_word = LlmAgent(
    model=qwen_model,
    name="wrong_word",
    description="""一个负责错别字审核的agent""",
    instruction=_promopt,
)


