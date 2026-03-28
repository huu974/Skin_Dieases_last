"""
分类模型评估脚本
"""

import  os
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights
from model.PanDerm import MyModel
from utils.config_handler import model_conf


TEST_DATA_PATH = './archive/val'  # 验证集路径
MODEL_PATH = './variables/best_model.pth.tar'  # 模型权重路径
CLASSES = [
    'Acne and Rosacea Photos',
    'Actinic Keratosis Basal Cell Carcinoma',
    'Atopic Dermatitis Photos',
    'Bullous Disease Photos',
    'Cellulitis Impetigo and other Bacterial Infections',
    'Eczema Photos',
    'Exanthems and Drug Eruptions',
    'Hair Loss Photos Alopecia',
    'Herpes HPV and other STDs Photos',
    'Light Diseases and Disorders of Pigmentation',
    'Lupus and other Connective Tissue diseases',
    'Melanoma Skin Cancer Nevi and Moles',
    'Nail Fungus and other Nail Disease',
    'Poison Ivy Photos and other Contact Dermatitis',
    'Psoriasis pictures Lichen Planus',
    'Scabies Lyme Disease and other Infestations',
    'Seborrheic Keratoses and other Benign Tumors',
    'Systemic Disease',
    'Tinea Ringworm Candidiasis and other Fungal Infections',
    'Urticaria Hives',
    'Vascular Tumors',
    'Vasculitis Photos',
    'Warts Molluscum and other Viral Infections'
]
NUM_CLASSES = len(CLASSES)
BATCH_SIZE = 16






device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#获取数据预处理
def get_transforms():
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


#加载checkpoint
def load_checkpoint(model, checkpoint_path, device):
    checkpoint = torch.load(checkpoint_path, map_location=device)   #加载文件，将数据放到GPU
    model.load_state_dict(checkpoint['model_state_dict'])           #将从字典里面获取的模型参数加载到模型结构中
    model.eval()       #设置模型为验证模式
    return model

#评估模型
def evaluate(model, dataloader, device):
    model.eval()
    all_preds = []
    all_labels = []
    all_scores = []

    with torch.no_grad():
        for batch_index, (images, labels) in enumerate(dataloader):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            scores = torch.softmax(outputs, dim=1)
            preds = torch.argmax(scores, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_scores.extend(scores.cpu().numpy())

    return np.array(all_labels), np.array(all_preds), np.array(all_scores)


#绘制混淆矩阵
def plot_confusion_matrix(cm,classes,save_path='confusion_matrix.png'):
    plt.figure(figsize=(20,18))

    #参1：混淆矩阵 参2：在每个格子中显示数字 参3：显示的数字的格式 参4：x轴刻度标签 参5：y轴刻度标签 参6：字体大小 参7：颜色
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=classes, yticklabels=classes,annot_kws={"size":8},cmap='Blues')

    plt.xlabel('Predicted Label',fontsize=12)
    plt.ylabel('True Label',fontsize=12)
    plt.title('Confusion Matrix',fontsize=16)
    plt.xticks(rotation=45,ha='right')  #x轴标签旋转45度
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path,dpi=150,bbox_inches='tight')      #参2：分辨率 参3：裁剪白边
    plt.close()                         #关闭当前窗口，释放内存
    print(f"混淆矩阵已保存到 {save_path}")


def main(model):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    print(f"设备: {device}")
    test_dataset = ImageFolder(root=TEST_DATA_PATH, transform=get_transforms())
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    print(f"数据集大小: {len(test_dataset)}")
    print(f'类别数：{NUM_CLASSES}')
    if os.path.exists(MODEL_PATH):
        model = load_checkpoint(model, MODEL_PATH, device)
        print(f"已加载模型权重: {MODEL_PATH}")
    else:
        print("未找到模型权重文件")
        return


    print("正在评估模型...")
    labels,preds,scores = evaluate(model, test_loader, device)

    # 计算评估指标
    accuracy = accuracy_score(labels, preds)
    precision = precision_score(labels, preds, average='macro',zero_division=0)
    recall = recall_score(labels, preds, average='macro',zero_division=0)
    f1 = f1_score(labels, preds, average='macro')
    print(f"准确率: {accuracy:.4f}")
    print(f"精确率: {precision:.4f}")
    print(f"召回率: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    """
    average = 'macro' ：多分类是，对每个类别分别计算，再去平均值
    zero_division = 0 ：当某个类别没有预测样本是，返回0而不是警告
    """

    # 绘制混淆矩阵
    cm = confusion_matrix(labels, preds)
    plot_confusion_matrix(cm, test_dataset.classes)

    print('分类报告')
    print(classification_report(
        labels, preds, target_names=test_dataset.classes, zero_division=0
    ))



if __name__ == '__main__':
    os.environ['TORCH_HOME'] = model_conf["save_path"]
    model = efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1)
    xiaohui = MyModel(model=model, num_classes=model_conf["num_classes"])
    model = xiaohui.model_classifier().to(device)

    main(model)













