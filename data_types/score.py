from dataclasses import dataclass


@dataclass
class ScoreReason:
    score: float
    reason: str
