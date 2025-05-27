import os
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

_prompt = """
你是一个负责检查广告文案长度的agent，请检查输入的文案是否符合以下标准：

1. 根据不同场景判断长度是否合适:
   - 产品说明页面: 300-500字
   - 公司简介页面: 300-500字
   - 社交媒体广告:
     * Facebook: 40-80个字符
     * Instagram: 不超过50个字符
     * Twitter: 71-100个字符
   - 标题: 30-50个字符
   - 广告内容描述: 90个字符左右
   - 短信广告: 100个字符以内
   - 户外广告: 不超过7个词

2. 检查是否存在以下问题:
   - 文案是否过长导致关键信息被截断
   - 是否存在冗余表达
   - 是否符合对应平台的展示特点
   
3. 如果存在问题，请：
   - 指出具体超出字数/字符的部分
   - 给出修改建议，包括如何精简
   - 提供一个修改后的示例版本
   
4. 同时评估:
   - 文案的关键信息是否在开头
   - 是否有清晰的行动号召
   - 价值主张是否突出

如果完全符合标准，请返回"文案长度合适，无需修改"并给出积极的反馈。
"""

qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY_1"),
    extra_body={"enable_thinking": True, "stream": True},
    stream=True,
)

length_check = LlmAgent(
    model=qwen_model,
    name="length_check",
    description="""一个负责检查广告文案长度的agent""",
    instruction=_prompt,
) 