# !/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：FormatTransformTools 
@File    ：json2txt.py
@Author  ：wpf
@Date    ：2023/9/21 15:02 
'''

from utils.splitter.randomSplitter import RandomSplitter
from utils.configReader import ConfigReader
import json
import argparse
import os
from tqdm import tqdm

CONFIG_PATH = '../config/transform_segmentation/json2txt.yaml'

# 读取启动参数
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="copy", help="copy | move . copy is recommended.")


def convert(origin_annotations_path: str):
    """
    将标注文件从json转化为txt并输出在该目录下

    :param origin_annotations_path: 源标注文件所处路径
    :return:
    """

    print("-----------⬇-------Creating annotations from json and output-------⬇-----------")
    for phase in tqdm(['train', 'val', 'test']):
        json_name = os.path.join(origin_annotations_path, f"{phase}.json")
        with open(json_name, 'r') as f:
            dataset = json.load(f)

        for image_info in dataset['images']:
            image_id = image_info['id']
            image_name = image_info['file_name']
            image_width = image_info['width']
            image_height = image_info['height']

            txt_file = image_name.replace('.jpg', '.txt').replace('.png', '.txt')

            annotations = [ann for ann in dataset['annotations'] if ann['image_id'] == image_id]

            with open(os.path.join(origin_annotations_path, txt_file), 'w') as fw:
                for ann in annotations:
                    category_id = ann['category_id']
                    bbox = ann['bbox']

                    x_center = bbox[0] + bbox[2] / 2
                    y_center = bbox[1] + bbox[3] / 2
                    width = bbox[2]
                    height = bbox[3]

                    x = x_center / image_width
                    y = y_center / image_height
                    w = width / image_width
                    h = height / image_height

                    line = f"{category_id} {x} {y} {w} {h}\n"
                    fw.write(line)


def txtToJson(origin_image_path: str, origin_annotations_path: str, output_path: str, ratio: dict, args):
    random_splitter = RandomSplitter(origin_img_path=origin_image_path, origin_annotation_path=origin_annotations_path,
                                     ratio=ratio)

    random_splitter.getSplitList(suffix="txt", random_state=233)
    convert(origin_annotations_path=origin_annotations_path)

    # 输出
    random_splitter.outputSplitAnnotations(output_path=output_path, mode="move")
    random_splitter.outputSplitImages(output_path=output_path, mode=args.mode)


def transform(args):
    config_reader = ConfigReader(CONFIG_PATH)
    origin_images_path, origin_annotations_path, output_path, ratio = config_reader.readYaml()
    txtToJson(origin_images_path, origin_annotations_path, output_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    transform(args)
