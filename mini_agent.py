import json
import sys

from . import simple_tools
from .llm import LLMClient

TOOLS = [simple_tools.LIST_DIR_SCHEMA, simple_tools.COUNT_FILES_SCHEMA]
IMPL = {"list_dir": simple_tools.list_dir, "count_files": simple_tools.count_files}
MAX_STEPS = 10


def run(task: str) -> str:
    client = LLMClient()
    messages = [
        {"role": "system", "content": "你是一个文件系统助手。回答必须基于工具返回的真实结果，不许猜测。"},
        {"role": "user", "content": task},
    ]
    for step in range(1, MAX_STEPS + 1):
        reply = client.chat(messages, tools=TOOLS)
        print(f"\n=== 第 {step} 步 ===")

        if not reply.tool_calls:                      # 模型不再要工具 → 最终答案
            print(reply.content)
            print(json.dumps(messages, ensure_ascii=False, indent=2))
            return reply.content

        # ① 先把"模型的调用请求"原样记入上下文（协议要求，缺了会报 400）
        messages.append({
            "role": "assistant",
            "content": reply.content or "",
            "tool_calls": [
                {"id": c.id, "type": "function",
                 "function": {"name": c.function.name, "arguments": c.function.arguments}}
                for c in reply.tool_calls
            ],
        })
        # ② 逐个执行，把结果以 role="tool" 回填
        for c in reply.tool_calls:
            name, raw_args = c.function.name, c.function.arguments
            try:
                args = json.loads(raw_args or "{}")
                result = json.dumps(IMPL[name](**args), ensure_ascii=False, default=str)
            except Exception as e:                    # 出错不崩溃，变成文本喂回去
                result = json.dumps({"error": f"{type(e).__name__}: {e}"}, ensure_ascii=False)
            print(f"[调用] {name}({raw_args})\n[结果] {result[:200]}")
            messages.append({"role": "tool", "tool_call_id": c.id, "content": result})

    return "（达到最大步数，任务未完成）"


if __name__ == "__main__":
    
    run(" ".join(sys.argv[1:]) or "列出当前目录下有什么")
