# Denario 技能

该技能封装了 **Denario** 框架，用于自动化科学研究流程，自动处理环境配置和 Z.ai 的集成。

**引擎：** `scripts/wrapper.sh`
**工作目录：** `./` （技能根目录）

---

## 触发语句

| 语句 | 操作 |
|--------|--------|
| **"Denario idea"** | 生成研究思路（通过 Maker/Hater 循环）。 |
| **"Denario methods"** | 制定研究方法。 |
| **"Denario results"** | 生成研究结果并进行分析。 |
| **"Denario paper"** | 编写完整的研究论文。 |
| **"Denario citations"** | 管理引用信息。 |

---

## 使用指南

### 1. 生成研究思路
> **用户：** 输入 “Denario idea”
> **机器人：** 运行 `wrapper.sh` 脚本以执行 `test_denario.py`。首次运行时会自动安装依赖项。

### 2. 完整的研究流程
> **用户：** 先输入 “Denario methods”，再输入 “Denario results”，最后输入 “Denario paper”
> **机器人：** 依次执行各个研究阶段。

---

## 配置要求

**需要 API 密钥：**
您必须在 Clawdbot 的环境中设置您的 Z.ai/Zhipu API 密钥：
```bash
clawdbot config set env.OPENAI_API_KEY <your-key>
```

**环境配置：**
该技能会在 `~/.denario_skill_env` 自动创建并管理一个虚拟环境。