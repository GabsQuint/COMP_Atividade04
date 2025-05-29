from analisador_lexico import analisador_lexico
from analisador_sintatico import Parser
from analisador_semantico import AnalisadorSemantico
import csv

ARQ_ENTRADA = "TESTE_SEM_ERRO.POR"
ARQ_TOKENS = "saida.TEM"
ARQ_CSV = "saida.csv"

print("=== FASE 2: ANÁLISE LÉXICA ===")
analisador_lexico(ARQ_ENTRADA, ARQ_TOKENS)

print("\n=== FASE 3: ANÁLISE SINTÁTICA ===")
parser = Parser(ARQ_TOKENS)
erros_sintaticos = parser.analisar()

if erros_sintaticos:
    print("Erros sintáticos encontrados:")
    for erro in erros_sintaticos:
        print("-", erro)
else:
    print("Análise sintática concluída com sucesso!")

print("\n=== FASE 4: ANÁLISE SEMÂNTICA ===")
semantico = AnalisadorSemantico(ARQ_TOKENS)
erros_semanticos = semantico.analisar()

if erros_semanticos:
    print("Erros semânticos encontrados:")
    for erro in erros_semanticos:
        print("-", erro)
else:
    print("Análise semântica concluída com sucesso!")

# Geração do CSV a partir do .TEM
def gerar_csv_formatado(caminho_tem, caminho_csv):
    with open(caminho_tem, "r", encoding="utf-8") as entrada, open(caminho_csv, "w", newline="", encoding="utf-8") as saida:
        writer = csv.writer(saida)
        writer.writerow(["Token", "Posição"])  # Cabeçalho
        for linha in entrada:
            partes = linha.strip().split()
            if len(partes) == 2:
                writer.writerow(partes)
    print(f"\nCSV gerado com sucesso: {caminho_csv}")

gerar_csv_formatado(ARQ_TOKENS, ARQ_CSV)
