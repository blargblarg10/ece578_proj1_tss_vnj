"""
csma_ca_ap.py

Description:
    The csma_ca_ap module represents an access point (AP) in a CSMA/CA network.
    It handles events related to RTS reception, data reception, and collision detection.

Responsibilities:
    - Sends CTS frames in response to RTS frames from transmitting stations.
    - Sends ACK frames in response to data frames from transmitting stations.
    - Handles collisions and waits for the medium to become idle.

Usage:
    - The module reacts to various events to simulate the behavior of an AP in a CSMA/CA network.
"""

# csma_ca_tx.py
from utility.logger_config import logger
from src.proj_data_classes import Event, NodeType
class CsmaCaAp:
    def __init__(self, id, collision_domain, params, visualizer=None):
        logger.debug("CsmaCaTx instance created.")
        self.ID = id
        self.CD = collision_domain
        self.ACK = params['ACK_size']
        self.SIFS = params['SIFS_size']
        self.PARM = params

        self.respond_list = []
        self.event = None
        
        self.collisions = 0

        # Histor of for the Sender
        self.history = []
        self.visualizer = visualizer

    def log_and_notify(self, timestamp, event_name, duration):
            """
            Appends event to history log and notifies observer.
            """
            self.history.append((timestamp, event_name, duration))
            if self.visualizer is not None:
                self.visualizer.plot_event(self.ID, timestamp, event_name, duration)
                
    def set_event(self, timestamp):
        self.event = Event("tx", self.ID, timestamp, self.PACKAGE_LENGTH, self.package_end)

    def inform_broadcasting(self):
        """
        Informed by the Network that this node is broadcasting.
        """
        message = "ACK" if self.event.data_type == NodeType.AP else "COLLISION"
        self.log_and_notify(self.event.timestamp, message, self.ACK)
        self.event = None
        self.respond_list.pop(0)

    def receive_event(self, event):
        """
        Receives a BroadcastEvent and processes it accordingly.
        :param event: The event to be processed.
        """
        # Collision Occurs
        if self.respond_list:
            self.collisions += 1
            for i in self.respond_list:
                i["response"].data_type = NodeType.COLLISION
            self.respond_list.append({"recieved" : event,
                                      "response" : Event(NodeType.COLLISION, self.ID, event.timestamp + event.duration + self.SIFS, self.ACK, event.nav)})
        else:
            self.respond_list.append({"recieved" : event,
                                      "response" : Event(NodeType.AP, self.ID, event.timestamp + event.duration + self.SIFS, self.ACK, event.nav)})
   
    
    def declare_event(self, timestamp):
        """
        Gets the next event from the node.
        :return: The next event from the node.
        """
        # An Event is already trying to occur
        if self.respond_list:
            self.event = self.respond_list[0]["response"]
            return self.event
        else:
            return None
        
    def print_statistics(self):
        print(f"AP: {self.ID} Collisions: {self.collisions}")