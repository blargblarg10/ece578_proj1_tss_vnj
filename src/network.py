# network.py
from utility.logger_config import logger
from src.collision_domain import CollisionDomain

class Network:
    def __init__(self):
        logger.debug("Network instance created.")
        self.collision_domains = []
        # ... (other methods and attributes) ...
        
    def add(self, collision_domain):
        """
        Adds a collision domain to the network.
        :param collision_domain: The collision domain to be added, must be of type CollisionDomain.
        """
        if isinstance(collision_domain, CollisionDomain):
            self.collision_domains.append(collision_domain)
        else:
            raise ValueError("Invalid collision domain type. Collision domain must be of type CollisionDomain.")

    def print_network_structure(self):
        """
        Logs the structure of the network, including domain IDs and node IDs in every collision domain.
        """
        logger.info("Network Structure:")
        for domain in self.collision_domains:
            tx_node_ids = [node.id for node in domain.tx_nodes]
            ap_node_ids = [node.id for node in domain.ap_nodes]
            logger.info(f"Collision Domain ID: {domain.id}")
            logger.info(f"  Tx Nodes: {', '.join(map(str, tx_node_ids)) if tx_node_ids else 'None'}")
            logger.info(f"  AP Nodes: {', '.join(map(str, ap_node_ids)) if ap_node_ids else 'None'}")
