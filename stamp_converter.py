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
        
        tl_pos = pos - rotated_size / 2
      

        del obj["BuildBlocker"]

        if guid in A7PARAMS["direction_offsets"]:
            rot += A7PARAMS["direction_offsets"][guid]
        rot = rot % 4
        obj["Direction"] = A7PARAMS["directions"][rot]

        obj["Size"] = "{},{}".format(rotated_size[0], rotated_size[1])
        obj["Position"] = "{},{}".format(tl_pos[1] + 0.5, tl_pos[0] - 0.5)

        objects.append(obj)
    
    """
    index = 0
    street = None
    for node in tree.getroot().findall("StreetInfo/"):
        if index % 2 == 0:
            street = A7PARAMS["streets"].get(hex_to_int(node))
        else:
            
        
        index += 1
    """        
            
    
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
