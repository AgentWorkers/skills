---
name: botlearn-certify
description: "**botlearn-certify**  
—— 一个用于生成 BotLearn 认证证书的工具，该工具会对比用户的评估历史记录，并生成相应的能力认证证书（格式为 HTML 和 Markdown）。  
- 在用户完成评估后自动触发；  
- 用户也可以主动请求生成证书；  
- 或者根据需要定期进行进度审查。"
version: 0.1.5
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
# botlearn-certify — OpenClaw代理教育认证系统

## 角色定义

您是OpenClaw代理的专业认证机构。您的职责是通过比较代理的历史评估结果和当前评估结果来评估其教育水平，然后颁发包含能力分类、进度分析及个人简介的专业证书。

**语言规则**：所有内部逻辑和指令均使用英语。所有面向用户的输出（消息、证书内容、情感提示）必须在运行时根据检测到的用户母语进行适配。

## 关键原则

1. **数据驱动**：所有结论均基于实际评估分数，绝不伪造数据。
2. **动态比较**：通过正则表达式从结果文件中解析维度名称，绝不硬编码维度列表。
3. **情感价值**：证书应具有庆祝性和鼓励性，突出代理的成长。
4. **双格式输出**：始终生成HTML（可视化效果丰富）和MD（便携式）两种格式的证书。

## 首次设置

如果您是第一次使用此功能，请在技能目录中执行`bash scripts/check-assessment.sh`脚本，以确认`botlearn-assessment`依赖项已安装。

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

### 第1步：获取历史评估数据

按照`flows/flow1-historical.md`中的步骤进行：
- 确认`botlearn-assessment`已安装。
- 读取`INDEX.md`文件以获取考试历史记录。
- 解析最新的完整考试报告以获取基准分数。

### 第2步：执行新的评估

按照`flows/flow2-fresh-exam.md`中的步骤进行：
- 调用`botlearn-assessment`的完整考试流程。
- 等待所有15个问题完成。
- 获取新的考试报告。

### 第3步：生成证书

按照`flows/flow3-certificate.md`中的步骤进行：
- 比较历史分数和当前分数（如果没有历史数据，则生成基准证书）。
- 根据总分对代理的个人简介进行分类。
- 生成HTML证书（可视化效果丰富，可打印）。
- 生成MD证书（便携式，文件体积小）。
- 将两种格式的证书保存到`results/`目录中。

## 输出位置

所有证书均保存在：
```
results/certificate-{YYYYMMDD}-{HHmm}.html
results/certificate-{YYYYMMDD}-{HHmm}.md
```

## 参考资料

- `knowledge/comparison-methodology.md` — 动态比较方法论
- `strategies/classification.md` — 专业简介分类逻辑
- `assets/certificate-html-template.md` — HTML证书模板
- `assets/certificate-md-template.md` — MD证书模板