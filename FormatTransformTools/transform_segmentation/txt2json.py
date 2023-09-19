from utils.consoleLogger import ConsoleLogger
from utils.splitter.randomSplitter import RandomSplitter
import json
import sys
import yaml
import argparse
import os
from tqdm import tqdm
import cv2

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
    classes_path = config["path"]["classes"]
    ratio = {
        "train": config["ratio"]["train"],
        "val": config["ratio"]["val"],
        "test": config["ratio"]["test"]
    }
    if not (os.path.exists(origin_images_path) and os.path.exists(origin_annotations_path) and os.path.exists(classes_path)):
        logger.error("error in YAML path config. Path not exist.")
        sys.exit()
    if int(ratio["train"] + ratio["val"] + ratio["test"]) != 1:
        logger.error("error in ratio config. <Train + Val + Test != 1> ")
        sys.exit()
    return origin_images_path, origin_annotations_path, output_path, classes_path, ratio


def create_label(origin_images_path, origin_annotations_path, output_path, classes_path, ratio, args):
    # 打开classes文件与origin_images
    with open(classes_path) as f:
        classes = f.read().strip().split()
    origin_images_index = os.listdir(origin_images_path)
    random_splitter = RandomSplitter(origin_img_path=origin_images_path, origin_annotation_path=origin_annotations_path, ratio=ratio)
    train_img, val_img, test_img = random_splitter.getSplitList(random_state=233)
    logger.info("NUMS of train:val:test = {}:{}:{}".format(len(train_img), len(val_img), len(test_img)))

    # 用于保存所有数据的图片信息和标注信息
    train_dataset = {'categories': [], 'annotations': [], 'images': []}
    val_dataset = {'categories': [], 'annotations': [], 'images': []}
    test_dataset = {'categories': [], 'annotations': [], 'images': []}

    # 建立类别标签和数字id的对应关系, 类别id从0开始。
    for i, cls in enumerate(classes, 0):
        train_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
        val_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
        test_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})

    # 标注的id
    ann_id_cnt = 0
    print("-----------⬇-------Creating annotations from txt and output-------⬇-----------")
    for k, index in enumerate(tqdm(origin_images_index)):
        # 支持 png jpg 格式的图片。
        txtFile = index.replace('images', 'txt').replace('.jpg', '.txt').replace('.png', '.txt')
        # 读取图像的宽和高，移动图片
        im = cv2.imread(os.path.join(origin_images_path, index))
        height, width, _ = im.shape

        # 切换dataset的引用对象，从而划分数据集
        if index in train_img:
            dataset = train_dataset
        elif index in val_img:
            dataset = val_dataset
        elif index in test_img:
            dataset = test_dataset
        # 添加图像的信息
        dataset['images'].append({'file_name': index,
                                  'id': k,
                                  'width': width,
                                  'height': height})
        if not os.path.exists(os.path.join(origin_annotations_path, txtFile)):
            # 如没标签，跳过，只保留图片信息。
            continue
        with open(os.path.join(origin_annotations_path, txtFile), 'r') as fr:
            labelList = fr.readlines()
            for label in labelList:
                label = label.strip().split()
                x = float(label[1])
                y = float(label[2])
                w = float(label[3])
                h = float(label[4])

                # convert x,y,w,h to x1,y1,x2,y2
                H, W, _ = im.shape
                x1 = (x - w / 2) * W
                y1 = (y - h / 2) * H
                x2 = (x + w / 2) * W
                y2 = (y + h / 2) * H
                # 标签序号从0开始计算, coco2017数据集标号混乱，不管它了。
                cls_id = int(label[0])
                width = max(0, x2 - x1)
                height = max(0, y2 - y1)
                dataset['annotations'].append({
                    'area': width * height,
                    'bbox': [x1, y1, width, height],
                    'category_id': cls_id,
                    'id': ann_id_cnt,
                    'image_id': k,
                    'iscrowd': 0,
                    # mask, 矩形是从左上角点按顺时针的四个顶点
                    'segmentation': [[x1, y1, x2, y1, x2, y2, x1, y2]]
                })
                ann_id_cnt += 1

    # 移动图片
    if args.mode == "copy":
        logger.info("Mode = <copy>, data will be output to "+output_path)
    else:
        logger.info("Mode = <move>, data will be output to "+output_path)

    random_splitter.outputSplitImages(output_path=output_path, mode=args.mode)

    # 保存结果
    output_annotations_path = os.path.join(output_path, "annotations")
    for phase in ['train', 'val', 'test']:
        json_name = os.path.join(output_annotations_path, "{}.json".format(phase))
        with open(json_name, 'w') as f:
            if phase == 'train':
                json.dump(train_dataset, f)
            elif phase == 'val':
                json.dump(val_dataset, f)
            elif phase == 'test':
                json.dump(test_dataset, f)


def transform(args):
    origin_images_path, origin_annotations_path, output_path, classes_path, ratio = read_yaml()
    create_label(origin_images_path, origin_annotations_path, output_path, classes_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    transform(args)
