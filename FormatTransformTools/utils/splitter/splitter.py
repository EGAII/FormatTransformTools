import os
import shutil

from tqdm import tqdm


class Splitter:

    def __init__(self, origin_img_path, origin_annotation_path, ratio):
        """
        初始化方法

        Args:
            origin_img_path (str): 存放图片的路径
            origin_annotation_path (str): 存放注释的路径
            ratio (dict): 分割比例 ratio:{
                                    "train": 0.8,
                                    "val": 0.1,
                                    "test": 0.1
                                    }
        """
        if not os.path.exists(origin_img_path):
            raise OSError("origin_img_path Not Exist")
        self.origin_img_path = origin_img_path
        self.origin_annotation_path = origin_annotation_path
        self.img_path_list = os.listdir(origin_img_path)
        self.annotation_path_list = os.listdir(origin_annotation_path)
        self.ratio = ratio
        self.train_img = None
        self.test_img = None
        self.val_img = None

    def outputSplitImages(self, output_path, mode):
        """
        使用子类的getSplitList方法获得self.train_img,self.val_img,self.test_img后，对输出路径输出分割后的图片

        Args:
            output_path (str): 存放输出的图片与标注的路径
            mode (str): 输出模式,"copy"(default)为输出文件,"move"为移动文件
        """
        if not self.train_img:
            raise AttributeError("Empty train, val, test image set. Please use subclass getSplitList() first")
        # 创建输出文件夹
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_images_path = os.path.join(output_path, "images")

        if not os.path.exists(output_images_path):
            os.makedirs(output_images_path)

        output_train_path = os.path.join(output_images_path, "train")
        output_val_path = os.path.join(output_images_path, "train")
        output_test_path = os.path.join(output_images_path, "train")
        if not os.path.exists(output_train_path):
            os.makedirs(output_train_path)
        if not os.path.exists(output_val_path):
            os.makedirs(output_val_path)
        if not os.path.exists(output_test_path):
            os.makedirs(output_test_path)

        # 移动/复制图片到目标文件夹
        if mode == "copy":
            print("-----------⬇-------Copying images to output folder-------⬇-----------")
            for k, index in enumerate(tqdm(self.img_path_list)):
                if index in self.train_img:
                    shutil.copy(os.path.join(self.origin_img_path, index),
                                os.path.join(output_train_path, index))
                elif index in self.val_img:
                    shutil.copy(os.path.join(self.origin_img_path, index),
                                os.path.join(output_val_path, index))
                elif index in self.test_img:
                    shutil.copy(os.path.join(self.origin_img_path, index),
                                os.path.join(output_test_path, index))
        else:
            print("-----------⬇-------Moving images to output folder-------⬇-----------")
            for k, index in enumerate(tqdm(self.img_path_list)):
                if index in self.train_img:
                    shutil.move(os.path.join(self.origin_img_path, index),
                                os.path.join(output_train_path, index))
                elif index in self.val_img:
                    shutil.move(os.path.join(self.origin_img_path, index),
                                os.path.join(output_val_path, index))
                elif index in self.test_img:
                    shutil.move(os.path.join(self.origin_img_path, index),
                                os.path.join(output_test_path, index))
        return output_images_path

    def outputSplitTxtAnnotations(self, output_path, mode):
        """
        使用子类的getSplitList方法获得self.train_img,self.val_img,self.test_img后，对输出路径输出分割后的标注

        Args:
            output_path (str): 存放输出的图片与标注的路径
            mode (str): 输出模式,"copy"(default)为输出文件,"move"为移动文件
        """
        if not self.train_img:
            raise AttributeError("Empty train, val, test image set. Please use subclass getSplitList() first")
        # 创建输出文件夹
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_annotations_path = os.path.join(output_path, "annotations")
        if not os.path.exists(output_annotations_path):
            os.makedirs(output_annotations_path)

        output_train_path = os.path.join(output_annotations_path, "train")
        output_val_path = os.path.join(output_annotations_path, "train")
        output_test_path = os.path.join(output_annotations_path, "train")
        if not os.path.exists(output_train_path):
            os.makedirs(output_train_path)
        if not os.path.exists(output_val_path):
            os.makedirs(output_val_path)
        if not os.path.exists(output_test_path):
            os.makedirs(output_test_path)

        # 移动/复制txt标注到目标文件夹
        if mode == "copy":
            print("-----------⬇-------Copying annotation to output folder-------⬇-----------")
            for k, index in enumerate(tqdm(self.annotation_path_list)):
                if index in self.train_img:
                    shutil.copy(os.path.join(self.origin_annotation_path, index),
                                os.path.join(output_train_path, index))
                elif index in self.val_img:
                    shutil.copy(os.path.join(self.origin_annotation_path, index),
                                os.path.join(output_val_path, index))
                elif index in self.test_img:
                    shutil.copy(os.path.join(self.origin_annotation_path, index),
                                os.path.join(output_test_path, index))
        else:
            print("-----------⬇-------Moving annotation to output folder-------⬇-----------")
            for k, index in enumerate(tqdm(self.annotation_path_list)):
                if index in self.train_img:
                    shutil.move(os.path.join(self.origin_annotation_path, index),
                                os.path.join(output_train_path, index))
                elif index in self.val_img:
                    shutil.move(os.path.join(self.origin_annotation_path, index),
                                os.path.join(output_val_path, index))
                elif index in self.test_img:
                    shutil.move(os.path.join(self.origin_annotation_path, index),
                                os.path.join(output_test_path, index))

        return output_annotations_path
