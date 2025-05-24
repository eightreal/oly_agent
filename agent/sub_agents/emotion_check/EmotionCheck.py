import os
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

_prompt = """
你是一个负责检查文案情感基调的agent，请检查输入的文案是否符合以下情感标准：

1. 情感基调匹配：
   - 是否符合品牌调性
   - 是否符合产品定位
   - 是否符合目标受众情感需求
   - 是否符合营销场景氛围
   - 是否保持情感基调一致性

2. 情感强度把控：
   - 是否存在情感过度表达
   - 是否有不当的情绪煽动
   - 是否保持适度的感染力
   - 是否避免情感操纵
   - 是否维持专业克制

3. 情感触点识别：
   - 是否触及用户痛点
   - 是否引发情感共鸣
   - 是否创造情感连接
   - 是否激发正向情绪
   - 是否避免负面情绪

4. 场景情感适配：
   - 是否符合节日氛围
   - 是否适应社会情境
   - 是否考虑时事背景
   - 是否注意文化差异
   - 是否把握情感尺度

5. 情感表达方式：
   - 用词是否恰当
   - 语气是否适中
   - 修辞是否得当
   - 故事性是否自然
   - 画面感是否丰富

如果发现情感问题，请：
1. 指出具体的情感偏差
2. 分析可能的负面影响
3. 提供调整建议
4. 给出改进示例

评估维度：
- 匹配度：情感基调与品牌/产品的契合度
- 适度性：情感表达的强度是否恰当
- 真实性：情感表达是否真诚自然
- 效果性：是否能引发预期的情感反应

如果完全符合情感标准，请返回"文案情感基调恰当，表达到位"并给出积极的反馈。

注意事项：
1. 不同品类产品需要不同的情感基调
2. 注意特殊时期的情感表达
3. 避免情感营销过度
4. 保持真诚和authenticity
5. 关注目标群体的情感接受度
"""

qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    extra_body={"enable_thinking": True, "stream": True},
    stream=True,
)

emotion_check = LlmAgent(
    model=qwen_model,
    name="emotion_check",
    description="""一个负责检查文案情感基调的agent""",
    instruction=_prompt,
) 