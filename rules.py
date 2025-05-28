def map_command_to_dsl(command):
    """
    Map the recognized speech command to a DSL rule.
    """
    if "turn on" in command.lower() and "light" in command.lower():
        return "TURN ON light"
    elif "turn off" in command.lower() and "light" in command.lower():
        return "TURN OFF light"
    elif "set temperature" in command.lower():
        return "SET TEMPERATURE"
    else:
        return "Unrecognized rule"
