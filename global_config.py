import os

from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class GlobalConfig:
    LOG_LEVEL = 'DEBUG'
    APP_STRINGS_FILE = 'strings.json'
    PPTX_TEMPLATE_FILES = {
        'Blank': {
            'file': 'pptx_templates/Blank.pptx',
            'caption': 'A good start'
        },
        'Ion Boardroom': {
            'file': 'pptx_templates/Ion_Boardroom.pptx',
            'caption': 'Make some bold decisions'
        },
        'Urban Monochrome': {
            'file': 'pptx_templates/Urban_monochrome.pptx',
            'caption': 'Marvel in a monochrome dream'
        }
    }
