# IoT-Aware Script Compiler for Home Automation

This project is a DSL-based script compiler for home automation simulation. It supports a basic rule-based language and compiles it into executable Python code for simulating smart home behaviors.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Write rules in `sample.dsl`.

3. Run:
   ```bash
   python main.py
   ```

## Example DSL

```
TURN ON light IF motion_detected
TURN OFF fan IF temperature_low
```
