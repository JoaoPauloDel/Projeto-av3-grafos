============================================================
PROJETO FINAL — RESOLUÇÃO DE PROBLEMAS EM GRAFOS
Disciplina: T290-40 Resolução prob com grafos — UNIFOR
============================================================

EQUIPE:
João Paulo Del Vecchio — 2413537
Reynaldo Athayde       — 2410371

PRÉ-REQUISITOS:
pip install matplotlib networkx

COMO EXECUTAR:
python main.py

USO DA INTERFACE:
1. Selecione "Definir Origem" e marque um bairro
2. Selecione "Definir Destino" e marque outro bairro
3. Clique em "Calcular Rota"
4. Laranja = Dijkstra (menor km) | Verde = BFS (menos bairros)
5. "Limpar Seleção" para reiniciar

ARQUIVOS:
main.py         → execução principalF
grafo.py        → construção do grafo
bfs.py          → algoritmo BFS
dijkstra.py     → algoritmo Dijkstra
analises.py     → análises do grafo
visualizacao.py → interface gráfica
    README.txt      → este arquivo
============================================================