import os
from sklearn.model_selection import train_test_split
import shutil

from utils.splitter.splitter import Splitter


class RandomSplitter(Splitter):

    def __init__(self, origin_img_path, origin_annotation_path, ratio):
        """
        初始化方法

        Args:
            origin_img_path (str): 存放图片的路径
            output_path (str): 存放输出的图片与标注的路径
            ratio (dict): 分割比例 ratio:{
                                    "train": 0.8,
                                    "val": 0.1,
                                    "test": 0.1
                                    }
        """
        super().__init__(origin_img_path=origin_img_path, origin_annotation_path=origin_annotation_path, ratio=ratio)
        self.random_state = 233

    def getSplitList(self, random_state=233):
        """
        获得数据集分割为train,val,test的输出

        Args:
            random_state (int): 随机数种子，默认为233

        Returns:
            train_img (list), val_img (list), test_img (list): 分割后图片名字的列表
        """
        if self.train_img and self.random_state == random_state:
            return self.train_img, self.val_img, self.test_img
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
            return train_img, val_img, test_img

    def outputSplitImages(self, output_path, mode):
        if not self.train_img:
            self.getSplitList()
        return super().outputSplitImages(output_path=output_path, mode=mode)

    def outputSplitTxtAnnotations(self, output_path, mode):
        if not self.train_img:
            self.getSplitList()
        return super().outputSplitTxtAnnotations(output_path=output_path, mode=mode)
