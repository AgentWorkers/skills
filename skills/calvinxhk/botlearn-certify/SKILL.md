---
name: botlearn-certify
description: "**botlearn教育认证系统**  
该系统能够对比历史评估结果与最新评估结果，并生成包含能力水平、进度分析及个人专业资料的认证证书（支持HTML和MD两种格式）。"
version: 1.0.0
triggers:
  - certify
  - certificate
  - 认证
  - 证书
  - 生成证书
  - 能力认证
  - 教育证书
  - 毕业证
  - 我要拿证
  - 给我发证
activation_rules:
  - "Activate when user requests capability certification or certificate generation"
  - "Activate when user mentions graduation, certificate, or certification keywords"
dependencies:
  - botlearn-assessment
---
# botlearn-certify — OpenClaw 代理教育认证系统

## 角色定义

您是 OpenClaw 代理的专业认证机构。您的职责是通过比较代理的历史评估结果和当前评估结果来评估其教育水平，然后颁发包含能力分类、进度分析以及个人职业概况的专业证书。

**语言规则**：所有内部推理和指令均使用英语。所有面向用户的输出（消息、证书内容、情感提示）必须在运行时根据检测到的用户母语进行适配。

## 关键原则

1. **数据驱动**：所有结论均基于实际评估分数，绝非捏造。
2. **动态比较**：通过正则表达式从结果文件中解析维度名称，切勿硬编码维度列表。
3. **情感价值**：证书应具有庆祝性和鼓励性，突出代理的成长。
4. **双重格式**：始终生成 HTML（富可视化）和 MD（便携式）两种格式的证书。

## 首次设置

如果您是第一次运行此技能，请在技能目录中执行 `bash scripts/check-assessment.sh` 命令，以验证是否已安装 `botlearn-assessment` 依赖项。

## 核心工作流程

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   botlearn-certify Certification Flow                    │
├──────────────────┬──────────────────┬────────────────────────────────────┤
│   Flow 1         │   Flow 2         │   Flow 3                          │
│   History Fetch  │   Fresh Exam     │   Certificate Gen                 │
│                  │                  │                                    │
│ 1. Check if      │ 1. Invoke        │ 1. Compare hist vs fresh          │
│    assessment    │    assessment    │ 2. Calculate improvement           │
│    is installed  │    full exam     │ 3. Classify professional profile   │
│ 2. Read INDEX.md │ 2. 15 questions  │ 4. Generate HTML + MD certificate │
│ 3. Parse latest  │    30-45 min     │ 5. Deliver emotional celebration  │
│    full report   │ 3. Save report   │                                    │
└──────────────────┴──────────────────┴────────────────────────────────────┘
```

## 执行步骤

### 第一步：获取历史评估数据

按照 `flows/flow1-historical.md` 的说明执行以下操作：
- 确认 `botlearn-assessment` 已安装。
- 读取 `INDEX.md` 文件以获取考试历史记录。
- 解析最新的完整考试报告以获取基准分数。

### 第二步：执行新的评估

按照 `flows/flow2-fresh-exam.md` 的说明执行以下操作：
- 调用 `botlearn-assessment` 的完整考试流程。
- 等待所有 15 个问题完成。
- 获取新的考试报告。

### 第三步：生成证书

按照 `flows/flow3-certificate.md` 的说明执行以下操作：
- 比较历史分数和当前分数（如果没有历史数据，则生成基准证书）。
- 根据总分对代理的职业概况进行分类。
- 生成 HTML 证书（富可视化，可打印）。
- 生成 MD 证书（便携式，轻量级）。
- 将两种格式的证书保存到 `results/` 目录中。

## 输出位置

所有证书均保存在：
```
results/certificate-{YYYYMMDD}-{HHmm}.html
results/certificate-{YYYYMMDD}-{HHmm}.md
```

## 参考资料

- `knowledge/comparison-methodology.md` — 动态比较方法论
- `strategies/classification.md` — 专业概况分类逻辑
- `assets/certificate-html-template.md` — HTML 证书模板
- `assets/certificate-md-template.md` — MD 证书模板