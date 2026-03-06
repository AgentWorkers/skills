---
name: aws-price-csv
description: 根据用户提供的服务列表生成 AWS 成本 CSV 文件。当用户提供服务列表以及 AWS 区域，并需要通过 AWS 定价列表 API 或批量定价 JSON 文件获取每项服务的价格及总费用时，可以使用此功能。
---
# AWS 价格 CSV 脚本

## 概述  
该脚本可将用户提供的 AWS 服务列表（如实例、存储卷、S3 存储桶等）转换为 CSV 格式的价格数据。脚本可以通过 `aws-cli` 查询 AWS 价格列表 API，或使用已缓存的批量 JSON 文件。它支持按需（On-Demand）和预留（Reserved）两种计费方式，并能自动计算每项服务的费用及总费用。

## 快速入门  
1. 准备一个包含 `name`、`service_code`、`filters`、`term` 和 `usage` 字段的 YAML/JSON 文件（示例见 `references/api_reference.md`）。  
2. 选择数据来源：  
   - **API 模式**：需要 `aws pricing get-products` 权限，并且需要互联网连接。  
   - **批量模式**：无需 IAM 权限；脚本会下载并缓存公开的批量 JSON 文件。  
3. 使用指定的区域和选项运行脚本：  
   ```bash
   python3 scripts/generate_pricing_csv.py \
     --input inputs/sample.yml \
     --region ap-northeast-1 \
     --source bulk \
     --cache-dir ~/.cache/aws-price-csv \
     --output quotes/apac_quote.csv
   ```  
4. 检查生成的 CSV 文件（每行包含服务名称、服务代码、计费类型、数量、单价、总费用等信息），如有需要，可将文件与原始请求数据一起提供。  

## 工作流程  

### 1. 准备输入数据  
- 使用 `references/api_reference.md` 中提供的 YAML/JSON 模板。  
- `filters` 需要与 AWS 价格相关的属性（如 `instanceType`、`regionCode`、`volumeApiName`、`usagetype`、`termType` 等）相匹配。  
- `term.type` 可设置为 `OnDemand` 或 `Reserved`（预留计费类型）。  
- `term.attributes`（可选）用于过滤预留计费的相关信息（如 `LeaseContractLength`、`PurchaseOption`、`OfferingClass` 等）。  
- `usage.quantity` 表示需要计算的数量（单位：小时、GB-Mo、请求次数等）。  

### 2. 选择数据来源  
| 模式 | 适用场景 | 备注 |  
|------|-------------|-------|  
| API (`--source api`) | 已具备 IAM 权限且需要实时数据 | 使用 `aws pricing get-products` 在 `us-east-1` 区域查询 |  
| 批量模式 (`--source bulk`) | 无需 IAM 权限或希望缓存数据 | 脚本会检查 `--cache-dir`（默认为 `~/.cache/aws-price-csv`）；超过 30 天的缓存文件会被重新下载 |  

> 也可以通过 `--bulk-files ServiceCode=/path/to/file.json` 选项覆盖缓存文件的使用。  

### 3. 生成 CSV 文件  
- 脚本路径：`scripts/generate_pricing_csv.py`  
- 主要参数：  
  - `--input`：输入的 YAML/JSON 数据列表  
  - `--region`：AWS 区域代码（区域名称会自动添加到过滤条件中）  
  - `--output`：输出 CSV 文件的路径（默认为 `aws_pricing.csv`）  
  - `--source`：数据来源（默认为 API 或批量模式）  
  - `--cache-dir`：批量数据缓存目录（默认为 `~/.cache/aws-price-csv`）  
  - `--force-refresh`：忽略缓存文件并重新下载数据  
  - `--bulk-files`：使用指定的 JSON 文件覆盖缓存数据（例如：`ServiceCode=/path/to/file.json`）  
- 输出列包括：`item_name`、`service_code`、`term_type`、`region`、`quantity`、`usage_unit`、`price_unit_usd`、`cost_usd`、`description`，以及一个表示总费用的 `TOTAL` 行。  

### 4. 验证与交付结果  
- 检查 CSV 文件，确保每项服务都有相应的价格和描述信息。  
- 确认 `TOTAL` 列的值符合预期。  
- 如有需要，可附上原始数据列表或相关文档。  

## 故障排除  
| 问题 | 解决方案 |  
|-------|-----|  
| `aws pricing` 返回空结果 | 重新检查过滤条件（区域、区域代码、计费类型等），或切换到批量模式 |  
| 无法使用 `aws-cli` | 安装 `aws-cli` v2，配置凭据，或改用批量模式 |  
| 需要刷新缓存数据 | 使用 `--force-refresh` 选项，或删除缓存文件以重新下载数据 |  
- 无法解析 YAML 文件 | 安装 `pyyaml`，或将输入数据转换为 JSON 格式 |  
- 预留计费信息缺失 | 在 `term.attributes` 中添加 `LeaseContractLength`、`PurchaseOption`、`OfferingClass` 等字段 |  

## 资源  
- `scripts/generate_pricing_csv.py`：主脚本，支持 API 和批量数据源，包含缓存逻辑以及按需/预留计费类型的处理。  
- `references/api_reference.md`：包含价格列表 API 的使用示例、批量数据下载方法、区域/地点信息，以及输入数据模板（包括 gp3 和预留计费类型的示例）。