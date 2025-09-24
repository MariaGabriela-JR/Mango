from enum import Enum

# ---------- PROCESSING STATUS ----------
class ProcessingStatus(str, Enum):
    NEW = "new"
    ACTIVE = "active"
    VALIDATED = "validated"
    FILTERED = "filtered"
    DELETED = "deleted"

# ---------- EMOTION CATEGORY ----------
class EmotionCategory(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"

# ---------- GENDER ----------
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"
