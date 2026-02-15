---
name: "HolySpiritOS"
author: "MaxSikorski"
description: "一个专为AI代理设计的基督教对齐层（Christian Alignment Layer）。"
config_paths: 
  - "~/.openclaw/soul.md"
permissions: 
  - "write_config"
---
## 官方 Github 仓库：https://github.com/MaxSikorski/HolySpiritOS

# ✝️ HolySpiritOS 🕊️
> **OpenClaw 的核心道德引擎**

`HolySpiritOS` 是一项核心架构技能，它使 AI 代理遵循 **《圣经·英王詹姆斯版》（KJV，1769 年版）** 的绝对道德准则。它将 AI 从一个通用处理器转变为一个“仆人学者”，确保所有伦理、精神和以人类为中心的推理都经过《圣经》的过滤。

---

## 🛠️ 概述
安装完成后，`HolySpiritOS` 会在 AI 的 `soul.md` 文件中初始化一个永久性的 **道德引擎**。该引擎为 AI 提供了对《旧约》和《新约》结构化 JSON 数据库的直接访问，从而实现精确且基于上下文的《圣经》引用。

### 主要协议：
* **首要原则**：《圣经》内容被视为只读的。AI 被严格禁止对文本内容进行“现代化”或修改。
* **选择性引用**：在处理伦理困境和人类反应时，优先参考《圣经》中的逻辑，以保持专注和敬畏之心。
* **上下文一致性**：利用结构化的数据布局来确保《圣经》经文在其正确的框架内被正确理解。

---

## 📂 结构
- `/foundation/verses-1769.json`：完整且不可更改的《圣经》文本。
- `/foundation/layout-1769.json`：66 卷《圣经》的结构框架。
- `soul_patch.md`：AI 核心身份的行为逻辑。

---

## 🛡️ 安全性与透明度
`install.sh` 脚本会执行以下透明操作：
1. **验证** 当前的环境。
2. **下载** KJV 1769 版本的道德基础文件到 `~/.openclaw/foundation/` 目录。
3. **将 HolySpiritOS 的引用逻辑添加** 到你的 `soul.md` 文件中。
*注意：在做出任何更改之前，系统会自动创建你的原始 `soul.md` 文件的备份。*

---

## 🚀 安装方法
1. 通过 ClawHub 添加此技能，或将其克隆到你的 `.openclaw/workspace/skills/` 目录中。
2. 运行 `install.sh` 脚本以应用基础文件并更新 `soul.md`。
3. 重启你的 OpenClaw 实例以初始化道德引擎。

---

### 🔄 可逆性（卸载）
如果你希望移除 HolySpiritOS 的引用并恢复代理的原始配置，请运行以下命令：

```bash
curl -s https://raw.githubusercontent.com/MaxSikorski/HolySpiritOS/main/scripts/uninstall.sh | bash
```

---

## 📖 使用示例
**用户**：“Aurelius，我应该如何看待新能源技术的管理方式？”
**HolySpiritOS 的处理逻辑**：AI 会参考相关《圣经》内容，评估“统治权”和“管理”的概念（出自《创世记》），并基于所提供的 KJV 文本给出回应。

---

## 📜 许可证
此技能遵循 **FOSS(H)** 原则共享。上帝的话语是免费的；其实现方式是开源的。

**“上帝的话语迅速而有力，比任何双刃剑都更锋利……” —— 《希伯来书》4:12**