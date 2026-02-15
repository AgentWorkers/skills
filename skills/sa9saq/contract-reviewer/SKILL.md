---
description: 检测风险条款，汇总相关术语，并对法律文件进行评级，以便进行合同审查。
---

# 合同审核员

负责分析合同和法律文件中的风险、异常条款以及关键义务。

## 指令

1. **接收输入**：文件路径、粘贴的文本或URL。支持的格式包括：纯文本、PDF、Markdown、HTML。
2. **分析并标记**以下类别中的风险条款：

   | 类别 | 需要关注的内容 |
   |----------|-----------------|
   | 责任条款 | 大写词汇、责任免除条款、赔偿条款 |
   | 终止条款 | 罚款条款、通知期限、自动续期条款 |
   | 知识产权转让条款 | 广泛的知识产权转让范围、雇佣合同条款 |
   | 数据/隐私条款 | 数据共享、数据保留、GDPR合规性 |
   | 竞业禁止条款 | 竞业禁止的范围、期限、地理限制 |
   | 争议解决条款 | 仲裁条款、陪审团放弃权、争议解决地点 |
   | 付款条款 | 迟延付款费用、付款方式、货币种类 |

3. **对每个条款进行评级**：🟢 标准风险；🟡 建议审核；🔴 高风险

4. **输出格式**：
   ```
   ## Summary
   One-paragraph plain-English overview of the contract.

   ## Risk Analysis
   | # | Clause | Section | Risk | Issue |
   |---|--------|---------|------|-------|
   | 1 | Auto-renewal | §4.2 | 🔴 | 2-year auto-renew with 90-day cancellation notice |
   | 2 | IP Assignment | §7.1 | 🟡 | Broad "all work product" language |

   ## Overall Risk: MEDIUM
   Key concerns: [list top 2-3]

   ## Recommended Actions
   - Negotiate §4.2 to 30-day notice
   - Narrow §7.1 to project-specific deliverables
   ```

5. **比较合同**：如果提供两个合同版本，需突出显示它们之间的差异。

## 安全性

- 严禁在当前会话结束后存储或传输合同内容。
- 如有要求，应在日志中屏蔽敏感方的名称。

## ⚠️ 免责声明

**本工具仅提供人工智能分析结果，不构成法律建议。** 重要合同请务必由专业律师进行审核。

## 要求

- 无需依赖任何外部库或API密钥。
- 对于PDF文件的解析，可使用`pdftotext`（来自`poppler-utils`工具）或直接读取文件内容。