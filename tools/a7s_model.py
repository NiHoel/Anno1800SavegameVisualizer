import csv
import json
import math
import os
import pathlib
import random
import re
import shutil
import struct
import subprocess
import zipfile
import zlib
from datetime import datetime

import copy
import lxml.etree as ET
import numpy as np
from ipywidgets import *
from typing import Dict

from tools.params import A7PARAMS

def get_documents_path():
    import ctypes.wintypes
    CSIDL_PERSONAL = 5  # My Documents
    SHGFP_TYPE_CURRENT = 0  # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

    return pathlib.Path(buf.value)  # .resolve() would turn letters for network drives into server names


def get_savegame_folder():
    accounts = (get_documents_path() / "Anno 1800/accounts")
    for folder in accounts.glob("*"):
        return folder
    return accounts


def get_temp_path():
    p = os.environ['TEMP']
    if p is None:
        return pathlib.Path(os.getcwd()) / "temp_files"
    else:
        return pathlib.Path(p) / "Anno1800SavegameVisualizer"


TEMP_PATH = get_temp_path()
try:
    shutil.rmtree(TEMP_PATH)
    pass
except:
    pass

LANG = "english"

lang_widget = Dropdown(options=A7PARAMS["languages"], value=LANG)


def set_language(lang: str):
    global LANG
    LANG = lang_widget.value


lang_widget.observe(set_language)
display(lang_widget)


def execute(args):
    exit_code = subprocess.call(args)

    if exit_code == 0:
        return

    executable = pathlib.Path(args[0]).stem + ".exe"
    print(subprocess.list2cmdline(args))
    # if exit_code < 1000:
    raise Exception(
        "Executing {} failed. Please ensure that the file is not corrupt or try running this application in a different directory.".format(
            executable))
    # else:
    #     raise Exception(
    #         "Windows blocked the execution of {exe}. Go into the tools directory and double click {exe}. A warning appears. Click 'More Information' and 'Run anyway'. Then re-run the code (Shift + Enter).".format(
    #             exe=executable))


def hex_to_bool(h: str) -> bool:
    '''
    Converts the binary representation of a boolean
    ('00', '01') to a Python boolean.

    Args:
        h (str or node): '00' or '01' or a node of an lxml tree.

    Returns:
        bool: True or False or None (if node has no text).

    Example:
        $ hex_to_bool('01')
            -> True
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        return bool(int(h))
    else:
        return None


def hex_to_utf16(h: str) -> str:
    '''
    Converts a hexadecimal UTF-16 encoded string to a human-
    readable string.

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns:
        str: A human-readable text string or None (if node has no text).

    Example:
        $ hex_to_utf16('4F006C006400200057006F0072006C006400')
            -> 'Old World'
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        return bytes.fromhex(h).decode('utf-16-le')
    else:
        return None


def hex_to_utf8(h: str) -> str:
    '''
    Converts a hexadecimal UTF-8 encoded string to a human-
    readable string.

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns:
        str: A human-readable text string or None (if node has no text).

    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        return bytes.fromhex(h).decode('utf-8')
    else:
        return None


def hex_to_int(h: str) -> int:
    '''
    Converts the hexadecimal representation of a
    Byte, Short, 32-bit, or 64-bit integer to an int.
    The precise type is determined based on the length of the string.

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns:
        int: Parsed int value or None (if node has no text).

    Example:
        $ hex_to_int('4DBF0200')
            -> 180045
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        if l == 2:
            return struct.unpack('<B', bytearray.fromhex(h))[0]
        elif l == 4:
            return struct.unpack('<h', bytearray.fromhex(h))[0]
        elif l == 8:
            return struct.unpack('<i', bytearray.fromhex(h))[0]
        elif l == 16:
            return struct.unpack('<q', bytearray.fromhex(h))[0]
        else:
            raise ValueError("Invalid length of {} characters".format(l))

    else:
        return None


def hex_to_float(h: str) -> int:
    '''
    Converts the hexadecimal representation of a
    single or double precision IEEE floating point number to a float.
    The precise type is determined based on the length of the string.

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns:
        int: Parsed float value or None (if node has no text).

    Example:
        $ hex_to_float('DB0FC93F')
            -> 1.5707963705062866
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        if l == 8:
            return struct.unpack('<f', bytearray.fromhex(h))[0]
        elif l == 16:
            return struct.unpack('<d', bytearray.fromhex(h))[0]
        else:
            raise ValueError("Invalid length of {} characters".format(l))

    else:
        return None


def hex_to_float_list(h: str, stride: int = 4) -> [float]:
    '''
    Converts the hexadecimal representation of a densly packed array of
    single or double precision IEEE floating point numbers to a list of floats.

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.
        stride (int): 4 or 8 - number of bytes a single value occupies.

    Returns:
        list: A list of floats or None (if node has no text).
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        s = stride * 2  # two chars encode one byte

        if not l % s == 0:
            raise ValueError("Invalid length of {} characters".format(l))

        arr = []
        for r in range(int(l / s)):
            arr.append(hex_to_float(h[s * r:s * (r + 1)]))

        return arr

    else:
        return None


def hex_to_int_list(h: str, stride: int = 4, limit_elements: int = 0) -> [int]:
    '''
    Converts the hexadecimal representation of a densly packed array of
    bytes, shorts, 32-bit, or 64-bit integers to a list of ints.

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.
        stride (int): 1,2,4, or 8 - number of bytes a single value occupies.
        limit_elements (int): The returned list has at most limit_elements many entries, default: 0 = unlimited

    Returns:
        list: A list of ints or None (if node has no text).
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        s = stride * 2  # two chars encode one byte

        if not l % s == 0:
            raise ValueError("Invalid length of {} characters".format(l))

        arr = []
        if limit_elements == 0:
            limit_elements = int(len(h) / s)
        for r in range(limit_elements):
            arr.append(hex_to_int(h[s * r:s * (r + 1)]))

        return arr

    else:
        return None


def show(ad_config):
    ad_json = json.dumps(ad_config)
    path = TEMP_PATH / "ad_files" / "{}.ad".format(hash(ad_json))
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(ad_json)

    subprocess.Popen([os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", "open", str(path)])
    # subprocess.Popen([os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", str(path)])


def save(ad_config, path):
    ad_json = json.dumps(ad_config)
    if not path.endswith(".ad"):
        path = pathlib.Path(path).with_suffix(".ad")
    else:
        path = pathlib.Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(ad_json)


def has_value(node):
    if node is None:
        return False

    if isinstance(node, ET._Element):
        node = node.text

    return not node is None and not len(node) == 0 and not node[0] == '\n'


def is_road(idx):
    s = A7PARAMS["streets"]
    if not idx in s:
        return False

    return s[idx]["road"]


def is_quay(idx):
    s = A7PARAMS["streets"]
    if not idx in s:
        return False

    return s[idx]["harbour"] and not s[idx]["road"] and not s[idx]["rail"]


def vary_color(color, random_value: float = None):
    """
    color: dict with keys "R", "G", "B", "A" (optional)
    random_value must be within [0,1]
    if random_value is not provided a pseudo random number is drawn

    Converts color into Cielab space (L*a*b*) and selects a new L from [L - 20, L + 20] determined by random_value

    Returns an RGB(A) color
    """

    XN = 95.0489
    YN = 100
    ZN = 108.8840

    srgb2xyz = np.array([0.4124, 0.3576, 0.1805,
                         0.2126, 0.7152, 0.0722,
                         0.0193, 0.1192, 0.9504]).reshape(3, 3)

    xyz2srgb = np.array([3.2406, -1.5372, -0.4986,
                         -0.9689, 1.8758, 0.0415,
                         0.0557, -0.2040, 1.0570]).reshape(3, 3)

    inv_gamma = lambda u: u / 12.92 if u <= 0.04045 else math.pow((u + 0.055) / 1.055, 2.4)
    gamma = lambda u: 12.92 * u if u <= 0.0031308 else 1.055 * math.pow(u, 1. / 2.4) - 0.055

    lin = np.array([
        inv_gamma(color["R"] / 255),
        inv_gamma(color["G"] / 255),
        inv_gamma(color["B"] / 255),
    ])

    xyz = 100 * srgb2xyz @ lin

    f = lambda t: math.pow(t, 1 / 3) if t > (6 / 29) * (6 / 29) * (6 / 29) else t / (3 * (6 / 29) * (6 / 29)) + 4. / 29.

    L = 116. * f(xyz[1] / YN) - 16.
    a = 500. * (f(xyz[0] / XN) - f(xyz[1] / YN))
    b = 200. * (f(xyz[1] / YN) - f(xyz[2] / ZN))

    if random_value is None:
        L = random.uniform(max(L - 20, 10), min(L + 20, 90))
    else:
        min_L = max(L - 20, 10)
        max_L = min(L + 20, 90)
        L = min_L + random_value * (max_L - min_L)

    inv_f = lambda t: math.pow(t, 3) if t > (6 / 29) else 3 * (6 / 29) * (6 / 29) * (6 / 29) * (t - 4 / 29)

    xyz = np.array([
        XN * inv_f((L + 16) / 116 + a / 500),
        YN * inv_f((L + 16) / 116),
        ZN * inv_f((L + 16) / 116 - b / 200)
    ])

    lin = xyz2srgb @ (0.01 * xyz)
    g = lambda x: max(0, min(255, int(gamma(x) * 255)))

    return {
        "A": color.get("A"),
        "R": g(lin[0]),
        "G": g(lin[1]),
        "B": g(lin[2]),
    }


class Interpreter:
    """
    Stores the XML tree of the savegame along with parsing rules
    to turn the hexadecimal values into meaningful ints, floats and strings
    """

    def __init__(self, savegame_path: str, keep_files=False, decode_all=False, progress_bar=None):
        path = pathlib.Path(savegame_path)
        if not path.exists():
            raise Exception("File or path do not exist: {}".format(path))

        self.tree = self.extract(savegame_path, keep_files, decode_all, progress_bar=progress_bar)
        self.node_to_rule = dict()
        self.tag_rules = dict()
        self.rules_cached = False

    def __cache_rules__(self):
        try:
            self.rule_tree = ET.parse(os.getcwd() + "/tools/FileDBReader/FileFormats/a7s_all.xml")
            for rule_node in self.rule_tree.findall(".//Converts/Convert"):
                path = rule_node.get("Path")

                if path is None:
                    continue

                match = re.fullmatch("\\.?//([^/\\[\\]\\(\\)@.*]+)", path)
                if match is None:
                    for node in self.tree.xpath(path):
                        if not node in self.node_to_rule:
                            self.node_to_rule[node] = rule_node
                else:
                    tag = match[1]
                    if not tag in self.tag_rules:
                        self.tag_rules[tag] = rule_node

            self.rules_cached = True
        except:
            pass

    @staticmethod
    def extract(path: str, keep_files=False, decode_all=False, progress_bar=None):
        """
        Returns an XML tree of the savegame located at path.
        """
        if progress_bar is None:
            print("Unpacking ...")
        else:
            progress_bar.value = 0.01
        path = pathlib.Path(path)
        out_path = TEMP_PATH / path.stem
        # print(out_path)
        # out_path = path.parent / path.stem
        out_path.mkdir(parents=True, exist_ok=True)
        tools_path = pathlib.Path(os.getcwd() + "/tools")
        execute(
            [str(tools_path / "RDAConsole.exe"), "extract", "-f", str(path), "-o", str(out_path), "-y", "-n"])

        # db_reader_path = pathlib.Path(distutils.spawn.find_executable("FileDBReader.exe"))

        tree = None
        files = list(out_path.glob("*.a7s"))  # necessary to iterate twice

        if len(files) < 4:
            raise Exception("Savegame could not be decoded or disk is full")
        elif len(files) > 4:
            raise Exception("The temporary directory got messed up with other files: " + str(out_path))

        # print(len([f for f in files]))
        if progress_bar is None:
            print("Decoding ...")
        else:
            progress_bar.value = 0.05

        total_size = 0
        for file in files:
            total_size += file.stat().st_size

        processed_size = 0
        for file in files:

            if not file.with_suffix(".xml").exists():
                content = open(file, 'rb').read()
                content = zlib.decompress(content)
                with open(file.with_suffix(".bin"), 'wb') as f:
                    f.write(content)

                execute([str(tools_path / "FileDBReader/FileDBReader.exe"), "decompress", "-i",
                         str(tools_path / (
                             "FileDBReader/FileFormats/a7s_all.xml" if decode_all else "FileDBReader/FileFormats/a7s_hex.xml")),
                         "-f",
                         str(file.with_suffix(".bin")), "-y"])

            if progress_bar is not None:
                progress_bar.value = 0.05 + 0.6 * (processed_size / total_size + file.stat().st_size / total_size * 0.8)

            parser = ET.XMLParser(huge_tree=True)
            data = ET.parse(str(file.with_suffix(".xml")), parser)
            if tree is None:
                tree = data
            else:
                tree.getroot().extend(data.getroot())

            processed_size += file.stat().st_size

            if progress_bar is not None:
                progress_bar.value = 0.05 + 0.6 * processed_size / total_size

        if not keep_files:
            try:
                shutil.rmtree(out_path)
            except:
                pass

        if progress_bar is not None:
            progress_bar.value = 0.65

        return tree

    def parse(self, node):
        if not has_value(node):
            return None

        rule = self.node_to_rule.get(node)
        if rule is None:
            rule = self.tag_rules.get(node.tag)

        if rule is None:
            l = len(node.text)
            if l == 2 or l == 4 or l == 8 or l == 16:
                return hex_to_int(node)
            else:
                return node.text

        else:
            return self.parse_with_rule(node, rule)

    def parse_with_rule(self, node, rule):
        rule_type = rule.get("Type").lower()
        is_list = not rule.get("Structure") is None and rule.get("Structure").lower() == "list"

        if rule_type == "string":
            if rule.get("Encoding").lower() == "utf-16":
                return hex_to_utf16(node)
            else:
                return hex_to_utf8(node)
        elif rule_type == "single":
            if is_list:
                return hex_to_float_list(node, 4)
            else:
                return hex_to_float(node)
        elif rule_type == "double":
            if is_list:
                return hex_to_float_list(node, 8)
            else:
                return hex_to_float(node)

        if not is_list:
            return hex_to_int(node)

        stride = 1
        if "16" in rule_type:
            stride = 2
        elif "32" in rule_type:
            stride = 4
        elif "64" in rule_type:
            stride = 8

        return hex_to_int_list(node, stride)

    @staticmethod
    def merge(lhs, rhs):
        """
        Utility method for inspect()
        """

        if lhs is None:
            return rhs
        elif rhs is None:
            return lhs

        attr = dict()
        if isinstance(lhs, dict) and isinstance(rhs, dict):
            multi_keys = dict()

            for key in (lhs.keys() | rhs.keys()):
                k = key.split(" ")
                count = int(k[1]) if len(k) > 1 else 1

                if k[0] in multi_keys:
                    other_key = multi_keys[k[0]]
                    new_key = "{} {}".format(k[0], count + int(other_key.split(" ")[1]))
                    if key in lhs:
                        new_value = Interpreter.merge(lhs.get(key), rhs.get(other_key))
                    else:
                        new_value = Interpreter.merge(lhs.get(other_key), rhs.get(key))
                    del attr[other_key]
                    attr[new_key] = new_value

                elif k[0] in attr:
                    new_key = "{} {}".format(k[0], count + 1)
                    if key in lhs:
                        new_value = Interpreter.merge(lhs.get(key), rhs.get(k[0]))
                    else:
                        new_value = Interpreter.merge(lhs.get(k[0]), rhs.get(key))
                    del attr[k[0]]
                    attr[new_key] = new_value

                else:
                    if len(k) > 1:
                        multi_keys[k[0]] = key
                    in_both = key in lhs and key in rhs

                    if in_both:
                        new_key = "{} {}".format(k[0], 2 * count)
                        attr[new_key] = Interpreter.merge(lhs.get(key), rhs.get(key))
                    else:
                        attr[key] = lhs.get(key) if key in lhs else rhs.get(key)

            return attr

        if isinstance(lhs, dict):
            attr = copy.deepcopy(lhs)
            attr[""] = rhs
            return attr
        elif isinstance(rhs, dict):
            attr = copy.deepcopy(rhs)
            attr[""] = lhs
            return attr

        if not isinstance(lhs, set):
            lhs = set([lhs])
        if not isinstance(rhs, set):
            rhs = set([rhs])

        return lhs | rhs

    def aggregate(self, node, depth):
        """
        Utility method for inspect()
        """

        attr = dict()
        duplicates = dict()
        if has_value(node):
            val = str(self.parse(node))
            if len(val) > 20:
                val = val[0:17] + "..."
            return val

        if depth == 0:
            return "{...}"

        for n in node:
            n_dic = self.aggregate(n, depth - 1)

            if n.tag in attr:
                attr[n.tag] = Interpreter.merge(attr.get(n.tag), n_dic)

                if n.tag in duplicates:
                    duplicates[n.tag] += 1
                else:
                    duplicates[n.tag] = 2
            else:
                attr[n.tag] = n_dic

        for key in duplicates:
            attr["{} {}".format(key, duplicates[key])] = attr[key]
            del attr[key]

        return attr

    def print_dic_tree(self, t, depth=0):
        """
        Utility method for inspect()
        """

        for key in t:
            s = "\t" * depth + key + ":"
            if isinstance(t[key], dict):
                print(s)
                self.print_dic_tree(t[key], depth + 1)
            elif isinstance(t[key], set):
                values = [v for v in t[key]]
                print("{} {}".format(s, values[0:10]))
            else:
                print("{} {}".format(s, t.get(key)))

    def inspect(self, node, depth=1):
        """
        Print an aggregated view of the tree starting in node up to depth. The values of nodes are decoded as
        ints, floats, etc. according to the saved rules
        """
        if node is None:
            return

        if not self.rules_cached:
            self.__cache_rules__();

        if type(node) is ET._ElementTree:
            node = node.getroot()

        agg = self.aggregate(node, depth)
        if isinstance(agg, dict):
            self.print_dic_tree(agg)
        else:
            print(self.parse(node))


class ADConfig:
    """
    Provides access for the information stored in the Anno Designer (AD) directory:
    * presets: json of all buildings readily available in AD
    * colors: json (coloring information for groups of buildings)
    """

    def __init__(self):
        self.presets = json.load(open(os.getcwd() + "/tools/Anno Designer/presets.json", encoding="utf8"))
        self.colors = json.load(open(os.getcwd() + "/tools/Anno Designer/colors.json", encoding="utf8"))
        self.special_templates = ["RoofColDef", "DefColFace", "RoofColFace"]
        self.resident_icons = dict()
        self.roof_colors = dict()
        self.island_outlines = dict()

        self.default_color = {
            "A": 255,
            "R": 255,
            "G": 0,
            "B": 0
        }

        self.templates_by_guid = dict()
        self.scenario_templates = dict()
        for session in A7PARAMS["scenarios"].values():
            self.scenario_templates[session] = dict()

        for b in self.presets["Buildings"]:
            if b.get("Guid") is None or b.get("Guid") == "0" or not b.get("Header") == "(A7) Anno 1800":
                continue

            t = copy.deepcopy(b)
            t["Icon"] = t["IconFileName"]
            t["Radius"] = t["InfluenceRadius"]
            for key in ["Header", "Faction", "Group", "Localization", "IconFileName"]:
                if key in t:
                    del t[key]

            for c in self.colors["AvailableSchemes"][0]["Colors"]:
                applies = (c["TargetTemplate"] == t["Template"] and
                           (c["TargetIdentifiers"] is None or
                            len(c["TargetIdentifiers"]) == 0 or
                            t["Identifier"] in c["TargetIdentifiers"]))

                if applies:
                    t["Color"] = copy.deepcopy(c["Color"])

            guid = int(b.get("Guid"))

            if t.get("Template") in self.special_templates:
                template = t.get("Template")

                if template == "RoofColDef":
                    self.roof_colors[guid] = copy.deepcopy(t.get("Color"))
                elif template == "DefColFace":
                    self.resident_icons[guid] = t.get("Icon")

                continue

            if t["Template"] in A7PARAMS["scenarios"]:
                self.scenario_templates[A7PARAMS["scenarios"][t["Template"]]][guid] = t
            else:
                self.templates_by_guid[guid] = t

        self.replaced_guids = dict()

        with open(os.getcwd() + "/tools/replaced_guids.csv", encoding="utf8") as f:
            nr = 0
            for line in csv.reader(f):
                nr += 1
                if nr <= 4:
                    continue

                guid = int(line[0])

                if guid not in self.templates_by_guid:
                    # raise Exception("GUID {} specified as the target of replacement but not found in presets.json".format(guid))
                    continue

                t = self.get_template(guid)

                for g in line[3:]:
                    r_guid = int(g)
                    if not self.has_template(r_guid):
                        self.templates_by_guid[r_guid] = t

        self.scenario_templates[655][101259] = self.scenario_templates[655][24136]  # replace boxing arena by water pump
        for guid in [893, 895, 896]:  # reward ornaments have scenario template but can be build everywhere
            if guid not in self.templates_by_guid:
                self.templates_by_guid[guid] = self.scenario_templates[655][guid]

        with zipfile.ZipFile(os.getcwd() + "/tools/island_outlines.zip") as archive:
            for file in archive.infolist():
                path = pathlib.Path(file.filename)
                self.island_outlines[path.stem] = json.loads(archive.read(file))

    def get_template(self, guid: int, session: int = None) -> json:
        if session in self.scenario_templates and guid in self.scenario_templates[session]:
            t = self.scenario_templates[session][guid]
        else:
            t = self.templates_by_guid.get(guid)

        if t is None:
            return None

        if not "Color" in t:
            t["Color"] = copy.deepcopy(self.default_color)

        return t

    def has_template(self, guid: int, session: int = None) -> bool:
        if session in self.scenario_templates and guid in self.scenario_templates[session]:
            return True
        return guid in self.templates_by_guid

    def get_island_outline(self, island_name: str):
        if island_name in self.island_outlines:
            return self.island_outlines[island_name].get("Objects")

        return None

    def has_island_outline(self, island_name: str):
        return island_name in self.island_outlines


class Ship:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * guid: int (ship type)
    * identifier: int
    * name: str
    * position: np.array of floats (x,y,z) where
        the x-axis points north east
        the y-axis is perpendicular to the water surface
        the z-axis points north west
    * goods: dict(int : guid, int: amount)
    """

    def __init__(self, node: ET._Element, guid, identifier, world):
        self.node = node
        self.guid = guid
        self.identifier = identifier
        self.world = world
        # self.slots = A7PARAMS["ships"][guid]
        self.position = hex_to_float_list(node.find("Position"))
        self.name = hex_to_utf16(node.find("Nameable/VehicleName"))

    def __str__(self):
        return "{} (type: {})".format(self.name, self.guid)


class StationVisit:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * ship_guid: int
    * station: Station
    * execution_time: int (in ms since game start)
    * goods: dict(int : guid, int: amount)
    """

    def __init__(self, node: ET._Element, ship_guid, station):
        self.node = node
        self.ship_guid = ship_guid
        self.station = station
        self.execution_time = hex_to_int(node.find("ExecutionTime"))
        finalized = hex_to_int(node.find("Finalized"))
        self.finalized = False if finalized is None or finalized == 0 else True
        self.goods = dict()

        for g in node.findall("TradedGoods/None"):
            self.goods[hex_to_int(g.find("GoodGuid"))] = hex_to_int(g.find("GoodAmount"))

    def __str__(self):
        return "Visit {} at {} ms".format(self.station.__str__(), self.execution_time)


class Station:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * identifier: int
    * island : Island | NPCIsland
    * route: Route
    * goods: dict(int : guid, int: amount)
    * visits: dict(int : ship guid, [StationVisit])
    """

    def __init__(self, node: ET._Element, island, route):
        self.node = node
        self.identifier = hex_to_int(node.find("StationID"))
        self.island = island
        self.route = route
        self.goods = dict()
        self.visits = dict()  # Map ship guid -> [StationVisit]

        for g in node.findall("GoodInfos/None"):
            self.goods[hex_to_int(g.find("ProductGUID"))] = hex_to_int(g.find("Amount"))

        for v in island.node.findall("PassiveTrade/History/TradeRouteEntries/None/"):
            r = hex_to_int(v.find("RouteID"))
            if not r == route.identifier:
                continue

            # The Guid of the ship, so we cannot distinguish which one
            s = hex_to_int(v.find("TraderShip"))
            if s not in self.visits:
                self.visits[s] = [StationVisit(v, s, self)]
            else:
                self.visits[s].append(StationVisit(v, s, self))

        for visits in self.visits.values():
            visits.sort(key=lambda x: x.execution_time)

    def get_ships_types(self):
        return self.visits.keys()

    def get_visits(self, ship: int):
        """

        :param ship:
        :return: Ordered list of finalized StationVisits
        """
        if not ship in self.visits:
            return []
        return self.visits[ship]

    def __str__(self):
        return "Station {} on route {}".format(self.island.name, self.route.name)


class Route:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * identifier: int
    * name: str
    * ships: dict(int, Ship)
    * stations: [Station]
    """

    def __init__(self, node: ET._Element, world):
        self.node = node
        self.world = world
        self.identifier = hex_to_int(node.find("ID"))
        self.name = hex_to_utf16(node.find("Name"))
        self.ships = dict()
        self.stations = []
        self.visit_counts = dict()

        ships = hex_to_int_list(node.find("Ships"), 8)
        if ships is not None:
            for s in ships:
                if s in world.ships:
                    self.ships[s] = world.ships[s]

        for s in node.findall("Stations/None"):
            area = hex_to_int(s.find("AreaID"))
            if area is None:
                continue

            island = world.get_island_by_id(area)
            if island is None:
                continue

            self.stations.append(Station(s, island, self))
            island.add_route(self)
            if island in self.visit_counts:
                self.visit_counts[island] += 1
            else:
                self.visit_counts[island] = 1

    def get_ship_guids_and_count(self):
        guids = dict()

        for s in self.ships.values():
            if s.guid in guids:
                guids[s.guid] += 1
            else:
                guids[s.guid] = 1

        return guids

    def round_trip_time(self, ship_guid: int = None):
        if ship_guid is None:
            weight = 0
            time = 0
            for guid, w in self.get_ship_guids_and_count().items():
                t = self.round_trip_time(guid)
                if t is not None:
                    weight += w
                    time += t * w

            if weight == 0:
                return None
            return time / weight

        intervals = []
        for s in self.stations:
            if self.visit_counts[s.island] > 1:
                continue

            visits = s.get_visits(ship_guid)

            l = len(visits) - len(self.ships)
            if l <= 0:
                continue

            l_ = min(l, len(self.ships))
            durations = [a.execution_time - b.execution_time for a, b in zip(visits[-l_:], visits[:l_])]
            intervals.append(sum(durations) / l)

        if len(intervals) == 0:
            return None

        return min(intervals)

    def __str__(self):
        return "Route {}".format(self.name)


class NPCIsland:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * session: Session
    * identifier: int
    * name: str
    * manager: ET._Element
    * routes: set(Route) (all trade routes with a station on this island)
    """

    def __init__(self, node: ET._Element, identifier: int, name: str, session):
        self.node = node
        self.identifier = identifier
        self.name = name
        self.session = session
        self.manager = None
        self.island_template = None
        self.rectangle = np.array([400, 400])
        self.island_template_name = None
        self.buildings = dict()
        self.routes = set()

    def __set_area_manager__(self, manager: ET._Element):
        self.manager = manager

    def __set_island_template__(self, template: ET._Element, rect: np.array, name: str):
        self.island_template = template
        self.rectangle = rect
        self.island_template_name = name
        self.rotation = hex_to_int(template.find("./Rotation90"))
        if self.rotation is None:
            self.rotation = 0

    def add_route(self, route: Route):
        self.routes.add(route)

    def __str__(self):
        s = "{} (NPC) in {}".format(self.name, self.session)
        if not self.island_template_name is None:
            s += "\tIsland type: {}".format(self.island_template_name)

        return s


class ResidenceEffectsSummaryEntry:
    def __init__(self, residence: object or None, effects_map: Dict[int, object]):
        self.residence = residence
        self.effects_map = effects_map
        self.effects_counter = dict()
        self.building_counter = 0
        self.townhall_counter = 0

    def get_residence_name(self):
        return "" if self.residence is None else self.residence["locaText"][LANG]

    def add_list(self, upgrades: [int]):
        self.building_counter += 1
        applied = set()
        for guid in upgrades:
            if guid not in self.effects_map or guid in applied:
                continue

            if guid in self.effects_counter:
                self.effects_counter[guid] += 1
            else:
                self.effects_counter[guid] = 1

            effect = self.effects_map[guid]
            if "allowStacking" in effect and effect["allowStacking"] is False:
                applied.add(guid)

    def empty(self):
        return len(self.effects_counter) == 0 and self.townhall_counter == 0

    def __str__(self):
        isFirst = True
        result = ""

        def comp(item):
            effect = self.effects_map.get(item[0])

            if "panoramaLevel" in effect:
                return " {}{}".format(str(effect["residences"][0])[-1], 9-effect["panoramaLevel"])

            return effect["locaText"][LANG]

        l = list(self.effects_counter.items())
        l.sort(key=comp)
        for guid, count in l:
            if not isFirst:
                result += "; "

            isFirst = False
            result += "{:.2%} {}".format(count / self.building_counter, self.effects_map.get(guid)["locaText"][LANG])

        return result


class Island:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * session: Session
    * identifier: int
    * name: str
    * count_residences: int
    * count_production_buildings: int
    * count_modules: int
    * count_other_buildings: int
    * routes: set(Route) (all trade routes with a station on this island)
    * manager: ET._Element (stores information for buildings, population, irrigation, railway, incidents,
                            electricity, consumption, items, happiness)

    To iterate all buildings, use:
    for i in self.buildings.values()
    """

    def __init__(self, node: ET._Element, identifier: int, name: str, session):
        self.node = node
        self.identifier = identifier
        self.name = name
        self.session = session
        self.buildings = dict()
        self.routes = set()

        self.count_residences = 0
        self.count_production_buildings = 0
        self.count_modules = 0
        self.count_other_buildings = 0

        self.__store_coverage_computed__ = False
        self.__building_grid__ = None
        self.__building_grid_no_blueprints__ = None

    def __set_area_manager__(self, manager: ET._Element):
        self.manager = manager

        for obj in manager.find("./AreaObjectManager/GameObject/objects"):
            try:
                identifier = hex_to_int(obj.find("ID"))
                store_index = Store.get_index(self.session.world.ad_config, hex_to_int(obj.find("guid").text))
                if store_index > 0:
                    self.buildings[identifier] = Store(obj, store_index, self)
                    self.count_production_buildings += 1
                elif (not obj.find("./BuildingModule/ParentFactoryID") is None and
                      not hex_to_int(obj.find("./BuildingModule/ParentFactoryID")) == 0):
                    self.buildings[identifier] = Module(obj, self)
                    self.count_modules += 1
                elif not obj.find("./Residence7/*") is None:
                    self.buildings[identifier] = Residence(obj, self)
                    self.count_residences += 1
                elif has_value(obj.find("./ModuleOwner/BuildingModules")) or has_value(obj.find("./ModuleOwner/BinArray")):
                    self.buildings[identifier] = Farm(obj, self)
                    self.count_production_buildings += 1
                elif not obj.find("./Factory7/*") is None:
                    self.buildings[identifier] = Factory(obj, self)
                    self.count_production_buildings += 1
                elif hex_to_int(obj.find("guid")) in [114751, 117547, 100780]:
                    self.buildings[identifier] = Powerplant(obj, self)
                    self.count_other_buildings += 1
                elif obj.find("./ItemContainer/SocketContainer/SocketItems") is not None:
                    self.buildings[identifier] = Guildhouse(obj, self)
                    self.count_other_buildings += 1
                else:
                    self.buildings[identifier] = Building(obj, self)
                    self.count_other_buildings += 1

            except:
                pass

        for b in self.buildings.values():
            if isinstance(b, Farm):
                converted = b.process_modules(self.buildings)
                self.count_modules += converted
                self.count_other_buildings -= converted


    def __set_island_template__(self, template: ET._Element, rect: np.array, name: str):
        self.island_template = template
        self.rectangle = rect
        self.island_template_name = name
        self.rotation = hex_to_int(template.find("./Rotation90"))
        if self.rotation is None:
            self.rotation = 0

    def __str__(self):
        s = "{} in {}\tIsland type: {}".format(self.name, self.session, self.island_template_name)
        if self.count_residences > 0:
            s += "\tResidences : " + str(self.count_residences)
        if self.count_production_buildings > 0:
            s += "\tProduction Buildings : " + str(self.count_production_buildings)
        if self.count_modules > 0:
            s += "\tModules : " + str(self.count_modules)
        if self.count_other_buildings > 0:
            s += "\tOther Buildings : " + str(self.count_other_buildings)

        return s

    def add_route(self, route):
        self.routes.add(route)

    def get_building_grid(self, exclude_blueprints=False):
        """
        Returns an np.array of objects where each cell points to the building that occupies the corresponding tile
        """
        if exclude_blueprints:
            if not self.__building_grid_no_blueprints__ is None:
                return self.__building_grid_no_blueprints__
        else:
            if not self.__building_grid__ is None:
                return self.__building_grid__

        grid = np.empty(shape=(self.rectangle[1] - self.rectangle[0]), dtype=object)

        for b in self.buildings.values():
            if b.size is None:
                continue

            if b.is_blueprint and exclude_blueprints:
                continue

            if b.guid == 117741:  # Enbesa river slot
                continue

            s = b.rotated_size

            if s is None:
                continue

            p = b.get_relative_position()

            to_int = lambda x: int(round(x))
            for x in range(to_int(p[0]), to_int(p[0] + s[0])):
                for y in range(to_int(p[1]), to_int(p[1] + s[1])):
                    grid[x, y] = b

        if exclude_blueprints:
            self.__building_grid_no_blueprints__ = grid
        else:
            self.__building_grid__ = grid

        return grid

    def get_streets(self):
        """
        Returns an np.array of int where each cell corresponds to a tile
        Uses the special id for roads, canals, quays, etc.
        """

        rect = self.rectangle
        array = self.session.get_streets()[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
        # array = np.transpose(array)
        array = np.flip(array)
        return array

    def __mark_in_range__(self, grid: np.array, b, r: float, update_mode: int):
        r += 1
        n_tiles = []
        c_tiles = []
        p = b.get_relative_position()
        s = b.rotated_size

        if s is None:
            return

        streets = copy.deepcopy(self.get_streets())
        to_int = lambda x: int(round(x))
        for x in range(to_int(p[0]), to_int(p[0] + s[0])):
            for y in range(to_int(p[1]), to_int(p[1] + s[1])):
                if x == p[0] or y == p[1] or x == p[0] + s[0] - 1 or y == p[1] + s[1] - 1:
                    n_tiles.append(np.array([x, y]))
                    streets[x, y] = 3

        at = lambda container, pos: container[pos[0]][pos[1]]

        while r > 0:
            c_tiles = n_tiles
            n_tiles = []

            r -= 1

            for center in c_tiles:
                for direction in [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]:
                    n = center + direction
                    neighbor = at(grid, n)
                    street = A7PARAMS["streets"].get(at(streets, n))

                    if not neighbor is None and isinstance(neighbor, Residence):
                        neighbor.stores[update_mode - 1] = max(neighbor.stores[update_mode - 1], 1 if r >= 1 else r)

                    elif not street is None and street["road"]:
                        n_tiles.append(n)

                        if r >= 1:
                            streets[n[0], n[1]] = 0

    def calculate_coverage(self):
        if not self.__store_coverage_computed__:
            grid = self.get_building_grid()

            for b in self.buildings.values():
                if isinstance(b, Store):
                    self.__mark_in_range__(grid, b, 63.667, b.index)

                """if self.is_th(obj):
                    #print("TH", pos(obj))
                    p = pos(obj) - self.tl
                    center = p + np.array([1.5, 1.5])
                    for x in range(p[0] - r_th, p[0] + r_th+2) :
                        for y in range(p[1] - r_th, p[1] + r_th+2) :
                            h = self.area[x][y]

                            if h is None:
                                continue


                            if np.linalg.norm(center - h.center) <= r_th :
                                h.th = True """

            self.__store_coverage_computed__ = True

    def get_layout(self, options: dict = {}):
        """
        Returns a configuration object for Anno Designer

        options is a dict with strings as keys and lists of strings as values.
        Each key represents an attribute of an Anno Designer object.
        The list of strings represents rules how the value of the attribute is set.
        The list is traversed left to right until the first rule matches.

        The following keys are valid:
        * "exclude": Exclude certain object types (some are class names, so no quotation marks)
                    "outline" (island outline)
                    "blueprints"
                    Possible values are: Farm, Factory, Powerplant, Residence, Store,
                        "StorageBuilding", "Farmfield", "SupportBuilding", "PublicServiceBuilding",
                        "OrnamentalBuilding", "OrnamentalBuilding_Park", ... (basically all Anno Designer templates)

        * "label" : Uses a stat of the building as the label. Possible values are:
                    "residents", "productivity", "count_modules",
                    "upgrades" (guids of buffs affecting the building), "guid",
                    "identifier" (save specific, internal object number)

        * "color" : "store_coverage": Mix blue, green, and red if department, furniture and drug store reach a residence
                    "roof": use roof colors for residences
                    "main_building": Use the same color for a farm and its modules
                    "vary_farms": Slightly vary luminosity of farms
                    "random" : Use random colors for all buildings and modules

        * "icon" : "residents": use resident portraits as icons for residences
                   "no_1x1_ornaments" : don't show icons on 1x1 buildings or ornaments
                   "no_1x1_modules": don't show icons on 1x1 modules

        Usage:
        get_layout(options = {"color" : ["vary_farms", "main_building"], "exclude": [Store], "icon": ["no_1x1", "no_1x1_modules"]})
        """

        objects = []

        e_options = options.get("exclude", {})
        l_options = options.get("label", {})
        c_options = options.get("color", {})
        i_options = options.get("icon", {})

        exclude_blueprints = ("blueprints" in e_options)

        if "store_coverage" in c_options:
            self.calculate_coverage()

        ad_config = self.session.world.ad_config

        # process buildings
        for b in self.buildings.values():
            if isinstance(b, Module) or (exclude_blueprints and b.is_blueprint) or type(b) in e_options:
                continue

            if b.guid == 117741:  # Enbesa river slot
                continue

            obj = b.generate_ad_object()

            if obj is None:
                continue

            if obj["Template"] in e_options:
                continue

            if "residents" in i_options and b.guid in ad_config.resident_icons:
                obj["Icon"] = ad_config.resident_icons[b.guid]

            if "no_1x1_ornaments" in i_options and obj["Size"] == "1,1":
                obj["Icon"] = None

            l: str
            for l in l_options:
                if not l in b.__dict__:
                    continue

                val = getattr(b, l)

                if not val is None:
                    if l == "productivity":
                        val = "{:.0%}".format(val)

                    obj["Label"] = str(val)
                    break

            main_building = False

            if isinstance(b, Residence) and obj["Size"] == "3,3" and "store_coverage" in c_options:
                c = 255 * np.array(b.stores)
                obj["Color"] = {
                    "A": 255,
                    "R": int(c[2]),
                    "G": int(c[1]),
                    "B": int(c[0])
                }

            elif isinstance(b, Store) and "store_coverage" in c_options:
                obj["Color"] = {
                    "A": 255,
                    "R": 255 if b.index == 3 else 0,
                    "G": 255 if b.index == 2 else 0,
                    "B": 255 if b.index == 1 else 0
                }

            elif "roof" in c_options and b.guid in ad_config.roof_colors:
                obj["Color"] = ad_config.roof_colors[b.guid]

            elif "random" in c_options:
                val = hash(abs(b.identifier).to_bytes(8, byteorder='little'))
                red = abs(val % 256)
                val = int(val / 256)
                green = abs(val % 256)
                val = int(val / 256)
                blue = abs(val % 256)

                obj["Color"] = {
                    "A": obj["Color"]["A"],
                    # "R": random.randrange(0, 255),
                    "R": red,
                    "G": green,
                    "B": blue,
                }

            elif isinstance(b, Farm) and "vary_farms" in c_options:
                h = hash(abs(b.identifier).to_bytes(8, byteorder='little'))
                obj["Color"] = vary_color(obj["Color"], (h % 1001) / 1000)

            if "main_building" in c_options:
                main_building = True

            if isinstance(b, Farm) and not Module in e_options:
                for m in b.modules:
                    if m is None:
                        continue

                    m_obj = m.generate_ad_object()

                    if m_obj is None:
                        continue

                    if main_building:
                        m_obj["Color"] = obj["Color"]

                    if "no_1x1_modules" in i_options and m_obj["Size"] == "1,1":
                        m_obj["Icon"] = None

                    for l in l_options:
                        if not l in m.__dict__:
                            continue

                        val = getattr(m, l)

                        if not val is None:
                            if l == "productivity":
                                val = "{:.0%}".format(val)

                            m_obj["Label"] = str(val)
                            break

                    objects.append(m_obj)

            objects.append(obj)

        # process streets
        grid = np.copy(self.get_building_grid(exclude_blueprints=exclude_blueprints))

        exclude_quay = ("quay" in e_options)

        streets = self.get_streets()
        ad_config = self.session.world.ad_config
        for x in range(len(streets)):
            for y in range(len(streets[0])):
                street = A7PARAMS["streets"].get(streets[x, y])
                if street is None:
                    continue

                if exclude_quay and is_quay(street["id"]):
                    continue

                if not grid[x, y] is None and not street.get("road"):
                    continue

                obj = ad_config.get_template(street.get("guid"), self.session.guid)
                if obj is None:
                    obj = {
                        "Guid": street.get("guid"),
                        "Identifier": street.get("identifier"),
                        "Template": street.get("template"),
                        "Size": "1,1",
                        "Position": "{},{}".format(x, y),
                        "Road": True if street.get("road") else False
                    }

                    if street.get("rail"):
                        obj["Icon"] = "A7_rails"

                obj["Borderless"] = True
                obj["Color"] = street.get("color")

                objects.append(obj)
                grid[x, y] = True

        # process outline
        if ("outline" not in e_options and
                ad_config.has_island_outline(self.island_template_name) and
                self.island_template_name in A7PARAMS["island_sizes"]):

            trafo = lambda x: [x[1], size[0] - x[0] - 1]
            size = np.array(A7PARAMS["island_sizes"][self.island_template_name])

            if self.rotation == 1:
                trafo = lambda x: [size[0] - x[0] - 1, size[1] - x[1] - 1]
            elif self.rotation == 2:
                trafo = lambda x: [size[1] - x[1] - 1, x[0]]
            elif self.rotation == 3:
                trafo = lambda x: x

            for obj in ad_config.get_island_outline(self.island_template_name):
                pos = trafo([int(x) for x in obj["Position"].split(",")])
                if grid[pos[0], pos[1]] is not None:
                    continue

                obj = copy.deepcopy(obj)
                obj["Position"] = "{},{}".format(pos[0], pos[1])
                obj["Road"] = False
                objects.append(obj)

        return {
            "FileVersion": 4,
            "LayoutVersion": "1.0.0.0",
            "Modified": str(datetime.now().isoformat()),
            "Objects": objects
        }

    def get_upgrades_summary(self):
        residences = dict()
        index = 0
        residence_indices = dict()
        for r in A7PARAMS["residence_buildings"]:
            residences[r["guid"]] = r
            residence_indices[r["guid"]] = index
            index += 1

        effects = dict()
        for e in A7PARAMS["residence_effects"]:
            effects[e["guid"]] = e

        summary = dict()
        blueprints = ResidenceEffectsSummaryEntry(None, effects)
        all_residences = ResidenceEffectsSummaryEntry(None, effects)

        for b in self.buildings.values():
            if b.guid not in residences:
                continue

            if b.guid not in summary:
                summary[b.guid] = ResidenceEffectsSummaryEntry(residences[b.guid], effects)

            if b.is_blueprint:
                blueprints.building_counter += 1
            else:
                summary[b.guid].add_list(b.upgrades)
            all_residences.add_list(b.upgrades)

        area = None
        visited = set()
        ad_config = self.session.world.ad_config
        for b in self.buildings.values():
            if not isinstance(b, Guildhouse) or not b.is_townhall():
                continue

            if area is None:
                area = self.get_building_grid(False)

            def coords_2d(b):
                return np.array([b.position[0], b.position[2]])

            p = b.get_relative_position()
            center = coords_2d(b)
            r_th = int(ad_config.get_template(b.guid)["Radius"])
            for x in range(p[0] - r_th, p[0] + r_th + 2):
                for y in range(p[1] - r_th, p[1] + r_th + 2):
                    h = area[x][y]

                    if h is None or h.guid not in residences or h in visited:
                        continue

                    if np.linalg.norm(center - coords_2d(h)) <= r_th:
                        visited.add(h)
                        if h.is_blueprint:
                            blueprints.townhall_counter += 1
                            all_residences.townhall_counter += 1
                        else:
                            if h.guid not in summary:
                                summary[h.guid] = ResidenceEffectsSummaryEntry(residences[h.guid], effects)

                            summary[h.guid].townhall_counter += 1
                            all_residences.townhall_counter += 1

        l = list(summary.values())
        l.sort(key=lambda s: residence_indices[s.residence["guid"]])
        return {
            "blueprints": blueprints,
            "all": all_residences,
            "residences": l
        }


class Session:
    """
    Defines the following attributes:
    * node: ET._Element
    * world: World
    * guid: int
    * name: str
    * dimensions: np.array storing x and y dimension
    * streets: np.array of size dimensions[0] x dimensions[1]
    * map_template: ET._Element

    To iterate all islands, use:
    for i in self.islands.values()
    """

    def __init__(self, node: ET._Element, identifier: int, world, extract_NPC_islands=False):
        manager = node.find("./SessionData/BinaryData/Content/GameSessionManager")

        self.node = node
        self.world = world
        self.guid = hex_to_int(node.find("./SessionDesc/SessionGUID"))
        self.name = None
        if self.guid in A7PARAMS["session_names"]:
            self.name = A7PARAMS["session_names"][self.guid][LANG]
        self.street_node = manager.find("./WorldManager/StreetMap")
        self.__streets__ = None
        self.dimensions = np.array(
            [hex_to_int(self.street_node.find(".//x")), hex_to_int(self.street_node.find(".//y"))])

        self.islands = dict()
        self.islands_by_name = dict()

        i_id = None
        for i in manager.findall("./AreaInfo/None"):
            if has_value(i):
                i_id = hex_to_int(i)
                continue

            owner = hex_to_int(i.find("Owner/id"))

            if owner is None:
                continue

            name = hex_to_utf16(i.find("./CityName"))
            if name is None:
                name = hex_to_int(i.find("./CityNameGuid"))

                if name is None or not name in A7PARAMS["city_names"]:
                    name = "[{}]".format(name)
                else:
                    name = A7PARAMS["city_names"][name][LANG]

            if owner < 4:
                island = Island(i, i_id, name, self)
            elif extract_NPC_islands:
                island = NPCIsland(i, i_id, name, self)
            else:
                continue

            self.islands_by_name[name] = island
            self.islands[i_id] = island

        for i in manager.find("./AreaManagers"):

            identifier = int(i.tag.split("_")[1])
            if identifier in self.islands:
                self.islands[identifier].__set_area_manager__(i)

        self.map_template = manager.find("./MapTemplate")
        for elem in self.map_template.findall("./TemplateElement/Element"):
            path = hex_to_utf16(elem.find("./MapFilePath"))
            position = hex_to_int_list(elem.find("./Position"))

            if path is None or position is None:
                continue

            position = np.array(position)
            path = pathlib.Path(path)
            size = np.array([200, 200])
            if path.stem in A7PARAMS["island_sizes"]:
                size = np.array(A7PARAMS["island_sizes"][path.stem])

            for i in self.islands.values():
                if len(i.buildings) == 0:
                    continue

                is_inside = True
                for b in i.buildings.values():
                    x = b.position[0]
                    y = b.position[2]

                    if x < position[0] or x > position[0] + size[0] or y < position[1] or y > position[1] + size[1]:
                        is_inside = False
                        break

                if is_inside:
                    i.__set_island_template__(elem, np.array([position, position + size]), path.stem)
                    break

    def get_island(self, name: str) -> Island:
        '''
        Args:
            name (str): Case sensitive name of the island.

        Returns:
            Island: Corresponding Island or None if not in savegame.
                    If multiple islands have the same name, the first
                    one encountered is returned

        Example:island.world
            get_island("Crown Falls")
        '''

        return self.islands_by_name.get(name)

    def get_island_by_id(self, idx: int) -> Island:
        return self.islands.get(idx)

    def get_streets(self):
        if self.__streets__ is None:
            arr = self.street_node.find("./StreetID/val")
            if arr is None:
                arr = self.street_node.find("./IDVar")
            street_arr = hex_to_int_list(arr, 1, limit_elements=self.dimensions[0] * self.dimensions[1])

            if street_arr is None:
                self.__streets__ = np.zeros(shape=self.dimensions, dtype=int)
            else:
                self.__streets__ = np.array(street_arr).reshape(self.dimensions)

        return self.__streets__

    def __str__(self):
        if self.guid in A7PARAMS["session_names"]:
            return A7PARAMS["session_names"][self.guid][LANG]
        else:
            return "Unknown Session"


class Building:
    """
    Defines the following attributes:
    * node: ET._Element
    * island: Island
    * guid: int
    * identifier: int
    * is_blueprint: bool
    * upgrades: list of int (GUIDs of applied effects)
    * productivity: float (if available)
    * position: np.array of floats (x,y,z) where
            the x-axis points north east
            the y-axis is perpendicular to the water surface
            the z-axis points north west
    * direction: float (rotation angle in radians around y-axis, in multiples of pi / 2)
    * size: np.array of int where
            the x-axis points south east
            the y-axis points south west

    * streets: np.array of size dimensions[0] x dimensions[1]
    * map_template: ET._Element
    """

    def __init__(self, node: ET._Element, island):
        self.node = node
        self.island = island
        self.guid = hex_to_int(node.find("guid"))
        self.identifier = hex_to_int(node.find("ID"))
        self.is_blueprint = not node.find("StateBits") is None
        self.position = np.array(hex_to_float_list(node.find("Position")))
        self.size = None
        self.direction = hex_to_float(self.node.find("Direction"))
        if self.direction is None:
            self.direction = 0
        self.discrete_rotation = int(round(self.direction / math.pi * 2) % 4)

        self.bounding_rectangle = None
        if self.guid in A7PARAMS["decentered_buildings"]:
            corners = np.array(A7PARAMS["decentered_buildings"][self.guid]).transpose()

            if len(corners[0]) >= 8:
                # skip second building blocker of mines
                diag0 = np.linalg.norm(np.max(corners[:, 0:4], axis=1) - np.min(corners[:, 0:4], axis=1))
                diag1 = np.linalg.norm(np.max(corners[:, 4:8], axis=1) - np.min(corners[:, 4:8], axis=1))

                if diag1 > diag0 + 0.1:
                    corners = corners[:, 0:4]

            m_rot = np.array([
                [math.cos(self.direction), -math.sin(self.direction)],
                [math.sin(self.direction), math.cos(self.direction)]
            ])

            to_int = lambda arr: np.array([int(round(val)) for val in arr])
            self.size = to_int((np.max(corners, axis=1) - np.min(corners, axis=1))[::-1])
            corners = m_rot @ corners
            self.bounding_rectangle = np.array([np.min(corners, axis=1), np.max(corners, axis=1)])
            self.rotated_size = to_int((self.bounding_rectangle[1] - self.bounding_rectangle[0])[::-1])
        else:

            t = island.session.world.ad_config.get_template(self.guid, self.island.session.guid)
            if not t is None and not t["BuildBlocker"] is None:
                sz = t["BuildBlocker"]
                self.size = np.array([sz["z"], sz["x"]])

            if not self.size is None:
                rotated = self.discrete_rotation % 2 == 1
                self.rotated_size = np.array([self.size[1], self.size[0]]) if rotated else self.size
            else:
                raise Exception(self.guid, t, self, node)

        self.upgrades = []

        upgrades = node.find("./UpgradeList/UpgradeGUIDs")
        if has_value(upgrades):
            self.upgrades = hex_to_int_list(upgrades)

        self.productivity = hex_to_float(node.find(".//CurrentProductivity"))  # under Powerplant or Factory7

    def get_relative_position(self):
        """
        Returns the integer 2D coordinates of the northern corner of the bounding box
        relative to the northern edge of the island
        Uses the same coordinate system as the size attribute
        """

        tl = self.island.rectangle[1]
        if self.bounding_rectangle is None:
            return np.array([int(tl[1] - round(self.position[2] + self.rotated_size[0] / 2)),
                             int(tl[0] - round(self.position[0] + self.rotated_size[1] / 2))])

        rect = self.position[::2] + self.bounding_rectangle[1]
        return np.array([int(round(val)) for val in (tl - rect)[::-1]])

    def generate_ad_object(self):
        """
        generates a representation of this object suitable for the Anno Designer
        """

        if self.rotated_size is None:
            return None

        ad_config = self.island.session.world.ad_config
        if not ad_config.has_template(self.guid, self.island.session.guid):
            return None
        obj = copy.deepcopy(ad_config.get_template(self.guid, self.island.session.guid))

        del obj["BuildBlocker"]

        rot = self.discrete_rotation
        if self.guid in A7PARAMS["direction_offsets"]:
            rot += A7PARAMS["direction_offsets"][self.guid]
        rot = rot % 4
        obj["Direction"] = A7PARAMS["directions"][rot]

        pos = self.get_relative_position()
        obj["Size"] = "{},{}".format(self.rotated_size[0], self.rotated_size[1])
        obj["Position"] = "{},{}".format(pos[0], pos[1])

        return obj


class Residence(Building):
    """
    Defines the following attributes:
    * residents: int
    * stores: 3-item list of int (values are either 0, 0.666 or 1)
              denoting the fulfillment of Department, Furniture and Drug store
    """

    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)
        self.residents = hex_to_int(node.find("./Residence7/ResidentCount"))
        self.stores = [0, 0, 0]


class Farm(Building):
    """
    Defines the following attributes:
    * modules: np.array of floats (nx2) array denoting the positions of modules
    * count_modules: int
    """

    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)
        self.modules = []
        self.modules_count = 0

    def process_modules(self, buildings):
        arr = self.node.find("./ModuleOwner/BinArray")
        if arr is not None:
            return self.process_modules_gu16(buildings)
        else:
            return self.process_modules_pre_gu16(buildings)

    def process_modules_gu16(self, buildings):
        arr = hex_to_int_list(self.node.find("./ModuleOwner/BinArray"), 8)
        if len(arr) == 0:
            return 0

        def add(i):
            m = buildings.get(i)
            if m is None:
                return 0

            convert = 0
            if not isinstance(m, Module):
                m = Module(m.node, m.island)
                buildings[i] = m
                convert = 1

            self.modules.append(m)
            return convert

        converted = 0
        identifier = arr[0]
        converted += add(identifier)

        # unclear why there is one more entry than modules and this entry is not necessarily 0
        for i in range(1, len(arr) - 1):
            identifier += arr[i] + 1
            converted += add(identifier)

        self.modules_count = len(self.modules)
        return converted

    def process_modules_pre_gu16(self, buildings):
        for k in ["AdditionalModule", "FertilizerModule"]:
            m = hex_to_int(self.node.find("./ModuleOwner/{}/ObjectID".format(k)))
            m = buildings.get(m)

            if m is not None:
                self.modules.append(m)

        for b in buildings.values():
            if isinstance(b, Module):
                parent = buildings.get(b.main_building)

                if not self == parent:
                    continue

                b.main_building = self

                if not b in self.modules:
                    self.modules.append(b)

        self.modules_count = len(self.modules)
        return 0


class Module(Building):
    """
    Defines the following attributes:
    * main_building: Farm
    """

    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)
        self.main_building = hex_to_int(node.find("./BuildingModule/ParentFactoryID"))


class Factory(Building):
    def __init__(self, node, island):
        super().__init__(node, island)


class Powerplant(Building):
    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)

    def generate_ad_object(self):
        obj = super().generate_ad_object()
        if obj is None:
            return None
        inf_range = int(obj["InfluenceRange"])
        inf_range -= 2
        for upgrade in self.upgrades:
            if upgrade in A7PARAMS["range_extension_buffs"]:
                inf_range += A7PARAMS["range_extension_buffs"][upgrade]

        obj["InfluenceRange"] = int(inf_range * 1.5)
        obj["PavedStreet"] = True

        return obj


class Guildhouse(Building):
    """
    Defines the following attributes:
    * items: list of int (GUIDs of equipped items)
    """

    def __init__(self, node, island):
        super().__init__(node, island)
        self.items = []
        for guid in node.findall("ItemContainer/SocketContainer/SocketItems/None/GUID"):
            self.items.append(hex_to_int(guid))

    def is_townhall(self):
        ad_config = self.island.session.world.ad_config

        if not ad_config.has_template(self.guid, self.island.session.guid):
            return False
        obj = ad_config.get_template(self.guid, self.island.session.guid)
        return not obj.get("Icon") is None and "A7_townhall" in obj.get("Icon")


class Store(Building):
    """
    Defines the following attributes:
    * index: int (store index, see get_index)
    """

    def __init__(self, node: ET._Element, index, island):
        super().__init__(node, island)
        self.index = index

    @staticmethod
    def get_index(ad_config: ADConfig, guid: int):
        """ Returns 
        0 = No Store, 
        1 = Department Store, 
        2 = Furniture Store,
        3 = Drug Store"""

        if not ad_config.has_template(guid):
            return 0

        t = ad_config.get_template(guid)["Identifier"]

        if "DepartmentStore" in t:
            return 1
        elif "FurnitureStore" in t:
            return 2
        elif "Pharmacy" in t:
            return 3

        return 0


class World:
    """
    Defines the following attributes:
    * interpreter: Interpreter (contains XML tree of savegame and applies rules to decode values)
    * node: ET._Element
    * playtime: int (elapsed in-game time in milliseconds)
    * seed: int
    * profile_name: str
    * ad_config: ADConfig (stores building information read from the presets.json and color.json of Anno Designer)

    To iterate all sessions, use:
    for s in self.sessions.values()

    To iterate all trade routes, use:
    for r in self.trade_routes
    """

    def __init__(self, interpreter, extract_routes=False, progress_bar=None):
        if progress_bar is None:
            print("Analyzing ...")

        self.interpreter = interpreter
        self.node = interpreter.tree.getroot()
        node = self.node
        self.sessions = dict()
        self.ships = dict()
        self.trade_routes = []
        self.playtime = hex_to_int(node.find("MetaGameManager/GameCount"))
        self.seed = hex_to_int(node.find("CorporationProfile/GameSetup/GameSeed"))
        self.profile_name = hex_to_utf16(node.find("CorporationProfile/GameSetup/SavegameFolderW"))

        self.ad_config = ADConfig()

        s_id = None
        session_nodes = node.findall("./MetaGameManager/GameSessions/None")
        count_sessions = len(session_nodes) / 2

        for i in session_nodes:
            if has_value(i):
                s_id = hex_to_int(i)
                continue

            session = Session(i, s_id, self, extract_routes)
            self.sessions[session.guid] = session

            if progress_bar is not None:
                progress_bar.value = 0.65 + 0.3 * len(self.sessions) / count_sessions

        if extract_routes:
            for s in node.findall(
                    "./MetaGameManager/GameSessions/None/SessionData/BinaryData/Content/GameSessionManager/AreaManagers/*/AreaObjectManager/GameObject/objects/None"):
                guid = hex_to_int(s.find("guid"))
                idx = hex_to_int(s.find("MetaPersistent/MetaID"))
                if guid is None or idx is None:  # or guid not in A7PARAMS["ships"]:
                    continue

                self.ships[idx] = Ship(s, guid, idx, self)

            for i in node.findall("./MetaGameManager/SessionTradeRouteManager/RouteMap/None"):
                # skip ids and NPC trade routes
                if not has_value(i) and hex_to_int(i.find("./Owner/id")) < 4:
                    self.trade_routes.append(Route(i, self))

        if progress_bar is None:
            print("Finished. Go ahead!")
        else:
            progress_bar.value = 1

    def get_session(self, name: str) -> Session:
        '''
        Args:
            name (str): Case sensitive name of the session (in any language), 
                        e.g. "Old World", "New World", "Cape Trelawney", "The Arctic", "Enbesa"

        Returns: 
            Session: Corresponding Session or None if not in savegame.

        Throws:
            ValueError: Invalid name provided.

        Example:
            get_session("Cape Trelawney")
        '''

        found = False
        for guid in A7PARAMS["session_names"]:
            if name in A7PARAMS["session_names"][guid].values():
                found = True
                break

        if not found:
            raise ValueError("{} is not a session".format(name))

        return self.sessions.get(guid)

    def get_island(self, name: str) -> Island:
        '''
        Args:
            name (str): Case sensitive name of the island.

        Returns: 
            Island: Corresponding Island or None if not in savegame.
                    If multiple islands have the same name, the first
                    one encountered is returned

        Example:
            get_island("Crown Falls")
        '''

        for s in self.sessions.values():
            i = s.get_island(name)

            if not i is None:
                return i

    def get_island_by_id(self, idx: int) -> Island:
        for s in self.sessions.values():
            i = s.get_island_by_id(idx)

            if not i is None:
                return i

    def print_island_summary(self):
        for s_guid in self.sessions:
            if not s_guid in A7PARAMS["session_names"] or len(self.sessions[s_guid].islands) == 0:
                continue

            print(A7PARAMS["session_names"][s_guid][LANG], ":",
                  ", ".join([i.name for i in self.sessions[s_guid].islands.values()]))

    def __str__(self):
        return "Profile: {}\tSeed: {}\tPlaytime: {:.1f}h".format(self.profile_name, self.seed, self.playtime / 3600)

    # def show_island_dropdown(self):
    #     options = []
    #
    #     for s in self.sessions.values():
    #         for i in s.islands.values():
    #             options.append((i.name, i))
    #
    #     widget = Dropdown(options=options)
    #
    #     def set_island(*args):
    #         self.selected_island = widget.value
    #
    #     widget.observe(set_island)
    #     display(widget)
