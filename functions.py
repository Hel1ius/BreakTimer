def is_valid_number(user_input):
    try:
        int(user_input)
        return True
    except ValueError:
        return False
