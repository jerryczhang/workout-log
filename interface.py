from item import LoggedItem
import os

class Interface:

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

    def get_command(self):
        """Get a command from the user."""
        prompt = "Enter command (" + ", ".join(self.commands) + "): "
        command = input(prompt).split()
        while command[0] not in self.commands:
            print("\tInvalid input entered: " + command[0])
            command = input(prompt).split()
        return command

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

    def view(self, parameters):
        """View the log, with parameters given by user."""
        usage = "\tUsage: view <item_name> [column] [filter_operation] [filter_value]"
        if len(parameters) == 0:
            print(usage)
        else:
            item = parameters[0]
            if item not in self.logs:
                self.logs[item] = self.create_item(item)
            if len(parameters) == 4:
                col = parameters[1]
                filter_op = parameters[2]
                value = parameters[3]
                self.logs[item].get_entries(col, filter_op, value)
            elif len(parameters) == 1:
                self.logs[item].get_entries()
            else:
                print(usage)

    def create_item(self, name):
        """Create a new logged item."""
        columns = input("Enter columns for new item: ").split()
        new_item = LoggedItem(name, ["date"] + columns)
        return new_item

    def log(self, parameters):
        """Add new entries to an item."""
        usage = "\tUsage: log <item_name>"
        if len(parameters) != 1:
            print(usage)
        else:
            item = parameters[0]
            self.logs[item].add_entry()

    def list(self):
        """List logged items."""
        print("\tYour items: " + ", ".join(list(self.logs.keys())))

    def edit(self, parameters):
        """Edit a previous entry."""
        item = parameters[0]
        index = parameters[1]
        self.logs[item].edit_entry(index)
        

