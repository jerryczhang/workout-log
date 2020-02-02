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
                "delete": self.delete,
        }                 
        self.load_logs()
        while True:
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
        usage = "\tUsage: view <item_name> [column] {filter_column} {filter_operation} {filter_value}"
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
        usage = "\tUsage: log <item_name>"
        if not self.check_num_params(parameters, [1], usage):
            return r.Status(False)
        else:
            item = parameters[0]
            if not self.check_item(item):
                return r.Status(False)
            item = self.logs[item]
            columns = item.get_columns()
            prompt = "Enter data for columns (" + ", ".join(columns) + ") (Enter 'quit' when done): "
            user_in = input(prompt)
            while user_in != "quit":
                data = list(map(en.encode_input, user_in.split()))
                if len(data) != len(columns):
                    print("\tColumn count mismatch: %d columns entered, needs %d." % (len(data), len(columns)))
                else:
                    item.append(data)
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
        item = self.logs[parameters[0]]
        index = parameters[1]
        columns = item.get_columns()
        prompt = "\nEnter data for columns (" + ", ".join(columns) + "): "
        user_in = input(prompt).split()
        user_in = list(map(en.encode_input, user_in))
        for entry in user_in:
            if type(entry) == r.Status:
                return entry
        return item.edit_entry(index, user_in)

    def delete(self, parameters):
        """Delete an entry from the table."""
        usage = "\tUsage: delete <item_name> <entry_number>"
        if not self.check_num_params(parameters, [2], usage):
            return r.Status(False)
        item = self.logs[parameters[0]]
        index = parameters[1]
        return item.delete_entry(int(index))
