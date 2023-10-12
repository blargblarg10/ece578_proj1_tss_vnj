import numpy as np

def generate_poisson_traffic(lam, simulation_time, slot_duration):
    """
    Generates Poisson-distributed traffic.

    Parameters:
    lam (float): The rate of arrivals (lambda).
    simulation_time (float): The total simulation time in seconds.
    frame_size (float): The size of a frame in seconds.

    Returns:
    list: A list of arrival times in terms of frame numbers.
    """
    # Generate uniform distribution
    uniform_distribution = np.random.uniform(low=0, high=1, size=int(lam * (simulation_time * 2)))
    # Convert uniform distribution to exponential distribution
    exponential_distribution = -(1 / lam) * np.log(1 - uniform_distribution)
    # Transform the packet transmittion time to interpacket slot times
    interpacket_time_slot = np.ceil(exponential_distribution / (slot_duration)).astype(int)
    # Find the approximated packet slot arrival time
    arrival_time_slot = np.cumsum(interpacket_time_slot)

    return arrival_time_slot

def main():
    # Example usage:
    lam = 2000  # Rate of arrivals (e.g., 100 frames per second)
    simulation_time = 0.01  # Total simulation time (e.g., 10 seconds)
    slot_duration = 10e-6  # Slot size (10 microseconds)
    traffic = generate_poisson_traffic(lam, simulation_time, slot_duration)
    print(traffic)

if __name__ == "__main__":
    main()
