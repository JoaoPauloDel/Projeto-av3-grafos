import heapq


def dijkstra(grafo, origem, destino=None):
    INF = float('inf')

    dist     = {v: INF for v in grafo.vertices}
    anterior = {v: None for v in grafo.vertices}
    dist[origem] = 0.0

    heap = [(0.0, origem)]
    visitados = set()

    while heap:
        dist_atual, u = heapq.heappop(heap)

        if u in visitados:
            continue
        visitados.add(u)

        if destino and u == destino:
            break

        for vizinho, peso in grafo.adj.get(u, []):
            if vizinho in visitados:
                continue
            nova_dist = dist_atual + peso
            if nova_dist < dist[vizinho]:
                dist[vizinho] = nova_dist
                anterior[vizinho] = u
                heapq.heappush(heap, (nova_dist, vizinho))

    if destino:
        if dist[destino] == INF:
            return None, INF
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anterior[atual]
        caminho.reverse()
        return caminho, round(dist[destino], 3)

    return dist