import numpy as np
import matplotlib.pyplot as plt
import os

class Simulation:
    # Simulation Parameters
    arrival_rates = [1000]
    simulation_time = 0.01
    slot_duration = 10 * 10**(-6)
    simulation_slots = round(simulation_time / slot_duration)
    bandwidth = 10 * 10**(6) # In bits per second
    packet_size = 1500 * 8 # In bits

    # Backoff Paremeters
    cw_base = 4
    cw_max = 1024

    # Packet Parameters
    difs = 4
    sifs = 1
    rts = 2
    cts = 2
    ack = 2
    tx_slots = packet_size / (bandwidth * slot_duration)
    pass

    def plot_simulation(self, report_single, report_singe_vcs):
        # Create output directory to store images
        if not os.path.exists('out'):
            os.mkdir('out')

        plt.plot(report_single['rate'], report_single['throughput_r1'])
        plt.plot(report_singe_vcs['rate'], report_singe_vcs['throughput_r1'])
        plt.legend(["(a)-CSMA", "(a)-CSMA/VCS"], loc ="lower right")
        plt.xlabel("Arrival Rate (Frames/Seconds)")
        plt.ylabel("Throughput (Kbps)")
        plt.title('Node A - Throughput vs. Rate')
        plt.savefig('out/throughput_a.png')   # save the figure to file

        plt.figure()
        plt.plot(report_single['rate'], report_single['throughput_r2'])
        plt.plot(report_singe_vcs['rate'], report_singe_vcs['throughput_r2'])
        plt.legend(["(a)-CSMA", "(a)-CSMA/VCS"], loc ="lower right")
        plt.xlabel("Arrival Rate (Frames/Seconds)")
        plt.ylabel("Throughput (Kbps)")
        plt.title('Node C - Throughput vs. Rate')
        plt.savefig('out/throughput_c.png')   # save the figure to file

        plt.figure()
        plt.plot(report_single['rate'], report_single['collisions'])
        plt.plot(report_singe_vcs['rate'], report_singe_vcs['collisions'])
        plt.legend(["(a)-CSMA", "(a)-CSMA/VCS"], loc ="lower right")
        plt.xlabel("Arrival Rate (Frames/Seconds)")
        plt.ylabel("Collissions (N)")
        plt.title('Node A - Number of Collissions vs. Rate')
        plt.savefig('out/collisions_a.png')   # save the figure to file

        plt.figure()
        plt.plot(report_single['rate'], report_single['fairness_index'])
        plt.plot(report_singe_vcs['rate'], report_singe_vcs['fairness_index'])
        plt.legend(["(a)-CSMA", "(a)-CSMA/VCS"], loc ="lower right")
        plt.xlabel("Arrival Rate (Frames/Seconds)")
        plt.ylabel("Fairness Index (FI)")
        plt.title('Fairnes Index vs. Rate')
        plt.savefig('out/fairness_index.png')   # save the figure to file

    def run_simulation(self):

        print("Running Simulation for Single Collision Domain...")
        single_collision_report = {'rate': [], 'collisions': [], 'throughput_r1': [], 'throughput_r2': [], 'fairness_index': []}
        for rate in self.arrival_rates:
            performance_metrics = self.start_simulation(rate, False)
            single_collision_report['rate'].append(performance_metrics['rate'])
            single_collision_report['collisions'].append(performance_metrics['collisions'])
            single_collision_report['throughput_r1'].append(performance_metrics['throughput_r1'])
            single_collision_report['throughput_r2'].append(performance_metrics['throughput_r2'])
            single_collision_report['fairness_index'].append(performance_metrics['fairness_index'])

        print("Running Simulation for Single Collision Domain with VCS enable...")
        single_collision_vcs_report = {'rate': [], 'collisions': [], 'throughput_r1': [], 'throughput_r2': [], 'fairness_index': []}
        for rate in self.arrival_rates:
            performance_metrics = self.start_simulation(rate, True)
            single_collision_vcs_report['rate'].append(performance_metrics['rate'])
            single_collision_vcs_report['collisions'].append(performance_metrics['collisions'])
            single_collision_vcs_report['throughput_r1'].append(performance_metrics['throughput_r1'])
            single_collision_vcs_report['throughput_r2'].append(performance_metrics['throughput_r2'])
            single_collision_vcs_report['fairness_index'].append(performance_metrics['fairness_index'])

        self.plot_simulation(single_collision_report, single_collision_vcs_report)

    def start_simulation(self, rate, isVCSEnable):
        # Create transmitting routers
        router1 = Router(rate, isVCSEnable)
        router2 = Router(rate, isVCSEnable)

        # Tracking Variables
        extension = 0
        collision_counter = 0

        # Initialize the startup timing slot
        current_time_slot = router1.arrival_slot[0] if router1.arrival_slot[0] <= router2.arrival_slot[0] else router2.arrival_slot[0]

        # Start simulation until simulation time exceeded
        while self.simulation_slots > current_time_slot:
            if router1.backoff < 0 or extension != 0:
                router1.backoff = np.random.randint(0, self.cw_base * 2**extension)
            if router2.backoff < 0 or extension != 0:
                router2.backoff = np.random.randint(0, self.cw_base * 2**extension)
            
            # Check if more than two frames are to compete for the same medium
            if router1.arrival_slot[router1.slot_index] <= current_time_slot and router2.arrival_slot[router2.slot_index] <= current_time_slot:
                # Check if for possible packet collision or detection of medium usage
                if router1.backoff == router2.backoff:
                    if isVCSEnable == True:
                        current_time_slot += self.difs + router1.backoff + self.rts + self.sifs + self.cts
                    else:
                        current_time_slot += self.difs + router1.backoff + self.tx_slots + self.sifs + self.ack
                    extension += 1
                    collision_counter += 1
                elif router1.backoff < router2.backoff:
                    # Adjust backoff of competing frame
                    router2.backoff = router2.backoff - router1.backoff
                    current_time_slot += router1.generate_transmission()
                    extension = 0
                else:
                    # Adjust backoff of competing frame
                    router1.backoff = router1.backoff - router2.backoff
                    current_time_slot += router2.generate_transmission()
                    extension = 0
            elif router1.arrival_slot[router1.slot_index] <= current_time_slot:
                current_time_slot += router1.generate_transmission()
            elif router2.arrival_slot[router2.slot_index] <= current_time_slot:
                current_time_slot += router2.generate_transmission()

            # In idle, thus increment the time slot till something to transmit
            else:
                current_time_slot += 1

        # Packet count that have been sent succesfully
        number_of_successes_1 = router1.slot_index
        number_of_successes_2 = router2.slot_index

        # Clean up post simulation to improve performance
        del router1, router2

        # Thorughput for each respective router
        throughput_1 = number_of_successes_1 * (self.packet_size / self.simulation_time)
        throughput_2 = number_of_successes_2 * (self.packet_size / self.simulation_time)

        fairness_index = number_of_successes_1 / number_of_successes_2

        print(f"------------------------Simulation with an arrival rate of {rate} frames/sec------------------------")
        print(f"Router 1 - Total packets succesfully sent: {number_of_successes_1}, Router 2 - Total packets succesfully sent: {number_of_successes_2}")
        print(f"Collisions: {collision_counter}, Router 1 Throughput: {throughput_1 * 10**(-3):.{2}f} Kbps, Router 2 Throughput: {throughput_2 * 10**(-3):.{2}f} Kbps, FI: {fairness_index:.{2}f}")

        performance_metrics = {'rate': rate, 'collisions': collision_counter, 'throughput_r1': throughput_1, 'throughput_r2': throughput_2, 'fairness_index': fairness_index}
        
        return performance_metrics

class Router(Simulation):
    def __init__(self, rate, isVCSEnable):
       self.arrival_slot = self.generate_traffic(rate)
       self.isVCSEnable = isVCSEnable
       self.slot_index = 0
       self.backoff = -1

    def generate_transmission(self):
        if self.isVCSEnable == True:
            transmission_time = self.difs + self.backoff + self.rts + self.sifs + self.cts + self.sifs + self.tx_slots + self.sifs + self.ack
        else:
            transmission_time = self.difs + self.backoff + self.tx_slots + self.sifs + self.ack
        self.slot_index += 1
        self.backoff = -1
        return transmission_time

    def generate_traffic(self, arrival_rate):
        # Generate uniform distribution
        uniform_distribution = np.random.uniform(low=0, high=1, size=int(arrival_rate * self.simulation_time))
        # Convert uniform distribution to exponential distribution
        exponential_distribution = -(1 / arrival_rate) * np.log(1 - uniform_distribution)
        # Transform the packet transmittion time to interpacket slot times
        interpacket_time_slot = np.ceil(exponential_distribution / self.slot_duration)
        # Find the approximated packet slot arrival time
        arrival_time_slot = np.cumsum(interpacket_time_slot)
        # Pad with extra values arriaval times that are greater then simulation tim so there is no overflow when reading data
        arrival_time_slot_padded = np.append(arrival_time_slot, np.full(int(arrival_rate * self.simulation_time), self.simulation_slots))
        
        return arrival_time_slot_padded

def main():
    simulation = Simulation()
    simulation.run_simulation()

main()