from log import LoggedItem

def load_logs():
    """Load in previously entered logs."""
    f = open("logs/items.txt", 'r')
    items = f.read().split()
    logs = {}
    for item in items:
        logs[item] = LoggedItem(item)
    return logs

def main():
    logs = load_logs()
    print("Your logs: " + ", ".join(list(logs.keys())))

if __name__ == "__main__":
    main()
