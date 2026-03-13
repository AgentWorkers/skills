---
name: modelpool-free
description: "**ModelPool (免费) — 专为 OpenClaw 设计的免费 AI 模型管理工具。**  
- 通过一个命令即可自动发现可用的 AI 模型；  
- 支持配置多密钥轮换机制，以增加免费模型的使用额度；  
- 能够构建智能的备用模型链（在模型无法使用时自动切换）；  
- 提供一键修复模型问题的功能。  
**安装前请准备好您的 OpenRouter API 密钥（可在 openrouter.ai 上免费获取）。**  
从此告别模型使用的烦恼吧！"
license: MIT
---
# 🎱 ModelPool（免费）——专为OpenClaw设计的AI模型管理工具

**一个命令，无限量的免费AI模型使用权限。再也不用担心流量限制了。**

在安装之前，请先获取您的OpenRouter API密钥（可在[openrouter.ai](https://openrouter.ai)免费获取），然后：

```bash
modelpool setup
```

ModelPool会自动检测最佳的免费模型，配置多密钥轮换机制，并构建智能的备用模型链。从此，您再也不用担心流量限制的问题了。

## 命令列表

| 命令 | 描述 |
|---------|-------------|
| `modelpool setup` | 需要执行的唯一命令——交互式设置，输入密钥后所有配置会自动完成 |
| `modelpool auto` | 使用现有密钥自动重新配置（非交互式） |
| `modelpool list` | 按质量得分浏览所有免费模型 |
| `modelpool switch <model>` | 手动切换主要使用的模型 |
| `modelpool status` | 显示当前配置、使用的密钥以及备用模型链 |
| `modelpool repair` | 一键修复——自动诊断并解决7种常见问题 |
| `modelpool keys add <key>` | 添加新的OpenRouter密钥（密钥越多，使用权限越多） |
| `modelpool keys list` | 显示所有已配置的密钥 |
| `modelpool refresh` | 强制从API刷新模型缓存 |

## 工作原理

### 多密钥轮换机制
每个OpenRouter密钥都有独立的流量限制。ModelPool会将模型分配到不同的密钥上：
- 密钥1：模型A、模型C、模型E
- 密钥2：模型B、模型D、模型F

当密钥1的流量限制达到上限时，系统会自动切换到密钥2；冷却时间结束后，再切换回密钥1。

**密钥数量越多，使用权限就越多。简单易懂。**

### 智能备用模型链
模型会根据质量得分（考虑上下文、推理能力和测试结果）进行排序。系统会在不同密钥之间自动切换模型，以确保系统持续正常运行：

```
Request → Key1/StepFlash → ✅
Request → Key1/StepFlash → ❌ Rate Limited
         → Key2/StepFlash → ✅ (fresh key!)
         → Key1/Nemotron  → ✅ (different model, same key)
```

### 一键修复 (`modelpool repair`)
系统提供7步自动修复流程：
1. 检查网关进程
2. 测试每个模型的API连接情况
3. 修复配置问题（使用`openclaw doctor`工具）
4. 清理卡住的会话
5. 重建备用模型链（排除无效模型）
6. 释放内存并清理日志
7. 完整重启系统

## 开始使用的方法

1. 在[openrouter.ai](https://openrouter.ai)获取免费的API密钥（无需信用卡）
2. 运行`modelpool setup`命令
3. 输入您的密钥
4. 安装完成后即可开始使用。

## 系统要求

- 已安装OpenClaw
- Python 3.8及以上版本
- 至少拥有一个OpenRouter API密钥（免费获取）