import numpy as np
import pandas as pd
from os import path
from datetime import date

class LoggedItem:
    """Represents one item to track data under."""

    def __init__(self, name, columns=[]):
        """Initialize data table."""
        self.name = name
        self.directory = "logs/" + name + ".txt"
        if path.exists(self.directory):
            self.data = pd.read_csv(self.directory, index_col=0)
        else:
            self.data = pd.DataFrame(columns=columns)

    def add_entry(self, index=None):
        """Add an entry under the item."""
        columns = list(self.data.columns)
        today = [date.today().strftime("%m/%d/%Y")]
        prompt = "Enter data for columns (" + ", ".join(columns[1:]) + ") (Enter 'quit' when done): "
        user_in = input(prompt)
        while user_in != "quit":
            data = today + list(map(int, user_in.split()))
            new_entry = pd.DataFrame([data], columns=columns)
            self.data = self.data.append(new_entry, ignore_index=True)
            self.get_entries()
            user_in = input(prompt)
        self.data.to_csv(self.directory)

    def get_entries(self, indices=None):
        """Pull up entries corresponding to indices."""
        if indices == None:
            print(self.data)

    def add_columns(self, columns):
        """Add columns to the DataFrame."""
        for column in columns:
            a[column] = []

    def edit_entry(self, index):
        """Edit an entry in the DatFrame."""
        columns = list(self.data.columns)
        prompt = "Enter data for columns (" + ", ".join(columns) + "): "
        user_in = input(prompt).split()
        user_in = [user_in[0]] + list(map(int, user_in[1:]))
        self.data.loc[int(index)] = user_in
        self.data.to_csv(self.directory)

