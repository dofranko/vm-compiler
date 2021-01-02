# Load lex file
import ply.yacc as yacc
from comp_lex import *
from variables import *
from commander import *


def add_variable(pid):
    global next_free_memory_location
    if pid not in variables.keys():
        var = Variable(pid)
        var.memory_location = next_free_memory_location
        next_free_memory_location += 1
        variables[var.pid] = var
    else:
        custom_error("Duplikat pid juz istnieje")


def add_variable_array(pid, start, end):
    global next_free_memory_location
    if pid not in variables.keys():
        var = VariableArray(pid, start, end)
        var.memory_location = next_free_memory_location
        next_free_memory_location += var.length
        variables[var.pid] = var
    else:
        custom_error("Duplikat pid juz istnieje")


def load_variable(pid):
    return variables[pid]


precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'DIV', 'MUL'),
)

# -----------------------------------
# Yacc rules

#--------- PROGRAM


def p_declare_begin_end(p):
    '''program : DECLARE declarations BEGIN commands END'''
    prog = Program(p[4])
    prog.execute_commands()
    pass


def p_begin_end(p):
    '''program : BEGIN commands END'''
    pass

#--------- DECLARATIONS


def p_declarations_pididentifier(p):
    '''declarations : declarations COMMA PIDENTIFIER'''
    add_variable(p[3])
    pass


def p_declarations_pididentifier_array(p):
    '''declarations : declarations COMMA PIDENTIFIER LBR NUM COLON NUM RBR'''
    pass


def p_declare_pididentifier(p):
    '''declarations : PIDENTIFIER'''
    add_variable(p[1])
    pass


def p_declare_array(p):
    '''declarations : PIDENTIFIER LBR NUM COLON NUM RBR '''
    add_variable_array(p[1], p[3], p[5])
    pass

#--------- COMMANDS


def p_commands_commands_command(p):
    '''commands : commands command'''
    p[0] = list(p[1]) if p[1] else []
    p[0].append(p[2])


def p_commands_command(p):
    '''commands : command'''
    p[0] = [p[1]]

#--------- COMMAND


def p_command_identifier_expression(p):
    '''command : identifier ASSIGN expression SEMICOLON'''
    p[0] = AssignCommand(p[1], p[3])
    pass


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    pass


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''
    pass


def p_command_while_do(p):
    '''command : WHILE condition DO commands ENDWHILE'''
    pass


def p_command_repeat_until(p):
    '''command : REPEAT commands UNTIL condition SEMICOLON'''
    pass


def p_command_for_from_to_do(p):
    '''command : FOR PIDENTIFIER FROM value TO value DO commands ENDFOR'''
    pass


def p_command_for_from_downto_do(p):
    '''command : FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR'''
    pass


def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    p[0] = ReadCommand(p[2])
    pass


def p_command_write(p):
    '''command : WRITE identifier SEMICOLON'''
    p[0] = WriteCommand(p[2])

#--------- EXPRESSION


def p_expression_value(p):
    '''expression : value'''
    p[0] = ValueExpression(p[1])
    pass


def p_expression_value_add(p):
    '''expression : value ADD value'''
    p[0] = AddExpression(p[1], p[3])
    pass


def p_expression_value_sub(p):
    '''expression : value SUB value'''
    p[0] = SubExpression(p[1], p[3])
    pass


def p_expression_value_mul(p):
    '''expression : value MUL value'''
    p[0] = MulExpression(p[1], p[3])
    pass


def p_expression_value_div(p):
    '''expression : value DIV value'''
    p[0] = DivExpression(p[1], p[3])
    pass


def p_expression_value_mod(p):
    '''expression : value MOD value'''
    p[0] = ModExpression(p[1], p[3])
    pass


#--------- CONDITION


def p_condition_eq(p):
    '''condition : value EQ value'''
    pass


def p_condition_neq(p):
    '''condition : value NEQ value'''
    pass


def p_condition_lt(p):
    '''condition : value LT value'''
    pass


def p_condition_gt(p):
    '''condition : value GT value'''
    pass


def p_condition_le(p):
    '''condition : value LE value'''
    pass


def p_condition_ge(p):
    '''condition : value GE value'''
    pass

#--------- VALUE


def p_value_num(p):
    '''value : NUM'''
    p[0] = p[1]  # p[1] should be as int
    pass


def p_value_identifier(p):
    '''value : identifier'''
    p[0] = p[1]  # p[1] should be as Variable
    pass


#--------- IDENTIFIER
def p_identifier_PIDENTIFIER(p):
    '''identifier : PIDENTIFIER'''
    p[0] = load_variable(p[1])


def p_identifier_array_PIDENTIFIER(p):
    '''identifier : PIDENTIFIER LBR PIDENTIFIER RBR'''
    pass


def p_identifier_array_num(p):
    '''identifier : PIDENTIFIER LBR NUM RBR'''
    pass

# ----------------------------------------


def custom_error(message: str):
    global flg_error
    print("ERROR: " + message)
    flg_error == 0


def p_error(p):
    if flg_error == 0:
        print("Error: syntax error")


# Globals
flg_error = 0       # Flaga erroru - czy był bład, czy nie
next_free_memory_location = 0
variables = {}

# Starting lex and yacc
if __name__ == '__main__':
    from sys import argv

    lex.lex()
    yacc.yacc()
    data = ""
    with open(argv[1], "r") as file:
        data = file.read()

    yacc.parse(data)
