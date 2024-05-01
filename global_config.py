import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class GlobalConfig:
    LOG_LEVEL: str = 'DEBUG'
    APP_STRINGS_FILE: str = 'strings.json'
    PPTX_TEMPLATE_FILES: dict = None

    def __post_init__(self):
        object.__setattr__(self, 'PPTX_TEMPLATE_FILES', self.load_templates())

    @staticmethod
    def load_templates():
        templates_path = 'pptx_templates'
        template_files = [f for f in os.listdir(templates_path) if f.endswith('.pptx')]

        templates = {}
        for pptx_file in template_files:
            base_name = os.path.splitext(pptx_file)[0]
            txt_file_path = os.path.join(templates_path, base_name + '.txt')
            caption = "Default caption"
            if os.path.exists(txt_file_path):
                with open(txt_file_path, 'r', encoding='utf-8') as f:
                    caption = f.read().strip()

            templates[base_name] = {
                'file': os.path.join(templates_path, pptx_file),
                'caption': caption
            }
        
        return templates


