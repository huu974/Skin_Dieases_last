# 完整示例：手写数字识别项目

> 从环境配置到运行代码的完整流程演示

---

## 📋 项目介绍

这是一个基于 PyTorch 的 MNIST 手写数字识别项目，包含：
- 数据下载与预处理
- 基线模型训练
- 数据增强训练
- 学习曲线可视化
- 真实手写照片测试

**项目路径**：`C:\Users\123\Desktop\1 - OCRExperiment\手写数字识别`

---

## 1. 创建项目环境


**1.打开**
![[Pasted image 20260331213421.png]]



**2.检查环境有没有新建的环境**

![[Pasted image 20260331213518.png]]

**因为我发现大家的环境用了我视频里面的指令出现没有环境名的情况，我今天发现是我指定了默认创建环境的目录，所以大家使用了我的指令出现了与我不一样的情况，接下来的几种方式应该可以解决，我将使用方法二给大家演示一下**

输入命令

```base
notepad %USERPROFILE%\.condarc
```


![[Pasted image 20260331214257.png]]

**修改我标注的路径即可**


### 方法 1：使用 `--prefix` 参数

```bash
# 在指定路径创建环境
conda create --prefix D:\envs\myenv python=3.10

# 激活指定路径的环境
conda activate D:\envs\myenv

# 注意：使用 --prefix 创建的环境不会显示在 env list 的默认列表中
# 但可以通过完整路径激活
```

### 方法 2：修改默认环境路径（推荐）

编辑 `~\.condarc` 文件（没有则创建）：

```yaml
envs_dirs:
  - D:\conda_envs        # 自定义环境目录
  - C:\Users\用户名\anaconda3\envs  # 保留默认目录

pkgs_dirs:
  - D:\conda_pkgs        # 自定义包缓存目录
```

然后正常使用：

```bash
conda create -n myenv python=3.10  # 会创建在 D:\conda_envs\myenv
```

### 方法 3：通过环境变量设置

```bash
# Windows PowerShell
$env:CONDA_ENVS_PATH = "D:\conda_envs"
conda create -n myenv python=3.10

# 或在系统环境变量中永久设置 CONDA_ENVS_PATH





```bash
# 进入项目根目录
cd "C:\Users\123\Desktop\1 - OCRExperiment"

# 创建 Python 3.10 环境
conda create -n mnist python=3.10

# 激活环境
conda activate mnist
```




### 安装依赖包

```bash
# 使用清华镜像加速安装
pip install torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install numpy matplotlib Pillow albumentations opencv-python-headless streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者从 requirements.txt 安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 2. PyCharm 配置项目

### 2.1 打开项目

1. 打开 PyCharm
2. `File` → `Open`
![[Pasted image 20260331214855.png]]


3. 选择 `C:\Users\123\Desktop\1 - OCRExperiment`

![[Pasted image 20260331215019.png]]


4. 点击 `选择文件夹`



### 2.2 配置 Python 解释器

1.点击右下角
![[Pasted image 20260331215317.png]]


2.选择添加新的解释器

3.添加本地解释器

![[Pasted image 20260331215358.png]]



4.选择现有

![[Pasted image 20260331215429.png]]




5.选择conda

![[Pasted image 20260331215453.png]]



6.找到你创建的环境即可


![[Pasted image 20260331215524.png]]



如果系统没有检测到你的conda路径

1.找到你安装anaconda的目录

![[Pasted image 20260331215632.png]]


2.进入condabin
![[Pasted image 20260331215659.png]]






3.点击conda.bat

![[Pasted image 20260331215725.png]]






## 3.跑通模型









```


3. 运行项目代码

```bash
# 进入手写数字识别目录
cd 手写数字识别

# 1. 下载 MNIST 数据集（首次运行）
python download_mnist.py

# 2. 可视化样本
python visualize_samples.py

# 3. 基线训练
python train_baseline.py

# 4. 数据增强训练
python train_with_augmentation.py

# 5. 对比学习曲线
python plot_learning_curves.py

# 6. 测试真实手写照片
python test_real_photos.py --image_dir <你的图片目录>
```

### 3.2 在 Anaconda Prompt 中运行

1. 打开 `Anaconda Prompt`
2. 激活环境并运行：

```bash
conda activate mnist
cd "C:\Users\123\Desktop\1 - OCRExperiment\手写数字识别"
python train_baseline.py
```

### 3.3 在 PyCharm 中直接运行



---

## 4. 完整工作流示例

### 场景：从零开始训练模型


项目路径
![[Pasted image 20260331220236.png]]



![[Pasted image 20260331220522.png]]


我创建了一个requirement.txt文件，大家激活环境之后使用下面命令就可以了

```base
pip install -r requirements.txt ```
-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```


这边也是成功了

![[Pasted image 20260331220752.png]]





```

```bash
# ========== 步骤 1: 准备环境 ==========
# 打开 Anaconda Prompt
conda create -n mnist python=3.10 -y
conda activate mnist

# ========== 步骤 2: 进入项目路径 ==========
cd /d "C:\Users\123\Desktop\1 - OCRExperiment"

#3.安装第三方库，使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# ========== 步骤 4: 下载数据 ==========
python download_mnist.py

# ========== 步骤 5: 查看数据样本 ==========
python visualize_samples.py

# ========== 步骤 6: 训练基线模型 ==========
python train_baseline.py

# ========== 步骤 7: 训练增强模型（对比效果）==========
python train_with_augmentation.py

# ========== 步骤 8: 可视化对比结果 ==========
python plot_learning_curves.py


```

---

## 5. 常用命令速查

### 环境管理

```bash
conda activate mnist          # 激活环境
conda deactivate              # 退出环境
pip list                    # 查看已安装包
conda env list                # 查看所有环境
```

### 使用镜像源安装

```bash
# 清华镜像
pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 阿里云镜像
pip install 包名 -i https://mirrors.aliyun.com/pypi/simple
```

---

## 6. 项目结构说明

```
1 - OCRExperiment/
├── 手写数字识别/              # 主项目目录
│   ├── data/                  # MNIST 数据集（自动下载）
│   ├── models/                # 保存的模型
│   ├── outputs/               # 训练输出
│   ├── download_mnist.py      # 下载数据
│   ├── train_baseline.py      # 基线训练
│   ├── train_with_augmentation.py  # 增强训练
│   ├── visualize_samples.py   # 可视化样本
│   ├── plot_learning_curves.py # 绘制学习曲线
│   └── test_real_photos.py    # 测试真实照片
├── app.py                     # Web 应用入口
├── requirements.txt           # 依赖列表
└── README.md                  # 项目说明
```



### 各脚本功能说明

| 脚本文件                         | 功能           | 输出                            |
| ---------------------------- | ------------ | ----------------------------- |
| `download_mnist.py`          | 下载 MNIST 数据集 | `data/` 目录                    |
| `visualize_samples.py`       | 显示样本图片       | 弹出图片窗口                        |
| `visualize_augmentation.py`  | 显示数据增强效果     | 弹出对比图片                        |
| `train_baseline.py`          | 基线模型训练       | `outputs/baseline/`           |
| `train_with_augmentation.py` | 数据增强训练       | `outputs/with_augmentation/`  |
| `plot_learning_curves.py`    | 对比学习曲线       | `outputs/learning_curves.png` |
| `test_real_photos.py`        | 测试真实照片       | 终端输出预测结果                      |

### 预期输出结果

运行完成后，`outputs/` 目录结构：

```
outputs/
├── baseline/
│   ├── model.pt              # 基线模型权重
│   └── history.json          # 训练历史记录
├── with_augmentation/
│   ├── model.pt              # 增强模型权重
│   └── history.json          # 训练历史记录
└── learning_curves.png       # 学习曲线对比图
```

###  单独运行某个脚本

如果只想运行特定步骤：

```bash
# 只训练基线模型
python train_baseline.py

# 只训练增强模型
python train_with_augmentation.py

# 只查看数据样本
python visualize_samples.py

# 只对比学习曲线（需要先完成两个训练）
python plot_learning_curves.py
```


## 7. 拓展：调节模型参数（详细版）

 为什么要调节参数

深度学习模型的性能很大程度上取决于超参数的选择。不同的参数组合会导致：
- **收敛速度**：有的参数几天才能收敛，有的几小时就行
- **最终精度**：好的参数组合可以提升 5-10% 的准确率
- **泛化能力**：参数不当会导致过拟合或欠拟合

###  可调节的参数详解

项目中的训练脚本支持以下命令行参数：

####  训练轮数（--epochs）

**定义**：整个训练数据集被遍历的次数

**默认值**：10

**影响**：
- epochs 太小 → 模型欠拟合，学不够
- epochs 适中 → 模型充分学习，泛化好
- epochs 太大 → 模型过拟合，记住训练集但泛化差

**实验对比**：

```bash
# 实验 A：5 轮（快速测试，可能欠拟合）
python train_baseline.py --epochs 5 --out_dir outputs/epochs_5
# 预期结果：训练准确率 90% 左右，测试准确率 88% 左右

# 实验 B：10 轮（标准配置，推荐）
python train_baseline.py --epochs 10 --out_dir outputs/epochs_10
# 预期结果：训练准确率 98% 左右，测试准确率 97% 左右

# 实验 C：20 轮（充分训练）
python train_baseline.py --epochs 20 --out_dir outputs/epochs_20
# 预期结果：训练准确率 99%+，测试准确率 98% 左右

# 实验 D：50 轮（可能过拟合）
python train_baseline.py --epochs 50 --out_dir outputs/epochs_50
# 预期结果：训练准确率 99.9%，测试准确率可能下降到 97%
```

**如何判断最佳 epochs**：

观察验证准确率（val_acc）：
- 如果 val_acc 还在上升 → 可以增加 epochs
- 如果 val_acc 开始下降 → 已经过拟合，应该停止
- 如果 val_acc 平稳 → 当前 epochs 刚好合适

#### 10.2.2 学习率（--lr）

**定义**：模型参数每次更新的步长大小

**默认值**：0.001（即 1e-3）

**重要性**：⭐⭐⭐⭐⭐ 最重要的超参数

**原理说明**：

想象你在下山找最低点（损失函数最小值）：
- **学习率太大** = 步子太大，可能跨过最低点，甚至往山上走
- **学习率适中** = 步子合适，能稳定走到最低点
- **学习率太小** = 步子太小，要走很久才能到，可能困在局部最小值

**实验对比**：

```bash
# 实验 A：学习率 0.0001（太小，收敛慢）
python train_baseline.py --lr 0.0001 --epochs 20 --out_dir outputs/lr_0.0001
# 现象：损失下降很慢，20轮后可能还没收敛
# 训练日志示例：
# Epoch 1: train loss=2.1234 acc=0.4567 | val loss=1.9876 acc=0.5234
# Epoch 20: train loss=0.5678 acc=0.8765 | val loss=0.6543 acc=0.8543

# 实验 B：学习率 0.001（推荐，适中）
python train_baseline.py --lr 0.001 --epochs 10 --out_dir outputs/lr_0.001
# 现象：损失稳定下降，10轮左右收敛
# 训练日志示例：
# Epoch 1: train loss=1.5432 acc=0.6543 | val loss=1.2345 acc=0.7654
# Epoch 5: train loss=0.3456 acc=0.9123 | val loss=0.4321 acc=0.8987
# Epoch 10: train loss=0.1234 acc=0.9789 | val loss=0.1876 acc=0.9654

# 实验 C：学习率 0.01（较大，收敛快但可能震荡）
python train_baseline.py --lr 0.01 --epochs 10 --out_dir outputs/lr_0.01
# 现象：前几轮下降很快，但后面可能震荡
# 训练日志示例：
# Epoch 1: train loss=0.8765 acc=0.7890 | val loss=0.6543 acc=0.8234
# Epoch 3: train loss=0.2345 acc=0.9456 | val loss=0.3456 acc=0.9234
# Epoch 5: train loss=0.1567 acc=0.9678 | val loss=0.2987 acc=0.9345
# Epoch 7: train loss=0.1890 acc=0.9567 | val loss=0.3123 acc=0.9289  <- 开始震荡

# 实验 D：学习率 0.1（太大，可能无法收敛）
python train_baseline.py --lr 0.1 --epochs 10 --out_dir outputs/lr_0.1
# 现象：损失可能不下降，甚至上升，准确率波动大
# 训练日志示例：
# Epoch 1: train loss=5.6789 acc=0.1234 | val loss=6.5432 acc=0.0987
# Epoch 2: train loss=7.8901 acc=0.0876 | val loss=8.7654 acc=0.0765
# 损失越来越大，模型学不到东西
```

**学习率调节策略**：

1. **初始尝试**：从 0.001 开始（大多数情况的良好起点）
2. **观察训练**：
   - 如果损失下降很慢 → 增大学习率（×10）
   - 如果损失震荡或不降 → 减小学习率（÷10）
3. **精细调节**：找到大致范围后，尝试中间值（如 0.001 和 0.01 之间试 0.003、0.005）

#### 10.2.3 批次大小（--batch_size）

**定义**：每次参数更新时使用的样本数量

**默认值**：128

**影响**：
- **内存占用**：batch_size 越大，需要的显存/GPU内存越多
- **训练速度**：batch_size 越大，每次迭代越快（并行计算效率高）
- **梯度稳定性**：batch_size 越大，梯度估计越稳定
- **泛化能力**：batch_size 太小可能泛化更好（有噪声的梯度有助于跳出局部最优）

**实验对比**：

```bash
# 实验 A：batch_size=32（小批次，适合小显存）
python train_baseline.py --batch_size 32 --out_dir outputs/bs_32
# 特点：
# - 显存占用：约 1-2 GB
# - 训练速度：较慢（每次迭代样本少，但迭代次数多）
# - 梯度：噪声较大，可能有助于泛化
# - 适用：显存 < 4GB 的 GPU，或 CPU 训练

# 实验 B：batch_size=128（标准批次，推荐）
python train_baseline.py --batch_size 128 --out_dir outputs/bs_128
# 特点：
# - 显存占用：约 2-4 GB
# - 训练速度：适中
# - 梯度：相对稳定
# - 适用：大多数情况

# 实验 C：batch_size=256（大批次，需要大显存）
python train_baseline.py --batch_size 256 --out_dir outputs/bs_256
# 特点：
# - 显存占用：约 4-8 GB
# - 训练速度：快（每次迭代处理更多样本）
# - 梯度：很稳定
# - 适用：显存 >= 8GB 的 GPU

# 实验 D：batch_size=512（超大批次，需要很大显存）
python train_baseline.py --batch_size 512 --out_dir outputs/bs_512
# 特点：
# - 显存占用：约 8GB+
# - 训练速度：很快
# - 注意：可能需要相应增大学习率（线性缩放规则）
```

**批次大小与学习率的关系**：

有一个经验法则叫"线性缩放规则"：
- 如果 batch_size 增大 N 倍，学习率也应该增大 N 倍
- 例如：batch_size 从 128 增加到 256（×2），学习率从 0.001 增加到 0.002

```bash
# 标准配置
python train_baseline.py --batch_size 128 --lr 0.001

# 大批次配置（应用线性缩放）
python train_baseline.py --batch_size 256 --lr 0.002

# 更大批次
python train_baseline.py --batch_size 512 --lr 0.004
```

#### 输出目录（--out_dir）

**定义**：保存模型和训练历史的目录

**默认值**：`outputs/baseline` 或 `outputs/with_augmentation`

**用途**：
- 区分不同实验的结果
- 避免覆盖之前的训练结果
- 方便对比不同参数的效果

**命名建议**：

```bash
# 按参数命名
python train_baseline.py --lr 0.001 --epochs 20 --out_dir outputs/lr0.001_ep20

# 按实验目的命名
python train_baseline.py --out_dir outputs/baseline_standard
python train_baseline.py --out_dir outputs/baseline_fast
python train_baseline.py --out_dir outputs/baseline_high_accuracy

# 按日期命名
python train_baseline.py --out_dir outputs/exp_20240331_v1
python train_baseline.py --out_dir outputs/exp_20240331_v2
```

系统化的参数调节方法

#### 单变量实验法（控制变量法）

每次只改变一个参数，保持其他参数不变，观察效果。

**步骤 1：确定基线**

```bash
# 使用默认参数作为基线
python train_baseline.py --epochs 10 --lr 0.001 --batch_size 128 --out_dir outputs/baseline
```

**步骤 2：调节学习率**

```bash
# 固定 epochs=10, batch_size=128，只改学习率
python train_baseline.py --lr 0.0001 --out_dir outputs/lr_0.0001
python train_baseline.py --lr 0.0005 --out_dir outputs/lr_0.0005
python train_baseline.py --lr 0.001  --out_dir outputs/lr_0.001   # 基线
python train_baseline.py --lr 0.003  --out_dir outputs/lr_0.003
python train_baseline.py --lr 0.005  --out_dir outputs/lr_0.005
python train_baseline.py --lr 0.01   --out_dir outputs/lr_0.01
```

对比结果，找到最佳学习率（假设是 0.0005）。

**步骤 3：调节训练轮数**

```bash
# 固定 lr=0.0005（上一步找到的最佳值），batch_size=128，只改 epochs
python train_baseline.py --lr 0.0005 --epochs 5  --out_dir outputs/ep5
python train_baseline.py --lr 0.0005 --epochs 10 --out_dir outputs/ep10
python train_baseline.py --lr 0.0005 --epochs 15 --out_dir outputs/ep15
python train_baseline.py --lr 0.0005 --epochs 20 --out_dir outputs/ep20
python train_baseline.py --lr 0.0005 --epochs 30 --out_dir outputs/ep30
```

对比结果，找到最佳 epochs（假设是 20）。

**步骤 4：调节批次大小**

```bash
# 固定 lr=0.0005, epochs=20，只改 batch_size
python train_baseline.py --lr 0.0005 --epochs 20 --batch_size 64  --out_dir outputs/bs64
python train_baseline.py --lr 0.0005 --epochs 20 --batch_size 128 --out_dir outputs/bs128
python train_baseline.py --lr 0.0005 --epochs 20 --batch_size 256 --out_dir outputs/bs256
```

**步骤 5：组合最优参数**

```bash
# 使用找到的最佳参数组合
python train_baseline.py --lr 0.0005 --epochs 20 --batch_size 128 --out_dir outputs/best
```



### 完整的参数调节流程

#### 阶段 1：快速探索（找到大致范围）

```bash
# 创建实验目录
mkdir outputs\exp_phase1

# 快速测试不同学习率（epochs=5 快速验证）
python train_baseline.py --lr 0.0001 --epochs 5 --out_dir outputs/exp_phase1/lr_small
python train_baseline.py --lr 0.001  --epochs 5 --out_dir outputs/exp_phase1/lr_medium
python train_baseline.py --lr 0.01   --epochs 5 --out_dir outputs/exp_phase1/lr_large

# 查看结果，假设 lr=0.001 最好
```

#### 阶段 2：精细调节（找到最佳值）

```bash
mkdir outputs\exp_phase2

# 在学习率 0.0005 ~ 0.003 之间精细搜索
python train_baseline.py --lr 0.0005 --epochs 10 --out_dir outputs/exp_phase2/lr_0.0005
python train_baseline.py --lr 0.0008 --epochs 10 --out_dir outputs/exp_phase2/lr_0.0008
python train_baseline.py --lr 0.001  --epochs 10 --out_dir outputs/exp_phase2/lr_0.001
python train_baseline.py --lr 0.002  --epochs 10 --out_dir outputs/exp_phase2/lr_0.002
python train_baseline.py --lr 0.003  --epochs 10 --out_dir outputs/exp_phase2/lr_0.003

# 查看结果，假设 lr=0.0008 最好
```

#### 阶段 3：调节训练轮数

```bash
mkdir outputs\exp_phase3

# 固定 lr=0.0008，调节 epochs
python train_baseline.py --lr 0.0008 --epochs 10 --out_dir outputs/exp_phase3/ep10
python train_baseline.py --lr 0.0008 --epochs 15 --out_dir outputs/exp_phase3/ep15
python train_baseline.py --lr 0.0008 --epochs 20 --out_dir outputs/exp_phase3/ep20
python train_baseline.py --lr 0.0008 --epochs 25 --out_dir outputs/exp_phase3/ep25

# 查看结果，假设 epochs=20 最好
```

#### 阶段 4：最终验证

```bash
# 使用找到的最佳参数进行充分训练
python train_baseline.py --lr 0.0008 --epochs 20 --batch_size 128 --out_dir outputs/final_best

# 同时训练数据增强版本作为对比
python train_with_augmentation.py --lr 0.0008 --epochs 20 --batch_size 128 --out_dir outputs/final_best_aug

# 对比学习曲线
python plot_learning_curves.py
```

###  结果分析与可视化

#### 查看训练历史

每个实验目录下都有 `history.json` 文件，包含：

```json
{
  "train_loss": [2.3, 1.5, 0.8, 0.5, 0.3, ...],
  "train_acc": [0.3, 0.6, 0.8, 0.9, 0.95, ...],
  "val_loss": [2.2, 1.4, 0.9, 0.6, 0.5, ...],
  "val_acc": [0.35, 0.65, 0.82, 0.89, 0.92, ...],
  "test_loss": 0.45,
  "test_acc": 0.93
}
```


### 数据增强的参数调节

`train_with_augmentation.py` 支持相同的参数，但效果可能不同：

```bash
# 数据增强通常可以使用更大的学习率（数据更多样化，需要更大步长）
python train_with_augmentation.py --lr 0.002 --epochs 15 --out_dir outputs/aug_lr0.002

# 或者更多轮数（数据增强相当于增加了数据量）
python train_with_augmentation.py --lr 0.001 --epochs 25 --out_dir outputs/aug_ep25

# 对比基线和增强版本
# 修改 plot_learning_curves.py
experiments = {
    "基线": "outputs/baseline/history.json",
    "数据增强": "outputs/with_augmentation/history.json",
}
```


---

> 💡 **总结**：参数调节是深度学习的重要技能。建议从默认参数开始，先理解每个参数的作用，然后系统地实验，记录结果，最终找到适合你任务的最佳配置。
