import os
from dataclasses import dataclass,field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 文件里的环境变量

@dataclass
class Settings:
    """配置类"""
    project_root: Path = Path(__file__).resolve().parent
    data_root:Path = Path(os.getenv("DATA_ROOT",str(Path(__file__).resolve().parent.parent)))
    output_dir: Path = None
    cards_dir: Path = None
    max_steps: int = int(os.getenv("AGENT_MAX_STEPS", "25"))
    max_result_chars: int = 6000

    def __post_init__(self):
        self.output_dir = self.project_root / "outputs"
        self.cards_dir = self.project_root / "cards"
        self.output_dir.mkdir(exist_ok=True)


settings = Settings()   # 模块级单例：全项目 import 同一个实例
