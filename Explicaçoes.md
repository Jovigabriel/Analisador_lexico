
# Documentação do Analisador Léxico (`lex.py`) para a Linguagem COOL

Este documento tem como objetivo explicar detalhadamente o funcionamento do código `lex.py`, o primeiro estágio do compilador para a linguagem COOL.

Decidimos usar a biblioteca nativa do Python **PLY**, ela recria o **LEX** (Léxico) e o **YACC** (Sintático), mas no momento só estamos utilizando o lex.

## 1. Definição de Estados (`states`)

O código começa com a definição de uma tupla chamada `states` (que obrigatoriamente tem que ter esse nome para o motor do PLY conseguir ler). Ela serve para guardar diferentes estados para os quais o nosso analisador léxico pode ter que transicionar durante a sua execução. A tupla armazena duas coisas para cada estado: o nome e o tipo de comportamento que esse estado vai apresentar.

O PLY oferece dois tipos de comportamentos diferentes:

* **Exclusive (Exclusivo):** Um modo de isolamento total. Nele, o Lexer fica completamente cego para todas as regras padrão e ignora tudo que não começa com a sintaxe `t_NomeDoEstado_`. Isso permite a reestruturação de como lemos o texto, já que precisamos ter comportamentos completamente diferentes (como ignorar comandos e variáveis) dentro de comentários ou strings.

* **Inclusive (Inclusivo):** É o oposto do exclusivo. Ele permite que o Lexer continue vendo e usando as regras do estado inicial, mas possibilita que você adicione regras novas criadas especialmente para esse estado temporário.

**OBS:** O estado padrão do PLY, chamado de `INITIAL`, não utiliza nenhum desses dois róulos, pois ele é justamente a base de referência para os outros.

## 2. Palavras Reservadas e Tokens

Após essa tupla, temos um dicionário enorme que contém as **palavras reservadas** em COOL, sendo que a chave é a versão delas em minúsculo e o valor é a versão em maiúsculo. O dicionário é usado aqui para evitar ter que criar milhares de métodos só para identificar essas palavras reservadas. Vamos explicar como ele é usado mais abaixo.

Seguindo a ordem do código, temos uma lista declarada como `tokens`. O nome desta lista precisa ser obrigatoriamente `tokens` para que o PLY consiga identificá-la. Ela funciona como o inventário oficial do nosso analisador e contém todos os tokens válidos da linguagem COOL, incluindo as palavras reservadas que definimos no dicionário. Por convenção, todos os nomes de tokens são escritos em letras **MAIÚSCULAS** para que na próxima fase do compilador, possamos diferenciá-los como símbolos "Terminais" no Analisador Sintático.

## 3. Criação de Regras

Agora vamos realmente começar a criar as regras do nosso analisador léxico. O PLY nos fornece duas formas de definir essas regras:

1. **Variáveis:** Usando variáveis para regras simples, como símbolos matemáticos, parênteses, colchetes e outros.

2. **Métodos (Funções):** Essa forma é direcionada para tokens mais complexos que precisam de um tratamento e análise prévia. Por exemplo, sabemos que um número deve ser do tipo `int`, mas como estamos lendo um arquivo de texto, ele acaba sendo capturado como uma String, então precisamos transformá-lo dentro do método.

Em ambos os casos, nós temos um padrão obrigatório de nomenclatura, que é o prefixo `t_NomeDoToken`. Além disso, em ambas as formas utilizamos **Expressões Regulares** para ensinar ao PLY o que ele deve procurar. A grande diferença é que, nas variáveis, o REGEX é atribuído diretamente (ex: `t_PLUS = r'\+'`), enquanto nos métodos, o REGEX fica escrito na primeira linha dentro da função, como uma string de documentação.

## 4. Regras de Nomenclatura em COOL

Em COOL, temos algumas regras bem definidas em relação à forma como algumas coisas são escritas. São elas:

* **Classes e Tipos (TYPEID):** Devem obrigatoriamente começar com letras Maiúsculas.

* **Variáveis e Objetos (OBJECTID):** Obrigatoriamente precisam começar com letras minúsculas.

* **Palavras Reservadas (Case-insensitive):** A linguagem COOL é case-insensitive, ou seja, tanto faz se escrevermos as palavras reservadas completamente em maiúsculas, minúsculas ou tudo misturado, o compilador vai entender.

* **Exceção (Booleanos):** As constantes booleanas (`true` e `false`) possuem uma restrição: a primeira letra obrigatoriamente precisa ser minúscula (o restante pode ser misturado).

## 5. O Parâmetro `t` 

Antes de explicar as funções, precisamos entender o que é esse parâmetro `t` que todas elas recebem. Ele é uma instância de um objeto interno do PLY chamado **LexToken**. É como uma *struct* (estrutura de dados) que o PLY gera dinamicamente.

Toda vez que uma Expressão Regular é reconhecida no código-fonte, o PLY não pode simplesmente devolver o texto solto, pois ele perderia o contexto espacial de onde essa palavra estava. Portanto, ele encapsula esse texto dentro do objeto `LexToken`, anexando a ele todos os metadados (como linha, posição e tipo) necessários para as próximas fases da compilação.

O PLY é responsável por gerenciar automaticamente a leitura do arquivo. Ele possui um tipo de ponteiro interno que armazena onde paramos na leitura, evitando que tenhamos que nos preocupar com isso. Quando ele acha um pedaço de texto válido, ele preenche o objeto `t` com os seguintes atributos:

* **`t.value`**: Contém o texto bruto que a regex acabou de capturar (ex: a string `"42"`). É neste atributo que fazemos conversões (como `t.value = int(t.value)`) para transformar o texto em `int` para o compilador.

* **`t.type`**: É o nome do token, a classificação que será enviada ao Analisador Sintático. O PLY preenche isso automaticamente com o nome da função (ex: `"INT_CONST"`). Nos identificadores, alteramos esse atributo manualmente quando encontramos uma palavra reservada no dicionário.

* **`t.lineno` e `t.lexpos`**: O PLY guarda a linha exata e a posição absoluta do caractere onde aquele token foi encontrado. Isso é ótimo para gerar mensagens de erro precisas (ex: "Erro de sintaxe na linha 15").

* **`t.lexer`**: Dá acesso direto ao motor do lexer que está rodando. Usamos isso para alterar estados (`t.lexer.begin`), pular caracteres em caso de erro (`t.lexer.skip(1)`) ou criar variáveis globais (como `t.lexer.comment_level`).

Uma observação importante é o destino do token: quando usamos `return t` o PLY entende que o token é válido e deve seguir adiante. Já quando usamos `pass` (ou não retornamos nada), o PLY entende que devemos descartar silenciosamente o que foi lido (útil para comentários e espaços em branco).

## 6. As Regras Complexas

### Números e Identificadores

* **`t_INT_CONST`**: É bem simples: utiliza uma regra de regex para receber qualquer quantidade de números e depois os transforma em `int` antes de retornar o objeto `t`.

* **`t_TYPEID`**: É a primeira onde iremos usar o dicionário que criamos. Como foi dito antes, COOL aceita palavras tanto em maiúsculas como minúsculas. A regex do `TYPEID` garante a primeira letra maiúscula, mas o restante da palavra formada pode acabar sendo uma das nossas palavras reservadas (ex: `Class`). Então pegamos essa palavra, convertemos para totalmente minúscula e conferimos se ela existe no dicionário. Se existir, o seu tipo será o valor da palavra reservada armazenada no dicionário; se não for será `TYPEID`.

* **`t_OBJECTID`**: Segue uma lógica bem parecida com o `TYPEID` (usa a mesma sacada dos dicionários), mas ele também precisa tratar a questão das constantes booleanas, já que `OBJECTID`s também começam com letras minúsculas. Para fazer isso, verificamos primeiro se a palavra que está sendo formada é exatamente `true` ou `false`. Se for, forçamos o seu tipo a ser `BOOL_CONST`. Se não for, seguimos para a busca no dicionário de reservadas.

### Controle e Comentários Simples

* **`t_newline`**: Serve somente para capturarmos as quebras de linha (`\n`) e somarmos essa quantidade na variável do PLY responsável por armazenar em qual linha o código está. Por servir apenas para esse controle interno de contagem, ela não retorna nenhum token para o sistema.

* **`t_comment_line`**: Lida com os comentários de linha única do tipo `--`. O nosso analisador ignora tudo o que for escrito após esses traços até encontrar uma quebra de linha. Assim como na função anterior, o conteúdo é descartado e não gera tokens.

* **`t_error`**: Serve para reportar caracteres inválidos na linguagem COOL (como o símbolo `$` ou `?`). Como o analisador léxico não deve interromper o programa abruptamente ao encontrar algo estranho, ele apenas informa ao usuário em qual linha o erro ocorreu e qual foi o caractere detectado. Após esse alerta, o analisador "pula" o erro e continuar lendo o restante do arquivo normalmente.

## 7. Tratamento de Strings (Estado `string`)

Para tratar as strings em COOL, saímos do estado `INITIAL` e entramos em um estado exclusivo. Isso é necessário porque, dentro de uma string, as regras normais do compilador (como identificar números ou palavras-chave) devem ser ignoradas.

Tudo começa com a função **`t_start_string`**. Ao encontrar uma aspas dupla (`"`) sendo aberta, ela executa duas tarefas:

1. Cria um buffer (`string_buf`) para armazenar os caracteres da string que será formada.

2. Muda o estado do analisador para `string` através do comando `t.lexer.begin('string')`.

No modo de string, utilizamos o método **`t_string_chars`**. Ele possui uma lógica dupla:

* **Texto Comum:** Recebe qualquer sequência de caracteres que não seja o fechamento de aspas, uma barra invertida ou uma quebra de linha.

* **Comandos de Escape:** Identifica o uso da contrabarra (`\`). Para processar isso, utilizamos uma tabela de escapes (dicionário) que armazena todas as sequências válidas em COOL (como `\n`, `\t`, `\b`). O caractere especial só é adicionado ao buffer se ele existir nessa tabela, caso contrário, a barra é ignorada e apenas o caractere seguinte é guardado.

A função **`t_string_fechar`** é chamada ao encontrar as aspas de fechamento. Ela realiza o encerramento do processo:

1. Atribui todo o conteúdo acumulado no buffer ao valor do token (`t.value`).

2. Define o tipo do token como `STR_CONST`.

3. Retorna o analisador ao estado `INITIAL` e devolve o objeto `t` pronto.

A função **`t_string_newline`** serve para identificar uma situação de erro comum: quando o USUARIO esquece de fechar as aspas e aperta "Enter". Como em COOL as strings não podem conter quebras de linha literais sem escape, o LEXER avisa o usuário sobre o erro, atualiza o contador de linhas e força o retorno ao estado inicial para não ATRAPALHAR a leitura do restante do arquivo.

## 8. Comentários de Bloco (Estado `comment`)

Entramos em outra parte importante, os comentários de bloco `(* ... *)`. Eles seguem um funcionamento parecido com o das Strings, pois precisamos mudar de estado e criar regras próprias. Uma característica marcante da linguagem COOL é permitir comentários aninhados (um comentário dentro de outro), o que exige uma lógica de contagem.

* **`t_start_comment`**: Possui uma lógica similar à abertura de strings. Quando o Lexer encontra o símbolo `(*` no estado inicial, ele entra nesta função, cria um contador de nível para rastrear quantos blocos foram abertos e muda o estado para `comment`.

* **`t_comment_abrir`**: É chamada se encontrarmos outro `(*` enquanto já estamos no estado de comentário. Sua única função é incrementar o nosso contador.

* **`t_comment_fechar`**: É chamada sempre que encontramos o símbolo `*)`. Ela diminui o contador e, caso esse contador chegue a zero (indicando que todos os blocos abertos foram fechados), a função retorna o estado para `INITIAL`.

* **`t_comment_chars`**: Serve para "engolir" e ignorar qualquer caractere que não seja parênteses, asterisco ou quebra de linha. Como não usamos o comando return, todo esse texto é descartado silenciosamente.

## 9. Execução do Analisador

O restante do código serve para fazer o nosso analisador léxico realmente entrar em ação. Por motivo de teste temos um código padrão que é usada sempre quando chamamos o lexer sem passar nada por parâmetro, caso passarmos um arquivo temos um pequeno tratamento para saber se ele é válido ou não.

Comandos principais:

* **`lexer = lex.lex()`**: Este comando aciona o motor de introspecção do PLY. Ele vasculha o arquivo atual em busca de variáveis e funções que comecem com `t_`, valida as expressões regulares e monta a máquina de estados interna. Ele pega o valor de todas as variáveis `t_` e extrai as docstrings de dentro de todas as funções `t_`. Ele junta todas essas expressões regulares em uma Máquina de Estados otimizada. Ele consegue capturar qualquer padrão do código de uma vez só com isso.

* **`lexer.input(...)`**: Aqui, carregamos o conteúdo do arquivo COOL para dentro do motor. A partir deste momento, o PLY assume o controle do ponteiro de leitura do arquivo.

* **`tok = lexer.token()`**: Este é o comando de iteração. Cada vez que ele é chamado, o Lexer busca o próximo token válido e o retorna. Usamos um laço `while True` para repetir esse processo até que o arquivo chegue ao fim (retornando `None`).