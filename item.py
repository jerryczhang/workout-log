import numpy as np
import pandas as pd
from os import path

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

    def get_columns(self):
        """Return the columns of this item."""
        return list(self.data.columns)
    
    def append(self, data):
        """Append a new entry."""
        data = pd.DataFrame([data], columns=self.get_columns())
        self.data = self.data.append(data, ignore_index=True)
        self.data.to_csv(self.directory)

    def get_entries(self, col=None, filter_op=None, value=None):
        """Pull up entries corresponding to filter."""
        if not col:
            print(self.data)
        else:
            column = self.data[col].map(self.parse_data)
            value = self.parse_data(value)
            if filter_op == "equals":
                mask = column == value
            elif filter_op == "greater":
                mask = column > value
            elif filter_op == "less":
                mask = column < value
            print(self.data[mask])

    def add_columns(self, columns):
        """Add columns to the DataFrame."""
        for column in columns:
            a[column] = []

    def edit_entry(self, index, data):
        """Edit an entry in the DatFrame."""
        self.data.loc[int(index)] = data
        self.data.to_csv(self.directory)

