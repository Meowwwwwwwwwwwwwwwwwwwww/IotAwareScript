def compile_rule(rule):
    """
    Compile the given rule (in the form of a DSL command) into executable Python code.
    """
    print(f"Compiling rule: {rule}")
    
    # Sample rule compilation (just as an example)
    if "turn on" in rule.lower() and "light" in rule.lower():
        return "TURN ON light"
    elif "turn off" in rule.lower() and "light" in rule.lower():
        return "TURN OFF light"
    else:
        return "Unrecognized rule"

