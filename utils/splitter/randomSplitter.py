import os
from sklearn.model_selection import train_test_split
import shutil

from typing import Tuple

from utils.splitter.splitter import Splitter


class RandomSplitter(Splitter):

    def __init__(self, origin_img_path: str, origin_annotation_path: str, ratio: dict):
        super().__init__(origin_img_path=origin_img_path, origin_annotation_path=origin_annotation_path, ratio=ratio)
        self.random_state = 233

    def getSplitList(self, suffix: str, random_state: int = 233) -> Tuple[list, list, list, list, list, list]:
        """
        获得数据集分割为train,val,test的输出

        :param suffix: (str)标注文件后缀,"txt","xml"
        :param random_state: (int)随机数种子，默认为233
        :return: train_img (list), val_img (list), test_img (list), train_annotation (list), val_annotation (list), test_annotation (list)分割后图片名与标注文件名的列表
        """

        self.suffix = suffix
        if self.train_img and self.random_state == random_state:
            return self.train_img, self.val_img, self.test_img, self.train_annotation, self.val_annotation, self.test_annotation
        else:
            # 更新使用的随机数种子
            self.random_state = random_state

            # 分割数据集
            train_img, middle_img = train_test_split(self.img_path_list, test_size=1 - self.ratio["train"],
                                                     random_state=random_state)
            val_img, test_img = train_test_split(middle_img, test_size=(self.ratio["val"] / (1 - self.ratio["train"])),
                                                 random_state=233)
            self.train_img = train_img
            self.val_img = val_img
            self.test_img = test_img
            self.train_annotation = [img.replace('.jpg', '.' + self.suffix) for img in train_img]
            self.val_annotation = [img.replace('.jpg', '.' + self.suffix) for img in val_img]
            self.test_annotation = [img.replace('.jpg', '.' + self.suffix) for img in test_img]
            print("NUMS of train:val:test = {}:{}:{}".format(len(train_img), len(val_img), len(test_img)))
            return train_img, val_img, test_img, self.train_annotation, self.val_annotation, self.test_annotation
