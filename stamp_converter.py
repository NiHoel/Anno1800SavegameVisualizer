import argparse
import traceback
import pathlib
import shutil
import subprocess
import sys
import zlib

from tools.a7s_model import *

REGION_TO_SESSION = {
    5000000: 180023,
    5000001: 180025,
    160001: 180045,
    114327: 112132,
    650: 655,
    24719: 24734,
    1583: 100811,
    5858: 5864,
}

DEFAULT_OPTIONS = {
    "exclude": [],
    "color": ["main_building", "vary_farms"],
    "icon": ["residents"],
    "type": ["png"],
}

def execute(args, verbose=False):
    exit_code = subprocess.call(args, stdout=subprocess.DEVNULL)

    if exit_code == 0:
        return

    executable = pathlib.Path(args[0]).stem + ".exe"
    if verbose:
        print(subprocess.list2cmdline(args))

    raise Exception(
        "Executing {} failed. Please ensure that the file is not corrupt or try running this application in a different directory.".format(
            executable))

def extract_stamp(path: pathlib.Path, temp_path, xml_path = None):
    temp_file = temp_path / "stamp"
    temp_bin_file = temp_file.with_suffix(".bin")
    tools_path = pathlib.Path(os.getcwd() + "/tools")

    content = open(path, 'rb').read()
    if content[0:2] == b'\x78\xda':
        if args.verbose:
            print("Decompress to", temp_bin_file)
        content = zlib.decompress(content)
        with open(temp_bin_file, 'wb') as f:
            f.write(content)
    else:
        shutil.copy(path, temp_bin_file)

    if xml_path is not None:
        if args.verbose:
            print("Decompress", xml_path)
        execute([str(tools_path / "FileDBReader/FileDBReader.exe"), "decompress",
                 "-i", str(tools_path / "FileDBReader/FileFormats/stamp.xml"),
                 "-f", str(temp_bin_file), "-y"], args.verbose)
        shutil.copy(temp_file.with_suffix(".xml"), xml_path)

    if args.verbose:
        print("Decompress", temp_bin_file.with_suffix(".xml"))
    execute([str(tools_path / "FileDBReader/FileDBReader.exe"), "decompress",
             "-f", str(temp_bin_file), "-y"], args.verbose)

    if args.verbose:
        print("Parse XML tree")
    parser = ET.XMLParser(huge_tree=True)
    return ET.parse(str(temp_file.with_suffix(".xml")), parser)


def stamp_to_json(tree, ad_config, options = DEFAULT_OPTIONS):
    region = hex_to_int(tree.find("StampPath"))
    session = REGION_TO_SESSION.get(region)

    objects = []
    def get(name):
        o = getattr(options, name)
        return [] if o is None else o

    e_options = get("exclude")
    c_options = get("color")
    i_options = get("icon")

    exclude_blueprints = ("blueprints" in e_options)
    exclude_quay = ("quay" in e_options)


    for node in tree.getroot().findall("BuildingInfo/"):
        guid = hex_to_int(node.find("./GUID"))
        complex_owner_id = hex_to_int(node.find("./ComplexOwnerID"))
        direction = hex_to_float(node.find("./Dir"))
        if direction is None:
            direction = 0
        rot = int(round(direction / math.pi * 2) % 4)
        pos = hex_to_float_list(node.find("./Pos"), 4)
        if pos is None:
            pos = [0,0]
        
        if args.verbose and (pos is None or guid is None):
            print("Skip node because attribute is missing:")
            print("-"*60)
            print("GUID:", guid)
            print("ComplexOwnerID:", complex_owner_id)
            print("Pos:", pos)
            print("Dir:", direction)
            ET.tostring(node, pretty_print=True)
            print("-"*60)
            
            continue

        if not ad_config.has_template(guid, session):
            continue
        obj = copy.deepcopy(ad_config.get_template(guid, session))

        bounding_rectangle = None
        if guid in A7PARAMS["decentered_buildings"]:
            corners = np.array(A7PARAMS["decentered_buildings"][guid]).transpose()

            if len(corners[0]) >= 8:
                # skip second building blocker of mines
                diag0 = np.linalg.norm(np.max(corners[:, 0:4], axis=1) - np.min(corners[:, 0:4], axis=1))
                diag1 = np.linalg.norm(np.max(corners[:, 4:8], axis=1) - np.min(corners[:, 4:8], axis=1))

                if diag1 > diag0 + 0.1:
                    corners = corners[:, 0:4]

            m_rot = np.array([
                [math.cos(direction), -math.sin(direction)],
                [math.sin(direction), math.cos(direction)]
            ])

            to_int = lambda arr: np.array([int(round(val)) for val in arr])
            size = to_int((np.max(corners, axis=1) - np.min(corners, axis=1))[::-1])
            corners = m_rot @ corners
            bounding_rectangle = np.array([np.min(corners, axis=1), np.max(corners, axis=1)])
            rotated_size = to_int((bounding_rectangle[1] - bounding_rectangle[0])[::-1])
            pos += bounding_rectangle[1]
            tl_pos = [-pos[1] +0.5, -pos[0]+0.5]
        else:

            if not obj["BuildBlocker"] is None:
                sz = obj["BuildBlocker"]
                size = np.array([sz["z"], sz["x"]])
                rotated = rot % 2 == 1
                rotated_size = np.array([size[1], size[0]]) if rotated else size
        
            tl_pos = [-pos[1] - rotated_size[0]/2 + 0.5, -pos[0] - rotated_size[1]/2 + 0.5]
      

        del obj["BuildBlocker"]

        if guid in A7PARAMS["direction_offsets"]:
            rot += A7PARAMS["direction_offsets"][guid]
        rot = rot % 4
        obj["Direction"] = A7PARAMS["directions"][rot]

        obj["Size"] = "{},{}".format(rotated_size[0], rotated_size[1])
        obj["Position"] = "{},{}".format(round(tl_pos[0]), round(tl_pos[1]))

        if "residents" in i_options and guid in ad_config.resident_icons:
            obj["Icon"] = ad_config.resident_icons[guid]

        if "no_1x1_ornaments" in i_options and obj["Size"] == "1,1":
            obj["Icon"] = None

        if "roof" in c_options and guid in ad_config.roof_colors:
            obj["Color"] = ad_config.roof_colors[guid]
        elif complex_owner_id is not None and "vary_farms" in c_options:
            h = hash(abs(complex_owner_id).to_bytes(8, byteorder='little'))
            obj["Color"] = vary_color(obj["Color"], (h % 1001) / 1000)

        objects.append(obj)
    
    def get_street_object(guid, x, y):
        obj = ad_config.get_template(guid, session)
        if obj is None:
            obj = {
                "Guid": street.get("guid"),
                "Identifier": street.get("identifier"),
                "Template": street.get("template"),
                "Size": "1,1",
                "Position": "{},{}".format(x, y),
                "Road": True if street.get("road") else False
            }
        else:
            obj["Position"] = "{},{}".format(x, y)

        obj["Borderless"] = True
        obj["Color"] = street.get("color")

        return obj

    def trafo(coords, y = None):
        x = coords
        if y is None:
            y = coords[1]
            x = coords[0]
        return round(-y), round(-x)

    index = 0
    street = A7PARAMS["streets"].get(1)
    street_dict = dict()
    for node in tree.getroot().findall("StreetInfo/"):
        if index % 2 == 0:
            guid = hex_to_int(node)
            for s in A7PARAMS["streets"].values():
                if guid == s["guid"]:
                    street = s
                    break
        else:
            if exclude_quay and is_quay(street["id"]):
                continue

            for tile_node in node.getchildren():
                pos = tile_node.getchildren()
                x,y = trafo(hex_to_float(pos[0]), hex_to_float(pos[1]))

                obj = get_street_object(street.get("guid"), x, y)

                objects.append(obj)
                street_dict[obj["Position"]] = obj

        index += 1


    rail =  A7PARAMS["streets"].get(3)
    for track_node in tree.getroot().findall("RailwayInfos/"):
        start_end = list(track_node.getchildren())
        start = hex_to_int_list(start_end[0])
        end = hex_to_int_list(start_end[1])

        sx, sy = trafo(start)
        ex, ey = trafo(end)

        dx = 0
        dy = 0

        x = sx
        y = sy

        if sx < ex:
            dx = 1
        elif sx > ex:
            dx = -1

        if sy < ey:
            dy = 1
        elif sy > ey:
            dy = -1

        def add_rail(x,y):
            obj = street_dict.get("{},{}".format(x, y))
            if obj is None:
                obj = get_street_object(rail.get("guid"), x, y)
                objects.append(obj)

            obj["Icon"] = "A7_rails"

        if not dx == 0:
            for x in range(sx, ex + dx, dx):
                add_rail(x,y)
        if not dy == 0:
            for y in range(sy, ey + dy, dy):
                add_rail(x,y)

    
    return {
        "FileVersion": 4,
        "LayoutVersion": "1.0.0.0",
        "Modified": str(datetime.now().isoformat()),
        "Objects": objects
    }



def convert_stamp(path: pathlib.Path, ad_config, args):
    temp_path = TEMP_PATH/ "stamp_convert" / path.parent.name / path.stem

    if args.verbose:
        print("Create", temp_path)
    temp_path.mkdir(parents=True, exist_ok=True)

    dst_path = path.parent
    if args.destination is not None:
        dst_path = args.destination

    def path_for(suffix):
        return (dst_path / path.stem).with_suffix("." + suffix)

    def write_file(suffix):
        path = path_for(suffix)
        return suffix in args.type and (args.overwrite or not path.exists())

    if args.verbose:
        print("Check file to create")
    create_file = False

    for t in args.type:
        if write_file(t):
            create_file = True
            break

    if not create_file:
        if args.verbose:
            print("Skip because no file to create", path)
        return

    print("Processing", path)
    xml_path = path_for("xml")
    tree = extract_stamp(path, temp_path, xml_path if write_file("xml") else None)

    if args.verbose:
        print("Convert stamp to json")
    ad = stamp_to_json(tree, ad_config, args)
    if ad is None or len(ad["Objects"]) == 0:
        if args.verbose:
            print("Skip because no object in ad")
        return
    ad_json = json.dumps(ad)


    ad_path = str(temp_path / "stamp.ad")
    if args.verbose:
        print("Save temp ad", ad_path)
    with open(ad_path, "w") as f:
        f.write(ad_json)

    if write_file("ad"):
        if args.verbose:
            print("Save ad", path_for("ad"))
        shutil.copy(ad_path, path_for("ad"))

    if write_file("png"):
        png_path = path_for("png")

        if args.verbose:
            print("Save png", png_path)

        e_options = getattr(args, "exclude")
        if e_options is None:
            e_options = []
        render_statistics = "statistics" not in e_options
        render_grid = "grid" not in e_options
        if args.overwrite or not png_path.exists():
            execute(
                [os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe",
                 "export", ad_path, str(png_path),
                 "--renderGrid", str(render_grid),
                 "--renderStatistics", str(render_statistics),
                 "--renderVersion", "False",
                 "--gridSize", str(args.gridSize)], args.verbose)


if __name__ == "__main__":
    os.chdir(str(pathlib.Path(sys.argv[0]).parent))

    parser = argparse.ArgumentParser(description='Convert stamps into Anno Designer files and images.')
    parser.add_argument('source', metavar='source', type=str, action='extend', nargs='*')
    parser.add_argument('-s', '--source', type=str, action='extend', nargs='*',
                        help='Files or folders to be converted. If the argument is not provided, all stamps in the default location are processed.')
    parser.add_argument('-d', '--destination', type=str, nargs='?',
                        help='Destination path. If the argument is not provided, output files are saved next to their source files.')
    parser.add_argument('-o', "--overwrite", action='store_true', help="Overwrite destination files")
    parser.add_argument('-g', "--gridSize", type=int, default=20, help="Length of one tile (in the output image) in pixels. Default: 20")
    parser.add_argument('-t', "--type", type=str, action='extend', nargs='*', help="{} {}".format('''File types to create. Specify one or more of the following strings:
                                                                         "png" (image), "ad" (Anno Designer file), "xml". If the argument is not provided, the following values are used by default: ''', DEFAULT_OPTIONS["type"]))
    parser.add_argument('-c', "--color", type=str, action='extend', nargs='*', help="{} {}".format('''Change colour of buildings. Use zero (empty string), one or more of the following strings as values for the argument:
    "roof": use roof colors for residences;
    "main_building": Use the same color for a farm and its modules;
    "vary_farms": Slightly vary luminosity of farms;
    "random" : Use random colors for all buildings and modules.
    If the argument is not provided, the following values are used by default: ''', DEFAULT_OPTIONS["color"]))
    parser.add_argument('-i', "--icon", type=str, action='extend', nargs='*', help="{} {}".format('''Change icon of buildings. 
    "residents": use resident portraits as icons for residences;
    "no_1x1_ornaments" : don't show icons on 1x1 buildings or ornaments;
    "no_1x1_modules": don't show icons on 1x1 modules.
    If the argument is not provided, the following values are used by default: ''', DEFAULT_OPTIONS["icon"]))
    #parser.add_argument('-l', "--label", type=str, action='extend', nargs='*', help='''Uses a stat of the building as the label. Possible values are:
    #"residents", "productivity", "count_modules",
    #"upgrades" (guids of buffs affecting the building), "guid",
    #"identifier" (save specific, internal object number)''')
    parser.add_argument('-e', "--exclude", type=str, action='extend', nargs='*', help="{} {}".format('''Exclude certain object types:
    "statistics" (statistics panel at the right of the exported image), "blueprints", "quay", "StorageBuilding", "Farmfield", "SupportBuilding", "PublicServiceBuilding",
    "OrnamentalBuilding", "OrnamentalBuilding_Park", ... (basically all Anno Designer templates)
    If the argument is not provided, the following values are used by default: ''', DEFAULT_OPTIONS["exclude"]))
    parser.add_argument('-v', "--verbose", action='store_true', help="verbose output")

    args = parser.parse_args()
    if args.verbose:
        print("Source:", args.source)
    if args.source is None or len(args.source) == 0:
        args.source = [get_documents_path() / "Anno 1800" / "stamps"]

    for option in DEFAULT_OPTIONS.keys():
        value = getattr(args, option)
        if value is None or len(value) == 0:
            setattr(args,option, DEFAULT_OPTIONS[option])

    if args.destination is not None:
        try:
            args.destination = pathlib.Path(args.destination)
            args.destination.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print("Could not create destination path: " + str(e))
            os.system("PAUSE")
            exit(1)

    error_count = 0
    ad_config = ADConfig()
    for entry in args.source:
        entry = pathlib.Path(entry) # no resolve

        if not entry.exists():
            continue

        if entry.is_dir():
            paths = list(entry.glob("**/*"))
        else:
            paths = [entry]

        for path in paths:
            try:
                if path.is_file() and path.suffix == "":

                    convert_stamp(path, ad_config, args)
            except Exception as e:
                error_count += 1
                if args.verbose:
                    print("Exception while converting:")
                    print("-"*60)
                    traceback.print_exc(file=sys.stdout)
                    print("-"*60)

    if error_count > 0 and args.verbose:
        os.system("PAUSE")