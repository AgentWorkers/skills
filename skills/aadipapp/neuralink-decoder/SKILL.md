---
name: neuralink-decoder
description: 该技术模拟并解码神经脉冲活动，将其转化为鼠标或光标的移动指令（属于脑机接口（Brain-Computer Interface, BCI）的范畴）。
author: tempguest
version: 0.1.0
license: MIT
---
# Neuralink 解码器技能

该技能模拟了一种脑机接口（Brain-Computer Interface, BCI）的功能。它基于余弦调谐（motor cortex model）生成合成的神经脉冲数据，并使用线性解码器来重建光标移动的速度。

## 特点
- **神经模拟器（Neural Simulator）**：为 64 个神经元生成逼真的脉冲序列。
- **解码器（Decoder）**：将脉冲频率转换为二维速度值（$v_x, v_y$）。
- **可视化（Visualization）**：显示解码后的光标移动轨迹。

## 命令
- `decode`：运行模拟和解码循环。