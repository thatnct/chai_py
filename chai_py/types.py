from dataclasses import dataclass


@dataclass
class LatestMessage:
    text: str
    timestamp: int  # Milliseconds since epoch


@dataclass
class Update:
    conversation_id: str
    latest_message: LatestMessage
