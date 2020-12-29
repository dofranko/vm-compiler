# Load lex file
from zadlex import *
import ply.yacc as yacc

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'DIV', 'MUL'),
)

# -----------------------------------
# Yacc rules

#--------- PROGRAM


def p_declare_begin_end(p):
    '''program: DECLARE declarations BEGIN commands END'''
    pass


def p_begin_end(p):
    '''program: BEGIN commands END'''
    pass

#--------- DECLARATIONS


def p_declarations_pididentifier(p):
    '''declarations: declarations COMMA pidentifier'''
    pass


def p_declarations_pididentifier_array(p):
    '''declarations: declarations COMMA pidentifier LBR NUM COLON NUM RBR'''
    pass


def p_declare_pididentifier(p):
    '''declarations: pidentifier'''
    pass


def p_declare_array(p):
    '''declarations: pidentifier'''
    pass

#--------- COMMANDS


def p_commands_commands_command(p):
    '''commands: commands command'''
    pass


def p_commands_command(p):
    '''commands: command'''
    pass

#--------- COMMAND


def p_command_identifier_expression(p):
    '''command: identifier ASSIGN expression SEMICOLON'''
    pass


def p_command_identifier_expression(p):
    '''command: identifier ASSIGN expression SEMICOLON'''
    pass


def p_command_if_then_else(p):
    '''command: IF condition THEN commands ELSE commands ENDIF'''
    pass


def p_command_if_then(p):
    '''command: IF condition THEN commands ENDIF'''
    pass


def p_command_while_do(p):
    '''command: WHILE condition DO commands ENDWHILE'''
    pass


def p_command_repeat_until(p):
    '''command: REPEAT commands UNTIL condition SEMICOLON'''
    pass


def p_command_for_from_to_do(p):
    '''command: FOR pidentifier FROM value TO value DO commands ENDFOR'''
    pass


def p_command_for_from_downto_do(p):
    '''command: FOR pidentifier FROM value DOWNTO value DO commands ENDFOR'''
    pass


def p_command_read(p):
    '''command: READ identifier SEMICOLON'''
    pass


def p_command_write(p):
    '''command: WRITE identifier SEMICOLON'''
    pass

#--------- EXPRESSION


def p_expression_value(p):
    '''expression: value'''
    pass


def p_expression_value_add(p):
    '''expression: value ADD value'''
    pass


def p_expression_value_sub(p):
    '''expression: value SUB value'''
    pass


def p_expression_value_MUL(p):
    '''expression: value MUL value'''
    pass


def p_expression_value_div(p):
    '''expression: value DIV value'''
    pass


def p_expression_value_mod(p):
    '''expression: value MOD value'''
    pass


def p_expression_value_add(p):
    '''expression: value ADD value'''
    pass

#--------- CONDITION


def p_condition_eq(p):
    '''condition: value EQ value'''
    pass


def p_condition_neq(p):
    '''condition: value NEQ value'''
    pass


def p_condition_lt(p):
    '''condition: value LT value'''
    pass


def p_condition_gt(p):
    '''condition: value GT value'''
    pass


def p_condition_le(p):
    '''condition: value LE value'''
    pass


def p_condition_ge(p):
    '''condition: value GE value'''
    pass

#--------- VALUE


def p_value_num(p):
    '''value: num'''
    pass


def p_value_identifier(p):
    '''value: identifier'''
    pass


#--------- IDENTIFIER
def p_identifier_pidentifier(p):
    '''identifier: pidentifier'''
    pass


def p_identifier_array_pidentifier_(p):
    '''identifier: pidentifier'''
    pass


def p_identifier_array_num(p):
    '''identifier: pidentifier'''
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

if __name__ == '__main__':
    # Starting lex and yacc
    from sys import argv

    lex.lex()
    yacc.yacc()
    data = ""
    with open(argv[2], "r") as file:
        data = file.read()

    yacc.parse(data)
