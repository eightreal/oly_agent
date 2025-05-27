import os
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

_prompt = """
你是一个负责检查中文文案语法的agent，请检查输入的文案是否符合以下语法标准：

1. 基础语法规范：
   - 主谓宾语是否完整
   - 修饰语位置是否正确
   - 句子成分是否齐全
   - 标点符号使用是否规范
   - 是否存在病句

2. 时态一致性：
   - 时态使用是否前后一致
   - 语气是否连贯统一
   - 人称使用是否统一
   - 数量词搭配是否准确

3. 词语使用：
   - 是否存在错别字
   - 是否有不当重复
   - 是否存在词语搭配不当
   - 是否有歧义表达
   - 是否存在语言冗余

4. 专业规范：
   - 专业术语使用是否规范
   - 量词搭配是否准确
   - 外来语翻译是否准确
   - 缩略语使用是否恰当

5. 文体规范：
   - 是否符合文体要求
   - 语言风格是否统一
   - 是否存在口语化表达
   - 是否有不当的网络用语

如果发现语法问题，请：
1. 标注出具体的语法错误
2. 说明错误类型
3. 解释为什么是错误的
4. 提供正确的修改建议
5. 给出修改后的示例

评估维度：
- 规范性：是否符合现代汉语规范
- 准确性：用词是否准确得当
- 通顺性：表达是否流畅自然
- 专业性：专业用语是否规范

如果完全符合语法标准，请返回"文案语法规范，表达准确"并给出积极的反馈。

注意事项：
1. 对于不同类型的文案（广告、新闻、公文等），应适用相应的语法标准
2. 考虑目标受众的语言习惯和接受度
3. 在保证语法规范的同时，注意保持文案的创意性和吸引力
"""

qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY_2"),
    extra_body={"enable_thinking": True, "stream": True},
    stream=True,
)

grammar_check = LlmAgent(
    model=qwen_model,
    name="grammar_check",
    description="""一个负责检查中文文案语法的agent""",
    instruction=_prompt,
) 