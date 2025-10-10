import json
import sys
import csv
import time


class AutomatoFinito:
    def __init__(self):
        self.inicial = None
        self.finais = set()
        self.transicoes = {}

    def executar(self, palavra):
        estado = self.inicial
        for simbolo in palavra:
            if estado in self.transicoes and simbolo in self.transicoes[estado]:
                estado = self.transicoes[estado][simbolo]
            else:
                return False
        return estado in self.finais

    @staticmethod
    def carregar(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)

            automato = AutomatoFinito()
            automato.inicial = str(dados.get("initial"))
            automato.finais = {str(s) for s in dados.get("final", [])}

            for transicao in dados.get("transitions", []):
                origem = str(transicao["from"])
                destino = str(transicao["to"])
                simbolo = transicao["read"]

                if origem not in automato.transicoes:
                    automato.transicoes[origem] = {}

                if simbolo in automato.transicoes[origem]:
                    raise ValueError(
                        f"Erro de AFD: Transição duplicada do estado {origem} lendo '{simbolo}'"
                    )

                automato.transicoes[origem][simbolo] = destino

            return automato

        except FileNotFoundError:
            print(f"Erro: Arquivo do autômato não encontrado: {caminho}")
        except json.JSONDecodeError:
            print(f"Erro: Formato JSON inválido no arquivo: {caminho}")
        except Exception as e:
            print(f"Erro inesperado ao carregar o autômato: {e}")

        return None


def processar_testes(automato, caminho_testes):
    resultados = []

    try:
        with open(caminho_testes, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')

            for linha in leitor:
                if len(linha) < 2:
                    continue

                entrada, esperado = linha[0], linha[1]
                inicio = time.time()
                aceitou = 1 if automato.executar(entrada) else 0
                fim = time.time()

                duracao = round(fim - inicio, 3)
                resultados.append((entrada, esperado, aceitou, duracao))
    except FileNotFoundError:
        print(f"Erro: Arquivo de testes não encontrado: {caminho_testes}")
        sys.exit(1)

    return resultados


def salvar_resultados(caminho_saida, resultados):
    try:
        with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write("palavra;resultadoesperado;resultado_obtido;tempo\n")
            for entrada, esperado, obtido, duracao in resultados:
                arquivo.write(f"{entrada};{esperado};{obtido};{duracao}\n")

        print(f"Execução concluída. Resultados salvos em '{caminho_saida}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de saída: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 4:
        print("Uso: python app.py <automato.json> <entradas.in> <saida.out>")
        sys.exit(1)

    caminho_automato = sys.argv[1]
    caminho_entradas = sys.argv[2]
    caminho_saida = sys.argv[3]

    automato = AutomatoFinito.carregar(caminho_automato)
    if automato is None:
        print("Erro ao carregar o autômato. Encerrando execução.")
        sys.exit(1)

    resultados = processar_testes(automato, caminho_entradas)
    salvar_resultados(caminho_saida, resultados)


if __name__ == "__main__":
    main()
