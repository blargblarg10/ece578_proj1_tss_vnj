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
from utility.plot_timeline import EventVisualizer
from src.csma_ca_ap import CsmaCaAp
from src.csma_ca_tx import CsmaCaTx
from src.network import Network

def load_parameters(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def create_and_run_simulation(params):
    visualizer = EventVisualizer()
    
    logger.info('Starting CSMA/CA simulation testbench')

    sim_params = load_parameters('sim/settings/settings.json')
    test_params = load_parameters(params.test_file)

    # Overwrite simulation parameters with test parameters if they are specified
    if "sim_overwrite" in test_params:
        for key, value in test_params["sim_overwrite"].items():
            sim_params[key] = value

    logger.info(f'Using simulation parameters:\n {json.dumps(sim_params, indent=2)}')

    # Create network with collision domains
    network = Network(sim_params)
    for tx_node in test_params['tx_nodes']:
        if "arrivals" in tx_node:
            arrivals = tx_node["arrivals"]
        else:
            arrivals = generate_poisson_traffic(sim_params['lambda_A'], sim_params['simulation_time'], sim_params['slot_duration'])
        
        node = CsmaCaTx(f"Tx_Node_{tx_node['id']}", tx_node['cd'],sim_params, arrivals, visualizer)
        network.add(node)

    for ap_node in test_params['ap_nodes']:
        node = CsmaCaAp(f"AP_Node_{ap_node['id']}", ap_node['cd'],sim_params, visualizer)
        network.add(node)

    visualizer.initialize(network.nodes)
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
