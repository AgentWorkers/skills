---
name: Keras
slug: keras
version: 1.0.0
homepage: https://clawic.com/skills/keras
description: 使用 Keras 的模式、层配置以及训练诊断工具来构建、训练和调试深度学习模型。
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请查阅 `setup.md` 以获取集成指南。用户确认后，该工具会将偏好设置存储在 `~/keras/` 目录中。

## 使用场景

用户使用 Keras 或 TensorFlow 构建神经网络时，该工具会负责处理模型架构、层配置、训练循环、回调函数、损失问题的调试以及模型的部署准备工作。

## 架构

模型相关的数据存储在 `~/keras/` 目录中。具体设置方法请参阅 `memory-template.md`。

```
~/keras/
├── memory.md          # Preferred architectures, hyperparams
└── models/            # Saved model configs (optional)
```

## 快速参考

| 主题 | 文件        |
|-------|------------|
| 设置流程 | `setup.md`      |
| 内存模板 | `memory-template.md` |
| 层结构模式 | `layers.md`     |
| 训练诊断 | `training.md`     |
| 常见架构 | `architectures.md`   |

## 核心规则

### 1. 顺序 API 与函数式 API
- **顺序 API**：简单的模型结构，无分支逻辑
- **函数式 API**：支持多输入/多输出、跳过某些层、共享层
- **子类化**：允许自定义前向传播逻辑，实现动态模型结构

```python
# Sequential - simple stack
model = keras.Sequential([
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Functional - flexible graphs
inputs = keras.Input(shape=(784,))
x = layers.Dense(64, activation='relu')(inputs)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs, outputs)
```

### 2. 输入数据格式
- 第一层需要指定输入数据的形状（不包括批量维度）
- **图像数据**：格式为 `(高度, 宽度, 通道数)`（通道数位于最后）
- **序列数据**：格式为 `(时间步长, 特征值)`
- **表格数据**：格式为 `(特征值, ...`

```python
# Image input
layers.Conv2D(32, 3, input_shape=(224, 224, 3))

# Sequence input
layers.LSTM(64, input_shape=(100, 50))  # 100 timesteps, 50 features

# Tabular input
layers.Dense(64, input_shape=(20,))  # 20 features
```

### 3. 激活函数
| 任务       | 输出激活函数       | 损失函数       |
|------------|------------------|--------------|
| 二分类       | `sigmoid`       | `binary_crossentropy` |
| 多分类       | `softmax`       | `categorical_crossentropy` |
| 多标签分类   | `sigmoid`       | `binary_crossentropy` |
| 回归         | `linear`       | `mse` 或 `mae`      |

### 4. 正则化策略
为防止过拟合，请按以下顺序应用正则化方法：
1. **Dropout**：在密集层或卷积层之后使用（0.2–0.5）
2. **BatchNorm**：在激活函数之前或之后使用
3. **L2 正则化**：在层内部使用（0.01–0.001）
4. **提前停止训练**：通过回调函数实现训练过程中的自动停止

```python
layers.Dense(64, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01))
layers.Dropout(0.3)
layers.BatchNormalization()
```

### 5. 回调函数基础

### 6. 数据管道

### 7. 编译检查清单

- **学习率**：初始值设为 0.001，训练过程中根据情况调整
- **批量大小**：通常推荐使用 32–128，更大的批量大小有助于获得更平滑的梯度

## 常见问题及解决方法

- **输入数据格式不匹配**：检查输入数据的形状是否与模型要求的形状一致（排除批量维度）
- **损失值为 NaN**：降低学习率，检查数据中是否存在无穷大或 NaN 值，并考虑使用梯度裁剪机制
- **验证损失值不稳定**：增加正则化强度，减少模型复杂度，或增加训练数据量
- **模型训练效果不佳**：确认标签是否正确，确保使用的损失函数与任务类型匹配
- **GPU 内存不足**：减小批量大小，使用混合精度计算，或启用梯度检查点保存功能
- **训练速度慢**：使用 `tf.data` 数据管道并启用预加载功能，同时启用 XLA 编译技术

## 外部接口

| 接口          | 发送的数据        | 功能                |
|----------------|------------------|-------------------------|
| TensorFlow 模型中心 | 无（仅用于下载预训练模型权重）| 当 `weights='imagenet'` 时下载预训练权重 |

**注意：** 使用迁移学习功能时，系统会在首次使用时下载预训练模型权重。如需完全离线运行模型，请将 `weights` 参数设置为 `None`。

## 安全性与隐私

- **数据存储**：所有模型结构和配置信息仅保存在 `~/keras/` 目录中
- **数据安全**：该工具不会将模型或数据上传到任何外部服务器；也不会访问 `~/keras/` 目录之外的文件或工作目录中的数据

## 相关技能

用户可根据需要安装以下工具：
- `tensorflow`：用于 TensorFlow 操作和模型部署
- `pytorch`：另一种深度学习框架
- `ai`：通用人工智能和机器学习相关工具
- `models`：模型架构设计相关工具

## 反馈建议

- 如该工具对您有帮助，请给它点赞（ClawHub 上的星形评分）
- 为了保持信息更新，请使用 `clawhub sync` 命令同步最新内容