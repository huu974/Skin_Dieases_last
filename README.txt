================================================================================
                            Skin diseases 项目说明
================================================================================

本项目是一个基于深度学习的皮肤病智能诊断系统，集成了图像分类、多Agent
智能诊断和RAG知识增强三大核心功能。

================================================================================
                              文件说明
================================================================================

【核心代码】
main.py                    - 模型训练主入口
train_validation.py       - 训练与验证逻辑实现
evaluate.py               - 模型评估脚本（生成混淆矩阵、分类报告）
test.py                   - 测试脚本
run_agent.py              - Agent智能诊断系统启动入口
dataset_split.py          - 数据集划分脚本
generate_ppt.py           - 诊断报告PPT生成
requirements.txt          - Python依赖包列表
README.md                 - 项目说明文档

【模型定义 - model/】
PanDerm.py                - EfficientNet-B3皮肤病分类模型
ResNet50.py               - ResNet50分类模型
custom_skin_net.py        - 自定义皮肤病网络（带CBAM注意力机制）
factory.py                - 模型工厂（根据配置动态创建模型）

【工具函数 - utils/】
dataset.py                - 数据集加载与增强（MixUp/CutMix/颜色抖动等）
arguments.py              - 命令行参数解析
config_handler.py         - YAML配置文件加载器
lr_policy.py              - 学习率调度策略（Cosine退火+Warmup）
optimizer_Adam.py         - 自定义Adam优化器封装
outputwriter.py           - 模型权重保存
writer.py                 - TensorBoard日志记录
logger.py                 - 日志管理
file_handler.py           - 文件操作工具
path_tool.py              - 路径处理工具
prompt_loader.py          - 提示词加载器
first_order_oracle.py     - 一阶Oracle工具

【智能体系统 - agent/】
multi_agent_manager.py    - 多Agent管理器（核心调度器）
symptom_agent.py          - 症状分析Agent
image_agent.py            - 图像诊断Agent（调用CNN分类模型）
treatment_agent.py       - 治疗建议Agent
test_agent.py            - Agent测试脚本
tools/
    agent_tools.py        - Agent功能工具集
    middleware.py         - 中间件

【RAG知识增强 - rag/】
rag_service.py            - RAG服务核心（检索/重排序/过滤/生成）
vector_store.py           - 向量存储（ChromaDB + text-embedding-v3）
enhanced_rag.py          - 增强版RAG（LangChain集成）

【配置文件 - config/】
default.yml               - 默认训练配置（batch_size/lr/epochs等）
model.yml                 - 模型配置（23类皮肤病类别定义）
rag.yml                   - RAG模块配置
agent.yml                 - Agent系统配置
chroma.yml                - Chroma向量数据库配置
prompts.yml               - 提示词配置
instructions.yml          - 指令配置
test_evaluate.yml         - 测试评估配置

【前端界面 - frontend-react/】
React + Vite + Tailwind CSS 构建的Web诊断界面
包含：诊断页面、聊天页面、历史记录、登录注册、个人中心

【后端服务 - backend/】
main.py                   - FastAPI后端服务入口
init_db.py                - 数据库初始化

【数据与知识库 - data/】
disease_info.txt          - 皮肤病基础知识
common_qa.txt             - 常见问答
prevention_tips.txt       - 预防建议
medication_guide.txt      - 用药指南
medical_advice.txt        - 医疗建议
differential_diagnosis.txt - 鉴别诊断知识

【数据集 - skin diseases/】
train-new/                - 训练集（23类皮肤病图像）
val/                      - 验证集
test/                     - 测试集

【其他资源】
prompts/                  - Agent提示词模板文件
pretrained/               - 预训练模型缓存
variables/                - 训练保存的模型权重
runs/                     - TensorBoard训练日志
logs/                     - 运行日志
confusion_matrix*.png     - 模型混淆矩阵图
checkpoint.pth.tar        - 训练保存的模型checkpoint
md5.text                  - 知识库MD5校验文件

================================================================================
                              使用说明
================================================================================

1. 模型训练：
   python main.py --val True

2. 模型评估：
   python evaluate.py

3. 启动Agent诊断：
   python run_agent.py

4. 启动前端：
   cd frontend-react && npm run dev

5. 启动后端：
   cd backend && python main.py

================================================================================