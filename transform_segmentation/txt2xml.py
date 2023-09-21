import os
from tqdm import tqdm
from utils.consoleLogger import ConsoleLogger
from utils.configReader import ConfigReader
from utils.splitter.randomSplitter import RandomSplitter
import argparse
import xml.etree.ElementTree as ET
from PIL import Image

CONFIG_PATH = '../config/transform_segmentation/txt2xml.yaml'

# 读取启动参数
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="copy", help="copy | move. copy is recommended.")

# 创建logger
logger = ConsoleLogger("logger").getLogger()


def convert(origin_annotations_path: str, origin_images_path: str, classes_path: str):
    """
    将源标注文件所处文件夹下的所有xml文件转化为txt文件并存放在该文件夹下

    :param origin_annotations_path: (str) 源标注文件所处文件夹的路径
    :param origin_images_path: (str) 源图片文件所处文件夹的路径
    :param classes_path: (str) class.txt文件的路径
    :return:
    """
    # 打开classes.txt, 录入到class_map中
    class_map = {}
    with open(classes_path, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            class_name = line.strip()
            class_map[index] = class_name

    # 打开源标注路径下的所有txt标注文件，转化为xml文件并保存在原标注路径下
    print("-----------⬇-------Creating annotations from txt and output-------⬇-----------")
    for txt_file in tqdm(os.listdir(origin_annotations_path)):
        if txt_file.endswith("txt"):
            with open(os.path.join(origin_annotations_path, txt_file), "r") as f:
                # 创建对应的xml文件标签
                root = ET.Element("annotation")
                filename = ET.SubElement(root, "filename")
                filename.text = txt_file.replace(".txt", ".jpg")
                path = ET.SubElement(root, "path")
                path.text = os.path.join(origin_images_path, filename.text)
                source = ET.SubElement(root, "source")
                database = ET.SubElement(source, "database")
                database.text = "Unknown"

                # 读取txt对应的图像文件，获得图像的width与height
                with Image.open(path.text) as image:
                    image_width, image_height = image.size
                size = ET.SubElement(root, "size")
                width = ET.SubElement(size, "width")
                width.text = str(image_width)
                height = ET.SubElement(size, "height")
                height.text = str(image_height)
                depth = ET.SubElement(size, "depth")
                depth.text = str(3)
                segmented = ET.SubElement(root, "segmented")
                segmented.text = str(0)

                # 读取txt文件，并获得其中的标签属性
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split(" ")
                    class_id = int(line[0])
                    x_center, y_center, width, height = [float(value) for value in line[1:5]]

                    # 创建xml文件下对应txt的每个标签的元素
                    object_elem = ET.SubElement(root, "object")
                    if (class_id + 1) > len(class_map):
                        raise ValueError(
                            "classes.txt not correct. Could not find corresponding label to one of the txt input labels in classes.txt")
                    name = ET.SubElement(object_elem, "name")
                    name.text = class_map[class_id]
                    pose = ET.SubElement(object_elem, "pose")
                    pose.text = "Unspecified"
                    truncated = ET.SubElement(object_elem, "truncated")
                    truncated.text = 0
                    difficult = ET.SubElement(object_elem, "difficult")
                    difficult.text = 0
                    bndbox = ET.SubElement(object_elem, "bndbox")
                    xmin = ET.SubElement(bndbox, "xmin")
                    xmin.text = str(int((x_center - width / 2) * image_width))
                    ymin = ET.SubElement(bndbox, "ymin")
                    ymin.text = str(int((y_center - height / 2) * image_height))
                    xmax = ET.SubElement(bndbox, "xmax")
                    xmax.text = str(int((x_center + width / 2) * image_width))
                    ymax = ET.SubElement(bndbox, "ymax")
                    ymax.text = str(int((y_center + height / 2) * image_height))

                tree = ET.ElementTree(root)
                xml_file = txt_file.replace(".txt", ".xml")
                tree.write(os.path.join(origin_annotations_path, xml_file))


def txtToXml(origin_images_path: str, origin_annotations_path: str, output_path: str, classes_path: str, ratio: dict,
             args):
    """

    :param origin_images_path: (str) 源图片文件所处的文件夹路径
    :param origin_annotations_path: (str) 源标注文件所处的文件夹路径
    :param output_path: (str) 输出路径
    :param classes_path: (str) classes.txt文件路径
    :param ratio: (dict) 训练集，评估集，测试集比例
    :param args: 启动参数
    :return:
    """
    random_splitter = RandomSplitter(origin_img_path=origin_images_path, origin_annotation_path=origin_annotations_path,
                                     ratio=ratio)
    random_splitter.getSplitList(suffix="xml", random_state=233)

    # 将源标注文件所处文件夹下的所有xml文件转化为txt文件并存放在该文件夹下
    convert(origin_annotations_path=origin_annotations_path, origin_images_path=origin_images_path,
            classes_path=classes_path)

    # 移动图片与标注文件
    random_splitter.outputSplitImages(output_path=output_path, mode=args.mode)
    random_splitter.outputSplitAnnotations(output_path=output_path, mode="move")


def transform(args):
    """
    读取yaml配置文件，将xml标注文件转化为txt标注文件并划分好训练集，评估集，测试集

    :param args: 启动参数
    :return:
    """
    config_reader = ConfigReader(CONFIG_PATH)
    origin_images_path, origin_annotations_path, output_path, classes_path, ratio = config_reader.readYamlWithClasses()
    txtToXml(origin_images_path, origin_annotations_path, output_path, classes_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    transform(args)
