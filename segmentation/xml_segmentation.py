import argparse
from utils.splitter.randomSplitter import RandomSplitter
from utils.configReader import ConfigReader


CONFIG_PATH = '../config/segmentation/xml_segmentation.yaml'

# 读取启动参数
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="copy", help="copy | move . copy is recommended.")


def divideDataset(origin_images_path, origin_annotations_path, output_path, ratio, args):
    random_splitter = RandomSplitter(origin_img_path=origin_images_path, origin_annotation_path=origin_annotations_path,
                                     ratio=ratio)
    random_splitter.getSplitList(suffix="xml", random_state=233)
    random_splitter.outputSplitAnnotations(output_path=output_path, mode=args.mode)
    random_splitter.outputSplitImages(output_path=output_path, mode=args.mode)


def segmentation(args):
    config_reader = ConfigReader(CONFIG_PATH)
    origin_images_path, origin_annotations_path, output_path, ratio = config_reader.readYaml()
    divideDataset(origin_images_path, origin_annotations_path, output_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    segmentation(args)
