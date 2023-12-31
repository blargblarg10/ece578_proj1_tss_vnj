"""
csma_ca_tx.py

Description:
    The csma_ca_tx module represents a transmitting node in a CSMA/CA network.
    It handles events related to data arrival, RTS transmission, CTS acknowledgement, data transmission, ACK reception, collision, and backoff timer expiration.

Responsibilities:
    - Initiates the CSMA/CA process upon data arrival if the medium is idle.
    - Sends RTS frames and handles CTS acknowledgements.
    - Transmits data frames and handles ACK receptions.
    - Manages backoff timers and retries in case of collisions.

Usage:
    - The module reacts to various events to simulate the behavior of a transmitting station in a CSMA/CA network.
"""
# csma_ca_tx.py
from utility.logger_config import logger
from src.proj_data_classes import Event, NodeType
from enum import Enum, auto
import random
from math import ceil

class TX_STATE(Enum):
    WAITING_FOR_ACK = auto()
    TRANSMITTING = auto()
class CsmaCaTx:
    def __init__(self, id, collision_domain, params, packet_arrival_times, visualizer=None):
        logger.debug("CsmaCaTx instance created.")
        
        # Constants for Sender
        self.ID = id
        self.CD = collision_domain
        self.DIFS = params['DIFS_size']
        self.SIFS = params['SIFS_size']
        self.ACK = params['ACK_size']
        self.CW_MIN = params['CW0']
        self.CW_MAX = params['CWmax']
        self.TX_ARRIVAL_LIST = packet_arrival_times
        self.params = params
        
        bandwidth = params['bandwidth']
        slot_duration = params['slot_duration']
        self.packet_size = params['data_frame_size'] * 8
        
        self.PACKAGE_LENGTH = ceil(self.packet_size / (bandwidth * slot_duration)
)
        # Variables for Sender
        self.backoff = 0
        self.backoff_start = 0
        self.state = TX_STATE.TRANSMITTING
        self.expected_ack_slot = 0      
        self.collision_cnt = 0    
        self.package_end = 0            
        self.event = None
        
        self.successful_transmissions = 0
        
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
        self.event = Event(NodeType.TX, self.ID, timestamp, self.PACKAGE_LENGTH, self.package_end)
    
    def set_backoff(self):
        """
        Randomly selects backoff based on the current collision count.
        """
        return random.randint(0, min(self.CW_MAX, 2 ** self.collision_cnt * self.CW_MIN))
    
    def determine_timestamps(self, event_timestamp):
        """
        Determines the timestamps for the declared event
        """
        # Add difs to timestamp and record history
        self.log_and_notify(event_timestamp, "DIFS", self.DIFS)
        event_timestamp += self.DIFS
        
        # Set the backoff start to this timestamp in case it is not chose to transmit
        self.backoff_start = event_timestamp
        
        # Add Backoff
        event_timestamp += self.backoff
        
        # Determine the Expected ACK Slot
        self.expected_ack_slot = event_timestamp + self.PACKAGE_LENGTH + self.SIFS
        
        # Determine when the NAV Process will end. After the ACK
        self.package_end = self.expected_ack_slot + self.ACK
        
        # Return Event Timestamp to be broadcasted to the network
        return event_timestamp

    def inform_broadcasting(self):
        """
        Informed by the Network that this node is broadcasting.
        Switch state to waiting for ACK
        """
        self.state = TX_STATE.WAITING_FOR_ACK
        # Add transmit time to history
        self.log_and_notify(self.event.timestamp, "DATA", self.PACKAGE_LENGTH)
        self.log_and_notify(self.event.timestamp + self.PACKAGE_LENGTH, "SIFS", self.SIFS)
    
    def collision_process(self):
        """
        Handles how the node reacts to a collision
        :param event: The event to be processed.
        """
        self.collision_cnt += 1
        
        # Collision Detected
        self.backoff = self.set_backoff()
        
        # Start time will be when this event was supposed to finish
        event_timestamp = self.package_end
        
        # Determine Timestampe
        event_timestamp = self.determine_timestamps(event_timestamp)
        
        self.set_event( event_timestamp)
        
    
    def wait_for_ack_process(self, event: Event):
        """
        Handles how the node reacts to a received event when it is in the waiting for ACK state.
        :param event: The event to be processed.
        """        

        # Event time beyond expected ACK slot (Collision)
        if event.timestamp > self.expected_ack_slot:
            logger.error(f"TX_NODE_{self.ID}: Did not receive ACK from AP in time. Simulation Failed.")
            quit()
        elif event.data_type == NodeType.COLLISION or event.timestamp != self.expected_ack_slot:
            # COLLISION
            self.collision_process()
            self.state = TX_STATE.TRANSMITTING
        elif event.data_type == NodeType.AP:
            # ACK Received
            self.successful_transmissions += 1
            self.collision_cnt = 0
            self.event = None
            self.state = TX_STATE.TRANSMITTING
        else:
            logger.err(f"TX_NODE_{self.ID}: Invalid Event Type: {event.data_type}. Simulation Failed.")
            quit()
            
    
    def transmit_process(self, event: Event):
        """
        Handles how the node reacts to a received event when it is in the transmitting state.
        :param event: The event to be processed.
        """       
        # When is the medium expected to be free
        expected_slot_free = event.nav
        
        # Do nothing if the event will end before node wants to transmit
        if self.event.timestamp > expected_slot_free:
            return
        
        # Check if the event is within the backoff window
        if self.backoff_start - event.timestamp < self.backoff:
            self.backoff = self.backoff_start + self.backoff - event.timestamp
        
        # Set the start time to the end of the event
        event_timestamp = expected_slot_free
        
        # Set Timestamps for the event
        event_timestamp = self.determine_timestamps(event_timestamp)
        
        self.set_event( event_timestamp)  


    def receive_event(self, event: Event):
        """
        Receives a BroadcastEvent and processes it accordingly.
        :param event: The event to be processed.
        """
        if self.event is None:
            return
        elif self.state == TX_STATE.WAITING_FOR_ACK:
           self.wait_for_ack_process(event)
        elif event.data_type != NodeType.COLLISION:
           # Collision is not a true event, it just notifies the node that a collision has occurred.
           # If this node is not looking for an ACK, id does not care
           self.transmit_process(event) 

    
    def declare_event(self, timestamp):
        """
        Gets the next event from the node.
        :return: The next event from the node.
        """
        # If Waiting for an ACK, do nothing
        if self.state == TX_STATE.WAITING_FOR_ACK:
            return None

        # An Event is already trying to occur
        elif self.event:
            return self.event
        
        # If an event is not already made, and there are arrivals
        elif self.TX_ARRIVAL_LIST:
            # New Packet. Retrieve next packet arrival time
            event_arr = self.TX_ARRIVAL_LIST.pop(0)
            
            # If the Packet arrival time is before the current timestamp, set the event timestamp to the current timestamp
            event_timestamp = event_arr if event_arr > timestamp else timestamp
       
            # Random Backoff
            self.backoff = self.set_backoff()
            
            # Set Timestamps for the event
            event_timestamp = self.determine_timestamps(event_timestamp)

            # Package duration will tell other nodes how long they have to wait before they can try to send
            self.set_event( event_timestamp)
            return self.event
        else:
            return None
        
    def print_statistics(self):
        print(f"TX: {self.ID}: Successful Transmission: {self.successful_transmissions}")
        print(f"TX: {self.ID}: Throughput: {self.successful_transmissions * self.packet_size / self.params['simulation_time'] / 10**3:.2f} Kbps")