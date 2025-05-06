
from analisador_lexico import analisador_lexico

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]

    def proximo(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_atual = self.tokens[self.pos]
        else:
            self.token_atual = ('EOF', '-')

    def erro(self, esperado):
        raise SyntaxError(f"Erro sintático: esperado {esperado}, encontrado {self.token_atual}")

    def aceitar(self, tipo):
        if self.token_atual[0] == tipo:
            self.proximo()
        else:
            self.erro(tipo)

    def analisar(self):
        while self.token_atual[0] != 'EOF':
            self.comando()

    def comando(self):
        if self.token_atual[0] == 'TIPO':
            self.declaracao()
        elif self.token_atual[0] == 'ID':
            self.atribuicao()
        elif self.token_atual[0] == 'ESCREVA':
            self.escreva()
        elif self.token_atual[0] == 'LEIA':
            self.leia()
        else:
            self.erro("comando")

    def declaracao(self):
        self.aceitar('TIPO')
        self.aceitar('ID')
        self.aceitar('PONTOEVIRGULA')

    def atribuicao(self):
        self.aceitar('ID')
        self.aceitar('ATR')
        self.expressao()
        self.aceitar('PONTOEVIRGULA')

    def escreva(self):
        self.aceitar('ESCREVA')
        self.aceitar('PARAB')
        if self.token_atual[0] in ['ID', 'NUMINT', 'STRING']:
            self.proximo()
        else:
            self.erro("ID, NUMINT ou STRING")
        self.aceitar('PARFE')
        self.aceitar('PONTOEVIRGULA')

    def leia(self):
        self.aceitar('LEIA')
        self.aceitar('PARAB')
        self.aceitar('ID')
        self.aceitar('PARFE')
        self.aceitar('PONTOEVIRGULA')

    def expressao(self):
        if self.token_atual[0] in ['ID', 'NUMINT']:
            self.proximo()
            if self.token_atual[0] in ['OPMAIS', 'OPMENOS', 'OPMULTI', 'OPDIVI']:
                self.proximo()
                if self.token_atual[0] in ['ID', 'NUMINT']:
                    self.proximo()
                else:
                    self.erro("ID ou NUMINT")
        else:
            self.erro("ID ou NUMINT")

def main():
    with open("codigo.POR", "r", encoding="utf-8") as f:
        codigo = f.read()

    tokens = analisador_lexico(codigo)
    parser = AnalisadorSintatico(tokens)
    try:
        parser.analisar()
        print("Análise sintática concluída com sucesso.")
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    main()
