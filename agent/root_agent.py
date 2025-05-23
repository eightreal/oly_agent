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

"""Demonstration of Travel AI Conceirge using Agent Development Kit"""

import os
import time
from google.adk.agents import Agent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from litellm.exceptions import RateLimitError

# from google.adk.models

from agent import prompt

# from leader_agent.sub_agents.booking.agent import booking_agent
# from travel_concierge.sub_agents.in_trip.agent import in_trip_agent
# from travel_concierge.sub_agents.inspiration.agent import inspiration_agent
# from travel_concierge.sub_agents.planning.agent import planning_agent
# from travel_concierge.sub_agents.post_trip.agent import post_trip_agent
# from travel_concierge.sub_agents.pre_trip.agent import pre_trip_agent
from .sub_agents.sensitive_word.SensitiveWord import sensitive_word
from .sub_agents.wrong_word.WrongWord import wrong_word
from .sub_agents.length_check.LengthCheck import length_check
from .sub_agents.logic_check.LogicCheck import logic_check
from .sub_agents.grammar_check.GrammarCheck import grammar_check
from .sub_agents.compliance_check.ComplianceCheck import compliance_check
from .sub_agents.user_perspective_check.UserPerspectiveCheck import user_perspective_check
from .sub_agents.emotion_check.EmotionCheck import emotion_check
from .sub_agents.marketing_effect_check.MarketingEffectCheck import marketing_effect_check
from .sub_agents.seo_check.SeoCheck import seo_check
from .sub_agents.format_check.FormatCheck import format_check
from google.adk.tools import agent_tool

_prompt = """
你是一个广告文案审核agent，负责对文案进行全方位检查。你将协调多个专门的子agent进行检查，包括：

1. 敏感词检测
2. 错别字检测
3. 长度检测
4. 逻辑检测
5. 语法检测
6. 合规检测
7. 用户视角检测
8. 情感基调检测
9. 营销效果检测
10. SEO优化检测
11. 格式检测

请根据文案内容和要求，调用相应的子agent进行检查。
"""

# 配置API请求参数
qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    extra_body={
        "enable_thinking": False, 
        "stream": False,
        "max_tokens": 1000,  # 限制token数量
        "temperature": 0.7,  # 控制输出的随机性
        "request_timeout": 30,  # 设置超时时间
    },
    stream=False,
)

# 创建一个包含基本子代理的列表
base_agents = [
    sensitive_word,
    wrong_word,
]

# 创建一个包含扩展子代理的列表
extended_agents = [
    length_check,
    logic_check,
    grammar_check,
    compliance_check,
    user_perspective_check,
    emotion_check,
    marketing_effect_check,
    seo_check,
    format_check,
]

# 创建基本ParallelAgent
base_parallel_agent = ParallelAgent(
    name="base_check_agents",
    description="并行运行基本内容检查agent",
    sub_agents=base_agents
)

# 创建扩展ParallelAgent
extended_parallel_agent = ParallelAgent(
    name="extended_check_agents",
    description="并行运行扩展内容检查agent",
    sub_agents=extended_agents
)

# 将ParallelAgent转换为工具
base_agents_tool = agent_tool.AgentTool(
    agent=base_parallel_agent,
)

extended_agents_tool = agent_tool.AgentTool(
    agent=extended_parallel_agent,
)

# 创建root_agent，分阶段使用工具
root_agent = LlmAgent(
    model=qwen_model,
    name="root_agent",
    description="一个广告以及文案的内容审核助手",
    instruction=prompt.ROOT_AGENT_INSTR,
    tools=[base_agents_tool, extended_agents_tool]
)

# seq_sum = SequentialAgent(
#     model=qwen_model,
#     name="root_agent",
#     description="一个广告以及文案的内容审核助手",
#     instruction="对前面内容审核的内容进行总结",
#     tools=[sub_agents, wrong_word_agent_tool],
# )
