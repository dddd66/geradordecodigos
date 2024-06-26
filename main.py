from pymediainfo import MediaInfo
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.bind_mouse_wheel()

    def bind_mouse_wheel(self) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)  # For Linux
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)  # For Linux

    def _on_mouse_wheel(self, event) -> None:
        if event.num == 4:  # Para linux
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Para linux
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class App:
    def __init__(self, win) -> None:
        self.window = win
        self.window.title("Gerador de Códigos")
        self.window.geometry("936x753")

        # Criando o frame scrollavel
        self.scrollable_frame = ScrollableFrame(self.window)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Frame que vai conter os widgets
        self.frame = tk.Frame(self.scrollable_frame.scrollable_frame)
        self.frame.pack(fill="both", expand=True)

        self.criar_widgets()

    def criar_widgets(self) -> None:
        self.topo = tk.LabelFrame(self.frame, text="Informações sobre o filme", padx=10, pady=10)
        self.topo.grid(row=0, column=0, sticky="ew")

        # Criando frame
        button_frame = tk.Frame(self.frame)
        button_frame.grid(row=3, column=0, padx=0, pady=0, sticky="ew")

        # Botões dentro do frame
        button = tk.Button(button_frame, text="Gerar Código", command=self.processar_input)
        button.grid(row=0, column=0, padx=5, pady=5)
        limpar = tk.Button(button_frame, text="Limpar Campos", command=self.limpar)
        limpar.grid(row=0, column=1, padx=5, pady=5)

        # Garantir que os botões continuem centralizados adicionando pesos de coluna
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Seções
        self.create_movie_info_section()
        self.criar_widget_releases()
        self.criar_widget_screenshots()
        self.criar_widget_info_adicional()

        # Garantir que o frame redimensiona corretamente
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)

    def create_movie_info_section(self):
        self.titulo_brasil_label = tk.Label(self.topo, text="Título no Brasil:", fg="red", padx=2, pady=2)
        self.titulo_brasil_label.grid(row=0, column=0, sticky="e")
        self.titulo_brasil_entry = tk.Entry(self.topo)
        self.titulo_brasil_entry.grid(row=0, column=1, columnspan=4, sticky="ew")

        self.titulo_original_label = tk.Label(self.topo, text="Título Original:", fg="red")
        self.titulo_original_label.grid(row=1, column=0, sticky="e")
        self.titulo_original_entry = tk.Entry(self.topo)
        self.titulo_original_entry.grid(row=1, column=1, columnspan=4, sticky="ew")

        self.sinopse_label = tk.Label(self.topo, text="Sinopse:", fg="red")
        self.sinopse_label.grid(row=2, column=0, sticky="e")
        self.sinopse_entry = tk.Text(self.topo, height=4, wrap="word", width=40)
        self.sinopse_entry.grid(row=2, column=1, columnspan=4, sticky="ew")
        sinopse_scroll = tk.Scrollbar(self.topo, command=self.sinopse_entry.yview)
        sinopse_scroll.grid(row=2, column=5, sticky='nsew')
        self.sinopse_entry.config(yscrollcommand=sinopse_scroll.set)

        self.elenco_label = tk.Label(self.topo, text="Elenco:")
        self.elenco_label.grid(row=3, column=0, sticky="e")
        self.elenco_entry = tk.Text(self.topo, height=4, wrap="word", width=40)
        self.elenco_entry.grid(row=3, column=1, columnspan=4, sticky="ew")
        elenco_scroll = tk.Scrollbar(self.topo, command=self.elenco_entry.yview)
        elenco_scroll.grid(row=3, column=5, sticky='nsew')
        self.elenco_entry.config(yscrollcommand=elenco_scroll.set)

        self.pais_de_origem_label = tk.Label(self.topo, text="País de Origem:", fg="red")
        self.pais_de_origem_label.grid(row=4, column=0, sticky="e")
        self.pais_de_origem_entry = tk.Entry(self.topo)
        self.pais_de_origem_entry.grid(row=4, column=1, columnspan=1, sticky="ew")

        self.diretor_label = tk.Label(self.topo, text="Diretor:", fg="red")
        self.diretor_label.grid(row=4, column=2, sticky="e")
        self.diretor_entry = tk.Entry(self.topo)
        self.diretor_entry.grid(row=4, column=3, columnspan=2, sticky="ew")

        self.genero_label = tk.Label(self.topo, text="Gênero:", fg="red")
        self.genero_label.grid(row=5, column=0, sticky="e")
        self.genero_entry = tk.Entry(self.topo)
        self.genero_entry.grid(row=5, column=1, columnspan=1, sticky="ew")

        self.duracao_label = tk.Label(self.topo, text="Duração:", fg="red")
        self.duracao_label.grid(row=5, column=2, sticky="e")
        self.duracao_entry = tk.Entry(self.topo)
        self.duracao_entry.grid(row=5, column=3, sticky="w")

        self.duracao_minutos = tk.Label(self.topo, text="minutos")
        self.duracao_minutos.grid(row=5, column=4, sticky="w")

        self.idioma_do_audio_label = tk.Label(self.topo, text="Idioma do Áudio:", fg="red")
        self.idioma_do_audio_label.grid(row=6, column=0, sticky="e")
        self.idioma_do_audio_entry = tk.Entry(self.topo, width=6)
        self.idioma_do_audio_entry.grid(row=6, column=1, sticky="ew")

        self.ano_label = tk.Label(self.topo, text="Ano:", fg="red")
        self.ano_label.grid(row=6, column=2, sticky="e")
        self.ano_entry = tk.Entry(self.topo)
        self.ano_entry.grid(row=6, column=3, sticky="ew")

        self.imdb_label = tk.Label(self.topo, text="IMDB:", fg="red")
        self.imdb_label.grid(row=7, column=0, sticky="ew")
        self.imdb_entry = tk.Entry(self.topo)
        self.imdb_entry.grid(row=7, column=1, columnspan=4, sticky="ew")

    def criar_widget_releases(self) -> None:
        self.release = tk.LabelFrame(self.frame, text="Informações sobre o release", padx=5, pady=5)
        self.release.grid(row=1, column=0, padx=0, pady=0, sticky="news")

        padding = {'padx': 2, 'pady': 2}

        self.file_path_entry = tk.Entry(self.release)
        self.file_path_entry.grid(row=0, column=1, columnspan=3, **padding, sticky="ew")

        self.pick_file_button = tk.Button(self.release, text="Escolher arquivo", command=self.pick_file)
        self.pick_file_button.grid(row=0, column=0, **padding, sticky="ew")

        self.qualidade_label = tk.Label(self.release, text="Qualidade:", fg="red")
        self.qualidade_label.grid(row=1, column=0, sticky="e", **padding)
        self.qualidade_combobox = ttk.Combobox(self.release,
                                               values=["Blu-Ray Full", "BDRemux", "BDRip", "DVD Full", "DVDRip",
                                                       "HDTVRip", "TVRip", "VHSRip", "WEB-DL", "WEBRip", "Outro"])
        self.qualidade_combobox.grid(row=1, column=1, columnspan=3, sticky="ew", **padding)

        self.videocodec_label = tk.Label(self.release, text="Video Codec:", fg="red")
        self.videocodec_label.grid(row=2, column=0, sticky="e", **padding)
        self.videocodec_entry = tk.Entry(self.release)
        self.videocodec_entry.grid(row=2, column=1, columnspan=3, sticky="ew", **padding)

        self.videobitrate_label = tk.Label(self.release, text="Video Bitrate:", fg="red")
        self.videobitrate_label.grid(row=3, column=0, sticky="e", **padding)
        self.videobitrate_entry = tk.Entry(self.release)
        self.videobitrate_entry.grid(row=3, column=1, columnspan=3, sticky="ew", **padding)

        self.audiocodec_label = tk.Label(self.release, text="Áudio Codec:", fg="red")
        self.audiocodec_label.grid(row=4, column=0, sticky="e", **padding)
        self.audiocodec_entry = tk.Entry(self.release)
        self.audiocodec_entry.grid(row=4, column=1, columnspan=3, sticky="ew", **padding)

        self.audiobitrate_label = tk.Label(self.release, text="Áudio Bitrate:", fg="red")
        self.audiobitrate_label.grid(row=5, column=0, sticky="e", **padding)
        self.audiobitrate_entry = tk.Entry(self.release)
        self.audiobitrate_entry.grid(row=5, column=1, columnspan=3, sticky="ew", **padding)

        self.container_label = tk.Label(self.release, text="Container:", fg="red")
        self.container_label.grid(row=6, column=0, sticky="e", **padding)
        self.container_combobox = ttk.Combobox(self.release, values=["MKV", "AVI"])
        self.container_combobox.grid(row=6, column=1, columnspan=3, sticky="ew", **padding)

        self.resolucao_label = tk.Label(self.release, text="Resolução:", fg="red")
        self.resolucao_label.grid(row=7, column=0, sticky="e", **padding)
        self.resolucao_entry = tk.Entry(self.release)
        self.resolucao_entry.grid(row=7, column=1, columnspan=3, sticky="ew", **padding)

        self.aspectratio_label = tk.Label(self.release, text="Formato da Tela:", fg="red")
        self.aspectratio_label.grid(row=8, column=0, sticky="e", **padding)
        self.aspectratio_entry = tk.Entry(self.release)
        self.aspectratio_entry.grid(row=8, column=1, columnspan=3, sticky="ew", **padding)

        self.framerate_label = tk.Label(self.release, text="Frame Rate:", fg="red")
        self.framerate_label.grid(row=9, column=0, sticky="e", **padding)
        self.framerate_entry = tk.Entry(self.release)
        self.framerate_entry.grid(row=9, column=1, columnspan=3, sticky="ew", **padding)

        self.tamanho_label = tk.Label(self.release, text="Tamanho:", fg="red")
        self.tamanho_label.grid(row=10, column=0, sticky="e", **padding)
        self.tamanho_entry = tk.Entry(self.release)
        self.tamanho_entry.grid(row=10, column=1, columnspan=3, sticky="ew", **padding)

        self.legendas_label = tk.Label(self.release, text="Legendas:", fg="red")
        self.legendas_label.grid(row=11, column=0, sticky="e", **padding)
        self.legendas_combobox = ttk.Combobox(self.release, values=["Anexas", "Fixas", "Sem legenda", "No torrent"])
        self.legendas_combobox.grid(row=11, column=1, columnspan=3, sticky="ew", **padding)

        self.release_label = tk.Label(self.release, text="Release:", fg="red")
        self.release_label.grid(row=12, column=0, sticky="e", **padding)
        self.release_entry = tk.Entry(self.release)
        self.release_entry.grid(row=12, column=1, columnspan=3, sticky="ew", **padding)

        for i in range(13):
            self.release.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.release.grid_columnconfigure(j, weight=1)

    def colar_screens(self, event) -> str | None:
        try:
            clipboard_content = self.frame.clipboard_get()
        except tk.TclError:
            clipboard_content = ""

        # Limpar conteúdo do teclado antes de colar
        urls = clipboard_content.replace(" ", "")
        urls = urls.split("\n")
        urls = [url for url in urls if len(url) > 2]

        # Se não for um tamanho válido para preenchimento

        if len(urls) not in (1, 4, 5, 6, 7, 8, 9):
            return None

        # Limpar o field que chamou, pra não ficar todo o conteúdo colado nesse field.
        event.widget.delete(0, tk.END)

        # Coloca as URLs em cada entry
        for entry, url in zip(self.screenshot_entries, urls):
            entry.delete(0, tk.END)
            entry.insert(0, url)

        return "break"  # Se der errado, apenas colar no field selecionado

    def criar_widget_screenshots(self) -> None:
        padding = {'padx': 2, 'pady': 2}
        self.baixo = tk.LabelFrame(self.frame, text="Screens", padx=5, pady=5)
        self.baixo.grid(row=0, column=3, padx=0, pady=0, sticky="news")

        self.poster_label = tk.Label(self.baixo, text="Poster:", fg="red")
        self.poster_label.grid(row=0, column=0, sticky="w", **padding)

        self.poster_entry = tk.Entry(self.baixo)
        self.poster_entry.grid(row=0, column=1, sticky="w", **padding)

        self.screenshot_labels = []
        self.screenshot_entries = []
        for i in range(8):
            fg_color = "red" if i < 4 else "black"
            label = tk.Label(self.baixo, text=f"Screenshot {i + 1}:", fg=fg_color)
            label.grid(row=i + 1, column=0, sticky="w", **padding)
            entry = tk.Entry(self.baixo)
            entry.grid(row=i + 1, column=1, sticky="w", **padding)
            self.screenshot_labels.append(label)
            self.screenshot_entries.append(entry)
        self.screenshot_entries[0].bind('<Control-v>', self.colar_screens)

    def criar_widget_info_adicional(self) -> None:
        self.dir = tk.LabelFrame(self.frame, text="Informações Adicionais")
        self.dir.grid(row=1, column=3, padx=0, pady=0, sticky="news")

        self.premiacoes_label = tk.Label(self.dir, text="Premiações:")
        self.premiacoes_label.grid(row=0, column=0, sticky="nsew")
        self.premiacoes_entry = tk.Text(self.dir, height=4, wrap="word", width=40)
        self.premiacoes_entry.grid(row=0, column=1, columnspan=4, sticky="ew")
        premiacoes_scroll = tk.Scrollbar(self.dir, command=self.premiacoes_entry.yview)
        premiacoes_scroll.grid(row=0, column=5, sticky='nsew')
        self.premiacoes_entry.config(yscrollcommand=premiacoes_scroll.set)

        self.curiosidade_label = tk.Label(self.dir, text="Curiosidade:")
        self.curiosidade_label.grid(row=1, column=0, sticky="nsew")
        self.curiosidade_entry = tk.Text(self.dir, height=4, wrap="word", width=40)
        self.curiosidade_entry.grid(row=1, column=1, columnspan=4, sticky="ew")
        curiosidade_scroll = tk.Scrollbar(self.dir, command=self.curiosidade_entry.yview)
        curiosidade_scroll.grid(row=1, column=5, sticky='nsew')
        self.curiosidade_entry.config(yscrollcommand=curiosidade_scroll.set)

        self.critica_label = tk.Label(self.dir, text="Crítica:")
        self.critica_label.grid(row=2, column=0, sticky="nsew")
        self.critica_entry = tk.Text(self.dir, height=4, wrap="word", width=40)
        self.critica_entry.grid(row=2, column=1, columnspan=4, sticky="ew")
        critica_scroll = tk.Scrollbar(self.dir, command=self.critica_entry.yview)
        critica_scroll.grid(row=2, column=5, sticky='nsew')
        self.critica_entry.config(yscrollcommand=critica_scroll.set)

    def limpar(self) -> None:
        entry_widgets = [
            self.titulo_brasil_entry,
            self.titulo_original_entry,
            self.sinopse_entry,
            self.elenco_entry,
            self.pais_de_origem_entry,
            self.diretor_entry,
            self.genero_entry,
            self.qualidade_combobox,
            self.duracao_entry,
            self.imdb_entry,
            self.idioma_do_audio_entry,
            self.videocodec_entry,
            self.videobitrate_entry,
            self.audiocodec_entry,
            self.audiobitrate_entry,
            self.legendas_combobox,
            self.container_combobox,
            self.resolucao_entry,
            self.aspectratio_entry,
            self.framerate_entry,
            self.tamanho_entry,
            self.poster_entry,
            self.release_entry,
            self.premiacoes_entry,
            self.curiosidade_entry,
            self.critica_entry
        ]
        for widget in entry_widgets:
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)
        for entry in self.screenshot_entries:
            entry.delete(0, tk.END)
        self.qualidade_combobox.set('')
        self.container_combobox.set('')
        self.legendas_combobox.set('')

    def processar_input(self) -> None:
        fields_necessarios = [
            self.titulo_brasil_entry,
            self.titulo_original_entry,
            self.sinopse_entry,
            self.pais_de_origem_entry,
            self.diretor_entry,
            self.genero_entry,
            self.duracao_entry,
            self.idioma_do_audio_entry,
            self.ano_entry,
            self.imdb_entry,
            self.qualidade_combobox,
            self.videocodec_entry,
            self.videobitrate_entry,
            self.audiocodec_entry,
            self.audiobitrate_entry,
            self.container_combobox,
            self.resolucao_entry,
            self.aspectratio_entry,
            self.framerate_entry,
            self.tamanho_entry,
            self.legendas_combobox,
            self.release_entry
        ]

        for field in fields_necessarios:
            if isinstance(field, tk.Text):
                if not field.get("1.0", "end-1c").strip():
                    messagebox.showwarning("Atenção", "Todos os campos em vermelho precisam ser preenchidos.")
                    return
            elif isinstance(field, ttk.Combobox):
                if not field.get().strip():
                    messagebox.showwarning("Atenção", "Todos os campos em vermelho precisam ser preenchidos.")
                    return
            else:
                if not field.get().strip():
                    messagebox.showwarning("Atenção", "Todos os campos em vermelho precisam ser preenchidos.")
                    return

        screenshot_count = sum(1 for entry in self.screenshot_entries if entry.get())
        if screenshot_count < 4 or screenshot_count not in [4, 6, 8]:
            messagebox.showwarning("Atenção", "Pelo menos 4 campos de screenshot precisam ser preenchidos.")
            return

        data_valores = {}
        entries = [
            (self.titulo_brasil_entry, "titulonobrasil"),
            (self.titulo_original_entry, "titulooriginal"),
            (self.sinopse_entry, "sinopse"),
            (self.elenco_entry, "elenco"),
            (self.pais_de_origem_entry, "paisdeorigem"),
            (self.diretor_entry, "diretor"),
            (self.genero_entry, "genero"),
            (self.qualidade_combobox, "qualidade"),
            (self.duracao_entry, "duracao"),
            (self.imdb_entry, "imdb"),
            (self.idioma_do_audio_entry, "idiomadoaudio"),
            (self.ano_entry, "ano"),
            (self.videocodec_entry, "videocodec"),
            (self.videobitrate_entry, "videobitrate"),
            (self.audiocodec_entry, "audiocodec"),
            (self.audiobitrate_entry, "audiobitrate"),
            (self.legendas_combobox, "legenda"),
            (self.container_combobox, "container"),
            (self.resolucao_entry, "resolucao"),
            (self.aspectratio_entry, "formatodatela"),
            (self.framerate_entry, "framerate"),
            (self.tamanho_entry, "tamanho"),
            (self.poster_entry, "poster"),
            (self.release_entry, "release"),
            (self.premiacoes_entry, "premiacoes"),
            (self.curiosidade_entry, "curiosidade"),
            (self.critica_entry, "critica")
        ]
        if 'screenshots' not in data_valores:
            data_valores['screenshots'] = []

        for entry in self.screenshot_entries:
            if entry.get():
                data_valores["screenshots"].append(entry.get())

        for widget, key in entries:
            if isinstance(widget, tk.Text):
                data_valores[key] = widget.get("1.0", "end-1c")
            elif isinstance(widget, ttk.Combobox):
                data_valores[key] = widget.get()
            else:
                data_valores[key] = widget.get()

        output_window = tk.Toplevel(self.window)
        output_window.title("Código")

        output_text_widget = tk.Text(output_window, wrap="word", height=20, width=60)
        output_text_widget.insert(tk.END, self.gerar_codigo(data_valores))
        output_text_widget.pack(fill="both", expand=True)

        copy_button = tk.Button(output_window, text="Copiar",
                                command=lambda: self.copiar_para_teclado(output_text_widget))

        copy_button.pack(anchor="s", expand=True, ipadx=5, ipady=5)

    def copiar_para_teclado(self, widget) -> None:
        self.window.clipboard_clear()
        self.window.clipboard_append(widget.get("1.0", tk.END))

    @staticmethod
    def gerar_codigo(data: dict) -> str:
        titulonobrasil = data["titulonobrasil"].strip("\n")
        titulooriginal = data["titulooriginal"].strip("\n")
        release = data["release"].strip("\n")
        imdb = re.sub(r"(\d+)/.*", r"\1", data['imdb'])
        codigo = f"""[tablePrinc][tr][titMasc]Título do Filme[/titMasc][/tr][tr][titTrad]{titulonobrasil}[/titTrad]\
[titOri]{titulooriginal}[/titOri][release]{release}[/release][/tr][tr][posterMasc]Poster[/posterMasc]\
[sinopseMasc]Sinopse[/sinopseMasc][/tr][tr][poster][posterIma]{data["poster"]}[/posterIma][/poster]\
[sinopse]{data["sinopse"]}[/sinopse][tableScreen]Screenshots[/tableScreen]"""

        screenshots = data.get('screenshots', [])
        num_screens = len(screenshots)
        if num_screens in {4, 6, 8}:
            for i in range(num_screens):
                if i % 2 == 0:
                    if i != 0:
                        codigo += '[/tr]'  # Fechar a linha anterior
                    codigo += '[tr]'  # Começar uma nova coluna para cada par de screenshots
                side = 'screenLeft' if i % 2 == 0 else 'screenRight'
                codigo += f'[{side}][screenIma]{screenshots[i]}[/screenIma][/{side}]'
            codigo += '[/tr]'  # Fechar a última linha de screenshots

        codigo += f"""[closeTab][/closeTab][/tr][/tablePrinc][tablePrinc][tr][posterMasc]Elenco[/posterMasc]\
[infoMasc]Informações sobre o filme[/infoMasc][infoMasc]Informações sobre o release[/infoMasc][/tr][tr]\
[elenco]{data["elenco"]}[/elenco][info][b]Gênero: [/b]{data["genero"]}
[b]Diretor: [/b]{data["diretor"]}
[b]Duração: [/b]{data["duracao"]} minutos
[b]Ano de Lançamento: [/b]{data["ano"]}
[b]País de Origem: [/b]{data["paisdeorigem"]}
[b]Idioma do Áudio: [/b]{data["idiomadoaudio"]}
[b]IMDB: [/b][url={imdb}]{imdb}[/url]
[/info][info][b]Qualidade de Vídeo: [/b]{data['qualidade']}
[b]Container: [/b]{data['container']}
[b]Vídeo Codec: [/b]{data['videocodec']}
[b]Vídeo Bitrate: [/b]{data['videobitrate']}
[b]Áudio Codec: [/b]{data['audiocodec']}
[b]Áudio Bitrate: [/b]{data['audiobitrate']}
[b]Resolução: [/b]{data['resolucao']}
[b]Formato de Tela: [/b]{data['formatodatela']}
[b]Frame Rate: [/b]{data['framerate']} FPS
[b]Tamanho: [/b]{data['tamanho']}
[b]Legendas: [/b]{data['legenda']}[/info][/tr]"""

        if data.get('premiacoes'):
            codigo += f"[tr][infoExtraMasc]Premiações[/infoExtraMasc][/tr][tr][infoExtra]{data['premiacoes']}\
[/infoExtra][/tr]\n"
        if data.get('curiosidade'):
            codigo += f"[tr][infoExtraMasc]Curiosidades[/infoExtraMasc][/tr][tr][infoExtra]{data['curiosidade']}\
[/infoExtra][/tr]\n"
        if data.get('critica'):
            codigo += f"[tr][infoExtraMasc]Crítica[/infoExtraMasc][/tr][tr][infoExtra]{data['critica']}[/infoExtra]\
[/tr]\n"
        codigo += "[tr][rodape]Coopere, deixe semeando ao menos duas vezes o tamanho do arquivo que baixar.[/rodape]\
[/tr][/tablePrinc]"
        return codigo

    def pick_file(self) -> None:
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("Video Files", "*.mkv *.avi"), ("All files", "*.*")))
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
        mi = self.extrair_metadata(file_path)

        self.videocodec_entry.delete(0, tk.END)
        self.videobitrate_entry.delete(0, tk.END)
        self.audiocodec_entry.delete(0, tk.END)
        self.audiobitrate_entry.delete(0, tk.END)
        self.resolucao_entry.delete(0, tk.END)
        self.aspectratio_entry.delete(0, tk.END)
        self.tamanho_entry.delete(0, tk.END)
        self.resolucao_entry.delete(0, tk.END)
        self.framerate_entry.delete(0, tk.END)
        self.release_entry.delete(0, tk.END)

        self.videocodec_entry.insert(0, mi['vcodec'])
        self.videobitrate_entry.insert(0, mi["vbitrate"])
        self.audiocodec_entry.insert(0, mi["acodec"])
        self.audiobitrate_entry.insert(0, mi["abitrate"])
        self.tamanho_entry.insert(0, mi["tamanho"])
        self.aspectratio_entry.insert(0, mi["aspectratio"])
        self.resolucao_entry.insert(0, mi["resolucao"])
        self.framerate_entry.insert(0, mi["fps"])
        self.release_entry.insert(0, mi["release"])

        if mi["ext"] == "mkv":
            self.container_combobox.current(0)
        else:
            self.container_combobox.current(1)

    @staticmethod
    def bitrate_format(bitrate: list) -> str:
        bstring = str(bitrate[0])
        bstring = bstring.replace(' ', '')
        kindex = bstring.index("k")
        return bstring[:kindex] + " " + bstring[kindex:]

    @staticmethod
    def substituir_codec(tracks, codec) -> str:
        codec_map = {"AVC": "h264",
                     "XVID": "XviD"}
        if codec == "MPEG Audio":
            if tracks[2]["format_profile"] == "Layer 3":
                return "MP3"
            elif tracks[2]["format_profile"] == "Layer 2":
                return "MP2"
            else:
                return "MP1"
        return codec_map.get(codec, codec)

    @staticmethod
    def to_gb(byt: int) -> float:
        return byt / 1073741824

    def extrair_metadata(self, caminho: str) -> dict:
        video = MediaInfo.parse(caminho).to_data()
        tracks = video.get("tracks")
        metadata = {"vcodec": self.substituir_codec(tracks, tracks[0].get("codecs_video", "")),
                    "acodec": self.substituir_codec(tracks, tracks[0].get("audio_codecs", "")),
                    "vbitrate": self.bitrate_format(tracks[1].get("other_bit_rate", "")),
                    "abitrate": self.bitrate_format(tracks[2].get("other_bit_rate", "")),
                    "resolucao": f'{tracks[1].get("sampled_width", "")} x {tracks[1].get("sampled_height", "")}',
                    "aspectratio": tracks[1].get("other_display_aspect_ratio", ""),
                    "fps": tracks[1].get("frame_rate", ""),
                    "tamanho": "{:.2f} GB".format(self.to_gb(int(tracks[0].get("file_size", "")))),
                    "release": os.path.basename(tracks[0].get("file_name", "")),
                    "ext": tracks[0].get("file_extension", "")
                    }
        return metadata


if __name__ == "__main__":
    window = tk.Tk()
    window.iconbitmap('resources/icon.ico')
    App(window)
    window.mainloop()  # loop
