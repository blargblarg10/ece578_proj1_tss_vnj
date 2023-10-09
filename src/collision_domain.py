"""
collision_domain.py

Description:
    The CollisionDomain class acts as a registry of devices within a collision domain.
    It maintains a list of devices (stations and AP) and facilitates the broadcasting of events to all devices within the domain.

Responsibilities:
    - Maintains a list of devices within its range.
    - Broadcasts events to all registered devices.

Usage:
    - Devices register themselves with the collision domain.
    - When a device wants to send an event, it informs the collision domain.
    - The collision domain broadcasts the event to all registered devices.
    - Each device handles the event based on its logic and state.
"""

# collision_domain.py
from utility.logger_config import logger
from src.csma_ca_ap import CsmaCaAp
from src.csma_ca_tx import CsmaCaTx
class CollisionDomain:
    def __init__(self, id):
        logger.debug("CollisionDomain instance created.")
        self.id = id
        self.tx_nodes = []
        self.ap_nodes = []

    def add(self, node):
        """
        Adds a node to the collision domain. Nodes are added to their respective lists based on their type.
        :param node: The node to be added, can be of type CsmaCaTx or CsmaCaAp.
        """
        if isinstance(node, CsmaCaTx):
            self.tx_nodes.append(node)
        elif isinstance(node, CsmaCaAp):
            self.ap_nodes.append(node)
        else:
            raise ValueError("Invalid node type. Node must be of type CsmaCaTx or CsmaCaAp.")

