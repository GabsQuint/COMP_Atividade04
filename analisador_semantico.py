class AnalisadorSemantico:
    def __init__(self, caminho_entrada):
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            self.tokens = [line.strip().split() for line in f.readlines()]
        self.pos = 0
        self.variaveis_declaradas = set()
        self.erros = []

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ["EOF", "-"]

    def proximo(self):
        self.pos += 1

    def analisar(self):
        while self.atual()[0] != "EOF":
            token = self.atual()[0]
            if token == "TIPO":
                self.analisar_declaracao()
            elif token in ["ID", "LEIA", "ESCREVA", "SE", "PARA"]:
                self.analisar_uso()
            else:
                self.proximo()

        return self.erros

    def analisar_declaracao(self):
        self.proximo()  # TIPO
        token = self.atual()
        if token[0] == "ID":
            self.variaveis_declaradas.add(token[1])
        else:
            self.erros.append("Esperado identificador após declaração de tipo.")
        self.proximo()  # ID
        self.proximo()  # ;

    def analisar_uso(self):
        token = self.atual()
        if token[0] == "ID":
            self.verificar_variavel(token[1])
            self.proximo()
            if self.atual()[0] == "ATR":
                self.proximo()
                self.analisar_expressao()
        elif token[0] == "LEIA":
            self.proximo()  # LEIA
            self.proximo()  # (
            token = self.atual()
            if token[0] == "ID":
                self.verificar_variavel(token[1])
            self.proximo()
            self.proximo()  # )
            self.proximo()  # ;
        elif token[0] == "ESCREVA":
            self.proximo()  # ESCREVA
            self.proximo()  # (
            if self.atual()[0] == "ID":
                self.verificar_variavel(self.atual()[1])
            self.proximo()
            self.proximo()  # )
            self.proximo()  # ;
        elif token[0] == "SE" or token[0] == "PARA":
            self.proximo()
            self.analisar_expressao()

    def analisar_expressao(self):
        while self.atual()[0] in ["ID", "NUMINT", "OPMAIS", "OPMENOS", "OPMULTI", "OPDIVI", "LOGIGUAL", "LOGDIFF", "LOGMAIOR", "LOGMENOR", "LOGMAIORIGUAL", "LOGMENORIGUAL"]:
            if self.atual()[0] == "ID":
                self.verificar_variavel(self.atual()[1])
            self.proximo()

    def verificar_variavel(self, id_pos):
        if id_pos not in self.variaveis_declaradas:
            self.erros.append(f"Variável usada sem declaração prévia: posição {id_pos}")
