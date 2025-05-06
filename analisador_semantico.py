
from analisador_lexico import analisador_lexico, tabela_simbolos

class AnalisadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = tokens[self.pos]
        self.simbolos_declarados = set()

    def proximo(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_atual = self.tokens[self.pos]
        else:
            self.token_atual = ('EOF', '-')

    def analisar(self):
        while self.token_atual[0] != 'EOF':
            if self.token_atual[0] == 'TIPO':
                self.proximo()
                if self.token_atual[0] == 'ID':
                    self.simbolos_declarados.add(self.token_atual[1])
                    self.proximo()
            elif self.token_atual[0] == 'ID':
                if self.token_atual[1] not in self.simbolos_declarados:
                    raise Exception(f"Erro semântico: variável '{self.recuperar_nome(self.token_atual[1])}' usada sem declaração.")
                self.proximo()
            else:
                self.proximo()

    def recuperar_nome(self, posicao):
        for nome, pos in tabela_simbolos.items():
            if pos == posicao:
                return nome
        return f"<pos {posicao} desconhecida>"

def main():
    with open("codigo.POR", "r", encoding="utf-8") as f:
        codigo = f.read()

    tokens = analisador_lexico(codigo)
    semantico = AnalisadorSemantico(tokens)
    try:
        semantico.analisar()
        print("Análise semântica concluída com sucesso.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
