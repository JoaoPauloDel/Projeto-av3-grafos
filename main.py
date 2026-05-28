"""
Projeto Final — Resolução de Problemas em Grafos
Disciplina: T290-40 Resolução prob com grafos 

Equipe:
    João Paulo Del Vecchio — 2413537
    Reynaldo Athayde       — 2410371
"""

from grafo import Grafo
from analises import analise_grau, analise_conectividade, analise_ciclos, analise_caminhos_minimos, resumo_grafo
from visualizacao import iniciar

LINHA = '=' * 60


def main():
    print()
    print(LINHA)
    print('  PROJETO FINAL — GRAFOS — UNIFOR')
    print('  Malha Viária e Rotas de Fortaleza')
    print(LINHA)

    grafo = Grafo()
    res   = resumo_grafo(grafo)

    print(f"\n  Vértices  : {res['vertices']}")
    print(f"  Arestas   : {res['arestas']}")
    print(f"  Conectado : {'Sim' if res['conectado'] else 'Não'}")
    print(f"  Ciclos    : {'Sim' if res['tem_ciclos'] else 'Não'}")
    print(f"  Grau médio: {res['grau_medio']}")

    print(f'\n{LINHA}')
    print('  ANÁLISE 1 — TOP 10 BAIRROS POR GRAU')
    print(LINHA)
    for i, (b, g) in enumerate(analise_grau(grafo)[:10], 1):
        print(f"  {i:2}. {b:<25} grau={g}  {'█' * g}")

    print(f'\n{LINHA}')
    print('  ANÁLISE 2 — CONECTIVIDADE (BFS)')
    print(LINHA)
    conectado, n_comp, _ = analise_conectividade(grafo)
    print(f"  Conectado: {'Sim' if conectado else 'Não'} | Componentes: {n_comp}")

    print(f'\n{LINHA}')
    print('  ANÁLISE 3 — CICLOS (DFS)')
    print(LINHA)
    print(f"  {'Ciclos encontrados.' if analise_ciclos(grafo) else 'Sem ciclos.'}")

    print(f'\n{LINHA}')
    print('  ANÁLISE 4 — CAMINHOS MÍNIMOS (Dijkstra + BFS)')
    print(LINHA)
    pares = [('Centro', 'Messejana'), ('Meireles', 'Conjunto Ceará'), ('Aldeota', 'Jangurussu')]
    for r in analise_caminhos_minimos(grafo, pares):
        print(f"\n  {r['origem']} → {r['destino']}")
        if r['caminho_dijkstra']:
            print(f"  Dijkstra : {' → '.join(r['caminho_dijkstra'])} ({r['distancia_km']} km)")
        if r['caminho_bfs']:
            print(f"  BFS      : {' → '.join(r['caminho_bfs'])} ({r['saltos']} salto(s))")

    print(f'\n{LINHA}')
    print('  Abrindo interface gráfica...')
    print(LINHA)
    iniciar()


if __name__ == '__main__':
    main()