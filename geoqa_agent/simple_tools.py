"""Lesson 1 的玩具工具：够简单，足以看清协议。"""
import os

LIST_DIR_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_dir",
        "description": "列出一个目录下的直接子项（文件和子目录），返回名称列表和数量。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "目录路径，绝对或相对当前工作目录"},
            },
            "required": ["path"],
        },
    },
}

COUNT_FILES_SCHEMA = {
    "type": "function",
    "function": {
        "name": "count_files",
        "description": "统计一个目录（含子目录）里某类扩展名文件的数量。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "目录路径"},
                "ext": {"type": "string", "description": "扩展名（不含点），如 txt、tif，默认统计全部"},
            },
            "required": ["path"],
        },
    },
}


def list_dir(path: str) -> dict:
    entries = sorted(os.listdir(path))
    return {"path": path, "count": len(entries), "entries": entries[:50]}


def count_files(path: str, ext: str = "") -> dict:
    n = 0
    for _, _, files in os.walk(path):
        n += sum(1 for f in files if not ext or f.endswith("." + ext))
    return {"path": path, "ext": ext or "all", "file_count": n}