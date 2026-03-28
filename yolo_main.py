""""
yolo模块主函数
"""

import os
import signal
import sys
import time
import torch
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
from model.yolo_detector import YOLOv10Detector
from utils.config_handler import yolov10
from utils.arguments import parse_yolo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from datetime import datetime


class InterruptHandler:
    def __init__(self,detector,opts):
        self.detector = detector
        self.opts = opts
        self.current_epochs = 0


    def handler(self, signum, frame):
        #参1：信号编号        参2：当前执行帧对象，用于获取程序中断时的状态
        print("\n检测到 Ctrl+C，正在保存模型...")
        #保存模型
        save_path = f'{self.opts.save_path}/checkpoint.pt'
        print(f'模型保存到 {save_path}')
        sys.exit(0)



def main():
    writer = SummaryWriter('runs/yolo_training')
    #1.解析参数
    opts = parse_yolo()

    #2.设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"设备: {device}")


    #3.初始化模型
    model_size = yolov10['model_size']
    detector = YOLOv10Detector(model_size=model_size,device=device)


    #5.选择微调模式
    if opts.yolo_lora:
        print("使用LoRA微调")
        detector.apply_lora(r=opts.lora_r,lora_alpha=opts.lora_alpha,dropout=opts.lora_dropout)

    if opts.yolo_freeze:
        print(f"冻结前{opts.yolo_freeze}层")
        detector.freeze_layers(opts.yolo_freeze)



    if opts.yolo_resume:
        print(f"从{opts.yolo_resume}恢复训练")
        start_epoch = detector.load(opts.yolo_resume)
        print(f"从第{start_epoch + 1}轮恢复训练")
    else:
        start_epoch = 0

    #6.训练参数
    # data_yaml = yolov10['data_yaml']
    # epochs = yolov10['epochs']
    # batch_size = yolov10['batch_size']
    # lr0 = yolov10['lr0']
    # imgsz = yolov10['imgsz']

    #7.设置 Ctrl+C 捕获
    handler = InterruptHandler(detector,opts)
    #参1：ctrl+c中断信号    参2：当收到中断信号时，执行handler函数
    signal.signal(signal.SIGINT, handler.handler)




    #7.训练与验证
    for epoch in range(opts.epochs):
        handler.current_epochs = epoch
        #8训练一个epoch
        print(f'Epoch {epoch + 1}/{opts.epochs}')
        print("训练中...")
        tra_results = detector.train(
            data_yaml="E:\\py项目\\Skin diseases\\HAM10000\\yolo_dataset\\data.yaml",
            epochs=1,
            batch_size=16,
            lr0=1e-3,
            imgsz=640,
            project=f'runs/detect/{datetime.now().strftime("%Y%m%d-%H%M%S")}',
        )
        tra_loss = tra_results.box.loss if hasattr(tra_results.box, 'loss') else tra_results.box.mp
        tra_acc = tra_results.box.mp
        writer.add_scalar('Train/Loss', tra_loss, epoch)
        writer.add_scalar('Train/Accuracy', tra_acc, epoch)


        print(f'训练：损失:{tra_loss:.4f} 精度:{tra_acc:.4f}\n')

        #9验证一个epoch
        print("正在验证...")
        val_results = detector.val(data_yaml="E:\\py项目\\Skin diseases\\HAM10000\\yolo_dataset\\data.yaml")
        val_loss = val_results.box.loss if hasattr(val_results.box, 'loss') else val_results.box.mp
        val_acc = val_results.box.mp
        writer.add_scalar('Val/Loss', val_loss, epoch)
        writer.add_scalar('Val/Accuracy', val_acc, epoch)

        print(f'验证：损失:{val_loss:.4f} 精度:{val_acc:.4f}\n')

        #11.保存模型
        save_path = f'{opts.save_path}/checkpoint.pt'
        detector.save(save_path, epoch=epoch)
        print(f'模型已保存到{save_path}')
    writer.close()

if __name__ == '__main__':
    main()





