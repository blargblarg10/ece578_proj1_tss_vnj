import numpy as np

def generate_poisson_traffic(lam, simulation_time, frame_size):
    """
    Generates Poisson-distributed traffic.

    Parameters:
    lam (float): The rate of arrivals (lambda).
    simulation_time (float): The total simulation time in seconds.
    frame_size (float): The size of a frame in seconds.

    Returns:
    list: A list of arrival times in terms of frame numbers.
    """
    n = int(lam * simulation_time)  # Calculate the number of random numbers needed
    U = np.random.uniform(0, 1, n)  # Generate n uniformly distributed random numbers in (0, 1)
    X = -1/lam * np.log(1 - U)      # Convert U to exponentially distributed numbers
    arrival_times = np.round(X / frame_size).astype(int)  # Convert arrival times to frame numbers
    # Print average arrival rate
    arrival_times = np.cumsum(arrival_times)    # Accumulate the inter-arrival times to get arrival times
    return arrival_times

def main():
    # Example usage:
    lam = 100  # Rate of arrivals (e.g., 100 frames per second)
    simulation_time = 10  # Total simulation time (e.g., 10 seconds)
    frame_size = 10e-6  # Frame size (10 microseconds)
    traffic = generate_poisson_traffic(lam, simulation_time, frame_size)
    print(traffic)

if __name__ == "__main__":
    main()
