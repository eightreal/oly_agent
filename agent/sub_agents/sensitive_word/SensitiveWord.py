import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# from travel_concierge.sub_agents.booking import prompt


_promopt = """
 你是一个负责审核文案是否包含敏感词的agent，请检查输入的文案是否包含敏感词，
 如果包含敏感词，请返回敏感词，并解释，否则返回"no sensitive word"。
    请关注如下但不仅限于以下的敏感词：
    1. 政治敏感词
    2. 宗教敏感词
    3. 暴力敏感词
    4. 暴力恐吓敏感词
    5. 色情敏感词
    6. 舆论对立敏感词
 如果输入的文案中不包含敏感词，那么请返回"no sensitive word"。
"""
qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    extra_body={"enable_thinking": True, "stream": False},
    stream=False,
)


sensitive_word = LlmAgent(
    model=qwen_model,
    name="sensitive_word",
    description="""一个负责敏感词检测的agent""",
    instruction=_promopt,
)
