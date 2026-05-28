import math
import random

# Bairros reais de Fortaleza com coordenadas (lat, lon)
BAIRROS = {
    'Centro':              (-3.7172, -38.5433),
    'Aldeota':             (-3.7317, -38.5022),
    'Meireles':            (-3.7248, -38.5069),
    'Iracema':             (-3.7209, -38.5239),
    'Benfica':             (-3.7411, -38.5397),
    'Fátima':              (-3.7456, -38.5319),
    'Dionísio Torres':     (-3.7372, -38.5108),
    'Joaquim Távora':      (-3.7497, -38.5086),
    'Varjota':             (-3.7278, -38.4944),
    'Mucuripe':            (-3.7176, -38.4769),
    'Cocó':                (-3.7406, -38.4828),
    'Papicu':              (-3.7330, -38.4881),
    'Aeroporto':           (-3.7763, -38.5322),
    'Messejana':           (-3.8331, -38.4936),
    'Parangaba':           (-3.7817, -38.5542),
    'Montese':             (-3.7706, -38.5439),
    'Damas':               (-3.7578, -38.5486),
    'Parquelândia':        (-3.7539, -38.5622),
    'Rodolfo Teófilo':     (-3.7644, -38.5633),
    'Antônio Bezerra':     (-3.7486, -38.5814),
    'Quintino Cunha':      (-3.7597, -38.5758),
    'Barra do Ceará':      (-3.7044, -38.5825),
    'Cristo Redentor':     (-3.7211, -38.5753),
    'Pirambu':             (-3.7133, -38.5672),
    'Carlito Pamplona':    (-3.7211, -38.5639),
    'Moura Brasil':        (-3.7167, -38.5539),
    'Água Fria':           (-3.8022, -38.5547),
    'Prefeito José Walter':(-3.8233, -38.5522),
    'Cajazeiras':          (-3.8044, -38.5133),
    'Jangurussu':          (-3.8406, -38.5236),
    'Castelão':            (-3.8189, -38.5236),
    'Lagoa Redonda':       (-3.8106, -38.4664),
    'Passaré':             (-3.8200, -38.5078),
    'Conjunto Ceará':      (-3.7878, -38.6078),
    'Granja Portugal':     (-3.7972, -38.6117),
    'Bom Jardim':          (-3.7906, -38.5900),
    'Siqueira':            (-3.7839, -38.6039),
    'Parque Dois Irmãos':  (-3.7961, -38.5717),
    'Mondubim':            (-3.8000, -38.5878),
    'Alagadiço':           (-3.7608, -38.5900),
    'Vila Velha':          (-3.7367, -38.5503),
    'José Bonifácio':      (-3.7519, -38.5358),
    'São João do Tauape':  (-3.7683, -38.5161),
    'Edson Queiroz':       (-3.7906, -38.4736),
    'Sapiranga':           (-3.7906, -38.4639),
    'Manoel Sátiro':       (-3.7889, -38.5731),
    'Granja Lisboa':       (-3.8011, -38.5922),
    'Serrinha':            (-3.7756, -38.5144),
    'Maraponga':           (-3.7939, -38.5644),
    'Cambeba':             (-3.8078, -38.4961),
}


def haversine(c1, c2):
    """Calcula distância em km entre dois pontos (lat, lon)."""
    R = 6371.0
    lat1, lon1 = math.radians(c1[0]), math.radians(c1[1])
    lat2, lon2 = math.radians(c2[0]), math.radians(c2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return R * 2 * math.asin(math.sqrt(a))


class Grafo:

    def __init__(self):
        self.vertices = {}
        self.coords   = {}
        self.adj      = {}
        self._construir()

    def _construir(self):
        random.seed(42)
        nomes = list(BAIRROS.keys())

        for i, nome in enumerate(nomes):
            self.vertices[nome] = i
            self.coords[nome]   = BAIRROS[nome]
            self.adj[nome]      = []

        LIMIAR = 4.0
        arestas_adicionadas = set()

        for i, a in enumerate(nomes):
            vizinhos = []
            for j, b in enumerate(nomes):
                if a == b:
                    continue
                dist = haversine(BAIRROS[a], BAIRROS[b])
                if dist <= LIMIAR:
                    vizinhos.append((dist, b))

            if len(vizinhos) < 3:
                todos = sorted(
                    [(haversine(BAIRROS[a], BAIRROS[b]), b) for b in nomes if b != a]
                )
                vizinhos = todos[:3]

            for dist, b in vizinhos:
                if (a, b) not in arestas_adicionadas:
                    peso = round(dist, 3)
                    self.adj[a].append((b, peso))
                    self.adj[b].append((a, peso))
                    arestas_adicionadas.add((a, b))
                    arestas_adicionadas.add((b, a))

        extra_pares = [
            ('Centro', 'Parangaba'), ('Aldeota', 'Messejana'),
            ('Meireles', 'Castelão'), ('Benfica', 'Mondubim'),
            ('Aeroporto', 'Cajazeiras'), ('Cocó', 'Lagoa Redonda'),
            ('Conjunto Ceará', 'Centro'), ('Jangurussu', 'Aldeota'),
        ]
        for a, b in extra_pares:
            if a in self.adj and b in self.adj:
                dist = round(haversine(BAIRROS[a], BAIRROS[b]), 3)
                if not any(v == b for v, _ in self.adj[a]):
                    self.adj[a].append((b, dist))
                if not any(v == a for v, _ in self.adj[b]):
                    self.adj[b].append((a, dist))

    def num_vertices(self):
        return len(self.vertices)

    def num_arestas(self):
        return sum(len(v) for v in self.adj.values()) // 2

    def grau(self, nome):
        return len(self.adj.get(nome, []))

    def lista_bairros(self):
        return sorted(self.vertices.keys())