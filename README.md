# 数据集划分与格式转换

## 划分数据集

### YOLO格式数据集 (txt) 划分
1. 对`config/txt_segmentation.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./segmentation/txt_segmentation.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./segmentation/txt_segmentation.py --mode="move"`

### XML格式数据集划分
1. 对`config/xml_segmentation.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./segmentation/xml_segmentation.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./segmentation/xml_segmentation.py --mode="move"`

---
## 格式转换+数据集划分

### YOLO格式数据集 (txt) 转COCO格式数据集 (json) 并划分
1. 对`config/txt2json.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./transform_segmentation/txt2json.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./transform_segmentation/txt2json.py --mode="move"`

### COCO格式数据集 (json) 转YOLO格式数据集 (txt) 并划分
1. 对`config/json2txt.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./transform_segmentation/json2txt.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./transform_segmentation/json2txt.py --mode="move"`

### YOLO格式数据集 (txt) 转XML格式数据集并划分
1. 对`config/txt2xml.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./transform_segmentation/txt2xml.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./transform_segmentation/txt2xml.py --mode="move"`

### XML格式数据集 转YOLO格式数据集 (txt)并划分
1. 对`config/xml2txt.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./transform_segmentation/xml2txt.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./transform_segmentation/xml2txt.py --mode="move"`