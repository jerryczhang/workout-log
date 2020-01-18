import numpy as np
import pandas as pd
from os import path

class LoggedItem:
    """Represents one item to track data under."""

    def __init__(self, name):
        """Initialize data table."""
        self.name = name
        self.directory = "logs/" + name + ".txt"
        if path.exists(self.directory):
            self.data = pd.read_csv(self.directory)
        else:
            self.data = pd.DataFrame()

    def add_entry(self, index=None):
        """Add an entry under the item."""
        columns = list(self.data.columns)
        prompt = "Enter data for columns (" + ", ".join(columns) + "):\n"
        user_in = input(prompt)
        while user_in != "quit":
            data = user_in.split()
            new_entry = pd.DataFrame([data], columns=columns)
            self.data = self.data.append(new_entry, ignore_index=True)
            self.get_entries()
            user_in = input(prompt)

    def get_entries(self, indices=None):
        """Pull up entries corresponding to indices."""
        if indices == None:
            print(self.data)
