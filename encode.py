from datetime import date
import return_code as r

def parse_data(string):
    """Convert a string from the table to the correct type."""
    if string.isnumeric():
        return int(string)
    elif '/' in string:
        return parse_date(string)
    elif ':' in string:
        return parse_slice(string)
    else:
        return string

def parse_date(string):
    """Convert a string input into a date object."""
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    date_in = string.split('/')
    try:
        if len(date_in) == 2:
            if date_in[1]:
                day = int(date_in[1])    
                month = int(date_in[0])
            elif date_in[0]:
                day = int(date_in[0])
        elif len(date_in) == 3:
            month, day, year = list(map(int, date_in))
        return date(year, month, day)
    except ValueError:
        return r.Status(False, "\tInvalid date entered: " + string)

def parse_slice(string):
    """Convert a string inpout into a list of indices."""
    indices = []
    slice_in = string.split(':')
    if len(slice_in) != 2 and len(slice_in) != 3:
        return r.Status(False, "\tIndex must be in the form start:end or start:end:step")
    for num in slice_in:
        if not num.isnumeric():
            return r.Status(False, "\tInvalid index \"" + num + "\", index must be an integer")
        indices.append(int(num))
    if len(indices) == 2:
        indices.append(1)
    if indices[1] < indices[0]:
        return r.Status(False, "\tIndex must have a greater ending position than starting position")
    indices[0] -= 1
    return indices

def encode_input(user_in):
    """Convert user input to a string."""
    user_in = parse_data(user_in)
    if type(user_in) == date:
        return user_in.strftime("%m/%d/%Y" )
    elif type(user_in) == r.Status:
        return user_in
    else:
        return str(user_in)

