import os

from utils.consoleLogger import ConsoleLogger
from utils.configReader import ConfigReader
from utils.splitter.randomSplitter import RandomSplitter
import argparse
import xml.etree.ElementTree as ET


CONFIG_PATH = '../config/transform_segmentation/xml2txt.yaml'

# 读取启动参数
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="copy", help="copy | move. copy is recommended.")

# 创建logger
logger = ConsoleLogger("logger").getLogger()


def convert(origin_annotations_path: str, classes_path: str):
    """
    将源标注文件所处文件夹下的所有xml文件转化为txt文件并存放在该文件夹下

    :param origin_annotations_path: (str) 源标注文件所处文件夹的路径
    :param classes_path: (str) class.txt文件的路径
    :return:
    """
    # 打开classes.txt, 录入到class_map中
    class_map = {}
    with open(classes_path, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            class_name = line.strip()
            class_map[class_name] = index

    # 打开源标注路径下的所有xml标注文件，转化为txt文件并保存在原标注路径下
    for xml_file in os.listdir(origin_annotations_path):
        print(xml_file)
        if xml_file.endswith(".xml"):
            tree = ET.parse(os.path.join(origin_annotations_path, xml_file))
            root = tree.getroot()

            image_width = int(root.find('size/width').text)
            image_height = int(root.find('size/height').text)

            with open(os.path.join(origin_annotations_path, xml_file.replace(".xml", ".txt")), 'w') as f:
                for obj in root.findall('object'):
                    class_name = obj.find('name').text
                    class_id = class_map[class_name]

                    bbox = obj.find('bndbox')
                    xmin = float(bbox.find('xmin').text)
                    ymin = float(bbox.find('ymin').text)
                    xmax = float(bbox.find('xmax').text)
                    ymax = float(bbox.find('ymax').text)

                    x_center = (xmin + xmax) / (2.0 * image_width)
                    y_center = (ymin + ymax) / (2.0 * image_height)
                    width = (xmax - xmin) / image_width
                    height = (ymax - ymin) / image_height

                    line = f"{class_id} {x_center} {y_center} {width} {height}\n"
                    print(line)
                    f.write(line)


def xmlToTxt(origin_images_path: str, origin_annotations_path: str, output_path: str, classes_path: str, ratio: dict, args):
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
    random_splitter.getSplitList(suffix="txt", random_state=233)

    # 将源标注文件所处文件夹下的所有xml文件转化为txt文件并存放在该文件夹下
    convert(origin_annotations_path=origin_annotations_path, classes_path=classes_path)

    # 移动图片与标注文件
    random_splitter.outputSplitAnnotations(output_path=output_path, mode="move")
    random_splitter.outputSplitImages(output_path=output_path, mode=args.mode)


def transform(args):
    """
    读取yaml配置文件，将xml标注文件转化为txt标注文件并划分好训练集，评估集，测试集

    :param args: 启动参数
    :return:
    """
    config_reader = ConfigReader(CONFIG_PATH)
    origin_images_path, origin_annotations_path, output_path, classes_path, ratio = config_reader.readYamlWithClasses()
    xmlToTxt(origin_images_path, origin_annotations_path, output_path, classes_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    transform(args)
