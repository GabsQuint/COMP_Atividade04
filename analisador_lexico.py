
import re

# Tabela de palavras reservadas e seus tokens
PALAVRAS_RESERVADAS = {
    'até': 'ATE',
    'então': 'ENTAO',
    'escreva': 'ESCREVA',
    'fim_para': 'FIMPARA',
    'fim_se': 'FIMSE',
    'leia': 'LEIA',
    'não': 'NAO',
    'ou': 'OU',
    'para': 'PARA',
    'passo': 'PASSO',
    'se': 'SE',
    'senão': 'SENAO',
    'inteiro': 'TIPO',
    'e': 'E',
}

OPERADORES = {
    '<-': 'ATR',
    '<=': 'LOGMENORIGUAL',
    '>=': 'LOGMAIORIGUAL',
    '<>': 'LOGDIFF',
    '=': 'LOGIGUAL',
    '>': 'LOGMAIOR',
    '<': 'LOGMENOR',
    '+': 'OPMAIS',
    '-': 'OPMENOS',
    '*': 'OPMULTI',
    '/': 'OPDIVI',
    '(': 'PARAB',
    ')': 'PARFE',
    ';': 'PONTOEVIRGULA'
}

# Expressões regulares
REGEXES = [
    (r'".*?"', 'STRING'),
    (r'\d+', 'NUMINT'),
    (r'[a-zA-Z_]\w*', 'ID'),
    (r'\s+', None),
    *[(re.escape(op), token) for op, token in OPERADORES.items()]
]

# Tabela de símbolos
tabela_simbolos = {}
posicao_simbolo = 0

def verifica_palavra_reservada(palavra):
    return PALAVRAS_RESERVADAS.get(palavra, None)

def analisador_lexico(codigo):
    global posicao_simbolo
    tokens = []

    while codigo:
        for regex, tipo in REGEXES:
            match = re.match(regex, codigo)
            if match:
                lexema = match.group(0)
                if tipo:
                    if tipo == 'ID':
                        reservado = verifica_palavra_reservada(lexema)
                        if reservado:
                            tokens.append((reservado, '-'))
                        else:
                            if lexema not in tabela_simbolos:
                                tabela_simbolos[lexema] = posicao_simbolo
                                posicao_simbolo += 1
                            tokens.append((tipo, tabela_simbolos[lexema]))
                    elif tipo == 'STRING':
                        tokens.append((tipo, lexema))
                    elif tipo == 'NUMINT':
                        tokens.append((tipo, lexema))
                    else:
                        tokens.append((tipo, lexema))
                codigo = codigo[len(lexema):]
                break
        else:
            raise SyntaxError(f"Token inválido próximo de: {codigo[:10]}")
    tokens.append(('EOF', '-'))
    return tokens

def main():
    with open("codigo.POR", "r", encoding="utf-8") as f:
        codigo = f.read()

    tokens = analisador_lexico(codigo)
    print("Tokens encontrados:")
    for token in tokens:
        print(token)

    print("\nTabela de símbolos:")
    for simbolo, pos in tabela_simbolos.items():
        print(f"{pos}: {simbolo}")

if __name__ == "__main__":
    main()
