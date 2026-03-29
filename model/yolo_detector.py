"""
YOLO检测器封装，集成训练，推理，加载
"""

import os
import torch
from ultralytics import YOLO
from utils.config_handler import yolov10
from peft import LoraConfig, get_peft_config, get_peft_model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class YOLOv10Detector:
    def __init__(self, model_size, device='cuda'):
        self.device = device
        self.num_classes = yolov10['nc']
        self.model_size = model_size
        self.weights_path = self._get_weights_path(model_size)
        self.model = YOLO(self.weights_path)
        self.loaded_checkpoint = None  # 记录是否从checkpoint恢复训练

    # 获取权重路径
    def _get_weights_path(self, model_size):
        pretrained_dir = os.path.join(os.path.dirname(__file__), '..', 'pretrained')
        weights_map = {
            'n': os.path.join(pretrained_dir, 'yolov10n.pt'),
            's': os.path.join(pretrained_dir, 'yolov10s.pt'),
            'm': os.path.join(pretrained_dir, 'yolov10m.pt'),
            'l': os.path.join(pretrained_dir, 'yolov10l.pt'),
            'x': os.path.join(pretrained_dir, 'yolov10x.pt'),
        }
        if model_size not in weights_map:
            raise ValueError('Invalid model size. Please choose from "n", "s", "m", "l", or "x".')
        return weights_map[model_size]

    #推理，返回检测结果
    def predict(self,img_path,conf=0.25,iou=0.45):
        return self.model.predict(
            img_path,
            conf=conf,      #置信度阈值，低于此阈值的预测将被忽略
            device=self.device,
        )



    #训练
    def train(self, data_yaml, epochs, batch_size, lr0, imgsz, project, resume=False, last_weights=None):
        from ultralytics import YOLO
        
        # 如果有上次保存的权重，从它继续训练
        if last_weights and os.path.exists(last_weights):
            self.model = YOLO(last_weights)
        else:
            self.model = YOLO(self.weights_path)
        
        result = self.model.train(
            data=data_yaml,
            epochs=epochs,
            batch=batch_size,
            lr0=lr0,
            imgsz=imgsz,
            project=project,
            amp=False,
            resume=False  # 不使用ultralytics的resume，用我们自己的方式
        )
        return result

    # #验证
    # def val(self, data_yaml=None):
    #     return self.model.val(data=data_yaml, device=self.device)



    #检测并裁剪返回皮损区域图像
    def predict_with_crop(self,img_path,conf=0.25):
        #1.调用预测获取检测结果
        results = self.predict(img_path,conf=conf)

        #2.创建空列表，用于存储裁剪后的图片
        crops = []
        #3.遍历每张图片的检测结果
        for result in results:
            #4.获取该图像的所有检测框
            boxes = result.boxes
            #5.如果该图像有检测框
            if boxes is not None and len(boxes) > 0:
                #6.遍历每个检测框
                for box in boxes:
                    #7.裁剪图像，基于框的坐标[y1:x1,y2:x2]     int(box.xyxy[0][1] ：y1    int(box.xyxy[0][3] ：y2
                    #   image[height,weight,channel]       int(box.xyxy[0][0] ：x1    int(box.xyxy[0][2] ：x2))
                    crop = result.orig_img[int(box.xyxy[0][1]):int(box.xyxy[0][3]),
                                           int(box.xyxy[0][0]):int(box.xyxy[0][2])]
                    #8.将裁剪的图像加入列表中
                    crops.append(crop)
        #9.返回裁剪后的图片列表和检测结果
        return crops,results



    #检测并裁剪返回皮损区域图像
    def predict_with_box(self,img_path,conf=0.25,save_path=None):
        results = self.predict(img_path,conf=conf)
        coordinates = []

        for result in results:
            boxes = result.boxes
            if boxes is not None and len(boxes) > 0:
                #获取坐标 [x1,y1,x2,y2]
                coords = boxes.xyxy.cpu().numpy().tolist()[0]
                coordinates.append(coords)


                #保存带框图片
                if save_path:
                    result.save(save_path)

        return results,coordinates


    #保存模型
    def save(self, save_path, epoch=0):
        self.model.save(save_path)


    #加载模型
    def load(self, weights_path):
        self.loaded_checkpoint = weights_path  # 记录加载了checkpoint
        # 尝试用YOLO直接加载（适用于best.pt格式，用于推理）
        try:
            self.model = YOLO(weights_path)
            return 0
        except:
            pass

        # 如果失败，用原来的方式加载state_dict（适用于checkpoint.pt，用于恢复训练）
        checkpoint = torch.load(weights_path, map_location=device, weights_only=False)

        if 'model' not in checkpoint:
            # 如果没有model键，说明是ultralytics格式，再用YOLO加载
            self.model = YOLO(weights_path)
            return 0

        model_state = self.model.model.state_dict()
        pretrained_state = checkpoint['model']
        matched_state = {}
        for k, v in pretrained_state.items():
            if k in model_state and v.shape == model_state[k].shape:
                matched_state[k] = v
        self.model.model.load_state_dict(matched_state, strict=False)
        return checkpoint.get('epoch', 0)



    #冻结层,冻结前num_layers层
    def freeze_layers(self,num_layers):
        for i,layer in enumerate(self.model.model.parameters()):
            if i < num_layers:
                layer.requires_grad = False


    #LoRA微调配置
    def apply_lora(self,r=8,lora_alpha=16,dropout=0.1):
        #参1：lora秩  参2:缩放因子  参3:随机失活比例

        lora_config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            lora_dropout=dropout,
            # target_modules=['.*'],
            bias="none",
            task_type="DETECTION",      #检测任务
        )


        self.model = get_peft_model(self.model.model,lora_config)
        self.model.print_trainable_parameters()
















