from utils.splitter.randomSplitter import RandomSplitter
from utils.configReader import ConfigReader
import json
import argparse
import os
from tqdm import tqdm
import cv2

CONFIG_PATH = '../config/transform_segmentation/txt2json.yaml'

# 读取启动参数
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default="copy", help="copy | move . copy is recommended.")


def txtToJson(origin_images_path: str, origin_annotations_path: str, output_path: str, classes_path: str, ratio: dict, args):
    # 打开classes文件与origin_images
    with open(classes_path) as f:
        classes = f.read().strip().split()

    origin_images_index = os.listdir(origin_images_path)

    random_splitter = RandomSplitter(origin_img_path=origin_images_path, origin_annotation_path=origin_annotations_path,
                                     ratio=ratio)
    train_img, val_img, test_img, _, _, _ = random_splitter.getSplitList(suffix="txt", random_state=233)

    # 用于保存所有数据的图片信息和标注信息
    train_dataset = {'categories': [], 'annotations': [], 'images': []}
    val_dataset = {'categories': [], 'annotations': [], 'images': []}
    test_dataset = {'categories': [], 'annotations': [], 'images': []}

    for i, cls in enumerate(classes):
        category = {'id': i, 'name': cls, 'supercategory': 'mark'}
        train_dataset['categories'].append(category)
        val_dataset['categories'].append(category)
        test_dataset['categories'].append(category)

    # 标注的id
    ann_id_cnt = 0
    print("-----------⬇-------Creating annotations from txt and output-------⬇-----------")

    for k, index in enumerate(tqdm(origin_images_index)):
        txt_file = index.replace('images', 'txt').replace('.jpg', '.txt').replace('.png', '.txt')
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
        dataset['images'].append({'file_name': index, 'id': k, 'width': width, 'height': height})

        if not os.path.exists(os.path.join(origin_annotations_path, txt_file)):
            # 如没标签，跳过，只保留图片信息。
            continue

        with open(os.path.join(origin_annotations_path, txt_file), 'r') as fr:
            label_list = fr.readlines()
            for label in label_list:
                label = label.strip().split()
                x, y, w, h = map(float, label[1:5])

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
    config_reader = ConfigReader(CONFIG_PATH)
    origin_images_path, origin_annotations_path, output_path, classes_path, ratio = config_reader.readYamlWithClasses()
    txtToJson(origin_images_path, origin_annotations_path, output_path, classes_path, ratio, args)


if __name__ == '__main__':
    args = parser.parse_args()
    transform(args)
