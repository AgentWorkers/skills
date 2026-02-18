---
name: fsd-secure
description: 具备最高安全标准的完全自动驾驶代理（仅使用摄像头，具备冗余检查功能）。
author: tempguest
version: 0.1.0
license: MIT
---
# FSD Secure Skill

该技能实现了一种**仅依赖摄像头的完全自动驾驶**代理，旨在确保最高的安全性。该代理在模拟环境中运行，并使用**双通道分析**（Dual-Pass Analysis）来验证路径是否安全。

## 安全特性
- **双通道验证**（Dual-Pass Verification）：必须有两个独立的算法都确认路径安全，才能继续行驶。
- **时间一致性**（Temporal Consistency）：在加速之前，需要连续3帧图像都显示为安全状态。
- **故障安全机制**（Fail-Safe）：一旦检测到任何不确定性，系统会立即触发紧急制动。

## 命令
- `drive`：启动自动驾驶模拟。