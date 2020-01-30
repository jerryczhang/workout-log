import numpy as np
import pandas as pd
import encode as en
import return_code as r
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
        filters = {
                "=" : lambda c, v : c == v,
                ">" : lambda c, v : c > v,
                "<" : lambda c, v : c < v,
                ">=" : lambda c, v : c >= v,
                "<=" : lambda c, v : c <= v,
        }
        if col is None:
            print(self.data)
            return r.Status(True)
        else:
            if col not in self.get_columns():
                return r.Status(False, "\tColumn \"" + col + "\" not found\n\tValid columns: " + ", ".join(self.get_columns()))
            if filter_op not in filters:
                return r.Status(False, "\tFilter operation \"" + filter_op + "\" invalid\n\tValid operations: " + ", ".join(filters.keys()))
            column = self.data[col].map(en.parse_data)
            value = en.parse_data(value)
            if type(column) is r.Status:
                return column
            if type(value) is r.Status:
                return value
            try:
                mask = filters[filter_op](column, value)
            except TypeError:
                return r.Status(False, "\tInvalid type entered (%s) for column type (%s)" % (type(value), type(column[0])))
            print(self.data[mask])
            return r.Status(True)

    def add_columns(self, columns):
        """Add columns to the DataFrame."""
        for column in columns:
            a[column] = []

    def edit_entry(self, index, data):
        """Edit an entry in the DatFrame."""
        self.data.loc[int(index)] = data
        self.data.to_csv(self.directory)

