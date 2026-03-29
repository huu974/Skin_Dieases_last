"""
模型测试脚本
"""

import os
import random
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights
from ultralytics import YOLO
from model.PanDerm import MyModel
from model.yolo_detector import YOLOv10Detector
from utils.config_handler import model_conf
from utils.config_handler import test_evaluate_conf


# SKIN_DISEASE_CLASSES= [
# "痤疮和酒渣鼻","光化性角化病和基底细胞癌","特应性皮炎",
# "大疱性疾病","蜂窝组织炎和细菌感染","湿疹",
# "发疹和药物性皮炎","脱发","疱疹/HPV",
# "色素性疾病","红斑狼疮","黑色素瘤和痣",
# "甲真菌病","毒葛皮炎","银屑病和扁平苔藓",
# "疥疮和莱姆病","脂溢性角化病和良性肿瘤","系统性疾病",
# "真菌感染","荨麻疹","血管瘤",
# "血管炎","疣和传染性软疣"
# ]


transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])



#1.测试分类模型
def test_classifier(image_path,model_name='efficientnet_b3'):
    print('开始测试分类模型...')
    device =  torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    # 根据模型名称加载分类模型
    if model_name == 'resnet50':
        from model.ResNet50 import ResNet50Classifier
        model = ResNet50Classifier(num_classes=model_conf["num_classes"], pretrained=False)
    elif model_name == 'efficientnet_b3':
        model = efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1)
        xiaohui = MyModel(model=model, num_classes=model_conf["num_classes"])
        model = xiaohui.model_classifier().to(device)
        checkpoint = torch.load(test_evaluate_conf['classification_model'], map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])

    else:
        raise ValueError(f"不支持的模型: {model_name}")


    model = model.to(device)
    print(f'使用模型：{model_name}')
    #测试开始
    model.eval()

    #图片预处理
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)


    #推理
    with torch.no_grad():
        outputs = model(image_tensor)
        proabilities = torch.softmax(outputs, dim=1)
        confidence,pred = torch.max(proabilities, 1)

    diease = test_evaluate_conf['class_names'][pred.item()]

    #打印测试结果
    print(f'分类结果：{diease}，置信度：{confidence.item():.2%}')


    return diease, confidence



#2.测试YOLO模型
def test_yolo(image_path, save_box_image=None):
    print('开始测试YOLO模型...')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 加载YOLO模型
    yolo = YOLOv10Detector(model_size='n')
    yolo.load(test_evaluate_conf['yolo_model'])

    # 检测并返回坐标和带框图片
    results, coordinates = yolo.predict_with_box(
        image_path,
        conf=0.25,
        save_path=save_box_image
    )

    result = results[0]
    boxes = result.boxes

    if boxes is not None and len(boxes) > 0:
        print(f'检测到{len(boxes)}个目标')
        for i, box in enumerate(boxes):
            conf = float(box.conf[0])
            print(f'区域{i+1}置信度：{conf:.2%}')
        print(f'检测框坐标: {coordinates}')
    else:
        print('未检测到皮损区域')

    return results, coordinates





#3.yolo+分类测试
def test_yolo_classifier(image_path,save_box_image,model_name='efficientnet_b3'):
    print('开始测试YOLO+分类模型...')
    device =  torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    #加载yolo
    yolo = YOLOv10Detector(model_size='n')
    yolo.load(test_evaluate_conf['yolo_model'])
    #检测并返回坐标和带框图片
    results,coordinates = yolo.predict_with_box(
        image_path,
        conf=0.25,
        save_path=save_box_image
    )
    result = results[0]
    boxes = result.boxes

    if boxes is None or len(boxes) == 0:
        print('未检测到皮损区域')
        return None, None

    #获取YOLO检测置信度
    yolo_conf = boxes[0].conf[0].item() if boxes is not None and len(boxes) > 0 else 0
    print(f'检测到{len(boxes)}个皮损目标，框坐标为：{coordinates}')

    # 根据模型名称加载分类模型
    if model_name == 'resnet50':
        from model.ResNet50 import ResNet50Classifier
        model = ResNet50Classifier(num_classes=model_conf["num_classes"], pretrained=False)
    elif model_name == 'efficientnet_b3':
        model = efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1)
        xiaohui = MyModel(model=model, num_classes=model_conf["num_classes"])
        model = xiaohui.model_classifier().to(device)
        checkpoint = torch.load(test_evaluate_conf['classification_model'], map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])

    else:
        raise ValueError(f"不支持的模型: {model_name}")


    model = model.to(device)
    print(f'使用模型：{model_name}')
    #测试开始
    model.eval()
    print(f'开始分类...')


    # 用原图分类（而不是裁剪区域），保持和直接分类一致
    original_img = Image.open(image_path).convert('RGB')
    original_tensor = transform(original_img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(original_tensor)
        proabilities = torch.softmax(outputs, dim=1)
        confidence,pred = torch.max(proabilities, 1)

    diease = test_evaluate_conf['class_names'][pred.item()]
    print(f'检测置信度：{yolo_conf:.2%}')
    print(f'分类结果：{diease}，置信度：{confidence.item():.2%}')

    return results,coordinates




#4.随机从测试集随机选择一张图片进行测试
def get_random_test_image(test_folder=test_evaluate_conf['test_data']):
    #获取所有类别文件夹
    classes = [ d for d in os.listdir(test_folder) if os.path.isdir(os.path.join(test_folder, d))]

    #随机选择一个类别
    random_class = random.choice(classes)

    #获取该类别下的所有图片
    class_folder = os.path.join(test_folder, random_class)
    images = [f for f in os.listdir(class_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    random_image = random.choice(images)
    image_path = os.path.join(class_folder, random_image)

    return image_path, random_class




if __name__ == '__main__':
     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
     print(f'使用设备：{device}')
     test_image,true_class = get_random_test_image()
     print(f'测试图片路径：{test_image}')
     print(f'真实类别：{true_class}')
     #1.测试分类模型
     pred_classifier, conf_classifier = test_classifier(test_image)

     print(f'分类结果：{pred_classifier}，置信度：{conf_classifier.item():.2%}')



     #2.测试YOLO模型
     # test_yolo(test_image)


     #3.测试YOLO+分类模型
     # test_yolo_classifier("HAM10000/yolo_dataset/images/val/ISIC_0024372.jpg", save_box_image="output.jpg")
     test_yolo_classifier(test_image, save_box_image="output.jpg")

