from tools.a7s_model import *

import ipywidgets as widgets
#import wmi  # to kill AD
from PyQt5.QtWidgets import QFileDialog, QApplication

# try:
#     from tkinter import Tk
#     from tkFileDialog import askopenfilenames
# except:
#     from tkinter import Tk
#     from tkinter import filedialog

# simplified replacement for gettext
i18n = {
    "Open Savegame": {
        "german": "Spielstand öffnen"
    },
    "Anno 1800 Savegames (*.a7s)": {
        "german": "Anno 1800 Speicherstände (*.a7s)"
    },
    "Open in Anno Designer": {
        "german": "In Anno Designer öffnen"
    },
    "Island": {
        "chinese": "岛屿",
        "english": "Island",
        "french": "Île",
        "german": "Insel",
        # "guid": 151271,
        "italian": "Isola",
        "japanese": "島",
        "korean": "섬",
        "polish": "Wyspa",
        "russian": "Остров",
        "spanish": "Isla",
        "taiwanese": "島嶼"
    },
    "Status": {
        "chinese": "状态",
        "english": "State",
        "french": "État",
        "german": "Status",
        # "guid": 23143,
        "italian": "Stato",
        "japanese": "状態",
        "korean": "상태",
        "polish": "Stan",
        "russian": "Состояние",
        "spanish": "Estado",
        "taiwanese": "狀態"
    },
    "Colors": {
        "german": "Farben"
    },
    "Icons": {
        "german": "Icons"
    },
    "Labels": {
        "german": "Beschriftungen"
    },
    "Farms and modules identical": {
        "german": "Farmen und Module identisch"
    },
    "Vary Farms": {
        "german": "Farmen variieren"
    },
    "Coverage by stores": {
        "german": "Abdeckung durch Geschäfte"
    },
    "Hide for farm modules of size 1x1": {
        "german": "Ausblenden bei Farmfeldern der Größe 1x1"
    },
    "Hide for ornaments of size 1x1": {
        "german": "Ausblenden bei Ornamenten der Größe 1x1"
    },
    "Random": {
        "chinese": "随机",
        "english": "Random",
        "french": "Aléatoire",
        "german": "Zufällig",
        # "guid": 16102,
        "italian": "Casuale",
        "japanese": "ランダム",
        "korean": "무작위",
        "polish": "Losowy",
        "russian": "Случайн.",
        "spanish": "Aleatorio",
        "taiwanese": "隨機"
    },
    "Residents": {
        "chinese": "居民",
        "english": "Residents",
        "french": "Résidents",
        "german": "Einwohner",
        # "guid": 22379,
        "italian": "Residenti",
        "japanese": "住民",
        "korean": "주민",
        "polish": "Mieszkańcy",
        "russian": "Жители",
        "spanish": "Residentes",
        "taiwanese": "居民"
    },
    "No. of Modules": {
        "chinese": "可耕农地数量",
        "english": "No. of Modules",
        "french": "Nombre de modules",
        "german": "Anzahl Module",
        # "guid": 12075,
        "italian": "N. di moduli",
        "japanese": "モジュールの数",
        "korean": "모듈 수",
        "polish": "Liczba modułów",
        "russian": "Кол-во модулей",
        "spanish": "Número de módulos",
        "taiwanese": "可耕農地數量"
    },
    "Items Equipped": {
        "chinese": "已装备物品",
        "english": "Items Equipped",
        "french": "Objets en stock",
        "german": "Ausgerüstete Items",
        # "guid": 9987,
        "italian": "Oggetti in uso",
        "japanese": "装備したアイテム",
        "korean": "배치한 아이템",
        "polish": "Przedmioty w użyciu",
        "russian": "Используемые предметы",
        "spanish": "Objetos equipados",
        "taiwanese": "已裝備物品"
    },
    "Buffs": {
        "german": "Buffs"
    },
    "Productivity": {
        "chinese": "生产力",
        "english": "Productivity",
        "french": "Productivité",
        "german": "Produktivität",
        # "guid": 100370,
        "italian": "Produttività",
        "japanese": "生産性",
        "korean": "생산성",
        "polish": "Wydajność",
        "russian": "Производительность",
        "spanish": "Productividad",
        "taiwanese": "生產力"
    },
    "GUID of the asset": {
        "german": "GUID des Assets"
    },
    "Object ID": {
        "german": "Objekt-ID"
    },
    "Ready": {
        "chinese": "准备就绪",
        "english": "Ready",
        "french": "Prêt",
        "german": "Bereit",
        # "guid": 11625,
        "italian": "Pronto",
        "japanese": "準備完了",
        "korean": "준비",
        "polish": "Gotowy",
        "russian": "Готов(а)",
        "spanish": "Preparado",
        "taiwanese": "準備就緒"
    },
    "Opening": {
        "chinese": "开启",
        "english": "Open",
        "french": "Ouvrir",
        "german": "Öffnen",
        # "guid": 145017,
        "italian": "Apri",
        "japanese": "開く",
        "korean": "열기",
        "polish": "Otwarte",
        "russian": "Открыть",
        "spanish": "Abrir",
        "taiwanese": "開啟"
    },
    "Failed to read file: ": {
        "german": "Datei konnte nicht gelesen werden: "
    },
    "Failed to generate preview: ": {
        "german": "Erstellen der Vorschau fehlgeschlagen: "
    },
    "Updating preview ...": {
        "german": "Vorschau aktualisieren ..."
    },
    "Preview updated": {
        "german": "Vorschau aktualisiert"
    },
    "Failed to save ": {
        "german": "Datei konnte nicht gespeichert werden: "
    },
    "Failed to open Anno Designer. File was saved to: ": {
        "german": "Anno Designer konnte nicht geöffnet werden. Pfad zur Datei: "
    }
}


def _(msg):
    if msg in i18n and LANG in i18n[msg]:
        return i18n[msg][LANG]

    return msg


class Option:
    def __init__(self, identifier, description, init_set=False):
        self.identifier = identifier
        self.description = description
        self.init_set = init_set
        self.widget = None

    def render(self):
        self.widget = widgets.Checkbox(value=self.init_set, description=self.description)
        self.widget.layout.width="30rem"
        return self.widget

    def enabled(self):
        return self.widget.value


class Group:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name
        self.options = []
        self.widget = None

    def add_option(self, option):
        self.options.append(option)

    def render(self):
        self.widget = widgets.GridBox([o.render() for o in self.options],
                                      layout=widgets.Layout(grid_template_columns="repeat(3, 35rem)"))
        return self.widget

    def get_options(self):
        return [o.identifier for o in self.options if o.enabled()]


class VisualizerGUI:
    def __init__(self):
        self.world = None
        self.ordered_sessions = None

        self.island_selector = None
        self.groups = []
        self.img_preview = None
        self.img_preview_id = None
        self.txt_status = None
        self.vertical_margins = "0 0 1rem 0"
        self.horizontal_margins = "0 2rem 0 0"

        btn_ok = widgets.Button(description=_("OK"),
                                disabled=False)
        self.model = widgets.VBox([btn_ok])



        def callback(btn):
            global LANG
            LANG = lang_widget.value
            self.show()

        btn_ok.on_click(callback)

    def set_status(self, txt: str):
        if self.txt_status is None:
            print(txt)
        else:
            self.txt_status.value = txt

    def compose_header(self):
        def callback(btn):
            self.select_file()

        def hide(elem):
            elem.layout.display = "none"

        btn_file_chooser = widgets.Button(description=_("Open Savegame"),
                                          disabled=False)
        btn_file_chooser.on_click(callback)
        btn_file_chooser.layout.margin = self.horizontal_margins

        self.progress_decoding = widgets.FloatProgress(value=0.01, min=0, max=1)
        hide(self.progress_decoding)

        self.label_filename = widgets.Label()
        hide(self.label_filename)

        return widgets.HBox([
            btn_file_chooser,
            self.label_filename,
            self.progress_decoding,
        ])

    def compose_body(self):
        def hide(elem):
            elem.layout.display = 'none'

        self.island_selector = widgets.Dropdown(options=[], description=_("Island") + ":")
        self.island_selector.layout.margin = self.horizontal_margins

        def callback_save(btn):
            self.open_in_ad()

        btn_open = widgets.Button(description=_("Open in Anno Designer"))
        btn_open.layout.width="12rem"
        btn_open.on_click(callback_save)

        g = Group("color", _("Colors"))
        g.add_option(Option("main_building", _("Farms and modules identical"), True))
        g.add_option(Option("vary_farms", _("Vary Farms"), True))
        g.add_option(Option("store_coverage", _("Coverage by stores")))
        g.add_option(Option("random", _("Random")))
        self.groups.append(g)

        g = Group("icon", _("Icons"))
        g.add_option(Option("no_1x1_modules", _("Hide for farm modules of size 1x1")))
        g.add_option(Option("no_1x1_ornaments", _("Hide for ornaments of size 1x1")))
        self.groups.append(g)

        g = Group("label", _("Labels"))
        g.add_option(Option("residents", _("Residents")))
        g.add_option(Option("count_modules", _("No. of Modules")))
        g.add_option(Option("items", _("Items Equipped")))
        g.add_option(Option("upgrades", _("Buffs")))
        g.add_option(Option("productivity", _("Productivity")))
        g.add_option(Option("guid", _("GUID of the asset")))
        g.add_option(Option("identifier", _("Object ID")))
        self.groups.append(g)

        def callback(event):
            self.on_change()

        tab = widgets.Tab(children=[g.render() for g in self.groups])
        titles = [g.name for g in self.groups]
        for i in range(len(tab.children)):
            tab.set_title(i, titles[i])
        # print(tab.titles)

        self.island_selector.observe(callback)
        for g in self.groups:
            for o in g.options:
                o.widget.observe(callback)

        self.preview_trigger = widgets.IntText(value=0)
        hide(self.preview_trigger)

        def show_image(any):
            return self.img_preview

        vbox = widgets.VBox([
            widgets.HBox([self.island_selector, btn_open]),
            tab,
            widgets.HTML(value="")
            # widgets.interactive(show_image, any=self.preview_trigger)
        ])

        for box in vbox.children:
            box.layout.margin = self.vertical_margins

        return vbox

    def compose_footer(self):
        self.txt_status = widgets.Text(value="", description=_("Status") + ":", disabled=True)
        self.txt_status.layout.width = "100%"
        return widgets.HBox([
            self.txt_status
        ])

    def display(self):
        return self.model

    def show(self):
        def hide(elem):
            elem.layout.display = 'none'

        lang_widget.close()
        hide(self.model.children[0])

        self.header = self.compose_header()
        self.body = self.compose_body()
        hide(self.body)
        self.footer = self.compose_footer()

        self.model.children += (self.header,)
        self.model.children += (self.body,)
        self.model.children += (self.footer,)

        for m in self.model.children:
            m.layout.margin = self.vertical_margins

        self.set_status(_("Ready"))


    def get_island(self):
        if self.island_selector is None:
            return None

        return self.island_selector.value

    def select_file(self):
        try:
            bytes = subprocess.check_output([sys.executable,
                                             str(pathlib.Path(__file__).resolve().parent / "savegame_selector.py"),
                                             str(get_savegame_folder()),
                                             _("Open Savegame"),
                                             _("Anno 1800 Savegames (*.a7s)"),
                                             ])

            path = pathlib.Path(bytes.decode(sys.stdout.encoding).strip())

            if not path.exists() or str(path) == ".":
                return
        except:
            return

        self.on_file_choosen(path)
        # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        # print("ask for files")
        # filenames = filedialog.askopenfilenames(filetypes=((_("Anno 1800 Savegames"), '*.a7s'),))  # show an "Open" dialog box and return the path to the selected file

        # if not filenames:
        #   return
        # self.on_file_choosen(self, filenames[0])

    def on_file_choosen(self, path):
        print(path)

        def hide(elem):
            elem.layout.display = 'none'

        def show(elem):
            elem.layout.display = None

        try:
            self.header.children[0].disabled = True

            self.set_status(_("Opening") + ": " + str(path))

            path = pathlib.Path(path)
            hide(self.body)
            hide(self.label_filename)
            self.progress_decoding.value = 0.01
            show(self.progress_decoding)

            self.world = World(Interpreter(path, progress_bar=self.progress_decoding),
                               progress_bar=self.progress_decoding)

            self.ordered_sessions = []
            for guid in [180023,110934,180025,180045,112132]:
                if guid in self.world.sessions :
                    self.ordered_sessions.append(self.world.sessions[guid])

            for ses in self.world.sessions.values():
                if ses not in self.ordered_sessions:
                    self.ordered_sessions.append(ses)

            hide(self.progress_decoding)

            self.label_filename.value = "{}/{}".format(path.parent.name, path.stem)
            show(self.label_filename)

            islands = []
            for s in self.ordered_sessions:
                isl = list(s.islands.values())
                isl.sort(key=lambda x: x.name)
                for i in isl:
                    islands.append(("{}: {}".format(s.name, i.name), i))

            self.island_selector.options = islands

            show(self.body)
            self.body.children[1].titles = [g.name for g in self.groups]

            self.on_change(init=True)

        except Exception as e:
            hide(self.progress_decoding)
            self.set_status(_("Failed to read file: ") + str(e))
        finally:
            self.header.children[0].disabled = False

    def get_options(self):
        options = dict()
        for g in self.groups:
            options[g.identifier] = g.get_options()

        return options

    def get_path(self, ad_json):
        path = TEMP_PATH / "ad_files" / "{}.ad".format(hash(ad_json))
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def on_change(self, init=False):
        if self.img_preview is None and not init:
            return

        island = self.get_island()
        if island is None:
            return

        try:
            ad_config = island.get_layout(options=self.get_options())
            ad_json = json.dumps(ad_config)
            path = self.get_path(ad_json)

            if path.stem == self.img_preview_id:
                return

            def parse(s):
                return np.array([int(val) for val in s.split(",")])

            if not path.with_suffix(".png").exists():
                self.set_status(_("Updating preview ..."))
                min_x = min_y = float('inf')
                max_x = max_y = float('-inf')
                for obj in ad_config["Objects"]:
                    tl = parse(obj["Position"])
                    br = tl + parse(obj["Size"])
                    min_x = min(min_x, tl[0])
                    min_y = min(min_y, tl[1])
                    max_x = max(max_x, br[0])
                    max_y = max(max_y, br[1])

                size = [max_x - min_x, max_y - min_y]
                zoom = max(8, min(100, round(1024 / max(size[0], size[1]))))

                with open(path, "w") as f:
                    f.write(ad_json)

                if not path.exists():
                    return

                exit_code = execute(
                    [os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", "export", "--renderGrid", "False",
                     "--gridSize",
                     str(zoom), str(path), str(path.with_suffix(".png"))])

            if path.stem == self.img_preview_id:
                return

            with open(str(path.with_suffix(".png")), "rb") as file:
                image = file.read()
                self.img_preview = widgets.Image(
                    value=image,
                    format='png'
                )
                self.img_preview.layout.margin = "auto"
                self.img_preview.layout.max_width = "1024px"
                self.img_preview.layout.max_height = "1024px"
                self.img_preview_id = path.stem
                self.body.children = self.body.children[:-1] + (self.img_preview,)
                self.set_status(_("Preview updated"))
                # self.preview_trigger.value = int(path.stem)
        except Exception as e:
            self.set_status(_("Failed to generate preview: ") + str(e))

    def open_in_ad(self):
        island = self.get_island()
        if island is None:
            return

        options = self.get_options()
        print("options = " + str(options))
        ad_config = island.get_layout(options=options)
        ad_json = json.dumps(ad_config)
        path = self.get_path(ad_json)

        with open(path, "w") as f:
            f.write(ad_json)

        if not path.exists():
            self.set_status(_("Failed to save ") + str(path))
            return

        # f = wmi.WMI()
        # for process in f.Win32_Process():
        #     # print(process.name)
        #     if (process.name == "AnnoDesigner.exe"):
        #         process.Terminate()

        try:
            execute([os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", "open", str(path)])
        except:
            self.set_status(_("Failed to open Anno Designer. File was saved to: ") + str(path))
