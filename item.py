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

    def to_integer(self, string):
        """Convert a string to integer, first checking for numeric."""
        if string.isnumeric():
            return int(string)
        else:
            return string

    def add_entry(self, index=None):
        """Add an entry under the item."""
        columns = list(self.data.columns)
        today = [date.today().strftime("%m/%d/%Y")]
        prompt = "Enter data for columns (" + ", ".join(columns[1:]) + ") (Enter 'quit' when done): "
        user_in = input(prompt)
        while user_in != "quit":
            data = today + list(map(self.to_integer, user_in.split()))
            new_entry = pd.DataFrame([data], columns=columns)
            self.data = self.data.append(new_entry, ignore_index=True)
            self.get_entries()
            user_in = input(prompt)
        self.data.to_csv(self.directory)

    def get_entries(self, col=None, filter_op=None, value=None):
        """Pull up entries corresponding to filter."""
        if not col:
            print(self.data)
        else:
            if filter_op == "equals":
                mask = self.data[col] == self.to_integer(value)
            elif filter_op == "greater":
                mask = self.data[col] >= self.to_integer(value)
            elif filter_op == "less":
                mask = self.data[col] <= self.to_integer(value)
            print(self.data[mask])

    def add_columns(self, columns):
        """Add columns to the DataFrame."""
        for column in columns:
            a[column] = []

    def edit_entry(self, index):
        """Edit an entry in the DatFrame."""
        columns = list(self.data.columns)
        prompt = "Enter data for columns (" + ", ".join(columns) + "): "
        user_in = input(prompt).split()
        user_in = list(map(self.to_integer, user_in))
        self.data.loc[int(index)] = user_in
        self.data.to_csv(self.directory)

