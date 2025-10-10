# Simulador de Autômatos Finitos

## Descrição
Esta ferramenta permite simular autômatos finitos a partir de arquivos de especificação (`.aut`) e arquivos de entradas de teste (`.in`). A execução gera um arquivo de saída (`.out`) com os resultados de cada teste, incluindo o tempo de processamento.

O simulador funciona totalmente via **linha de comando**, sem interface gráfica.

---

## Estrutura de Arquivos
- `src/simulador.py` → código-fonte do simulador.
- `tests/arquivo_do_automato.aut` → especificação do autômato em formato JSON.
- `tests/arquivo_de_testes.in` → arquivo CSV com palavras de teste e resultados esperados.
- `arquivo_de_saida.out` → arquivo que será gerado pelo simulador com os resultados obtidos.

---

## Como Executar
Na linha de comando, dentro da pasta do projeto, execute:

```bash
$ python src/simulador.py tests/arquivo_do_automato.aut tests/arquivo_de_testes.in arquivo_de_saida.out
