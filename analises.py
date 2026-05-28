from bfs import bfs, verificar_conectividade
from dijkstra import dijkstra


def analise_grau(grafo):
    graus = [(nome, grafo.grau(nome)) for nome in grafo.vertices]
    graus.sort(key=lambda x: x[1], reverse=True)
    return graus


def analise_conectividade(grafo):
    conectado, componentes = verificar_conectividade(grafo)
    return conectado, len(componentes), componentes


def analise_ciclos(grafo):
    def dfs(origem):
        pilha = [(origem, None)]
        vis_local = {}

        while pilha:
            v, pai = pilha.pop()
            if v in vis_local:
                continue
            vis_local[v] = pai

            for vizinho, _ in grafo.adj.get(v, []):
                if vizinho not in vis_local:
                    pilha.append((vizinho, v))
                elif vizinho != pai:
                    return True
        return False

    visitados = set()
    for bairro in grafo.vertices:
        if bairro not in visitados:
            if dfs(bairro):
                return True
    return False


def analise_caminhos_minimos(grafo, pares):
    resultados = []
    for origem, destino in pares:
        caminho_dijk, dist_dijk = dijkstra(grafo, origem, destino)
        caminho_bfs,  saltos    = bfs(grafo, origem, destino)
        resultados.append({
            'origem':            origem,
            'destino':           destino,
            'caminho_dijkstra':  caminho_dijk,
            'distancia_km':      dist_dijk,
            'caminho_bfs':       caminho_bfs,
            'saltos':            saltos,
        })
    return resultados


def resumo_grafo(grafo):
    conectado, n_comp, _ = analise_conectividade(grafo)
    return {
        'vertices':    grafo.num_vertices(),
        'arestas':     grafo.num_arestas(),
        'conectado':   conectado,
        'componentes': n_comp,
        'tem_ciclos':  analise_ciclos(grafo),
        'grau_medio':  round(
            sum(grafo.grau(v) for v in grafo.vertices) / grafo.num_vertices(), 2
        ),
    }