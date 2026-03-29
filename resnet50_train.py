import os
import torch
import torch.nn as nn
from torch import autocast
from torch.utils.data import DataLoader
from torchvision import models, transforms
from torchvision.datasets import ImageFolder
from tqdm import tqdm
import time
import numpy as np
from utils.dataset import mixup_cutmix_data
from utils.arguments import parse
from utils.config_handler import model_conf
from utils.lr_policy import LR






# 指标计量器
class AverageMeter(object):
    def __init__(self):
        self.reset()    #在每一个epoch中调用，清空所有值

    def reset(self):
        self.val = 0        #当前值
        self.avg = 0        #平均值
        self.sum = 0        #累计和
        self.count = 0      #样本数

    #更新计量器
    def update(self,val,n=1):
        """
        val:新值
        n:样本数量
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count













