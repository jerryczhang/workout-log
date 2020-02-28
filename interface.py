from item import LoggedItem
from datetime import date
import encode as en
import return_code as r
import os

class Interface:
    """Processes input and output for the user."""

    def start(self):
        """Start the interface, loops until user enters 'quit'."""
        self.commands = {
                "quit": None,
                "list": self.list,
                "view": self.view,
                "log":  self.log,
                "edit": self.edit,
                "expand": self.expand,
                "cut" : self.cut,
                "delete": self.delete,
                "rename": self.rename,
                "graph": self.graph,
        }                 
        while True:
            self.load_logs()
            command = self.get_command()
            if command[0] == "quit":
                break
            else:
                self.process_command(command)

    def load_logs(self):
        """Load in previously entered logs."""
        files = [f for f in os.listdir("logs/") if os.path.isfile(os.path.join("logs/", f))]
        self.logs = {}
        for item in files:
            name = item[:item.index('.')]
            self.logs[name] = LoggedItem(name)

    def process_command(self, command):
        """Perform actions based on the command."""
        keyword = command[0]
        parameters = command[1:]
        execute = self.commands[keyword](parameters)
        if execute.failed():
            execute.print_message()

    def get_command(self):
        """Get a command from the user."""
        prompt = "Enter command (" + ", ".join(self.commands.keys()) + "): "
        command = input(prompt).split()
        while command[0] not in self.commands:
            print("\tInvalid command entered: " + command[0])
            command = input(prompt).split()
        return command

    def check_item(self, item):
        """Check if the item is tracked, and add it."""
        if item not in self.logs:
            while True:
                user_in = input('\t' + item + " does not exist. Would you like to create it? (y/n): ")
                if user_in == 'y':
                    self.logs[item] = self.create_item(item)
                    return True
                elif user_in != 'n':
                    print("\tInvalid input entered: " + user_in)
                else:
                    return False
        return True

    def create_item(self, name):
        """Create a new logged item."""
        columns = input("Enter columns for new item: ").split()
        new_item = LoggedItem(name, columns)
        self.logs[name] = new_item
        return new_item

    def check_num_params(self, params, valid_nums, msg):
        """Checks if len of params is within bounds."""
        is_within = len(params) in valid_nums
        if is_within:
            return True
        else:
            print(msg)
            return False

    def view(self, parameters):
        """View the log, with parameters given by user."""
        usage = "\tUsage: view <item_name> [column(s)] {filter_column} {filter_operation} {filter_value}"
        if not self.check_num_params(parameters, [1,2,4,5], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        logged_item = self.logs[item]
        if len(parameters) == 5:
            col, filter_col, filter_op, filter_val = parameters[1:]
            return logged_item.get_entries(filter_col, filter_op, filter_val, col)
        elif len(parameters) == 4:
            filter_col, filter_op, filter_val = parameters[1:]
            return logged_item.get_entries(filter_col, filter_op, filter_val)
        elif len(parameters) == 2:
            col = parameters[1]
            return logged_item.get_entries(col=col)
        elif len(parameters) == 1:
            return logged_item.get_entries()

    def log(self, parameters):
        """Add new entries to an item."""
        usage = "\tUsage: log <item_name> [insert_index]"
        if not self.check_num_params(parameters, [1, 2], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        columns = item.get_columns()
        if len(parameters) == 2:
            index = parameters[1]
            if not index.isnumeric():
                return r.Status(False, "\tIndex must be an integer")
            prompt = "Enter data for columns (%s): " % ", ".join(columns)
            user_in = input(prompt)
            data = list(map(en.encode_input, user_in.split()))
            return item.insert(data, index)
        elif len(parameters) == 1:
            prompt = "Enter data for columns (%s) (Enter 'quit' when done): " % ", ".join(columns)
            user_in = input(prompt)
            while user_in != "quit":
                data = list(map(en.encode_input, user_in.split()))
                if len(data) != len(columns):
                    print("\tColumn count mismatch: %d columns entered, needs %d." % (len(data), len(columns)))
                else:
                    run = item.append(data)
                    if run.failed():
                        return run
                user_in = input(prompt)
            return r.Status(True)

    def list(self, parameters):
        """List logged items."""
        print("\tYour items: " + ", ".join(list(self.logs.keys())))
        return r.Status(True)

    def edit(self, parameters):
        """Edit a previous entry."""
        usage = "\tUsage: edit <item_name> <entry_number>"
        if not self.check_num_params(parameters, [2], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        index = parameters[1]
        if not index.isnumeric():
            return r.Status(False, "\tIndex must be an integer")
        columns = item.get_columns()
        prompt = "\nEnter data for columns (" + ", ".join(columns) + "): "
        user_in = input(prompt).split()
        user_in = list(map(en.encode_input, user_in))
        for entry in user_in:
            if type(entry) == r.Status:
                return entry
        return item.edit_entry(index, user_in)

    def expand(self, parameters):
        """Add a column to an item."""
        usage = "\tUsage: expand <item_name> <new_column_name>"
        if not self.check_num_params(parameters, [2], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        prompt = "\nEnter data for %d entries: " % (len(item.get_indices()))
        data = input(prompt).split()
        data = list(map(en.encode_input, data))
        return item.expand(parameters[1], data)

    def cut(self, parameters):
        """Delete a column from an item."""
        usage = "\tUsage: cut <item_name> <column_name>"
        if not self.check_num_params(parameters, [2], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        col = parameters[1]
        if self.get_conf_delete(col, "column"):
            return item.cut(col)
        else:
            return r.Status(False, "Input does not match column name, delete cancelled")

    def get_conf_delete(self, name, datatype):
        """Get user confirmation for deleting an item."""
        prompt = "\tDelete \"" + name + "\"? Re-type " + datatype + " name to confirm: " 
        user_in = input(prompt)
        if user_in == name:
            return True
        else:
            return False

    
    def delete(self, parameters):
        """Delete an entry from the table."""
        usage = "\tUsage: delete <item_name> [entry_number]"
        if not self.check_num_params(parameters, [1, 2], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        if len(parameters) == 2:
            index = parameters[1]
            return item.delete_entry(index)
        elif len(parameters) == 1:
            if self.get_conf_delete(item.name, "item"):
                self.logs.pop(item.name)
                return item.delete_item()
            else:
                return r.Status(False, "Input does not match item name, delete cancelled")

    def rename(self, parameters):
        """Rename an item."""
        usage = "\tUsage: rename <item_name> <new name>"
        if not self.check_num_params(parameters, [2], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        new_name = parameters[1]
        return item.rename(new_name)

    def graph(self, parameters):
        """Graph an item."""
        usage = "\tUsage: graph <item_name> <x_column> [graph_type]"
        if not self.check_num_params(parameters, [2, 3], usage):
            return r.Status(False)
        item = parameters[0]
        if not self.check_item(item):
            return r.Status(False)
        item = self.logs[item]
        x_col = parameters[1]
        if len(parameters) == 2:
            return item.graph(x_col, "line")
        else:
            graph_type = parameters[2]
            return item.graph(x_col, graph_type)
