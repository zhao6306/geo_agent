import json
from pathlib import Path

# 1) 依赖
import duckdb, shapely, plotly, yaml, PIL, openai  # noqa
print("[1/3] 依赖 OK:",
      "duckdb", duckdb.__version__, "|",
      "shapely", shapely.__version__, "|",
      "openai", openai.__version__)

# 2) 数据（数据根目录统一在 .env 的 DATA_ROOT 配置，所有课程共用）
import os
from dotenv import load_dotenv

load_dotenv()
DATA_ROOT = Path(os.getenv("DATA_ROOT", ""))
for rel in ["whumix/labels/val", "data_v4/annotations/data_v4_val.json",
            "whu/annotation/train.json"]:
    p = DATA_ROOT / rel
    print(f"[2/3] {'OK ' if p.exists() else '缺失!'} {rel}")

key = os.getenv("LLM_API_KEY", "")
print("[3/3] API:", "已配置 key =", key[:6] + "..." if key else "未配置（Lesson 1 前配好即可）")