from dataclasses import dataclass
from enum import Enum, auto

class NodeType(Enum):
    TX = auto()
    AP = auto()
    COLLISION = auto()

@dataclass
class Event:
    data_type: NodeType  # 'tx' for transmitting node, 'ap' for access point, 'idle' if it doesnt matter
    node_id: int # ID of the node
    timestamp: int  # Time (in slots) when the node wants to start its transmission
    duration: int  # Duration of the transmission (in slots)
    nav: int # Duration of the network allocation vector (in slots)