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

class streamLitllm(LiteLlm):
    def __init__ (self, model, **kwargs):
        super().__init__(model, **kwargs)
        self._additional_args["stream"] = False
        
        
stream_enabled = True
        
qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY_1"),
    extra_body={"enable_thinking": stream_enabled, "stream": stream_enabled},
)


wrong_word = LlmAgent(
    model=qwen_model,
    name="wrong_word",
    description="""一个负责文案错别字检测的agent""",
    instruction=_promopt,
    # stream=True,
)


