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

    def parse_input(self, string):
        """Convert a string to the correct type."""
        if string.isnumeric():
            return int(string)
        elif '/' in string:
            in_date = string.split('/')
            in_date = list(map(int, in_date))
            return date(in_date[2], in_date[0], in_date[1])
        else:
            return string

    def add_entry(self, index=None):
        """Add an entry under the item."""
        columns = list(self.data.columns)
        today = [date.today().strftime("%m/%d/%Y")]
        prompt = "Enter data for columns (" + ", ".join(columns[1:]) + ") (Enter 'quit' when done): "
        user_in = input(prompt)
        while user_in != "quit":
            data = today + list(map(self.parse_input, user_in.split()))
            if len(data) != len(columns):
                print("\tColumn count mismatch: %d columns entered, needs %d." % (len(data) - 1, len(columns) - 1))
            else:
                new_entry = pd.DataFrame([data], columns=columns)
                self.data = self.data.append(new_entry, ignore_index=True)
                self.get_entries()
            user_in = input(prompt)
        self.data.to_csv(self.directory)

    def get_entries(self, col=None, filter_op=None, value=None):
        """Pull up entries corresponding to filter."""
        failed = False
        if not col:
            print(self.data)
        else:
            if col not in list(self.data.columns):
                print("\tColumn \"" + col + "\" not found.")
                failed = True
            if filter_op not in ["equals", "greater", "less"]:
                print("\tFilter operation \"" + filter_op + "\" not valid.")
                failed = True
            if not failed:
                column = self.data[col].map(self.parse_input)
                value = self.parse_input(value)
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

    def edit_entry(self, index):
        """Edit an entry in the DatFrame."""
        columns = list(self.data.columns)
        prompt = "\nEnter data for columns (" + ", ".join(columns) + "): "
        user_in = input(prompt).split()
        user_in = list(map(self.parse_input, user_in))
        self.data.loc[int(index)] = user_in
        self.data.to_csv(self.directory)

