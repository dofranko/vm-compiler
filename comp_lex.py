import ply.lex as lex

# Globals

finished = False

# Stany
states = (
    ('comment', 'exclusive'),
)
# Tokens
tokens = (
    'NUM', 'PIDENTIFIER',

    'SUB', 'ADD',
    'MUL', 'DIV',
    'MOD',

    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'ASSIGN',
    'COLON', 'SEMICOLON', 'COMMA',

    'IF', 'THEN', 'ELSE', 'ENDIF',
    'WHILE', 'DO', 'ENDWHILE',
    'REPEAT', 'UNTIL',
    'FOR', 'FROM', 'TO', 'DOWNTO', 'ENDFOR',

    'READ', 'WRITE',
    'LBR', 'RBR',

    'DECLARE', 'BEGIN', 'END'
)

# Simple rules

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_EQ = r'='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_ASSIGN = r':='
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'
t_WHILE = r'WHILE'
t_DO = r'DO'
t_ENDWHILE = r'ENDWHILE'
t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'
t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_DOWNTO = r'DOWNTO'
t_ENDFOR = 'ENDFOR'
t_READ = r'READ'
t_WRITE = r'WRITE'
t_LBR = r'\('
t_RBR = r'\)'
t_DECLARE = r'DECLARE'
t_BEGIN = r'BEGIN'
t_END = 'END'
t_PIDENTIFIER = r'[_a-z]+'

t_ignore = ' \t'
t_comment_ignore = ''

# Complex rules


def t_begin_comment(t):
    r'\['
    t.lexer.begin('comment')


def t_comment_end(t):
    r'\]'
    t.lexer.begin('INITIAL')
    pass


def t_comment_any(t):
    r'.'
    pass


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rules
def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_comment_error(t):
    #print("Illegal character in comment '%s'" % t.value[0])
    t.lexer.skip(1)
