# 发票生成器

根据简单的输入，生成专业的Markdown或HTML格式发票。

## 使用方法

```bash
./generate-invoice.sh \
  --client "Acme Corp" \
  --email "billing@acme.com" \
  --date "2026-02-22" \
  --due "2026-03-22" \
  --item "Web Development|40|150.00" \
  --item "Design Review|5|120.00" \
  --tax 10 \
  --currency USD \
  --invoice-number INV-001 \
  --from "Shelly Labs" \
  --format html
```

### 参数

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--client` | 客户名称（必填） | — |
| `--email` | 客户邮箱 | — |
| `--date` | 发票日期 | 当前日期 |
| `--due` | 应付日期 | 30天后 |
| `--item` | `"描述\|数量\|单价"`（可重复输入） | — |
| `--tax` | 税率 | 0 |
| `--currency` | 货币代码 | USD |
| `--invoice-number` | 发票编号 | INV-{timestamp} |
| `--from` | 您的姓名/公司名称 | — |
| `--format` | `md` 或 `html` | `md` |
| `--output` | 输出文件路径 | stdout |

### 输出格式

- **Markdown**: 简洁的表格格式发票
- **HTML**: 使用 `template.html` 格式生成——适合打印

### 示例

```bash
# Quick markdown invoice
./generate-invoice.sh --client "Bob" --item "Consulting|10|100" --format md

# HTML invoice saved to file
./generate-invoice.sh --client "Acme" --item "Dev|40|150" --format html --output invoice.html
```