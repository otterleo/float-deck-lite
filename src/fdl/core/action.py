from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Dict, Optional


class ActionType(Enum):
    HUD_ACTION = auto()
    LAUNCH_APP = auto()
    DEBUG_PRINT = auto()
    MEDIA_CONTROL = auto()


@dataclass
class Action:
    action_type: ActionType
    payload: Any
    label: str
    key: str