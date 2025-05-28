def simulate_execution(run_func, conditions):
    actions = run_func(conditions)
    for action, device in actions:
        print(f"{action} {device.upper()}")
