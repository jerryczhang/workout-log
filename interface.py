from item import LoggedItem
from datetime import date
import encode as e
import os

class Interface:
    """Processes input and output for the user."""

    def start(self):
        """Start the interface, loops until user enters 'quit'."""
        self.commands = ["list", "view", "log", "edit", "quit"]
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
        if command[0] == "view":
            self.view(command[1:])
        if command[0] == "log":
            self.log(command[1:])
        if command[0] == "list":
            self.list()
        if command[0] == "edit":
            self.edit(command[1:])

    def get_command(self):
        """Get a command from the user."""
        prompt = "Enter command (" + ", ".join(self.commands) + "): "
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
        new_item = LoggedItem(name, ["date"] + columns)
        return new_item

    def check_num_params(self, params, lower, upper, msg):
        """Checks if len of params is within bounds."""
        is_within = lower <= len(params) <= upper
        if is_within:
            return True
        else:
            print(msg)
            return False

    def view(self, parameters):
        """View the log, with parameters given by user."""
        usage = "\tUsage: view <item_name> [column] [filter_operation] [filter_value]"
        if not self.check_num_params(parameters, 1, 4, usage):
            return
        item = parameters[0]
        if not self.check_item(item):
            return
        if len(parameters) == 4:
            col = parameters[1]
            filter_op = parameters[2]
            value = parameters[3]
            self.logs[item].get_entries(col, filter_op, value)
        elif len(parameters) == 1:
            self.logs[item].get_entries()
        else:
            print(usage)

    def log(self, parameters):
        """Add new entries to an item."""
        usage = "\tUsage: log <item_name>"
        if not self.check_num_params(parameters, 1, 1, usage):
            return
        else:
            item = parameters[0]
            if not self.check_item(item):
                return
            item = self.logs[item]
            columns = item.get_columns()
            prompt = "Enter data for columns (" + ", ".join(columns) + ") (Enter 'quit' when done): "
            user_in = input(prompt)
            while user_in != "quit":
                data = list(map(e.encode_input, user_in.split()))
                if len(data) != len(columns):
                    print("\tColumn count mismatch: %d columns entered, needs %d." % (len(data), len(columns)))
                else:
                    item.append(data)
                user_in = input(prompt)

    def list(self):
        """List logged items."""
        print("\tYour items: " + ", ".join(list(self.logs.keys())))

    def edit(self, parameters):
        """Edit a previous entry."""
        usage = "\tUsage: edit <item_name> <entry_number>"
        if not self.check_num_params(parameters, 2, 2, usage):
            return
        item = self.logs[parameters[0]]
        index = parameters[1]
        columns = item.get_columns()
        prompt = "\nEnter data for columns (" + ", ".join(columns) + "): "
        user_in = input(prompt).split()
        user_in = list(map(e.encode_input, user_in))
        item.edit_entry(index, user_in)
        

