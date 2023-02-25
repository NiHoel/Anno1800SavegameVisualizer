import argparse
import pathlib
import zlib

from tools.a7s_model import *

REGION_TO_SESSION = {
    5000000: 180023,
    5000001: 180025,
    160001: 180045,
    114327: 112132,
}


def extract_stamp(path: pathlib.Path):
    temp_path = TEMP_PATH / path.parent.name / path.stem
    temp_file = temp_path / path.stem
    temp_path.mkdir(parents=True, exist_ok=True)
    tools_path = pathlib.Path(os.getcwd() + "/tools")


    if not temp_file.with_suffix(".xml").exists():
        content = open(path, 'rb').read()
        content = zlib.decompress(content)
        with open(temp_file.with_suffix(".bin"), 'wb') as f:
            f.write(content)

        execute([str(tools_path / "FileDBReader/FileDBReader.exe"), "decompress",
                 # "-i", str(tools_path / "FileDBReader/FileFormats/stamp.xml"),
                 "-f", str(temp_file.with_suffix(".bin")), "-y"])

    parser = ET.XMLParser(huge_tree=True)
    return ET.parse(str(temp_file.with_suffix(".xml")), parser)


def stamp_to_json(tree, ad_config):
    region = hex_to_int(tree.find("StampPath"))
    session = REGION_TO_SESSION.get(region)
    exclude_quay = False

    objects = []

    for node in tree.getroot().findall("BuildingInfo/"):
        guid = hex_to_int(node.find("./GUID"))
        complex_owner_id = hex_to_int(node.find("./ComplexOwnerID"))
        direction = hex_to_float(node.find("./Dir"))
        if direction is None:
            direction = 0
        rot = int(round(direction / math.pi * 2) % 4)
        pos = hex_to_float_list(node.find("./Pos"), 4)
        variation = hex_to_int(node.find("./Variation"))


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

        print(start, end)

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


def convert_stamp(path: pathlib.Path, ad_config, overwrite: bool = False):
    try:

        ad_path = path.with_suffix(".ad")
        if overwrite or not path.with_suffix(".ad").exists():
            tree = extract_stamp(path)
            ad_config = stamp_to_json(tree, ad_config)
            ad_json = json.dumps(ad_config)

            with open(str(ad_path), "w") as f:
                f.write(ad_json)

        png_path = path.with_suffix(".png")
        if overwrite or not png_path.exists():
            execute(
                [os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe",
                 "export", str(ad_path), str(png_path),
                 "--renderGrid", "True",
                 "--renderStatistics", "True",
                 "--renderVersion", "False",
                 "--gridSize", str(100)])

    except Exception as e:
        print(e)
        raise e


parser = argparse.ArgumentParser(description='Convert stamps into Anno Designer files and images and vice versa.')
parser.add_argument('paths', metavar='path', type=str, nargs='+',
                    help='files or folders to be converted')
parser.add_argument('-o', "--overwrite", action='store_true', help="Overwrite destination files")

args = parser.parse_args()

for path in args.paths:
    path = pathlib.Path(path) # no resolve

    if not path.exists():
        continue

    ad_config = ADConfig()
    if path.suffix == "":
        convert_stamp(path, ad_config, args.overwrite)
