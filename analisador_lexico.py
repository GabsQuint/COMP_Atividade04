import re

# Tabela de palavras reservadas e seus códigos
PALAVRAS_RESERVADAS = {
    "até": "ATE",
    "então": "ENTAO",
    "escreva": "ESCREVA",
    "fim_para": "FIMPARA",
    "fim_se": "FIMSE",
    "leia": "LEIA",
    "não": "NAO",
    "ou": "OU",
    "para": "PARA",
    "passo": "PASSO",
    "se": "SE",
    "senão": "SENAO",
    "inteiro": "TIPO",
    "e": "E"
}

# Expressões regulares para os tokens
PADROES = [
    (r'\d+', "NUMINT"),
    (r'\".*?\"', "STRING"),
    (r'\<\-', "ATR"),
    (r'\<\>', "LOGDIFF"),
    (r'\>\=', "LOGMAIORIGUAL"),
    (r'\<\=', "LOGMENORIGUAL"),
    (r'\>', "LOGMAIOR"),
    (r'\<', "LOGMENOR"),
    (r'\=', "LOGIGUAL"),
    (r'\+', "OPMAIS"),
    (r'\-', "OPMENOS"),
    (r'\*', "OPMULTI"),
    (r'\/', "OPDIVI"),
    (r'\(', "PARAB"),
    (r'\)', "PARFE"),
    (r';', ";"),
    (r'\w+', "ID"),
    (r':', "DOISPONTOS"),
]

# Função auxiliar para verificar se é palavra reservada
def verifica_palavra_reservada(token):
    return PALAVRAS_RESERVADAS.get(token, None)

# Lê arquivo .POR e processa os tokens
def analisador_lexico(caminho_entrada, caminho_saida):
    tabela_simbolos = {}
    tokens = []
    
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        conteudo = f.read()
        conteudo = conteudo.replace(":", " ")

    posicao = 0
    while conteudo:
        conteudo = conteudo.lstrip()
        for padrao, tipo_token in PADROES:
            match = re.match(padrao, conteudo)
            if match:
                lexema = match.group(0)
                token_tipo = verifica_palavra_reservada(lexema)
                if token_tipo:
                    tokens.append((token_tipo, "-"))
                elif tipo_token == "ID":
                    if lexema not in tabela_simbolos:
                        tabela_simbolos[lexema] = len(tabela_simbolos)
                    tokens.append((tipo_token, tabela_simbolos[lexema]))
                else:
                    tokens.append((tipo_token, "-"))
                conteudo = conteudo[len(lexema):]
                break
        else:
            if conteudo.strip() == "":
                break  # fim do conteúdo, só espaços em branco
            print("Erro léxico próximo a:", conteudo[:10])
            break


    tokens.append(("EOF", "-"))  # Token de final de arquivo

    with open(caminho_saida, "w", encoding="utf-8") as f:
        for token, pos in tokens:
            f.write(f"{token} {pos}\n")

    print("Tokens gerados com sucesso em:", caminho_saida)


