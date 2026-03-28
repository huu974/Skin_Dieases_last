"""
数据集划分
"""
import os
import shutil
import random


#获取验证集 ->就是在训练集的基础上随机选择一部分作为验证集
def split_dataset(source_dir, val_ratio=0.2):
    train_dir = 'archive/train-new'
    val_dir = 'archive/val'

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    total_train, total_val = 0, 0

    #遍历所有子目录
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        if not os.path.isdir(class_path):
            continue

        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)

        images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        random.seed(42)
        random.shuffle(images)

        val_count = int(len(images) * val_ratio)
        val_images = images[:val_count]
        train_images = images[val_count:]

        for img in train_images:
            shutil.copy(os.path.join(class_path, img), os.path.join(train_dir, class_name, img))
        for img in val_images:
            shutil.copy(os.path.join(class_path, img), os.path.join(val_dir, class_name, img))

        total_train += len(train_images)
        total_val += len(val_images)
        print(f"{class_name}: 训练 {len(train_images)}, 验证 {len(val_images)}")

    print(f"\n总计: 训练 {total_train}, 验证 {total_val}")
    print(f"训练集目录: {train_dir}")
    print(f"验证集目录: {val_dir}")


if __name__ == '__main__':
    split_dataset('archive/train', val_ratio=0.2)