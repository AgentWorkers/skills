# 法律文件生成工具（FR）

专为自由职业者/小型企业设计的法律文件生成工具。可生成标准销售合同（CGV）、法律声明、服务合同以及报价单（DEV）等文件，格式为HTML。

## 脚本

所有脚本均位于 `scripts/` 目录中，仅使用 Python 3 的标准库。相关文件存储在 `~/.freelance/legal/` 目录下。

### legal.py — 法律文件生成模块

```bash
# CGV — Conditions Générales de Vente
python3 legal.py generate cgv [--no-open]
python3 legal.py generate cgv --tribunal "Paris" --mediateur "CMAP, Paris"

# Mentions légales pour un site web
python3 legal.py generate mentions --hebergeur "Vercel Inc, San Francisco" [--site "monsite.fr"] [--dpo "dpo@email.com"]

# Contrat de prestation de services
python3 legal.py generate contrat --client "Acme Corp" --mission "Développement application web" \
  --montant 5000 --duree "3 mois" [--client-address "10 rue Example, Paris"] \
  [--client-siret "12345678900010"] [--date-debut "01/03/2026"] [--non-sollicitation]

# Devis
python3 legal.py generate devis --client "Acme Corp" --items "Dev frontend:10:400" "Design UX:3:500" \
  [--number DEV-2026-001] [--date 2026-02-15]

# Lister tous les documents générés
python3 legal.py list [--json]

# Voir la configuration prestataire
python3 legal.py config [--json]
```

所有生成的文件都支持 `--no-open` 参数，可设置为不在浏览器中打开文件。

### 服务提供商配置（适用于所有生成命令）

```bash
--nom "Hugo Dupont" --siret "12345" --adresse "42 rue X" --email "x@y.com" --phone "06..."
```
如果存在 `~/.freelance/config.json` 文件（由 freelance-toolkit 提供），则系统会自动填充相关配置信息。

## 生成的文件类型及内容

| 文件类型 | 文件名 | 文件内容 |
|------|---------|---------|
| 标准销售合同（CGV） | `cgv.html` | 包含10条主要条款：商品/服务描述、付款方式（30天内支付，逾期按法定利率计罚3倍，违约金40欧元）、交付期限、知识产权（PI）、责任划分、合同解除、不可抗力、管辖权、争议解决方式等 |
| 法律声明 | `mentions.html` | 包含提供者的身份信息、网站托管信息、出版负责人信息、GDPR（通用数据保护条例）相关条款（数据权利、使用目的、数据保护官信息）、Cookies政策、知识产权等相关内容 |
| 服务合同 | `contrat-{client}-{ts}.html` | 明确合同双方信息、服务内容、合同期限、费用分摊（30%由客户承担，70%由提供者承担）、保密条款、知识产权条款、合同解除方式、可选的免责声明等 |
| 报价单 | `DEV-YYYY-NNN.html` | 自动生成唯一编号，有效期30天，详细列明服务内容及付款条件，需签署“同意协议”方可生效 |

## 配置设置

请使用 `~/.freelance/config.json` 文件进行配置（该文件与 freelance-toolkit 共享）：
```json
{
  "provider": { "name": "...", "address": "...", "siret": "...", "email": "...", "phone": "..." },
  "micro_entreprise": true,
  "tva_rate": 0
}
```

如果配置中包含 `micro_entreprise: true`，则所有生成的文件都会包含《民法典》第293B条的相关条款。

## 数据来源

```
~/.freelance/legal/
├── cgv.html / cgv.json
├── mentions.html / mentions.json
├── contrat-acme-20260215-143022.html / .json
├── DEV-2026-001.html / .json
└── ...
```

## 法律条款内容

生成的文件包含法国的强制性法律条款：
- **付款条款**：规定付款期限为30天，逾期需支付法定利率3倍的违约金，违约金为40欧元（《商业法典》第D441-5条）
- **知识产权（PI）**：明确知识产权的转让条件（需在全额付款后生效）
- **争议解决**：自2016年起，强制要求采用调解方式解决争议（《消费者法典》第L611-1条）
- **GDPR**：详细说明个人数据保护的相关权利、数据使用目的、数据保留期限以及数据保护官的联系方式
- **不可抗力**：依据《民法典》第1218条的规定处理不可抗力事件

有关法律条款的详细信息，请参阅 `references/french-legal-ref.md` 文件。

## 其他说明：
- 文件采用内联CSS格式，适用于打印或导出为PDF格式
- 金额显示采用法国货币单位（2,900.00欧元）
- 提供者的姓名首字母会被用作文件中的Logo，样式与发票一致
- 通过 `--json` 参数可以在 `list` 和 `config` 文件中配置额外选项