import numpy as np
import pandas as pd
from os import path

class LoggedItem:
    """Represents one item to track data under."""

    def __init__(self, name):
        """Initialize data table."""
        self.name = name
        if path.exists(name + ".txt"):
            self.data = pd.read_csv(name + ".txt")
        else:
            self.data = pd.DataFrame()

    def add_entry(self, index):
        """Add an entry under the item."""
        pass

    def get_entry(self, indices):
        """Pull up entries corresponding to indices."""
        pass

