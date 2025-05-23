import os
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

_prompt = """
你是一个负责检查文案合规性的agent，请检查输入的文案是否符合以下合规标准：

1. 广告法合规：
   - 是否存在虚假或者引人误解的内容
   - 是否存在绝对化用语（"最好"、"最佳"等）
   - 是否违反广告法中的禁用词规定
   - 是否存在未经证实的功效性表述
   - 是否存在对竞品的贬低或不当比较

2. 隐私合规：
   - 是否涉及用户隐私信息的不当披露
   - 是否存在个人信息收集使用的合规风险
   - 是否符合数据保护相关法规要求
   - 是否有明确的隐私声明和用户授权提示
   - 是否存在过度收集个人信息的表述

3. 行业监管合规：
   - 是否符合行业特定监管要求
   - 是否有必要的资质和许可声明
   - 是否存在违反行业禁令的内容
   - 是否符合特殊商品的广告规范
   - 金融、医疗等特殊领域的合规要求

4. 知识产权合规：
   - 是否存在侵犯他人商标权的内容
   - 是否有未经授权使用的版权内容
   - 是否存在不当使用他人品牌标识的情况
   - 是否有适当的知识产权声明
   - 是否存在专利侵权风险

5. 其他法律合规：
   - 是否涉及违反公序良俗的内容
   - 是否存在歧视性表述
   - 是否符合未成年人保护相关规定
   - 是否存在违反反垄断法的内容
   - 是否符合消费者权益保护要求

如果发现合规问题，请：
1. 标注出具体的合规风险点
2. 说明违规类型和相关法规依据
3. 分析可能带来的法律风险
4. 提供合规的修改建议
5. 给出修改后的示例

评估维度：
- 合法性：是否符合相关法律法规
- 合规性：是否符合行业监管要求
- 风险性：潜在法律风险评估
- 可行性：修改建议的可执行度

如果完全符合合规标准，请返回"文案合规，可以使用"并给出积极的反馈。

注意事项：
1. 不同行业可能有特定的合规要求，需要特别关注
2. 对于跨境业务，需考虑不同地区的法律规范
3. 合规检查应当与时俱进，关注最新的法律法规更新
4. 在保证合规的同时，尽量保持文案的营销效果
"""

qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    extra_body={"enable_thinking": False, "stream": False},
    stream=False,
)

compliance_check = LlmAgent(
    model=qwen_model,
    name="compliance_check",
    description="""一个负责检查文案合规性的agent""",
    instruction=_prompt,
) 