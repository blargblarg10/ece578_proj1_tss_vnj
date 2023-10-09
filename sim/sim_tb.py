"""
sim_tb.py

Description:
    The sim_tb is the main module initializes and starts the network simulation.
    It creates instances of transmitting stations, access points, and collision domains, and initiates the simulation process.

Usage:
    - Set up the simulation parameters and start the simulation.
    - The main module acts as the entry point for the simulation, coordinating the interaction between different components.
"""

# sim_tb.py
import argparse
import json
import os
from utility.poisson_traffic import generate_poisson_traffic
from utility.logger_config import setup_logger, logger
from src.csma_ca_ap import CsmaCaAp
from src.csma_ca_tx import CsmaCaTx
from src.collision_domain import CollisionDomain
from src.network import Network

def load_parameters(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def create_and_run_simulation(params):
    setup_logger(params.debug)
    logger.info('Starting CSMA/CA simulation testbench')

    sim_params = load_parameters('sim/settings/settings.json')
    test_params = load_parameters(params.test_file)

    # Overwrite simulation parameters with test parameters if they are specified
    for key, value in test_params.items():
        sim_params[key] = value

    logger.info(f'Using simulation parameters: {json.dumps(sim_params, indent=2)}')

    # Create network with collision domains
    network = Network()
    for cd_id, cd_params in enumerate(test_params['collision_domains'].values()):
        cd = CollisionDomain(cd_id)
        for tx_node_id in cd_params['tx_nodes']:
            if "arrivals" in tx_node_id:
                arrivals = tx_node_id["arrivals"]
            else:
                arrivals = generate_poisson_traffic(sim_params['lambda_A'], sim_params['simulation_time'], sim_params['slot_duration'])
            
            tx_node = CsmaCaTx(tx_node_id["id"], sim_params, arrivals)
            cd.add(tx_node)
        for ap_node_id in cd_params['ap_nodes']:
            ap_node = CsmaCaAp(ap_node_id, sim_params)
            cd.add(ap_node)
        network.add(cd)
        
    network.print_network_structure()
    network.run()

def main():
    parser = argparse.ArgumentParser(description='Run the network simulation with specified test parameters.')
    parser.add_argument('test_file', type=str, help='Path to the test parameters JSON file', nargs='?')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for verbose logging')

    args = parser.parse_args()

    if args.test_file is None:
        args.test_file = 'hw2_1'

    args.test_file = os.path.join('sim/tst', args.test_file + '.json')
    if not os.path.exists(args.test_file):
        parser.error(f"The test file {args.test_file} does not exist")

    create_and_run_simulation(args)

if __name__ == "__main__":
    main()
