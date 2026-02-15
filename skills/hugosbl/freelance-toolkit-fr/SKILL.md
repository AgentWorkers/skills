# 自由职业者工具包

专为法国的自由职业者/独立工作者设计的工具集：包括发票生成、时间跟踪、客户管理以及仪表盘功能。

## 脚本

所有脚本均位于 `scripts/` 目录中，仅使用 Python 3 的标准库。数据存储在 `~/.freelance/` 目录下。

### config.py — 服务提供商配置
```bash
python3 config.py set --name "Hugo Dupont" --address "42 rue de la Paix, 75002 Paris" \
  --siret "98765432100010" --email "hugo@example.com" --phone "0600000000" \
  --iban "FR76 1234 5678 9012 3456 7890 123" --rate 80 --micro
python3 config.py show [--json]
```
数据存储路径：`~/.freelance/config.json`

### clients.py — 客户管理
```bash
python3 clients.py add --name "Acme" --email "contact@acme.fr" --phone "0612345678" \
  --address "10 rue Example, 75001 Paris" --siret "12345678900010" --rate 80 --notes "Client fidèle"
python3 clients.py list [--json]
python3 clients.py show "Acme" [--json]
python3 clients.py edit "Acme" --rate 90 --notes "Nouveau taux"
python3 clients.py remove "Acme"
```
数据存储路径：`~/.freelance/clients.json`

### timetrack.py — 时间跟踪
```bash
python3 timetrack.py start "Site web Acme" [--client "Acme"]
python3 timetrack.py stop
python3 timetrack.py status [--json]
python3 timetrack.py log [--from 2026-01-01] [--to 2026-01-31] [--project "Site web"] [--json]
python3 timetrack.py report [--month 2026-01] [--json]
```
数据存储路径：`~/.freelance/timetrack.json`

### invoice.py — HTML发票生成
```bash
python3 invoice.py generate --client "Acme" --items "Dev site web:5:400" "Design logo:1:200" \
  [--number 2026-001] [--date 2026-02-15] [--due-days 30] [--no-open]
python3 invoice.py list [--json]
python3 invoice.py show 2026-001
python3 invoice.py paid 2026-001
```
- 生成专业的 HTML 格式发票，保存在 `~/.freelance/invoices/` 目录下
- 如果未指定 `--number` 参数，发票会自动编号（格式为 YYYY-NNN）
- 默认情况下会在浏览器中打开发票（除非指定了 `--no-open`）
- 如果系统找到客户信息，会自动从 `clients.json` 中填充客户详情
- 包含法国的法律声明（默认适用于微型企业）
- `paid` 标志表示发票已支付（会在仪表盘中显示）
- 金额显示为法语格式（例如：2 900,00 €）
- 服务提供商的缩写会作为发票上的Logo显示

### dashboard.py — 收入仪表盘
```bash
python3 dashboard.py summary [--year 2026] [--json]
python3 dashboard.py monthly [--year 2026] [--json]
```
- 综合显示所有发票和时间跟踪数据
- 按月份和客户统计总收入
- 显示工作小时数、工作日数（每周工作7小时）、实际小时费率
- 区分已支付和未支付的发票
- 仅针对有收入的月份计算实际费率

## 配置

可选配置文件 `~/.freelance/config.json`：
```json
{
  "provider": {
    "name": "Hugo Dupont",
    "address": "42 rue de la Paix, 75002 Paris",
    "siret": "98765432100010",
    "email": "hugo@example.com",
    "phone": "0600000000"
  },
  "default_rate": 80,
  "tva_rate": 0,
  "micro_entreprise": true,
  "payment_delay_days": 30,
  "payment_method": "Virement bancaire",
  "iban": "FR76 1234 5678 9012 3456 7890 123"
}
```

- 如果设置 `micro_entreprise: true`，则增值税（TVA）为0%（依据法国税法第293B条）
- 如果 `tva_rate` 大于0，则会在每张发票上计算增值税

## 数据存储

所有数据均存储在 `~/.freelance/` 目录下：
```
~/.freelance/
├── config.json          — Configuration prestataire
├── clients.json         — Base clients
├── timetrack.json       — Entrées de temps
└── invoices/
    ├── 2026-001.html    — Factures HTML
    ├── 2026-001.json    — Métadonnées facture
    └── ...
```

## 注意事项：
- 所有金额均以欧元（€）显示，输出格式为法语
- 所有命令均支持 `--json` 选项，便于机器自动化处理
- HTML发票格式适合通过浏览器打印或导出为 PDF
- 详细的法律要求请参阅 `references/french-law.md` 文件