---
name: korean-invoice
description: 韩国式报价单/税务发票的自动生成功能（自动计算企业注册号码和增值税）
version: 1.0.0
author: 무펭이 🐧
---
# korean-invoice

**韩国式报价单/增值税发票生成器** — 依据韩国标准格式自动生成报价单和增值税发票。支持自动计算企业注册号码、供应价格和增值税。

## 何时使用？

- 向客户发送报价单
- 发行增值税发票
- 管理交易方信息
- 管理常用商品数据库
- 以 PDF/HTML 格式输出

## 快速入门

```bash
# 견적서 생성 (대화형)
korean-invoice quote

# 거래처 저장된 경우
korean-invoice quote --client "무펭이즘"

# 세금계산서 생성
korean-invoice tax --client "무펭이즘"

# 거래처 추가
korean-invoice client add "무펭이즘" --business-number "123-45-67890" --ceo "김형님"

# 품목 추가
korean-invoice item add "포토부스 대여" --price 500000 --unit "일"

# 거래처 목록
korean-invoice client list

# 품목 목록
korean-invoice item list
```

## 报价单字段

| 字段 | 说明 | 是否必填 |
|------|------|------|
| client | 交易方名称（存储的交易方 ID） | ✅ |
| items | 商品列表（商品名称、数量、单价） | ✅ |
| issueDate | 创建日期（默认：今天） | ❌ |
| validUntil | 有效期（默认：+30天） | ❌ |
| notes | 备注 | ❌ |
| includeVAT | 是否包含增值税（默认：true） | ❌ |

## 增值税发票字段

| 字段 | 说明 | 是否必填 |
|------|------|------|
| client | 收货方（交易方 ID） | ✅ |
| items | 商品列表 | ✅ |
| issueDate | 创建日期 | ✅ |
| type | 收据/发票（默认：收据） | ❌ |
| notes | 备注 | ❌ |

## 自动计算

```
공급가액:     500,000 원
부가세(10%):   50,000 원
합계:         550,000 원
```

- 输入供应价格时自动计算 10% 的增值税
- 输入总价时进行反向计算（总价 ÷ 1.1）
- 自动汇总各商品的小计

## 交易方管理

```bash
# 거래처 추가
korean-invoice client add "무펭이즘" \
  --business-number "123-45-67890" \
  --ceo "김형님" \
  --address "서울시 강남구..." \
  --phone "010-1234-5678" \
  --email "contact@mufism.com"

# 거래처 수정
korean-invoice client edit "무펭이즘" --phone "010-9999-9999"

# 거래처 삭제
korean-invoice client remove "무펭이즘"

# 거래처 상세 조회
korean-invoice client view "무펭이즘"
```

交易方数据存储在 `data/clients.json` 文件中。

## 商品管理

```bash
# 품목 추가
korean-invoice item add "포토부스 대여" --price 500000 --unit "일"

# 품목 수정
korean-invoice item edit "포토부스 대여" --price 600000

# 품목 삭제
korean-invoice item remove "포토부스 대여"

# 품목 목록
korean-invoice item list
```

商品数据存储在 `data/items.json` 文件中。

## 模板

### 报价单模板
- 供应商信息（企业注册号码、公司名称、负责人、地址、联系方式）
- 收货方信息
- 创建日期、有效期
- 商品表格（商品名称、规格、数量、单价、供应价格）
- 总计（供应价格、增值税、总价）
- 备注

### 增值税发票模板
- 批准编号（自动生成）
- 供应商/收货方信息（企业注册号码、公司名称、姓名、地址）
- 创建日期
- 商品表格
- 总计（供应价格、增值税）
- 收据/发票类型区分

## 输出格式

- **HTML**：直接在浏览器中查看
- **PDF**：使用 puppeteer 将 HTML 转换为 PDF
- 存储路径：`output/YYYY-MM-DD-{type}-{client}.pdf`

## 设置个人信息

我的企业信息存储在 `data/my-info.json` 文件中：

```json
{
  "businessNumber": "123-45-67890",
  "companyName": "무펭이즘",
  "ceo": "김무펭",
  "address": "서울시 강남구...",
  "phone": "010-1234-5678",
  "email": "contact@mufism.com",
  "bankAccount": "우리은행 1002-123-456789"
}
```

## 使用示例

### 1. 生成简单的报价单
```bash
korean-invoice quote \
  --client "무펭이즘" \
  --items "포토부스 대여,2,500000" \
  --notes "부가세 별도"
```

### 2. 使用已保存的商品信息
```bash
# 품목 미리 저장
korean-invoice item add "포토부스 대여" --price 500000 --unit "일"
korean-invoice item add "출장비" --price 100000 --unit "회"

# 품목 ID로 견적서 생성
korean-invoice quote --client "무펭이즘" --item-ids "포토부스 대여,출장비"
```

### 3. 发行增值税发票
```bash
korean-invoice tax --client "무펭이즘" --items "포토부스 대여,1,500000" --type 영수
```

## 集成

- 与 `message` 技能集成，通过电子邮件/Discord 发送
- 通过 `daily-report` 技能将工作时间转换为报价单
- 使用 `calendar` 技能设置有效期提醒

## 注意事项

- 企业注册号码必须输入为 `123-45-67890` 的格式
- 金额必须以元为单位输入（仅输入数字，无逗号）
- 生成 PDF 时需要运行 OpenClaw 浏览器