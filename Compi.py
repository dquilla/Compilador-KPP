import ply.lex as lex
import ply.yacc as yacc

#Lista de tokens posibles
tokens = ['TIPO_INT', 'TIPO_FLOAT', 'TIPO_STRING', 'TIPO_CHAR', 'INT', 'STRING', 'CHAR', 'FLOAT',
            'MAIN', 'DELIMITADOR', 'SEPARADOR', 'OPERADOR', 'OPERADOR_LOGICO', 'IDENTIFICADOR', 'OPERADOR_ASIGNACION', ##Checar que hacer con MAIN D:
            'IF', 'ELSE', 'FOR', 'WHILE', 'PRINT', 'INPUT']

#Tokens para palabras reservadas
t_ignore = ' \t\n'
#Tipos
t_TIPO_INT = r'int'
t_TIPO_FLOAT = r'float'
t_TIPO_STRING = r'string'
t_TIPO_CHAR = r'char'

#Constantes
t_INT = r'[0-9]+'
t_FLOAT = r'[0-9]*\.[0-9]+'
t_CHAR = r'\'[a-zA-Z]\'' ##Checar prioridades de regex
t_STRING = r'"[A-Za-z0-9]+"'

#Estatutos
t_PRINT = r'print'
t_INPUT = r'input'
t_IF = r'if'
t_ELSE = r'else'
t_FOR = r'for'
t_WHILE = r'while'

#Identificador del programa
t_MAIN = r'main' ##Pendiente

#Operadores
t_OPERADOR = r'\+|\-|\*|/'
t_OPERADOR_LOGICO = r'<>|<|>|==|&|\|'
t_DELIMITADOR = r'\;|\{|\}|\(|\)|\[|\]'
t_SEPARADOR = r'\,'

#Para segmentos de codigo hay que hacer una funcion
def t_error(t):
    print 'Error de sintaxis en entrada: Caracter Invalido ' + t.value[0]
    errores = True
    return t

#Definicion de las reglas de la gramatica

#Programa
def p_programa(p):
    '''programa : programaX MAIN DELIMITADOR bloqueCodigo DELIMITADOR'''
    print "Programa Correcto!"

def p_programaX(p):
    '''programaX : var programa
                 | funcion programa
                 | ''' #Epsilon

#Bloque Codigo
def p_bloqueCodigo(p):
    '''bloqueCodigo : bloqueCodigoX bloqueCodigoY'''
    
def p_bloqueCodigoX(p):
    '''bloqueCodigoX : estatuto
                     | var'''

def p_bloqueCodigoY(p):
    '''bloqueCodigoY : bloqueCodigo
                     | ''' #Epsilon

#Estatuto
def p_estatuto(p):
    '''estatuto : escritura
                | input
                | if
                | asignacion
                | for
                | while
                | idFuncion'''

#Funcion
def p_funcion(p):
    '''funcion : tipo idFuncion DELIMITADOR bloqueCodigo DELIMITADOR'''
    
def p_idFuncion(p):
    '''idFuncion : IDENTIFICADOR DELIMITADOR idFuncionX'''
    
def p_idFuncionX(p):
    '''idFuncionX : tipo IDENTIFICADOR idFuncionY DELIMITADOR
                  | DELIMITADOR''' #Epsilon
    
def p_idFuncionY(p):
    '''idFuncionY : SEPARADOR idFuncionX'''
    
#Variables
def p_var(p):
    '''var : tipo varX'''
    
def p_varX(p):
    '''varX : IDENTIFICADOR varY'''
    
def p_varY(p):
    '''varY : DELIMITADOR exp DELIMITADOR varZ DELIMITADOR
            | varZ DELIMITADOR''' #Epsilon
       
def p_varZ(p):
    '''varZ : SEPARADOR varX
            | ''' #Epsilon
            
#Operacion
def p_operacion(p):
    '''operacion : expresion operacionX'''
    
def p_operacionX(p):
    '''operacionX : OPERADOR_LOGICO operacion
                  | ''' #Epsilon
                  
#Expresion
def p_expresion(p):
    '''expresion : exp expresionX'''
    
def p_expresionX(p):
    '''expresionX : OPERADOR_LOGICO exp
                  | ''' #Epsilon

#Factor
def p_factor(p):
    '''factor : DELIMITADOR expresion DELIMITADOR
              | constante
              | OPERADOR constante'''

#Escritura
def p_escritura(p):
    '''escritura : PRINT DELIMITADOR operacion DELIMITADOR DELIMITADOR'''

#Asignacion
def p_asignacion(p):
    '''asignacion : IDENTIFICADOR asignacionX OPERADOR_ASIGNACION asignacionY DELIMITADOR'''
    
def p_asignacionX(p):
    '''asignacionX : DELIMITADOR exp DELIMITADOR
                   | ''' #Epsilon

def p_asignacionY(p):
    '''asignacionY : idFuncion
                   | operacion'''

#Exp
def p_exp(p):
    '''exp : termino expX'''
    
def p_expX(p):
    '''expX : OPERADOR exp
            | ''' #Epsilon
            
#Termino
def p_termino(p):
    '''termino : factor terminoX'''
    
def p_terminoX(p):
    '''terminoX : OPERADOR termino
                | ''' #Epsilon
                
#For
def p_for(p):
    '''for : FOR DELIMITADOR asignacion DELIMITADOR operacion DELIMITADOR forX DELIMITADOR DELIMITADOR bloqueCodigo DELIMITADOR'''

def p_forX(p):
    '''forX : exp
            | asignacion'''

#While
def p_while(p):
    '''while : WHILE DELIMITADOR operacion DELIMITADOR DELIMITADOR bloqueCodigo DELIMITADOR'''
    
#If
def p_if(p):
    '''if : IF DELIMITADOR operacion DELIMITADOR DELIMITADOR bloqueCodigo DELIMITADOR ifX'''
    
def p_ifX(p):
    '''ifX : ELSE DELIMITADOR bloqueCodigo DELIMITADOR
           | ''' #Epsilon

#Input
def p_input(p):
    '''input : IDENTIFICADOR OPERADOR_ASIGNACION INPUT DELIMITADOR tipo DELIMITADOR'''

#Constante
def p_constante(p):
    '''constante : STRING
                 | CHAR
                 | INT
                 | FLOAT'''
                 
#Tipo
def p_tipo(p):
    '''tipo : TIPO_STRING
            | TIPO_CHAR
            | TIPO_INT
            | TIPO_FLOAT'''


#Funcion de error para el parser
def p_error(p):
    print "Error al parsear el programa. Mensaje: "
    print p
    return p

#Inicializacion del Lexer
lex.lex()

###Entrada
##lex.input("var int float program if else program 14 { 3.141592654 } , \"hola\" <>")
##
###Uso de los tokens (imprimiendo por lo pronto)
##while True:
##    tok = lex.token()
##    if not tok:
##        break
##    else:
##        print tok.type

#Inicializacion del Parser
yacc.yacc()

nombreArchivo = raw_input("Nombre del Archivo: ")

archivo = open(nombreArchivo, 'r')

datos = archivo.read()

yacc.parse(datos)
