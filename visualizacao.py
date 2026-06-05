import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

from grafo import Grafo
from bfs import bfs
from dijkstra import dijkstra
from analises import analise_grau, resumo_grafo

C_FUNDO      = '#0D1117'
C_PAINEL     = '#161B22'
C_CARD       = '#21262D'
C_BORDA      = '#30363D'
C_TEXTO      = '#E6EDF3'
C_SUBTEXTO   = '#8B949E'
C_DESTAQUE   = '#58A6FF'
C_ORIGEM     = '#FF6B6B'
C_DESTINO    = '#C084FC'
C_ROTA_DIJK  = '#F39C12'
C_ROTA_BFS   = '#2ECC71'
C_ARESTA     = '#2A4A6B'
C_VERTICE    = '#4A90D9'
C_BTN_CALC   = '#238636'
C_BTN_LIMPAR = '#DA3633'


class App:
    def __init__(self):
        self.grafo   = Grafo()
        self.bairros = self.grafo.lista_bairros()
        self.origem  = None
        self.destino = None
        self.caminho_dijk = None
        self.caminho_bfs  = None
        self.popup_origem  = [None]
        self.popup_destino = [None]

        self.root = tk.Tk()
        self.root.title('Malha Viária de Fortaleza')
        self.root.configure(bg=C_FUNDO)
        self.root.state('zoomed')

        self._build_ui()
        self._desenhar_grafo()
        self.root.mainloop()

    def _build_ui(self):
        main = tk.Frame(self.root, bg=C_FUNDO)
        main.pack(fill='both', expand=True)

        painel = tk.Frame(main, bg=C_PAINEL, width=300)
        painel.pack(side='left', fill='y')
        painel.pack_propagate(False)

        mapa_frame = tk.Frame(main, bg=C_FUNDO)
        mapa_frame.pack(side='left', fill='both', expand=True)

        self._build_painel(painel)
        self._build_mapa(mapa_frame)

    def _build_painel(self, p):
        tk.Label(p, text='Malha Viária · Fortaleza', bg=C_PAINEL,
                 fg=C_DESTAQUE, font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=14, pady=(16,2))
        tk.Label(p, text='UNIFOR · Teoria dos Grafos', bg=C_PAINEL,
                 fg=C_SUBTEXTO, font=('Segoe UI', 8)).pack(anchor='w', padx=14)
        self._sep(p)

        # Origem
        tk.Label(p, text='Origem', bg=C_PAINEL, fg=C_SUBTEXTO,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=14, pady=(10,2))
        self.var_origem = tk.StringVar()
        self.ent_origem = tk.Entry(p, textvariable=self.var_origem,
                                   bg=C_CARD, fg=C_TEXTO, insertbackground=C_TEXTO,
                                   relief='flat', font=('Segoe UI', 10),
                                   highlightthickness=1, highlightbackground=C_BORDA,
                                   highlightcolor=C_ORIGEM)
        self.ent_origem.pack(fill='x', padx=14, ipady=6)
        self.var_origem.trace('w', lambda *a: self._sugerir(
            self.var_origem, self.ent_origem, self.popup_origem, 'origem'))

        # Destino
        tk.Label(p, text='Destino', bg=C_PAINEL, fg=C_SUBTEXTO,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=14, pady=(10,2))
        self.var_destino = tk.StringVar()
        self.ent_destino = tk.Entry(p, textvariable=self.var_destino,
                                    bg=C_CARD, fg=C_TEXTO, insertbackground=C_TEXTO,
                                    relief='flat', font=('Segoe UI', 10),
                                    highlightthickness=1, highlightbackground=C_BORDA,
                                    highlightcolor=C_DESTINO)
        self.ent_destino.pack(fill='x', padx=14, ipady=6)
        self.var_destino.trace('w', lambda *a: self._sugerir(
            self.var_destino, self.ent_destino, self.popup_destino, 'destino'))

        # Botões
        tk.Button(p, text='Calcular Rota', bg=C_BTN_CALC, fg='white',
                  activebackground='#2EA043', activeforeground='white',
                  relief='flat', font=('Segoe UI', 10, 'bold'),
                  cursor='hand2', command=self._calcular
                  ).pack(fill='x', padx=14, pady=(14,4), ipady=8)

        tk.Button(p, text='Limpar', bg=C_BTN_LIMPAR, fg='white',
                  activebackground='#F85149', activeforeground='white',
                  relief='flat', font=('Segoe UI', 10),
                  cursor='hand2', command=self._limpar
                  ).pack(fill='x', padx=14, ipady=6)

        self._sep(p)

        # Info do Grafo
        res = resumo_grafo(self.grafo)
        tk.Label(p, text='Info do Grafo', bg=C_PAINEL, fg=C_SUBTEXTO,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=14, pady=(8,4))
        for lbl, val in [
            ('Vértices',   str(res['vertices'])),
            ('Arestas',    str(res['arestas'])),
            ('Conectado',  'Sim' if res['conectado'] else 'Não'),
            ('Ciclos',     'Sim' if res['tem_ciclos'] else 'Não'),
            ('Grau médio', str(res['grau_medio'])),
        ]:
            card = tk.Frame(p, bg=C_CARD)
            card.pack(fill='x', padx=14, pady=2)
            tk.Label(card, text=lbl, bg=C_CARD, fg=C_SUBTEXTO,
                     font=('Segoe UI', 8)).pack(side='left', padx=8, pady=5)
            tk.Label(card, text=val, bg=C_CARD, fg=C_DESTAQUE,
                     font=('Segoe UI', 9, 'bold')).pack(side='right', padx=8)

        self._sep(p)

        # Resultado
        tk.Label(p, text='Resultado', bg=C_PAINEL, fg=C_SUBTEXTO,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=14, pady=(8,4))

        card_d = tk.Frame(p, bg=C_CARD)
        card_d.pack(fill='x', padx=14, pady=2)
        tk.Label(card_d, text='Dijkstra', bg=C_CARD, fg=C_ROTA_DIJK,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=8, pady=(5,0))
        self.lbl_dijk = tk.Label(card_d, text='—', bg=C_CARD, fg=C_TEXTO,
                                  font=('Segoe UI', 8), wraplength=260, justify='left')
        self.lbl_dijk.pack(anchor='w', padx=8, pady=(0,5))

        card_b = tk.Frame(p, bg=C_CARD)
        card_b.pack(fill='x', padx=14, pady=2)
        tk.Label(card_b, text='BFS', bg=C_CARD, fg=C_ROTA_BFS,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=8, pady=(5,0))
        self.lbl_bfs = tk.Label(card_b, text='—', bg=C_CARD, fg=C_TEXTO,
                                 font=('Segoe UI', 8), wraplength=260, justify='left')
        self.lbl_bfs.pack(anchor='w', padx=8, pady=(0,5))

        self._sep(p)

        # Legenda
        tk.Label(p, text='Legenda', bg=C_PAINEL, fg=C_SUBTEXTO,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=14, pady=(8,4))
        for cor, txt in [(C_ORIGEM,'Origem'), (C_DESTINO,'Destino'),
                         (C_ROTA_DIJK,'Dijkstra (menor km)'), (C_ROTA_BFS,'BFS (menos bairros)')]:
            row = tk.Frame(p, bg=C_PAINEL)
            row.pack(anchor='w', padx=14, pady=1)
            tk.Frame(row, bg=cor, width=10, height=10).pack(side='left', padx=(0,6))
            tk.Label(row, text=txt, bg=C_PAINEL, fg=C_TEXTO,
                     font=('Segoe UI', 8)).pack(side='left')

    def _build_mapa(self, frame):
        self.fig, self.ax = plt.subplots(facecolor=C_FUNDO)
        self.ax.set_facecolor(C_FUNDO)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(C_BORDA)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def _sep(self, p):
        tk.Frame(p, bg=C_BORDA, height=1).pack(fill='x', padx=10, pady=6)

    def _sugerir(self, var, entry, popup_ref, tipo):
        texto = var.get().strip().lower()
        if popup_ref[0]:
            popup_ref[0].destroy()
            popup_ref[0] = None
        if not texto:
            return
        matches = [b for b in self.bairros if texto in b.lower()][:7]
        if not matches:
            return

        entry.update_idletasks()
        x = entry.winfo_rootx()
        y = entry.winfo_rooty() + entry.winfo_height()
        w = entry.winfo_width()
        h = min(len(matches) * 26 + 4, 190)

        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)
        popup.geometry(f'{w}x{h}+{x}+{y}')
        popup.configure(bg=C_BORDA)
        popup_ref[0] = popup

        lb = tk.Listbox(popup, bg=C_CARD, fg=C_TEXTO,
                        selectbackground=C_DESTAQUE, selectforeground='white',
                        relief='flat', font=('Segoe UI', 9),
                        activestyle='none', bd=0, highlightthickness=0)
        lb.pack(fill='both', expand=True, padx=1, pady=1)
        for m in matches:
            lb.insert('end', '  ' + m)

        def on_select(event, pr=popup_ref, t=tipo):
            sel = lb.curselection()
            if sel:
                valor = lb.get(sel[0]).strip()
                var.set(valor)
                if pr[0]:
                    pr[0].destroy()
                    pr[0] = None
                if t == 'origem':
                    self.origem = valor if valor in self.grafo.vertices else None
                else:
                    self.destino = valor if valor in self.grafo.vertices else None
                self._desenhar_grafo()

        lb.bind('<<ListboxSelect>>', on_select)

    def _calcular(self):
        origem  = self.var_origem.get().strip()
        destino = self.var_destino.get().strip()

        if origem not in self.grafo.vertices:
            self.lbl_dijk.config(text='Origem inválida.')
            return
        if destino not in self.grafo.vertices:
            self.lbl_bfs.config(text='Destino inválido.')
            return

        self.origem  = origem
        self.destino = destino

        self.caminho_dijk, dist   = dijkstra(self.grafo, origem, destino)
        self.caminho_bfs,  saltos = bfs(self.grafo, origem, destino)

        if self.caminho_dijk:
            rota = ' → '.join(self.caminho_dijk)
            self.lbl_dijk.config(text=f'{rota}\n{dist} km | {len(self.caminho_dijk)-1} salto(s)')
        else:
            self.lbl_dijk.config(text='Sem caminho encontrado.')

        if self.caminho_bfs:
            rota = ' → '.join(self.caminho_bfs)
            self.lbl_bfs.config(text=f'{rota}\n{saltos} salto(s)')
        else:
            self.lbl_bfs.config(text='Sem caminho encontrado.')

        self._desenhar_grafo(self.caminho_dijk, self.caminho_bfs)

    def _limpar(self):
        self.origem  = None
        self.destino = None
        self.caminho_dijk = None
        self.caminho_bfs  = None
        self.var_origem.set('')
        self.var_destino.set('')
        self.lbl_dijk.config(text='—')
        self.lbl_bfs.config(text='—')
        self._desenhar_grafo()

    def _desenhar_grafo(self, caminho_dijk=None, caminho_bfs=None):
        self.ax.cla()
        self.ax.set_facecolor(C_FUNDO)
        self.ax.set_title('Malha Viária — Fortaleza, CE', color=C_TEXTO, fontsize=12, pad=10)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(C_BORDA)

        coords = self.grafo.coords
        adj    = self.grafo.adj

        def xy(n):
            lat, lon = coords[n]
            return lon, lat

        desenhadas = set()
        for a, vizinhos in adj.items():
            for b, _ in vizinhos:
                ch = tuple(sorted([a, b]))
                if ch in desenhadas:
                    continue
                desenhadas.add(ch)
                xa, ya = xy(a); xb, yb = xy(b)
                self.ax.plot([xa, xb], [ya, yb], color=C_ARESTA, lw=0.8, alpha=0.5, zorder=1)

        if caminho_bfs and len(caminho_bfs) > 1:
            for i in range(len(caminho_bfs) - 1):
                xa, ya = xy(caminho_bfs[i]); xb, yb = xy(caminho_bfs[i+1])
                self.ax.plot([xa, xb], [ya, yb], color=C_ROTA_BFS, lw=3,
                              alpha=0.75, zorder=3, linestyle='--',
                              path_effects=[pe.Stroke(linewidth=5, foreground='#1a5c3a', alpha=0.3), pe.Normal()])

        if caminho_dijk and len(caminho_dijk) > 1:
            for i in range(len(caminho_dijk) - 1):
                xa, ya = xy(caminho_dijk[i]); xb, yb = xy(caminho_dijk[i+1])
                self.ax.plot([xa, xb], [ya, yb], color=C_ROTA_DIJK, lw=3.5,
                              alpha=0.95, zorder=4,
                              path_effects=[pe.Stroke(linewidth=6, foreground='#6b4200', alpha=0.4), pe.Normal()])

        graus    = dict(analise_grau(self.grafo))
        max_grau = max(graus.values())

        for nome in self.grafo.vertices:
            x, y = xy(nome)
            r    = 3 + 5 * (graus[nome] / max_grau)

            if nome == self.origem:
                cor, zo, r, ec = C_ORIGEM, 7, 14, 'white'
            elif nome == self.destino:
                cor, zo, r, ec = C_DESTINO, 7, 14, 'white'
            elif caminho_dijk and nome in caminho_dijk:
                cor, zo, ec = C_ROTA_DIJK, 5, C_FUNDO
            elif caminho_bfs and nome in caminho_bfs:
                cor, zo, ec = C_ROTA_BFS, 5, C_FUNDO
            else:
                cor, zo, ec = C_VERTICE, 2, C_FUNDO

            self.ax.scatter(x, y, s=r**2, c=cor, zorder=zo,
                             edgecolors=ec, linewidths=0.8, alpha=0.9)

            if nome in [self.origem, self.destino] or \
               (caminho_dijk and nome in caminho_dijk):
                self.ax.annotate(nome, (x, y),
                                  textcoords='offset points', xytext=(5, 5),
                                  fontsize=7, color=C_TEXTO, zorder=8,
                                  fontfamily='monospace',
                                  bbox=dict(boxstyle='round,pad=0.3', fc='#161B22',
                                            ec=C_BORDA, alpha=0.85, lw=0.8))

        self.ax.tick_params(colors='#444', labelsize=7)
        self.ax.set_xlabel('Longitude', color='#444', fontsize=7)
        self.ax.set_ylabel('Latitude',  color='#444', fontsize=7)
        self.canvas.draw()


def iniciar():
    App()