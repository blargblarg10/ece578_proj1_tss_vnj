# network.py
from utility.logger_config import logger
import time
from src.proj_data_classes import Event
from src.csma_ca_ap import CsmaCaAp
from src.csma_ca_tx import CsmaCaTx

class Network:
    def __init__(self, sim_params):
        logger.debug("Network instance created.")
        self.nodes = []
        self.slot_limit = int(sim_params['simulation_time']/(sim_params['slot_duration']))
        pass
        # ... (other methods and attributes) ...
        
    def add(self, node):
        """
        Adds a node to the collision domain. Nodes are added to their respective lists based on their type.
        :param node: The node to be added, can be of type CsmaCaTx or CsmaCaAp.
        """
        if isinstance(node, CsmaCaTx) or isinstance(node, CsmaCaAp):
            self.nodes.append(node)
        else:
            raise ValueError("Invalid node type. Node must be of type CsmaCaTx or CsmaCaAp.")

    def print_network_structure(self):
        """
        Logs the structure of the network, including domain IDs and node IDs in every collision domain.
        """
        logger.info("Network Structure:")
        
        # Create a dictionary to store nodes for each collision domain
        collision_domains = {}
        
        # Iterate over all nodes and add them to the corresponding collision domain in the dictionary
        for node in self.nodes:
            for collision_id in node.CD:
                if collision_id not in collision_domains:
                    collision_domains[collision_id] = {'tx_nodes': [], 'ap_nodes': []}
                if isinstance(node, CsmaCaTx):
                    collision_domains[collision_id]['tx_nodes'].append(node.ID)
                elif isinstance(node, CsmaCaAp):
                    collision_domains[collision_id]['ap_nodes'].append(node.ID)
        
        # Log the nodes in each collision domain
        for collision_id, nodes in collision_domains.items():
            logger.info(f"Collision Domain ID: {collision_id}")
            logger.info(f"  Tx Nodes: {', '.join(map(str, nodes['tx_nodes'])) if nodes['tx_nodes'] else 'None'}")
            logger.info(f"  AP Nodes: {', '.join(map(str, nodes['ap_nodes'])) if nodes['ap_nodes'] else 'None'}")

    def run(self):
        """
        Runs the simulation for all collision domains in the network.
        """     
        # set timeout to 120 seconds
        timeout = 120
        start_time = time.time()
        current_slot = 0

        while current_slot < self.slot_limit:
            nodes_w_events = []
            for node in self.nodes:
                if node.declare_event(current_slot) is not None:
                    nodes_w_events.append(node.event)
            if not nodes_w_events:
                logger.error("No events to process. Ending simulation.")
                quit()
            earliest_timestamp = min(event.timestamp for event in nodes_w_events)
            earliest_events = [event for event in nodes_w_events if event.timestamp == earliest_timestamp]

            # Inform nodes that they will be broadcasting
            for event in earliest_events:
                corresponding_node = next(node for node in self.nodes if node.ID == event.node_id)
                corresponding_node.inform_broadcasting()

            # Inform other nodes of the event
            for node in self.nodes:
                if node.ID not in [event.node_id for event in earliest_events]:
                    for event in earliest_events:
                        node.receive_event(event)

            current_slot = max([event.nav for event in earliest_events])  # Update current slot to the timestamp of the earliest event

            # elapsed_time = time.time() - start_time
            # if elapsed_time > timeout:
            #     logger.error("Time limit reached. Ending simulation.")
            #     break
            
        for node in self.nodes:
            node.print_statistics()

    def broadcast(self, event: Event):
        # Broadcasting logic here
        pass