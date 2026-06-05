# 🗺️ Malha Viária de Fortaleza
> Projeto Final · T290-40 · UNIFOR

**Equipe:** João Paulo Del Vecchio `2413537` · Reynaldo Athayde `2410371`

---

## Instalação e execução
```bash
pip install matplotlib networkx
python main.py
```

## Como usar
1. Digite a **Origem** e o **Destino** nos campos e selecione a sugestão
2. Clique em **Calcular Rota**
3. 🟠 Laranja = Dijkstra (menor km) · 🟢 Verde = BFS (menos bairros)

## Arquivos
| Arquivo | Descrição |
|---|---|
| `main.py` | Execução principal |
| `grafo.py` | Construção do grafo |
| `bfs.py` | Algoritmo BFS |
| `dijkstra.py` | Algoritmo Dijkstra |
| `analises.py` | Análises do grafo |
| `visualizacao.py` | Interface gráfica |
