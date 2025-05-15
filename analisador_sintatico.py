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
        return self.consumir("TIPO") and self.consumir("ID") and self.consumir(";")

    def atribuicao(self):
        return self.consumir("ID") and self.consumir("ATR") and self.expressao() and self.consumir(";")

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
        return self.consumir("LEIA") and self.consumir("PARAB") and self.consumir("ID") and self.consumir("PARFE") and self.consumir(";")

    def cmd_escreva(self):
        if not self.consumir("ESCREVA") or not self.consumir("PARAB"):
            return False
        if self.atual()[0] in ["ID", "NUMINT", "STRING"]:
            self.pos += 1
        else:
            self.erros.append("Argumento inválido para escreva")
            return False
        return self.consumir("PARFE") and self.consumir(";")

    def cmd_se(self):
        if not self.consumir("SE"):
            return False
        if not self.expressao_logica():
            return False
        if not self.consumir("ENTAO"):
            return False
        while self.atual()[0] not in ["SENAO", "FIMSE", "EOF"]:
            if not self.comando():
                return False
        if self.atual()[0] == "SENAO":
            self.consumir("SENAO")
            while self.atual()[0] != "FIMSE":
                if not self.comando():
                    return False
        return self.consumir("FIMSE")

    def cmd_para(self):
        return (
            self.consumir("PARA") and
            self.atribuicao() and
            self.consumir("ATE") and
            self.expressao() and
            (self.consumir("PASSO") and self.expressao() if self.atual()[0] == "PASSO" else True) and
            self.lista_comandos("FIMPARA")
        )

    def lista_comandos(self, fim_token):
        while self.atual()[0] != fim_token:
            if self.atual()[0] == "EOF":
                self.erros.append(f"Esperado {fim_token}, mas chegou ao final do arquivo.")
                return False
            if not self.comando():
                return False
        return self.consumir(fim_token)

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
