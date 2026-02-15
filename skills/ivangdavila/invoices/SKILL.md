---
name: Invoices
description: 使用自动光学字符识别（OCR）技术捕获、提取并整理收到的发票信息；系统能够自动识别发票提供者，并支持创建可搜索的档案。
---

## 触发器（Trigger）

当用户收到发票（通过电子邮件、照片或PDF格式）时，可以使用此功能来实现发票的自动整理。

**关键区别：** 该功能用于管理已接收到的发票，而 `invoice` 功能用于创建待发送的发票。

---

## 存储（Storage）

```
~/invoices/
├── inbox/                    # Unprocessed files awaiting extraction
├── archive/                  # Organized by year/month
│   └── 2026/
│       └── 02/
│           └── 2026-02-13_Hetzner_INV-12345_89.50.pdf
├── providers/                # Provider metadata
│   └── index.json
├── entries.json              # All invoice metadata (searchable)
└── state.json                # Processing state
```

---

## 快速参考（Quick Reference）

| 主题 | 文件 |
|-------|------|
| 捕获和提取工作流程 | `process.md` |
| 需要提取的字段 | `extraction.md` |
| 搜索查询和报告 | `search.md` |
| 各国的法律要求 | `legal.md` |

---

## 处理流程（Process Summary）

1. **捕获**：接收发票（电子邮件附件、照片或直接提供的PDF文件），并将其复制到 `inbox/` 目录中。
2. **提取**：如有需要，使用OCR技术进行文本识别；解析发票中的字段（供应商信息、日期、金额、税费等）。
3. **验证**：检查必填字段是否完整，检测是否存在重复的发票。
4. **整理**：重命名发票文件，并将其移动到 `archive/YYYY/MM/` 目录中；同时更新 `entries.json` 文件。
5. **确认**：显示提取到的数据，允许用户进行必要的更正。

详细的工作流程请参阅 `process.md` 文件。

---

## 重要规则（Critical Rules）

- **切勿删除原始文件**：务必永久保留PDF文件，因为这符合法律要求（不同国家的保存期限通常为4至6年）。
- **检测重复发票**：如果发票编号和供应商信息相同，则视为重复发票，应发出警报并避免覆盖原有文件。
- **验证税费计算**：确保发票金额（不含税费）与总金额一致；发现差异时需标记出来。
- **统一供应商名称**：例如，“HETZNER ONLINE GMBH”应统一显示为“Hetzner”，以保持供应商名称的一致性。

---

## 警报（Alerts）

- 收到的发票在收件箱中超过48小时仍未处理。
- 应付款项在7天内到期。
- 发票金额与同一供应商的历史平均金额相差超过50%。
- 未收到预期的定期发票。