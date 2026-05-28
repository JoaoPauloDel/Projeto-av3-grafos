from collections import deque


def bfs(grafo, origem, destino=None):
    visitados = {origem}
    fila = deque()
    fila.append((origem, [origem]))
    visitados_ordem = [origem]

    while fila:
        atual, caminho = fila.popleft()

        if destino and atual == destino:
            return caminho, len(caminho) - 1

        for vizinho, _ in grafo.adj.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                visitados_ordem.append(vizinho)
                fila.append((vizinho, caminho + [vizinho]))

    if destino:
        return None, -1

    return visitados_ordem


def verificar_conectividade(grafo):
    todos = set(grafo.vertices.keys())
    nao_visitados = todos.copy()
    componentes = []

    while nao_visitados:
        raiz = next(iter(nao_visitados))
        alcancados = set(bfs(grafo, raiz))
        componentes.append(alcancados)
        nao_visitados -= alcancados

    conectado = len(componentes) == 1
    return conectado, componentes