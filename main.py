from parser import parse_dsl
from compiler import compile_rules
from executor import simulate_execution

def main():
    with open('sample.dsl') as f:
        dsl_code = f.read()

    print("Parsing DSL...")
    parsed = parse_dsl(dsl_code)

    print("Compiling to Python...")
    py_code = compile_rules(parsed)

    namespace = {}
    exec(py_code, namespace)

    print("Simulating execution with conditions:")
    test_conditions = ['motion_detected', 'temperature_low']
    print("Conditions:", test_conditions)

    simulate_execution(namespace['run_rules'], test_conditions)

if __name__ == '__main__':
    main()
