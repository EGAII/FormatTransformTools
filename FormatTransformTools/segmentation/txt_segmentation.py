import json
import shutil
import sys
import yaml
import argparse
from utils.consoleLogger import ConsoleLogger
from utils.splitter.randomSplitter import RandomSplitter
import os
from tqdm import tqdm

# 读取启动参数
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="copy", help="copy | move . copy is recommended.")


# 读取YAML配置文件
with open('../config/txt2json.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

# 创建logger
logger = ConsoleLogger("logger").getLogger()


def read_yaml():
    origin_images_path = config["path"]["origin_images"]
    origin_annotations_path = config["path"]["origin_annotations"]
    output_path = config["path"]["output"]
    ratio = {
        "train": config["ratio"]["train"],
        "val": config["ratio"]["val"],
        "test": config["ratio"]["test"]
    }
    if not (os.path.exists(origin_images_path) and os.path.exists(origin_annotations_path)):
        logger.error("error in YAML path config. Path not exist.")
        sys.exit()
    if int(ratio["train"] + ratio["val"] + ratio["test"]) != 1:
        logger.error("error in ratio config. <Train + Val + Test != 1> ")
        sys.exit()
    return origin_images_path, origin_annotations_path, output_path, ratio


def divideDataset(origin_images_path, origin_annotations_path, output_path, ratio, args):
    random_splitter = RandomSplitter(origin_img_path=origin_images_path, origin_annotation_path=origin_annotations_path, ratio=ratio)
    train_img, val_img, test_img = random_splitter.getSplitList(random_state=233)
    logger.info("NUMS of train:val:test = {}:{}:{}".format(len(train_img), len(val_img), len(test_img)))
    random_splitter.outputSplitTxtAnnotations(output_path=output_path, mode=args.mode)
    random_splitter.outputSplitImages(output_path=output_path, mode=args.mode)



def segmentation(args):
    origin_images_path, origin_annotations_path, output_path, ratio = read_yaml()
    divideDataset(origin_images_path, origin_annotations_path, output_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    segmentation(args)
