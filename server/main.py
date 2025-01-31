import agentpy as ap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use('TkAgg')
import IPython.display
import os

from RouteModel import RouteModel


file_path = os.path.join(os.path.dirname(__file__), "streets.npy")

# Load street data
streets = np.load(file_path)

# Define parameters
parameters = {
    'streets': streets,
    'start': (11, 0),
    'goal': (6, 29)
}



# Run the simulation
model = RouteModel(parameters)
model.run()