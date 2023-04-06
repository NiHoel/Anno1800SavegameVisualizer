VERSION = "v4.2"

import json
import lxml.etree as ET
import os
import sys
import zipfile
from io import BytesIO

import ipywidgets as widgets
import pandas as pd
import requests

from PyQt5.QtWidgets import QFileDialog, QApplication
from tools.a7s_model import *

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
    "Save as stamp": {
        "german": "Als Stempel speichern"
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
        "german": "Bezeichnungen"
    },
    "Exclusion": {
        "german": "Ausschluss"
    },
    "Roof colors of residences": {
      "german": "Dachfarben der Wohnhäuser"
    },
    "Farms and modules identical": {
        "german": "Farmen und Module identisch"
    },
    "Vary Farms": {
        "german": "Farmen variieren"
    },
    "Coverage by stores": {
        "german": "Abdeckung durch Einkaufspassagen"
    },
    "Portraits of residents": {
        "german": "Einwohnerportraits"
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
    "Effects": {
        "chinese": "效果",
        "english": "Effects",
        "french": "Effets",
        "german": "Effekte",
        #"guid": 134656,
        "italian": "Effetti",
        "japanese": "効果",
        "korean": "영향",
        "polish": "Efekty",
        "russian": "Эффекты",
        "spanish": "Efectos",
        "taiwanese": "效果"
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
    "Island outline": {
      "german": "Inselumriss"
    },
    "Blueprints": {
      "german": "Blaupausen"
    },
    "Quay": {
            "chinese": "码头",
            "english": "Quay",
            "french": "Quai",
            "german": "Kaimauer",
            #"guid": 1010567,
            "italian": "Banchina",
            "japanese": "波止場",
            "korean": "선창",
            "polish": "Nabrzeże",
            "russian": "Пристань",
            "spanish": "Embarcadero",
            "taiwanese": "碼頭"
        },
    "Slots": {
            "chinese": "矿产资源",
            "english": "Mineral Resource",
            "french": "Ressource minérale",
            "german": "Rohstoffvorkommen",
            #"guid": 1591,
            "italian": "Risorsa mineraria",
            "japanese": "鉱物資源",
            "korean": "광물 자원",
            "polish": "Surowiec mineralny",
            "russian": "Минеральные ресурсы",
            "spanish": "Recursos minerales",
            "taiwanese": "礦產資源"
        },
    "Routes": {
            "chinese": "路线",
            "english": "Routes",
            "french": "Routes",
            "german": "Routen",
            #"guid": 3992,
            "italian": "Rotte",
            "japanese": "ルート",
            "korean": "무역로",
            "polish": "Szlaki",
            "russian": "Маршруты",
            "spanish": "Rutas",
            "taiwanese": "路線"
        },
    "Trade Route Stations": {
            "chinese": "贸易航线站点",
            "english": "Trade Route Stations",
            "french": "Comptoirs de route commerciale",
            "german": "Handels-​Stationen",
            #"guid": 4005,
            "italian": "Stazioni rotta commerciale",
            "japanese": "取引ルートステーションの拠点",
            "korean": "항로 기항지",
            "polish": "Stacje szlaku handlowego",
            "russian": "Пункты торгового маршрута",
            "spanish": "Estaciones de ruta comercial",
            "taiwanese": "貿易路線站點"
        },
    "Ships": {
            "chinese": "船只",
            "english": "Ships",
            "french": "Navires",
            "german": "Schiffe",
            #"guid": 2736,
            "italian": "Navi",
            "japanese": "船",
            "korean": "배",
            "polish": "Statki",
            "russian": "Корабли",
            "spanish": "Barcos",
            "taiwanese": "船隻"
        },
    "Duration": {
            "chinese": "持续时间",
            "english": "Duration",
            "french": "Durée",
            "german": "Dauer",
            #"guid": 3898,
            "italian": "Durata",
            "japanese": "持続時間",
            "korean": "지속 시간",
            "polish": "Czas trwania",
            "russian": "Длительность",
            "spanish": "Duración",
            "taiwanese": "持續時間"
        },
    "Travel Time": {
            "chinese": "航行时间",
            "english": "Travel Time",
            "french": "Durée du voyage",
            "german": "Reisezeit",
            #"guid": 12736,
            "italian": "Durata viaggio",
            "japanese": "移動時間",
            "korean": "이동 시간",
            "polish": "Czas podróży",
            "russian": "Время путешествия",
            "spanish": "Tiempo de viaje",
            "taiwanese": "航行時間"
        },
    "Trade Routes": {
            "chinese": "贸易航线",
            "english": "Trade Routes",
            "french": "Routes commerciales",
            "german": "Handelsrouten",
            #"guid": 4010,
            "italian": "Rotte commerciali",
            "japanese": "取引ルート",
            "korean": "무역로",
            "polish": "Szlaki handlowe",
            "russian": "Торговые маршруты",
            "spanish": "Rutas de comercio",
            "taiwanese": "貿易航線"
        },
    "Buildings": {
            "chinese": "建筑",
            "english": "Buildings",
            "french": "Bâtiments",
            "german": "Gebäude",
            #"guid": 22659,
            "italian": "Edifici",
            "japanese": "建物",
            "korean": "건물",
            "polish": "Budynki",
            "russian": "Сооружения",
            "spanish": "Edificios",
            "taiwanese": "建築"
        },
    "Loading duration (s)": {
        "german": "Verladedauer (s)"
    },
    "Important Notice: Durations are incorrect if within the last 60 min the route has been changed (stations, goods, ships) or nothing was loaded/unloaded at a station.":
    {
        "german": "Wichtiger Hinweis: Angaben zur Dauer sind nicht korrekt, falls innerhalb der letzten 60 Minuten die Route geändert (Stationen, Waren, Schiffe) oder an einer Station nichts ver-/entladen wurde."
    },
    "Residence": {
        "chinese": "住所",
        "english": "Residence",
        "french": "Résidence",
        "german": "Wohngebäude",
        "guid": 100004,
        "italian": "Residenza",
        "japanese": "住居",
        "korean": "주거지",
        "polish": "Dom",
        "russian": "Жилое здание",
        "spanish": "Residencia",
        "taiwanese": "住所"
    },
    "All Residences": {
        "chinese": "所有住所",
        "english": "All Residences",
        "french": "Toutes les résidences",
        "german": "Alle Wohnhäuser",
        #"guid": 103502,
        "italian": "Tutte le residenze",
        "japanese": "すべての住居",
        "korean": "모든 주거지",
        "polish": "Wszystkie domy mieszkalne",
        "russian": "Все жилые здания",
        "spanish": "Todas las residencias",
        "taiwanese": "所有住所"
    },
    "Townhall Coverage": {
      "german": "Rathausabdeckung"
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
    "Stamp saved": {
      "german": "Stempel gespeichert"
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
    },
    "A new version is available":{
        "german": "Eine neue Version ist verfügbar"
    },
    "Update": {
        "german": "Aktualisieren"
    },
    "Ignore": {
        "german": "Ignorieren"
    },
    "Close and re-open the application!": {
        "german": "Schlißen und öffnen Sie die Anwendung erneut!"
    },
    "Failed to save stamp.": {
        "german": "Speichern des Stempels fehlgeschlagen."
    },
    "Abort. Stamp would be empty.": {
        "german": "Abbruch. Stempel wäre leer."
    },
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


CSS_TABLE_STRIPED = [
                        {'selector': 'th', 'props': [('padding', '0 6px 0 6px'),('border-bottom', '1px solid black')]},
                        {'selector': 'tr:nth-child(even)', 'props': [('background', '#E0E0E0'), ('color', 'black')]}
                     ]


class RouteTable:
    def __init__(self, routes, loading_duration = 12):
        self.routes = routes
        self.df = pd.DataFrame(columns =[_("Routes"), _("Trade Route Stations"), _("Ships"), _("Duration"), _("Travel Time")])

        for r in self.routes:
            duration = None
            try:
                duration = r.round_trip_time()
            except:
                pass

            if duration is None:
                duration = "-"
                travel_time = "-"
            else:
                travel_time = "{:.2f} min".format((duration / 1000 - loading_duration * len(r.stations))/ 60)
                duration = "{:.2f} min".format(duration / 60 / 1000)

            self.df.loc[len(self.df)] = [r.name, str(len(r.stations)), str(len(r.ships)), duration, travel_time]

        self.df.sort_values(_("Routes"), inplace=True)

    def render(self):
        return (self.df.style.set_table_styles(CSS_TABLE_STRIPED)
                         .set_properties(**{'text-align': 'center'})
                         .set_properties(subset = pd.IndexSlice[:,[_("Routes")]], **{'font-weight': '700'})
                         .hide(axis='index').to_html())

class EffectTable:
    def __init__(self, effects_summary: object):
        self.effects_summary = effects_summary
        self.df = pd.DataFrame(columns =[_("Residence"), _("Effects")])

        def th_string(summary):
            return "" if summary.townhall_counter == 0 else "{:.2%} {}<br/>".format(
                summary.townhall_counter / summary.building_counter, _("Townhall Coverage"))

        for summary in self.effects_summary["residences"]:
            if summary.empty():
                continue

            self.df.loc[len(self.df)] = [summary.get_residence_name(), th_string(summary) + str(summary)]

        if not effects_summary["blueprints"].empty():
            self.df.loc[len(self.df)] = [_("Blueprints"), th_string(effects_summary["blueprints"])[:-2]]

        if not len(self.df) == 0:
            summary = effects_summary["all"]
            self.df.loc[len(self.df)] = [_("All Residences"), th_string(summary) + str(summary)]

    def render(self):
        return (self.df.style.set_table_styles(CSS_TABLE_STRIPED)
                         .set_properties(**{'text-align': 'center'})
                         .set_properties(subset = pd.IndexSlice[:,[_("Residence")]], **{'font-weight': '700'})
                         .hide(axis='index').to_html())


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

        def hide(elem):
            elem.layout.display = 'none'

        def callback(btn):
            global LANG
            LANG = lang_widget.value

            lang_widget.close()
            hide(self.model.children[0])

            self.check_version()

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

        def callback_open_in_ad(btn):
            self.open_in_ad()

        def callback_save_stamp(btn):
            self.save_stamp()

        btn_open = widgets.Button(description=_("Open in Anno Designer"))
        btn_open.layout.width="12rem"
        btn_open.on_click(callback_open_in_ad)

        btn_save = widgets.Button(description=_("Save as stamp"))
        btn_save.layout.width="12rem"
        btn_save.on_click(callback_save_stamp)

        g = Group("color", _("Colors"))
        g.add_option(Option("store_coverage", _("Coverage by stores")))
        g.add_option(Option("roof", _("Roof colors of residences")))
        g.add_option(Option("main_building", _("Farms and modules identical"), True))
        g.add_option(Option("vary_farms", _("Vary Farms"), True))
        g.add_option(Option("random", _("Random")))
        self.groups.append(g)

        g = Group("icon", _("Icons"))
        g.add_option(Option("residents", _("Portraits of residents")))
        g.add_option(Option("no_1x1_modules", _("Hide for farm modules of size 1x1")))
        g.add_option(Option("no_1x1_ornaments", _("Hide for ornaments of size 1x1")))
        self.groups.append(g)

        g = Group("label", _("Labels"))
        g.add_option(Option("residents", _("Residents")))
        g.add_option(Option("count_modules", _("No. of Modules")))
        g.add_option(Option("items", _("Items Equipped")))
        g.add_option(Option("upgrades", _("Effects")))
        g.add_option(Option("productivity", _("Productivity")))
        g.add_option(Option("guid", _("GUID of the asset")))
        g.add_option(Option("identifier", _("Object ID")))
        self.groups.append(g)

        g = Group("exclude", _("Exclusion"))
        g.add_option(Option("outline", _("Island outline")))
        g.add_option(Option("blueprints", _("Blueprints")))
        g.add_option(Option("quay", _("Quay")))
        g.add_option(Option("Slot", _("Slots")))
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

        self.layout_body = widgets.VBox([
            tab,
            widgets.HTML(value="")
        ])

        def set_spacing(container):
            for box in container.children:
                box.layout.margin = self.vertical_margins

        set_spacing(self.layout_body)


        self.input_loading_duration = widgets.BoundedIntText(value=12, min=5, max=400,step=1,
                                                       description=_("Loading duration (s)") + ":",disabled=False,
                                                             style = {'description_width': 'initial'} )
        self.input_loading_duration.observe(callback)
        self.input_loading_duration.layout.width = "15rem"

        self.route_table = widgets.HTML(value="")
        self.route_body = widgets.VBox([
            widgets.Label(value = _("Important Notice: Durations are incorrect if within the last 60 min the route has been changed (stations, goods, ships) or nothing was loaded/unloaded at a station.")),
            self.input_loading_duration,
            self.route_table
        ])
        set_spacing(self.route_body)

        self.effect_table = widgets.HTML(value="")

        tab = widgets.Tab(children=[self.layout_body, self.route_body, self.effect_table])
        titles = [_("Buildings"), _("Trade Routes"), _("Effects")]
        for i in range(len(tab.children)):
            tab.set_title(i, titles[i])

        vbox = widgets.VBox([
            widgets.HBox([self.island_selector, btn_open, btn_save]),
            tab
        ])

        set_spacing(vbox)

        return vbox

    def compose_footer(self):
        self.txt_status = widgets.Text(value="", description=_("Status") + ":", disabled=True)
        self.txt_status.layout.width = "100%"
        return widgets.HBox([
            self.txt_status
        ])

    def check_version(self):
        """
        Check GitHub for a new release. If one was found, buttons to install the update or ignore it are displayed.
        """

        def hide(elem):
            elem.layout.display = 'none'

        try:
            response = requests.get("https://api.github.com/repos/NiHoel/Anno1800SavegameVisualizer/releases/latest")
            release = json.loads(response.content)
            version = release["tag_name"]
            if not version == VERSION:
                label_update = widgets.Label(value=_("A new version is available"))
                btn_download = widgets.Button(description=_("Download"))
                btn_ignore = widgets.Button(description=_("Ignore"))

                update_box = widgets.VBox([
                    label_update,
                    widgets.HBox([btn_download, btn_ignore])
                ])

                def callback_ignore(btn):
                    hide(update_box)
                    self.show()

                def callback_download(btn):
                    try:
                        hide(update_box)
                        asset_url = release["assets"][0]["browser_download_url"]
                        print(asset_url)

                        img_loading = None
                        with open("imgs/loading-buffering.gif", "rb") as f:
                            img_loading = widgets.Image(
                                value=f.read(),
                                format='gif',
                                width="20px",
                                margin="auto"
                            )

                            self.model.children = tuple([img_loading] + list(self.model.children[1:]))

                        zip_response = requests.get(asset_url)
                        cfg_path = pathlib.Path(os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe.config")
                        if cfg_path.exists():
                            cfg_path.unlink()
                        with zipfile.ZipFile(BytesIO(zip_response.content)) as archive:
                            archive.extractall(path=os.getcwd())

                        label_restart = widgets.HTML(value="<b><font color='red' size='20px'>{}</b>".format(
                            _("Close and re-open the application!")))
                        self.model.children = tuple([label_restart] + list(self.model.children[1:]))

                    except Exception as e:
                        print(e)
                        self.set_status(str(e))
                        if img_loading is not None:
                            hide(img_loading)
                        self.show()

                btn_download.on_click(callback_download)
                btn_ignore.on_click(callback_ignore)

                # show buttons first
                self.model.children = tuple([update_box] + list(self.model.children))

            else:
                self.show()
        except Exception as e:
            print(e)
            self.set_status(str(e))
            self.show()


    def display(self):
        return self.model

    def show(self):
        def hide(elem):
            elem.layout.display = 'none'

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
                               extract_routes=True,
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
                    if isinstance(i, Island):
                        islands.append(("{}: {}".format(s.name, i.name), i))

            self.island_selector.options = islands
            if len(islands) > 0:
                self.island_selector.value = islands[0][1]

            show(self.body)
            self.layout_body.children[1].titles = [g.name for g in self.groups]

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
            self.route_table.value = RouteTable(self.world.trade_routes, self.input_loading_duration.value).render()
            return

        self.route_table.value = RouteTable(island.routes, self.input_loading_duration.value).render()
        self.effect_table.value = EffectTable(island.get_upgrades_summary()).render()

        try:
            ad_config = island.get_layout(options=self.get_options())
            if "Modified" in ad_config:
                del ad_config["Modified"]
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
                    [os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe",
                     "export", str(path), str(path.with_suffix(".png")),
                     "--renderGrid", "False",
                     "--renderStatistics", "False",
                     "--renderVersion", "False",
                     "--gridSize", str(zoom)])

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
                self.layout_body.children = self.layout_body.children[:-1] + (self.img_preview,)
                self.set_status(_("Preview updated"))

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
            # open async
            subprocess.Popen([os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", "open", str(path)])
        except:
            self.set_status(_("Failed to open Anno Designer. File was saved to: ") + str(path))

    def save_stamp(self):
        island = self.get_island()
        if island is None:
            return

        try:
            xml = island.get_stamp(options=self.get_options())

            if xml is None:
                self.set_status(_("Abort. Stamp would be empty."))

            path = TEMP_PATH / "stamp"
            with open(path.with_suffix(".xml"), "wb") as f:
                f.write(ET.tostring(xml, pretty_print=True))

            subprocess.call(
                [os.getcwd() + "/tools/FileDBReader/FileDBReader.exe", "compress",
                 "-i", os.getcwd() + "/tools/FileDBReader/FileFormats/stamp.xml",
                 "-y", "-c", "3", "-o", "", "-f", str(path.with_suffix(".xml"))])

            region = "The Old World"
            try:
                region = A7PARAMS["region_names"].get(island.session.get_region_guid())["english"]
            except:
                pass
            stamp_path = get_documents_path() / "Anno 1800" / "stamps" / region / "Islands"
            stamp_path.mkdir(parents=True, exist_ok=True)

            dst_path = stamp_path / re.sub(r'[^\w_. -]', '_', island.name)
            shutil.copy(path.with_suffix(""), dst_path)
            self.set_status("{}: {}".format(_("Stamp saved"), dst_path))

        except Exception as e:
            self.set_status(_("Failed to save stamp."))
            print(e)