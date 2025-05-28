import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'TURN', 'ON', 'OFF', 'IF',
    'DEVICE', 'CONDITION'
)

t_TURN = r'TURN'
t_ON = r'ON'
t_OFF = r'OFF'
t_IF = r'IF'
t_DEVICE = r'(light|fan|heater|ac|tv)'
t_CONDITION = r'(motion_detected|temperature_low|temperature_high|no_motion)'

t_ignore = ' \t\n'

def t_error(t):
    raise Exception(f"Illegal character '{t.value[0]}'")

lexer = lex.lex()

def p_rule(p):
    'rule : TURN action DEVICE IF CONDITION'
    p[0] = ('RULE', p[2], p[3], p[5])

def p_action(p):
    '''action : ON
              | OFF'''
    p[0] = p[1]

def p_error(p):
    raise Exception("Syntax error in input")

parser = yacc.yacc()

def parse_dsl(dsl_code):
    return [parser.parse(line) for line in dsl_code.strip().split('\n') if line]
