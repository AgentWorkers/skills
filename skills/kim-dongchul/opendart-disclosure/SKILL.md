---
name: opendart-disclosure
description: 使用 OpenDART API 阅读韩国上市公司的公开披露文件（Korea OpenDART disclosures）。适用于用户需要查询 DART 公开披露信息、查看公司的最新文件、按文件类型/日期进行筛选，或获取带有来源链接的快速摘要的情况。该 API 支持通过公司名称或公司代码（corp_code）进行查找，并能够提取结构化的数据结果。
---
# OpenDART信息披露

从 OpenDART 获取并汇总韩国企业的信息披露资料。

## 需要收集的输入参数：

- 公司标识符：`corp_code`（推荐使用）或公司名称
- 时间范围：`bgn_de` / `end_de`（格式为 `YYYYMMDD`）
- 文件类型筛选条件（可选）：定期报告（`A`）、重大问题（`B`）、股票相关文件（`C`）等
- 输出要求：最新的 N 条记录、仅显示链接或简短摘要

## 工作流程：

1. 确定公司身份：
   - 如果用户提供了 `corp_code`，直接使用该代码。
   - 如果用户提供了公司名称，先运行 `search-corp` 脚本进行查询。
2. 使用 `recent` 参数获取最新的信息披露文件。
3. 按时间顺序排序，并保留用户指定的记录数量。
4. 返回以下信息：
   - 文件提交日期
   - 报告名称
   - 接收编号
   - OpenDART 链接（格式：`https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<rcept_no>`）
5. 如有要求，提供报告内容的简短韩文摘要。

## 命令使用方式：

请使用以下打包好的脚本：

```bash
python3 scripts/opendart.py search-corp --name "삼성전자"
python3 scripts/opendart.py recent --corp-code 00126380 --from 20260101 --to 20261231 --limit 10
python3 scripts/opendart.py recent-by-name --name "삼성전자" --from 20260101 --to 20261231 --limit 10

# Shortcuts (less typing)
python3 scripts/opendart.py recent-by-name --name "삼성전자" --days 7 --limit 10
python3 scripts/opendart.py recent-by-name --name "삼성전자" --today
```

## API 密钥选项：

- `--api-key <KEY>`  
- 或通过环境变量 `OPENDART_API_KEY` 设置 API 密钥

## 注意事项：

- OpenDART 以 JSON 格式返回状态码。非 `000` 的状态码表示 API 请求失败，请及时报告。
- 公司名称的匹配可能不够精确；如果有多个相似的公司名称，会显示排名靠前的结果。
- 最终答案中建议直接引用 DART 的文件链接。
- 有关端点详情和 `corp_code` 的使用规则，请参阅 `references/opendart-endpoints.md`。