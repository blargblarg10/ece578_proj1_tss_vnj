import matplotlib.pyplot as plt
import matplotlib.patches as patches

class EventVisualizer:
    def __init__(self):
        self.colors = {
            'ACK': 'green',
            'DATA': 'blue',
            'DIFS': 'gray',
            'SIFS': 'gray',
            'COLLISION': 'red'
        }
        self.fig, self.ax = plt.subplots()
        self.max_x = 0  # Initialize max_x to keep track of the maximum x value

    def initialize(self, nodes):
        self.node_ids = [node.ID for node in nodes]
        self.ax.set_yticks(range(len(self.node_ids) + 1))  # Set yticks to one larger than the number of nodes
        self.ax.set_yticklabels(self.node_ids + [""])  # Add an extra label for the additional tick
        self.ax.set_xlabel('Time (slots)')
        legend_handles = [patches.Patch(color=color, label=event) for event, color in self.colors.items()]
        self.ax.legend(handles=legend_handles)
        plt.draw()
        plt.pause(0.001)

    def plot_event(self, node_id, timestamp, event_name, duration):
        y_position = self.node_ids.index(node_id)
        color = self.colors.get(event_name, "black")
        rect = patches.Rectangle((timestamp, y_position), duration, 1, linewidth=0.7, edgecolor='black', facecolor=color)
        self.ax.add_patch(rect)
        self.max_x = max(self.max_x, timestamp + duration)  # Update max_x after adding the event
        self.ax.set_xlim(0, self.max_x)  # Set the x-axis limit to max_x
        plt.draw()  # This will update the plot in real-time
        plt.pause(0.001)

    def show(self):
        plt.show()
