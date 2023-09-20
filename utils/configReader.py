import yaml
import os
import sys


class ConfigReader:
    def __init__(self, config_path):
        self.config_path = config_path

    def readYaml(self):
        # 读取YAML配置文件
        with open(self.config_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
        origin_images_path = config["path"]["origin_images"]
        origin_annotations_path = config["path"]["origin_annotations"]
        output_path = config["path"]["output"]
        ratio = {
            "train": config["ratio"]["train"],
            "val": config["ratio"]["val"],
            "test": config["ratio"]["test"]
        }
        if not (os.path.exists(origin_images_path) and os.path.exists(origin_annotations_path)):
            print("[Error] Error in YAML path config. Path not exist.")
            sys.exit()
        if int(ratio["train"] + ratio["val"] + ratio["test"]) != 1:
            print("[Error] error in ratio config. <Train + Val + Test != 1> ")
            sys.exit()
        return origin_images_path, origin_annotations_path, output_path, ratio

    def readYamlWithClasses(self):
        # 读取YAML配置文件
        with open(self.config_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
        origin_images_path = config["path"]["origin_images"]
        origin_annotations_path = config["path"]["origin_annotations"]
        output_path = config["path"]["output"]
        classes_path = config["path"]["classes"]
        ratio = {
            "train": config["ratio"]["train"],
            "val": config["ratio"]["val"],
            "test": config["ratio"]["test"]
        }
        if not (os.path.exists(origin_images_path) and os.path.exists(origin_annotations_path) and os.path.exists(
                classes_path)):
            print("[Error] Error in YAML path config. Path not exist.")
            sys.exit()
        if int(ratio["train"] + ratio["val"] + ratio["test"]) != 1:
            print("[Error] error in ratio config. <Train + Val + Test != 1> ")
            sys.exit()
        return origin_images_path, origin_annotations_path, output_path, classes_path, ratio
