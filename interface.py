from item import LoggedItem
from item import LoggedItem

class Interface:

    def load_logs(self):
        """Load in previously entered logs."""
        f = open("logs/items.txt", 'r')
        items = f.read().split()
        self.logs = {}
        for item in items:
            self.logs[item] = LoggedItem(item)

    def get_command(self):
        """Get a command from the user."""
        prompt = "Enter command [view, log, quit]: "
        command = input(prompt).split()
        while command[0] not in ["view", "log", "quit"]:
            print("Invalid input entered: " + command[0])
            command = input(prompt).split()
        return command

    def view(self, parameters):
        """View the log, with parameters given by user."""
        item = parameters[0]
        self.logs[item].get_entries()

    def log(self, parameters):
        """Add new entries to an item."""
        item = parameters[0]
        self.logs[item].add_entry()

    def process_command(self, command):
        """Perform actions based on the command."""
        if command[0] == "view":
            self.view(command[1:])
        if command[0] == "log":
            self.log(command[1:])

    def start(self):
        """Start the interface, loops until user enters 'quit'."""
        self.load_logs()
        print("Your items: " + ", ".join(list(self.logs.keys())))
        while True:
            command = self.get_command()
            if command[0] == "quit":
                break
            else:
                self.process_command(command)
