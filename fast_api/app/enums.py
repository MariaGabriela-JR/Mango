# app/enums.py
from enum import Enum

class ProcessingStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"

class EmotionCategory(str, Enum):
    JOY = "joy"
    INSPIRATION = "inspiration"
    TENDERNESS = "tenderness"
    SADNESS = "sadness"
    FEAR = "fear"
    DISGUST = "disgust"
    NEUTRAL = "neutral"# app/enums.py
from enum import Enum

class ProcessingStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"

class EmotionCategory(str, Enum):
    JOY = "joy"
    INSPIRATION = "inspiration"
    TENDERNESS = "tenderness"
    SADNESS = "sadness"
    FEAR = "fear"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

