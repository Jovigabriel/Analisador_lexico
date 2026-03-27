import ply.lex as lex

# Palavras reservadas
reserved = {
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'case': 'CASE',
    'esac': 'ESAC',
    'let': 'LET',
    'in': 'IN',
    'new': 'NEW',
    'isvoid': 'ISVOID',
    'not': 'NOT'
}

tokens = [

    # Literais
    'INT_CONST', 'STR_CONST', 'BOOL_CONST',

    # Identificadores
    'OBJECTID', 'TYPEID',

    # Operadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LT', 'LE', 'EQ',
    'ASSIGN', 'DARROW',

    # Símbolos
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'COLON', 'SEMICOLON',
    'COMMA', 'DOT',

    # Outros
    'AT', 'TILDE',

] + list(reserved.values())

# Operadores
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_ASSIGN = r'<-'
t_LE = r'<='
t_LT = r'<'
t_DARROW = r'=>'
t_EQ = r'='

# Símbolos
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'

t_AT = r'@'
t_TILDE = r'~'

# Ignorar espaços
t_ignore = ' \t'

# =========================
# IMPORTANTE: ORDEM IMPORTA
# =========================

# Strings (ANTES de OBJECTID)
def t_STR_CONST(t):
    r'"([^\\\n]|(\\.))*?"'
    return t

# Booleanos (ANTES de OBJECTID)
def t_BOOL_CONST(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

# TYPEID
def t_TYPEID(t):
    r'[A-Z][a-zA-Z0-9_]*'
    return t

# OBJECTID + reserved
def t_OBJECTID(t):
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'OBJECTID')
    return t

# Inteiros
def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Comentário de linha
def t_COMMENT(t):
    r'--.*'
    pass

# Comentário de bloco
def t_COMMENT_MULTI(t):
    r'\(\*[\s\S]*?\*\)'
    t.lexer.lineno += t.value.count('\n')
    pass

# Controle de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lista de erros
erros_lexicos = []

# Tratamento de erro
def t_error(t):
    erros_lexicos.append(
        f"Linha {t.lineno}: caractere inválido '{t.value[0]}'"
    )
    t.lexer.skip(1)

# Criar lexer
lexer = lex.lex()

# =========================
# TESTE
# =========================

codigo = r"""
class Main inherits IO {
    main(): Object {
        let hello: String <- "Hello, ",
            name: String <- "",
            ending: String <- "!\n"
        in {
            out_string("Please enter your name:\n");
            name <- in_string();
            out_string(hello.concat(name.concat(ending)));
        }
    };
};
"""

lexer.input(codigo)

for tok in lexer:
    print(tok)

# Mostrar erros, se houver
if erros_lexicos:
    print("\nErros léxicos:")
    for erro in erros_lexicos:
        print(erro)