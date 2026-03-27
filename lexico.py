import ply.lex as lex

#Criando um dicionario que irá armazenar as palavras reservadas de cool e o valor será a versão maiuscula dessas palavras

reservadas = {
    'class' : 'CLASS',
    'if': 'IF',
    'else': 'ELSE',
    'fi' : 'FI',
    'case' : 'CASE',
    'loop' : 'LOOP',
    'pool' : 'POOL',
    'case' : 'CASE',
    'esac' : 'ESAC',
    'in': 'IN',
    'while' : 'WHILE',
    'new' : 'NEW',
    'of': 'OF',
    'not': 'NOT',
    'inherits': 'INHERITS',
    'isvoid': 'ISVOID',
    'let': 'LET',
    'then': 'THEN',
}

#Lista de Tokens com esse nome é necessaria, pois a biblioteca usa essa lista para realizar suas funções
tokens = [
    
    #TOKENS DAS PALAVRAS RESERVADAS
    'CLASS',
    'IF',
    'ELSE',
    'FI',
    'CASE',
    'LOOP',
    'POOL',
    'CASE',
    'ESAC',
    'IN',
    'WHILE',
    'NEW',
    'OF',
    'NOT',
    'INHERITS',
    'ISVOID',
    'LET',
    'THEN',

    #tokens para identificadores

    'TYPEID',
    'OBJECTID',
    'INT_CONST',
    'STR_CONST',
    'BOOL_CONST', #na linguagem cool true e false obrigatoriamente precisam começar com letra maiuscula, o restante pode ser minusculo ou maiuscula

    #Operadores
    'LE',
    'ASSIGN', #ATRIBUIÇÃO EM COOL <-
    'DARROW', #=>
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'COLON',
    'SEMI',
    'DOT',
    'COMMA',
    'LESSER',
    'EQUAL'
    'TILDE' #TIL ~ , EM COOL o til é usado para dizer que um número negativo, o sinal de menos serve somente para a operação de menos
    'AT' #ARROBA @, serve para chamar metodo do pai de um objeto
]


# Nessa etapa temos que adicionar nas variaveis que o PLY oferece os respectivos simbolos que irão representar os tokens acima

#Ordem de tamanho parece ser importante, os maiores precisam ficar antes dos menores, para evitar que um token seja criado antes do tempo

# O nome precisa sempre começar com t_ e o restante tem que ser escrito examtamente igual a como estar na lista dos tokens
t_DARROW = r'=>'
t_ASSIGN =  r'<-'
t_LE = r'<='
t_PLUS= r'\+' #A contrabarra serve para que fique claro que queremos a expressão literal e não o sentido que o regex impoe
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV    = r'/'
t_LESS   = r'<'
t_EQUAL  = r'='
t_TILDE  = r'~'
t_AT     = r'@'
t_LBRACE = r'\{'   
t_RBRACE = r'\}'  
t_LPAREN = r'\('   
t_RPAREN = r'\)'   
t_COLON  = r':'
t_SEMI   = r';'
t_DOT    = r'\.'   
t_COMMA  = r','

#Agora temos que criar funções para identificar tokens que não seguem o mesmo padrão dos anteriores

#LEMBRETE IMPORTATE cool é Case insensitive, então se eu escrever as palavras chaves maiusculas, minusculas ou misturado, tanto faz para ele, só não podemos fazer isso para true e false, pois suas primeiras letras precisam ser minusculas

def t_BOOL_CONST(t):
    r't[Rr][Uu][Ee]|f[Aa][lL][Ss][Ee]' #Regex que tenta ler a palavra true ou false, sendo que a primeira letra é sempre minuscula e as outras podem ser ou nao

    palavra = t.value.lower()
    if palavra == 'true':
        t.value = True
    else:
        t.value = False
    return t

def t_INT_CONST(t):
    r'\d+'

    t.value = int(t.value) #transformando a string númerica em int 
    return t

def t_TYPEID(t): #TYPE ID obrigatoriamente começa com letras maiusculas
    r'[A-Z][A-Za-z0-9_]*'

    #Verificando se as letras lidas formam alguma palavra reservada, se não formar, type vai ser TYPE_ID
    palavra = t.value.lower()
    t.type = reservadas.get(palavra, "TYPEID")
    return t


def t_OBJECTID(t): #OBJECT ID obrigatoriamente começa com letras MINUSCULAS
    r'[a-z][A-Za-z0-9_]*'

    #Verificando se as letras lidas formam alguma palavra reservada, se não formar, type vai ser TYPE_ID
    palavra = t.value.lower()
    t.type = reservadas.get(palavra, "OBJECTID")
    return t

