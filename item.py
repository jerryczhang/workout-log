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
            self.data = pd.read_csv(self.directory, index_col=0, dtype=str)
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
        return r.Status(True)

    def insert(self, data, index):
        """Insert a new entry at index."""
        dataf = pd.DataFrame([data], columns=self.get_columns())
        if not index.isnumeric():
            return r.Status(False, "\tIndex must be an integer")
        index = int(index)
        max_index = list(self.data.index)[-1]
        if index < 0:
            return r.Status(False, "\tIndex must be at least 0")
        elif index > max_index:
            return self.append(data)
        else:
            data_a = self.data.iloc[:index]
            data_b = self.data.iloc[index:]
            self.data = data_a.append(dataf).append(data_b).reset_index(drop=True)
            self.data.to_csv(self.directory)
            return r.Status(True)

    def get_entries(self, filter_col=None, filter_op=None, value=None, col=None):
        """Pull up entries corresponding to filter."""
        filters = {
                "=" : lambda c, v : c == v,
                ">" : lambda c, v : c > v,
                "<" : lambda c, v : c < v,
                ">=" : lambda c, v : c >= v,
                "<=" : lambda c, v : c <= v,
        }
        mask = None
        if filter_col is not None:
            if filter_col not in self.get_columns():
                return r.Status(False, "\tColumn \"%s\" not found\n\tValid columns: %s" % (col, ", ".join(self.get_columns())))
            if filter_op not in filters:
                return r.Status(False, "\tFilter operation \"" + filter_op + "\" invalid\n\tValid operations: " + ", ".join(filters.keys()))
            column = self.data[filter_col].map(en.parse_data)
            value = en.parse_data(value)
            if type(column) is r.Status:
                return column
            if type(value) is r.Status:
                return value
            try:
                mask = filters[filter_op](column, value)
            except TypeError:
                return r.Status(False, "\tInvalid type entered (%s) for column type (%s)" % (type(value), type(column[0])))
        if col:
            if col not in self.get_columns():
                return r.Status(False, "\tColumn \"%s\" not found\n\tValid columns: %s" % (col, ", ".join(self.get_columns())))
    
        if mask is not None and col:
            print(self.data[col][mask])
        elif mask is not None:
            print(self.data[mask])
        elif col:
            print(self.data[col])
        else:
            print(self.data)
        return r.Status(True)

    def add_columns(self, columns):
        """Add columns to the DataFrame."""
        for column in columns:
            a[column] = []

    def edit_entry(self, index, data):
        """Edit an entry in the DataFrame."""
        self.data.loc[int(index)] = data
        self.data.to_csv(self.directory)
        return r.Status(True)

    def delete_entry(self, index):
        """Delete an entry in the DataFrame."""
        if index not in self.data.index:
            return r.Status(False, "\tEntry number " + str(index) + " does not exist")
        self.data = self.data.drop(index)
        return r.Status(True)
