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
from openai import OpenAI
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

# from google.adk.models

from agent import prompt

# from leader_agent.sub_agents.booking.agent import booking_agent
# from travel_concierge.sub_agents.in_trip.agent import in_trip_agent
# from travel_concierge.sub_agents.inspiration.agent import inspiration_agent
# from travel_concierge.sub_agents.planning.agent import planning_agent
# from travel_concierge.sub_agents.post_trip.agent import post_trip_agent
# from travel_concierge.sub_agents.pre_trip.agent import pre_trip_agent
from agent.sub_agents.sensitive_word.SensitiveWord import sensitive_word
from agent.sub_agents.wrong_word.WrongWord import wrong_word
from google.adk.tools import agent_tool


qwen_model = LiteLlm(
    model="openai/Qwen/Qwen3-235B-A22B",
    api_base=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    extra_body={"enable_thinking": False, "stream": False},
    stream=False,
)


sub_agents = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[sensitive_word, wrong_word],
    description="Runs multiple research agents in parallel to check content.",
)

sub_agents_tool = agent_tool.AgentTool(
    agent=sub_agents,
)

root_agent = LlmAgent(
    model=qwen_model,
    name="root_agent",
    description="一个广告以及文案的内容审核助手",
    instruction=prompt.ROOT_AGENT_INSTR,
    tools=[sub_agents_tool],
)

# seq_sum = SequentialAgent(
#     model=qwen_model,
#     name="root_agent",
#     description="一个广告以及文案的内容审核助手",
#     instruction="对前面内容审核的内容进行总结",
#     tools=[sub_agents, wrong_word_agent_tool],
# )
