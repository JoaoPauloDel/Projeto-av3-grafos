import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import CheckButtons, Button, RadioButtons

from grafo import Grafo
from bfs import bfs
from dijkstra import dijkstra
from analises import analise_grau, resumo_grafo

COR_ARESTA      = '#CCCCCC'
COR_VERTICE     = '#4A90D9'
COR_SELECIONADO = '#E74C3C'
COR_ROTA_DIJK   = '#E67E22'
COR_ROTA_BFS    = '#2ECC71'
COR_FUNDO       = '#1A1A2E'
COR_PAINEL      = '#16213E'
COR_TEXTO       = 'white'


class App:
    def __init__(self):
        self.grafo   = Grafo()
        self.bairros = self.grafo.lista_bairros()
        self.origem  = None
        self.destino = None
        self._build_ui()
        self._desenhar_grafo()
        self._atualizar_info()
        plt.show()

    def _build_ui(self):
        self.fig = plt.figure(figsize=(18, 10), facecolor=COR_FUNDO)
        self.fig.canvas.manager.set_window_title('Malha Viária de Fortaleza — Grafos')

        self.ax_mapa = self.fig.add_axes([0.22, 0.05, 0.77, 0.90])
        self.ax_mapa.set_facecolor(COR_FUNDO)
        for spine in self.ax_mapa.spines.values():
            spine.set_edgecolor('#444')

        self.ax_check = self.fig.add_axes([0.01, 0.12, 0.19, 0.83])
        self.ax_check.set_facecolor(COR_PAINEL)
        self.ax_check.set_title('1º clique = Origem  |  2º = Destino', color=COR_TEXTO, fontsize=8, pad=6)

        self.checks = CheckButtons(self.ax_check, self.bairros, [False] * len(self.bairros))
        for txt in self.checks.labels:
            txt.set_color(COR_TEXTO)
            txt.set_fontsize(7.5)
        try:
            for rect in self.checks.rectangles:
                rect.set_facecolor('#2C3E50')
                rect.set_edgecolor('#7F8C8D')
        except AttributeError:
            pass
        self.checks.on_clicked(self._on_check)

        self.ax_btn_calc = self.fig.add_axes([0.01, 0.065, 0.19, 0.04])
        self.btn_calc = Button(self.ax_btn_calc, 'Calcular Rota', color='#27AE60', hovercolor='#2ECC71')
        self.btn_calc.label.set_color('white')
        self.btn_calc.label.set_fontsize(9)
        self.btn_calc.on_clicked(self._calcular_rota)

        self.ax_btn_limpar = self.fig.add_axes([0.01, 0.02, 0.19, 0.04])
        self.btn_limpar = Button(self.ax_btn_limpar, 'Limpar Seleção', color='#C0392B', hovercolor='#E74C3C')
        self.btn_limpar.label.set_color('white')
        self.btn_limpar.label.set_fontsize(9)
        self.btn_limpar.on_clicked(self._limpar)

        self.ax_info = self.fig.add_axes([0.01, 0.00, 0.98, 0.018])
        self.ax_info.set_facecolor('#0F3460')
        self.ax_info.axis('off')
        self.txt_info = self.ax_info.text(
            0.01, 0.5, '', color=COR_TEXTO, fontsize=8,
            va='center', ha='left', transform=self.ax_info.transAxes
        )

    def _desenhar_grafo(self, caminho_dijk=None, caminho_bfs=None):
        self.ax_mapa.cla()
        self.ax_mapa.set_facecolor(COR_FUNDO)
        self.ax_mapa.set_title('Malha Viária — Fortaleza, CE', color=COR_TEXTO, fontsize=12, pad=10)

        coords = self.grafo.coords
        adj    = self.grafo.adj

        def xy(nome):
            lat, lon = coords[nome]
            return lon, lat

        desenhadas = set()
        for a, vizinhos in adj.items():
            for b, peso in vizinhos:
                chave = tuple(sorted([a, b]))
                if chave in desenhadas:
                    continue
                desenhadas.add(chave)
                xa, ya = xy(a)
                xb, yb = xy(b)
                self.ax_mapa.plot([xa, xb], [ya, yb], color=COR_ARESTA, lw=0.5, alpha=0.4, zorder=1)

        if caminho_bfs and len(caminho_bfs) > 1:
            for i in range(len(caminho_bfs) - 1):
                xa, ya = xy(caminho_bfs[i])
                xb, yb = xy(caminho_bfs[i + 1])
                self.ax_mapa.plot([xa, xb], [ya, yb], color=COR_ROTA_BFS, lw=2.5, alpha=0.8, zorder=3, linestyle='--')

        if caminho_dijk and len(caminho_dijk) > 1:
            for i in range(len(caminho_dijk) - 1):
                xa, ya = xy(caminho_dijk[i])
                xb, yb = xy(caminho_dijk[i + 1])
                self.ax_mapa.plot([xa, xb], [ya, yb], color=COR_ROTA_DIJK, lw=3, alpha=0.9, zorder=4)

        graus    = dict(analise_grau(self.grafo))
        max_grau = max(graus.values())

        for nome in self.grafo.vertices:
            x, y = xy(nome)
            grau  = graus[nome]
            r     = 4 + 6 * (grau / max_grau)

            if nome == self.origem:
                cor, zorder, r = '#E74C3C', 6, 12
            elif nome == self.destino:
                cor, zorder, r = '#9B59B6', 6, 12
            elif caminho_dijk and nome in caminho_dijk:
                cor, zorder = COR_ROTA_DIJK, 5
            elif caminho_bfs and nome in caminho_bfs:
                cor, zorder = COR_ROTA_BFS, 5
            else:
                cor, zorder = COR_VERTICE, 2

            self.ax_mapa.scatter(x, y, s=r**2, c=cor, zorder=zorder, edgecolors='white', linewidths=0.5)

            if nome in [self.origem, self.destino] or (caminho_dijk and nome in caminho_dijk):
                self.ax_mapa.annotate(
                    nome, (x, y),
                    textcoords='offset points', xytext=(4, 4),
                    fontsize=6.5, color=COR_TEXTO, zorder=7,
                    bbox=dict(boxstyle='round,pad=0.2', fc='#0F3460', ec='none', alpha=0.7)
                )

        legenda = [
            mpatches.Patch(color='#E74C3C',     label=f'Origem: {self.origem or "—"}'),
            mpatches.Patch(color='#9B59B6',     label=f'Destino: {self.destino or "—"}'),
            mpatches.Patch(color=COR_ROTA_DIJK, label='Rota Dijkstra (menor distância)'),
            mpatches.Patch(color=COR_ROTA_BFS,  label='Rota BFS (menos bairros)'),
        ]
        self.ax_mapa.legend(handles=legenda, loc='lower right', facecolor=COR_PAINEL,
                            labelcolor=COR_TEXTO, fontsize=8, framealpha=0.9)
        self.ax_mapa.set_xlabel('Longitude', color=COR_TEXTO, fontsize=8)
        self.ax_mapa.set_ylabel('Latitude',  color=COR_TEXTO, fontsize=8)
        self.ax_mapa.tick_params(colors='#888', labelsize=7)
        self.fig.canvas.draw_idle()

    def _on_check(self, label):
        marcados = [b for b, ativo in zip(self.bairros, self.checks.get_status()) if ativo]
        if len(marcados) > 2:
            idx = self.bairros.index(label)
            self.checks.set_active(idx)
            return
        if len(marcados) == 0:
            self.origem  = None
            self.destino = None
        elif len(marcados) == 1:
            self.origem  = marcados[0]
            self.destino = None
        else:
            self.origem  = marcados[0]
            self.destino = marcados[1]
        self._desenhar_grafo()
        self._atualizar_info()

    def _calcular_rota(self, event):
        if not self.origem or not self.destino:
            self.txt_info.set_text('⚠  Selecione origem E destino antes de calcular.')
            self.fig.canvas.draw_idle()
            return
        caminho_dijk, dist   = dijkstra(self.grafo, self.origem, self.destino)
        caminho_bfs,  saltos = bfs(self.grafo, self.origem, self.destino)
        self._desenhar_grafo(caminho_dijk=caminho_dijk, caminho_bfs=caminho_bfs)
        info_dijk = f'Dijkstra: {" → ".join(caminho_dijk)} | {dist} km' if caminho_dijk else 'Dijkstra: sem caminho'
        info_bfs  = f'BFS: {saltos} bairro(s) intermediário(s)' if caminho_bfs else 'BFS: sem caminho'
        self.txt_info.set_text(f'  {info_dijk}       |       {info_bfs}')
        self.fig.canvas.draw_idle()

    def _limpar(self, event):
        self.origem  = None
        self.destino = None
        for i, ativo in enumerate(self.checks.get_status()):
            if ativo:
                self.checks.set_active(i)
        self._desenhar_grafo()
        self._atualizar_info()

    def _atualizar_info(self):
        from analises import resumo_grafo
        res = resumo_grafo(self.grafo)
        self.txt_info.set_text(
            f"  Vértices: {res['vertices']}  |  Arestas: {res['arestas']}  |  "
            f"Conectado: {'Sim' if res['conectado'] else 'Não'}  |  "
            f"Ciclos: {'Sim' if res['tem_ciclos'] else 'Não'}  |  "
            f"Grau médio: {res['grau_medio']}  |  "
            f"Origem: {self.origem or '—'}  |  Destino: {self.destino or '—'}"
        )
        self.fig.canvas.draw_idle()


def iniciar():
    App()