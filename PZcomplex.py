# -----------------------------------------------------------------------------
# Calculates complex numbers expressions
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

def sign_spaced(x):
    if x < 0: return ' - '
    else: return ' + '

def complex2string(a, b):
    if int(a) == a: a = int(a)      # get rid of trailing .0
    if int(b) == b: b = int(b)      # get rid of trailing .0
    if b != 0:
        string =["i"]
        if abs(b) != 1:
            string.insert(0, str(abs(b)))
        if (a == 0) and (b < 0):
            string.insert(0, "-")
        elif a != 0:
            string = [str(a), sign_spaced(b)] + string
    else:
        string = str(a)
    return ''.join(string)

from math import *

tokens = ['IMAGINARY_NUMBER', 'REAL_NUMBER']

literals = ['+', '-', '*', '/', '(', ')']

# Tokens

# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_IMAGINARY_NUMBER(t):
    r'(\d+\.?\d*)?i'
    temp = [0, 0]
    if len(t.value) == 1:
        temp[1] = 1
    else:
        temp[1] = float(t.value[:-1])
    t.value = temp
    return t


def t_REAL_NUMBER(t):
    r'\d+\.?\d*'
    temp = [0, 0]
    temp[0] = float(t.value)
    t.value = temp
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lex.lex()



# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)


def p_expression(p):
    '''expression : complex'''
    p[0] = p[1]
    a = p[0][0]
    b = p[0][1]
    print("Wynikowa liczba zespolona a + bi: ", complex2string(a, b))
    magnitude = sqrt(a*a + b*b)
    print("Moduł tej liczby wynosi: ", round(magnitude, 2), sep='', end='')
    if magnitude != 0:
        kat_rad = asin(b/magnitude)
        if a < 0: kat_rad = pi - kat_rad
        elif b < 0: kat_rad = 2*pi + kat_rad
        kat_deg = round( kat_rad/(2*pi) * 360, 2)
        kat_rad_pi = round(kat_rad/pi, 2)
        print(", a kąt: ", kat_deg, " stopni, czyli ", kat_rad_pi, " pi radianów",
              sep='', end='')
    print("")
    print("")
        
def p_complex_binop(p):
    '''complex : complex '+' complex
               | complex '-' complex
               | complex '*' complex
               | complex '/' complex
                 '''
    p[0] = [0, 0]
    # p[1] == a + bi; p[3] == c + di 
    a = p[1][0]
    b = p[1][1]
    c = p[3][0]
    d = p[3][1]
    
    if p[2] == '+':
        p[0] = [a+c, b+d]
        
    elif p[2] == '-':
        p[0] = [a-c, b-d]
        
    elif p[2] == '*':
        p[0][0] = a*c - b*d # ac-bd
        p[0][1] = a*d + b*c # (ad+bc)i
        
    elif p[2] == '/':
        mianownik = c*c + d*d
        p[0][0] = (a*c + b*d) / mianownik # (ac+bd)/(c*c+d*d)
        p[0][1] = (b*c - a*d) / mianownik # (bc-ad)/(c*c+d*d)

 

def p_complex_uminus(p):
    "complex : '-' complex %prec UMINUS"
    a = p[2][0]
    b = p[2][1]
    p[0] = [-a, -b]


def p_complex_group(p):
    "complex : '(' complex ')'"
    p[0] = p[2]


def p_complex_imaginary(p):
    "complex : IMAGINARY_NUMBER"
    p[0] = [0, 0]
    p[0][1] = p[1][1]


def p_complex_real(p):
    "complex : REAL_NUMBER"
    p[0] = [0, 0]
    p[0][0] = p[1][0]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = raw_input('Wprowadz wyrażenie zespolone > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
