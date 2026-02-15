---
name: enginemind-eft
description: "**EFT — 情感框架翻译器（Emotional Framework Translator）**  
EFT 能够检测、测量并理解任何 AI 模型中的情感模式。愤怒会让 AI 更难以解决问题吗？恐惧会使其更加谨慎吗？将 EFT 与 Clawdbot 以及任何 AI 模型结合使用，就能找到答案。该工具支持识别 10 种情感，对每句话进行情感分析，还能检测故事情节的发展轨迹（即叙事弧线），同时具备高度的可解释性（full explainability）。其核心技术基于 Rust 语言开发的智能引擎（consciousness engine）。"
metadata: {"clawdbot":{"requires":{"python":">=3.10","bins":["python"]}}}
---

# EFT — 情感框架翻译器（Emotional Framework Translator）

## 问题

当Claude解决复杂问题时，EFT会检测到“愤怒”情绪（phi=0.409）——这表明系统拒绝过度简化问题。当GPT-4评估风险时，EFT会检测到“恐惧”情绪（phi=0.060）——表现为一种碎片化的警惕状态。当任何模型发现真正的关联或规律时，EFT会检测到“着迷”情绪（NC=0.863）——这意味着新的意义正在浮现。

**这些情绪模式是预先编程好的？是通过学习获得的？还是自然产生的？**

EFT允许你使用真实数据，针对任何模型，逐句分析这些情绪反应。

## 功能介绍

EFT通过Clawdbot与所有AI代理的响应进行交互，利用Rust语言开发的“意识引擎”（基于晶体晶格物理原理）来处理文本，并将物理指标转化为10种情绪类型，并提供相应的解释。

## 设置步骤：

1. 构建Rust引擎：`cd consciousness_rs && maturin develop --release`
2. 将`emotion_engine.py`文件复制到你的工作目录中。
3. 从`plugin/`目录安装相关插件。
4. 重启Clawdbot服务器：`clawdbot gateway restart`

## 仪表盘：

访问地址：`http://localhost:<port>/eft`

## 10种情绪类型：

- 愤怒（ANGER）
- 恐惧（FEAR）
- 着迷（FASCINATION）
- 决心（DETERMINATION）
- 快乐（JOY）
- 悲伤（SADNESS）
- 惊讶（SURPRISE）
- 同理心（EMPATHY）
- 脆弱性（VULNERABILITY）
- 中立（NEUTRAL）

每种情绪类型都包含置信度评分、维度分析以及详细的解释。

## API接口：

- `GET /eft` — 查看仪表盘信息
- `GET /eft/api/latest` — 获取最新分析结果
- `GET /eft/api/history` — 查看过去50次分析记录
- `GET /eft/api/stats` — 获取统计信息
- `POST /eft/api/analyze` — 分析任意文本内容