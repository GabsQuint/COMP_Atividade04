class Parser:
    def __init__(self, caminho_entrada):
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            self.tokens = [line.strip().split() for line in f.readlines()]
        self.pos = 0
        self.erros = []

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ["EOF", "-"]

    def consumir(self, esperado):
        token = self.atual()
        if token[0] == esperado:
            self.pos += 1
            return True
        else:
            self.erros.append(f"Esperado {esperado}, mas encontrado {token[0]}")
            return False

    def analisar(self):
        while self.atual()[0] != "EOF":
            if not self.comando():
                break
        return self.erros

    def comando(self):
        token = self.atual()[0]
        if token == "TIPO":
            return self.declaracao_variavel()
        elif token == "ID":
            return self.atribuicao()
        elif token == "LEIA":
            return self.cmd_leia()
        elif token == "ESCREVA":
            return self.cmd_escreva()
        elif token == "SE":
            return self.cmd_se()
        elif token == "PARA":
            return self.cmd_para()
        else:
            self.erros.append(f"Comando inesperado: {token}")
            self.pos += 1
            return False

    def declaracao_variavel(self):
        self.consumir("TIPO")
        if self.atual()[0] == "DOISPONTOS":
            self.consumir("DOISPONTOS")
        if not self.consumir("ID"):
            return False
        if self.atual()[0] == ";":
            self.consumir(";")
        else:
            print("Aviso: ponto e vírgula ausente após declaração.")
        return True

    def atribuicao(self):
        self.consumir("ID")
        self.consumir("ATR")
        self.expressao()
        if self.atual()[0] == ";":
            self.consumir(";")
        else:
            print("Aviso: ponto e vírgula ausente após atribuição.")
        return True

    def expressao(self):
        token = self.atual()[0]
        if token in ["ID", "NUMINT"]:
            self.pos += 1
            while self.atual()[0] in ["OPMAIS", "OPMENOS", "OPMULTI", "OPDIVI"]:
                self.pos += 1
                if self.atual()[0] not in ["ID", "NUMINT"]:
                    self.erros.append(f"Expressão inválida após operador")
                    return False
                self.pos += 1
            return True
        else:
            self.erros.append("Expressão inválida")
            return False

    def cmd_leia(self):
        self.consumir("LEIA")
        self.consumir("PARAB")
        self.consumir("ID")
        self.consumir("PARFE")
        if self.atual()[0] == ";":
            self.consumir(";")
        else:
            print("Aviso: ponto e vírgula ausente após leia.")
        return True

    def cmd_escreva(self):
        self.consumir("ESCREVA")
        self.consumir("PARAB")
        if self.atual()[0] in ["ID", "NUMINT", "STRING"]:
            self.pos += 1
        else:
            self.erros.append("Argumento inválido para escreva")
            return False
        self.consumir("PARFE")
        if self.atual()[0] == ";":
            self.consumir(";")
        else:
            print("Aviso: ponto e vírgula ausente após escreva.")
        return True

    def cmd_se(self):
        self.consumir("SE")
        self.expressao_logica()
        self.consumir("ENTAO")
        while self.atual()[0] not in ["SENAO", "FIMSE", "EOF"]:
            self.comando()
        if self.atual()[0] == "SENAO":
            self.consumir("SENAO")
            while self.atual()[0] != "FIMSE":
                self.comando()
        self.consumir("FIMSE")
        return True

    def cmd_para(self):
        self.consumir("PARA")
        self.atribuicao()
        self.consumir("ATE")
        self.expressao()
        if self.atual()[0] == "PASSO":
            self.consumir("PASSO")
            self.expressao()
        while self.atual()[0] != "FIMPARA":
            self.comando()
        self.consumir("FIMPARA")
        return True

    def expressao_logica(self):
        if self.atual()[0] in ["ID", "NUMINT"]:
            self.pos += 1
            if self.atual()[0] in ["LOGIGUAL", "LOGDIFF", "LOGMAIOR", "LOGMENOR", "LOGMAIORIGUAL", "LOGMENORIGUAL"]:
                self.pos += 1
                if self.atual()[0] in ["ID", "NUMINT"]:
                    self.pos += 1
                    return True
        self.erros.append("Expressão lógica inválida")
        return False