import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

class LLMClient:
    def __init__(self):
        # 用项目专用变量名，避免被 shell 里给其他工具（如 Codex）导出的
        # OPENAI_API_KEY/OPENAI_BASE_URL 抢占——load_dotenv 不会覆盖已存在的环境变量
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
        )
        self.model = os.getenv("AGENT_MODEL", "glm-5.3-flash")

    def chat(self, messages, tools=None):
        """一轮对话。返回的是 SDK 的 message 对象（含 .content 和 .tool_calls）。"""
        kwargs = dict(model=self.model, messages=messages, temperature=0)
        if tools:
            kwargs["tools"] = tools
        resp = self.client.chat.completions.create(**kwargs)
        return resp.choices[0].message
