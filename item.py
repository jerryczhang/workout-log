import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import encode as en
import return_code as r
from matplotlib.dates import date2num
from datetime import date
import os

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class LoggedItem:
    """Represents one item to track data under."""

    def __init__(self, name, columns=[], copy_from=None):
        """Initialize data table."""
        self.name = name
        self.directory = "logs/" + name + ".txt"
        if os.path.exists(self.directory):
            self.data = pd.read_csv(self.directory, index_col=0, dtype=str)
        elif columns:
            self.data = pd.DataFrame(columns=columns)
            self.save()
        elif copy_from:
            self.data = copy_from.data.copy()
            self.save()

    def get_columns(self):
        """Return the columns of this item."""
        return list(self.data.columns)

    def get_indices(self):
        """Return the indices of this item."""
        return list(self.data.index)

    def save(self):
        """Save the data to CSV."""
        self.data.to_csv(self.directory)
    
    def checktype(self, vals):
        """Check if the types of incoming data are compatible."""
        if len(self.data) == 0:
            return -1
        item_parsed = list(map(en.parse_data, self.data.loc[0]))
        item_types = list(map(type, item_parsed))
        vals_parsed = list(map(en.parse_data, vals.loc[0]))
        vals_types = list(map(type, vals_parsed))
        for index in range(len(item_types)):
            if item_types[index] != vals_types[index]:
                return index
        return -1

    def insert(self, data, index=None):
        """Insert a new entry at index."""
        dataf = pd.DataFrame([data], columns=self.get_columns())
        col_index = self.checktype(dataf)
        if col_index != -1:
            return r.Status(False, "\tInvalid type entered for column \"%s\"" 
                    % self.get_columns()[col_index])
        if index == None or index >= len(self.data):
            self.data = self.data.append(dataf, ignore_index=True)
        else:
            data_a = self.data.iloc[:index]
            data_b = self.data.iloc[index:]
            self.data = data_a.append(dataf).append(data_b).reset_index(drop=True)
        self.save()
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
        if filter_col:
            if filter_col not in self.get_columns():
                return r.Status(False, "\tColumn \"%s\" not found\n\tValid columns: %s" 
                        % (filter_col, ", ".join(self.get_columns())))
            if filter_op not in filters:
                return r.Status(False, "\tFilter operation \"%s\" invalid\n\tValid operations: %s"
                        % (filter_op, ", ".join(filters.keys())))
            column = self.data[filter_col].map(en.parse_data)
            value = en.parse_data(value)
            if type(column) is r.Status:
                return column
            if type(value) is r.Status:
                return value
            try:
                mask = filters[filter_op](column, value)
            except TypeError:
                return r.Status(False, "\tInvalid type entered (%s) for column type (%s)" 
                        % (type(value), type(column[0])))
        else:
            mask = [True for _ in range(len(self.data))]
        if col:
            col = en.parse_data(col)
            if type(col) == str:
                if col not in self.get_columns():
                    return r.Status(False, "\tColumn \"%s\" not found\n\tValid columns: %s" 
                            % (col, ", ".join(self.get_columns())))
            elif type(col) == list:
                if col[1] > len(self.get_columns()):
                    return r.Status(False, "\tColumn index %d out of bounds, max is %d" 
                            % (col[1], len(self.get_columns())))
                col = self.get_columns()[col[0]:col[1]:col[2]]
            elif type(col) == r.Status:
                return col
        else:
            col = self.get_columns() 
        filtered_data = self.data[col][mask]
        if type(filtered_data) == pd.core.series.Series:
            filtered_data = filtered_data.to_frame()
        print(filtered_data)
        filtered_data.to_csv("logs/last.txt")
        return r.Status(True)

    def add_columns(self, columns):
        """Add columns to the DataFrame."""
        for column in columns:
            a[column] = []

    def expand(self, col_name, data):
        """Add a column with data to the DataFrame."""
        if len(data) != len(self.data) and len(data) != 0:
            return r.Status(False, "\tInvalid number of entries: %d entered, 0 or %d needed" 
                    % (len(data), len(self.data)))
        if len(data) == 0:
            self.data[col_name] = [0 for x in range(len(self.data))]
        else:
            self.data[col_name] = data
        self.save()
        return r.Status(True)

    def delete_col(self, col_name):
        """Remove a column from the DataFrame."""
        if col_name not in self.get_columns():
            return r.Status(False, "\tColumn \"%s\" not found\n\tValid columns: %s" 
                    % (col_name, ", ".join(self.get_columns())))
        self.data = self.data.drop(col_name, axis=1)
        self.save()
        return r.Status(True)

    def edit_entry(self, index, data):
        """Edit an entry in the DataFrame."""
        dataf = pd.DataFrame([data], columns=self.get_columns())
        col_index = self.checktype(dataf)
        if col_index != -1:
            return r.Status(False, "\tInvalid type entered for column \"%s\"" 
                    % self.get_columns()[col_index])
        self.data.loc[int(index)] = data
        self.save()
        return r.Status(True)

    def delete_entry(self, index):
        """Delete an entry in the DataFrame."""
        if not index.isnumeric():
            return r.Status(False, "\tIndex must be numeric")
        else:
            index = int(index)
        if index not in self.data.index:
            return r.Status(False, "\tEntry number %d does not exist" % index)
        self.data = self.data.drop(index)
        self.save()
        return r.Status(True)

    def delete_item(self):
        """Delete this item."""
        os.remove(self.directory)
        return r.Status(True)

    def rename(self, name, col=None):
        """Rename this item, or a column."""
        if col == None:
            self.name = name
            os.remove(self.directory)
            self.directory = "logs/" + name + ".txt"
            self.save()
            return r.Status(True)
        else:
            if col not in self.get_columns():
                return r.Status(False, "\tColumn \"%s\" not found\n\tValid columns: %s" 
                        % (col, ", ".join(self.get_columns())))
            self.data = self.data.rename(columns={col:name})
            self.save()
            return r.Status(True)
    def graph(self, x_col, graph_type):
        """Graph the data wrt to x_col."""
        parsed_data = self.data.applymap(en.parse_data)
        graph_operations = {
                "line": lambda x_col : parsed_data.groupby(x_col).mean(),
                "bar" : lambda x_col : parsed_data.groupby(x_col).sum(),
                "count": lambda x_col, d=self.data[x_col].value_counts() : pd.DataFrame({x_col:d.index,"count":d.values}).groupby(x_col).sum()
                }
        try:
            if graph_type in graph_operations:
                data = graph_operations[graph_type](x_col)
            else:
                return r.Status(False, "\tGraph type \"%s\" invalid\n\tValid graph types: %s" 
                    % (graph_type, ", ".join(graph_operations.keys())))
        except pd.core.base.DataError as e:
            return r.Status(False, "\t" + str(e))
        x_data = list(data.index)
        for idx, col in enumerate(data.columns):
            y_data = list(data[col])
            if graph_type == "line":
                plt.plot(x_data, y_data, label=data[col].name)
            elif graph_type == "bar" or graph_type == "count":
                bar_count = len(data.columns)
                bar_width = 0.7 / bar_count
                index = np.arange(len(x_data))
                plt.bar(index + idx * bar_width, y_data, bar_width, label=data[col].name)
                x_ticks = index + (bar_count * bar_width - bar_width) / 2
                plt.xticks(x_ticks, x_data)
        if type(x_data[0]) == date:
            plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()
        return r.Status(True)
