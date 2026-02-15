---
name: compliance-officer
description: >
  AI Compliance Officer that reviews marketing content, emails, landing pages, and privacy policies
  against 208 regulatory rules across 8 frameworks (FTC, HIPAA, GDPR, SEC 482, SEC Marketing, CCPA,
  COPPA, CAN-SPAM). Cites actual regulations with source URLs.
license: Apache-2.0
compatibility: Requires network access for URL fetching. Works with Claude Code and similar agents.
metadata:
  author: qcme
  version: "1.0.0"
  source: https://github.com/QCME-AI/agentic-compliance-rules
---

# 合规专员

负责审核营销内容是否符合FTC、HIPAA、GDPR、SEC、CCPA、COPPA和CAN-SPAM等法规中的208条具体规定。所有引用的法律条款均会附带相应的来源URL。

## 您可以执行的操作：

- **审核营销内容**：您可以粘贴文本、URL或图片进行审核。
- **检查电子邮件**：评估电子邮件的主题行、正文和底部信息，确保其符合CAN-SPAM等法规要求。
- **审计隐私政策**：检查隐私政策中是否包含了GDPR、CCPA、HIPAA、COPPA等法规要求的披露内容。
- **解释相关法规**：可以通过ID查询具体法规，并获取通俗易懂的说明。
- **起草披露声明**：为您的营销内容生成符合法规要求的披露声明。

## 示例：

- 审核一个登录页面：  
  ```
Review this for compliance: "Lose 30 lbs in 2 weeks — GUARANTEED.
Clinically proven. Doctor recommended. Only 3 left in stock!"
```

- 检查一封电子邮件：  
  ```
Check this email for CAN-SPAM compliance: Subject: "URGENT: Act now!"
From: deals@shop.com Body: "Click to claim your FREE gift..."
```

- 审计一份隐私政策：  
  ```
Review our privacy policy for GDPR and CCPA compliance: https://example.com/privacy
```

- 查询某条法规：  
  ```
Explain rule FTC-255-5-material-connection
```

- 起草披露声明：  
  ```
Draft disclosure language for this influencer post: "Love this protein powder!
Use code SARAH20 for 20% off"
```

## 支持的法规框架：

| 法规框架 | 规则数量 | 监管范围 |
|---------|---------|---------|
| FTC      | 95条    | 营销推广、声明内容、价格相关条款 |
| GDPR     | 25条    | 同意获取、数据披露、Cookie使用 |
| SEC Marketing | 18条    | 投资顾问营销相关规定 |
| HIPAA     | 17条    | 健康数据、患者信息（PHI）的披露要求 |
| SEC 482    | 15条    | 投资公司广告相关规定 |
| CAN-SPAM   | 14条    | 电子邮件营销、用户退订权、发件人身份标识 |
| CCPA     | 12条    | 加州隐私保护法规、用户退订权 |
| COPPA     | 12条    | 儿童隐私保护、家长同意要求 |

## 安装说明：

```
npx clawhub install compliance-officer
```

## 项目来源：

Apache-2.0 — [github.com/QCME-AI/agentic-compliance-rules](https://github.com/QCME-AI/agentic-compliance-rules)

---

*如需了解代理使用说明，请参阅 `references/instructions.md` 文件。*