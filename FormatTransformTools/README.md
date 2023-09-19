# 数据集划分与格式转换
## YOLO格式数据集划分
1. 对`config/txt_segment.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./segmentation/txt_segmentation.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./segmentation/txt_segmentation.py --mode="move"`

## YOLO格式数据集(txt)转COCO格式数据集(json)并划分
1. 对`config/txt2json.yaml`进行修改配置文件
2. 运行以下linux指令
    - 复制模式(default) `python ./segmentation/txt2json.py --mode="copy"`
    - 移动模式(会移动源数据) `python ./segmentation/txt2json.py --mode="move"`
