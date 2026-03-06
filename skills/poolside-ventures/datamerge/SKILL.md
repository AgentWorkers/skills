---
name: datamerge
description: 使用 DataMerge MCP 服务器（mcp.datamerge.ai）来丰富企业信息并寻找 B2B 联系人。当用户需要公司的基本信息、经过验证的联系人邮箱或电话号码、类似公司的搜索结果、企业层级结构数据，或者想要管理目标账户列表时，可以使用该服务。该服务可访问全球超过 3.75 亿家公司的信息。使用该服务需要一个 DataMerge API 密钥（可在 app.datamerge.ai 获取免费试用额度）。
---
# DataMerge

请连接到 DataMerge MCP 服务器，地址为 `https://mcp.datamerge.ai`。

## 认证
在使用任何其他工具之前，需要使用用户的 API 密钥调用 `configure_datamerge` 函数进行身份验证。新用户可以在 [https://app.datamerge.ai](https://app.datamerge.ai) 获取 20 个免费信用额度。

## 信用额度
- 1 个信用额度：用于公司信息补充（包括验证过的电子邮件地址）
- 4 个信用额度：用于获取手机号码
- `record_id` 的检索（`get_company`、`get_contact`）：免费——建议始终使用此方法来重新获取相关数据

## 核心工作流程

### 补充公司信息
- 对单个域名，使用 `start_company_enrichment_and_wait` 函数；该函数会自动进行数据采集并在完成后返回结果。
- 对批量任务，可以使用 `start_company_enrichment` 结合 `get_company_enrichment_result` 函数。

### 查找联系人
1. 使用 `contact_search` 函数，指定目标域名，并设置 `enrich_fields` 为 `["contact.emails"]`。
2. 不断调用 `get_contact_search_status` 函数，直到任务完成。
3. 使用 `get_contact` 函数，根据每个 `record_id` 获取联系人详细信息（免费）。

- 可以通过 `job_titles` 参数按职位等级筛选联系人。建议先仅使用电子邮件地址进行筛选；如果确实需要手机号码，再添加 `contact.phones` 参数（费用为普通费用的 4 倍）。

### 查找相似公司
1. 使用 `start_lookalike` 函数，并设置 `companiesFilters.lookalikeDomains` 参数（指定种子域名）。
2. 不断调用 `get_lookalike_status` 函数，直到任务完成。
3. 使用 `get_company` 函数，根据每个 `record_id` 获取相似公司的详细信息（免费）。

### 公司层级结构
- 首先补充公司信息以获取 `datamerge_id`，然后调用 `get_company_hierarchy` 函数。设置 `include_names: true` 参数可获取公司名称（费用为 1 个信用额度）。

### 列表操作
- 使用 `create_list` 函数保存一组公司或联系人信息。
- 将 `list` 参数传递给数据补充/搜索任务，以便自动添加结果。
- 使用 `get_list_items` 函数检索已保存的记录。
- 设置 `skip_if_exists: true` 参数可避免重复数据被再次补充。

## 提示
- 在执行大规模批量任务之前，请先检查 `get_credits_balance` 函数以确认剩余信用额度。
- 设置 `global_ultimate: true` 可以获取公司的顶级母公司而非子公司信息。
- 设置 `strict_match: true` 可确保域名完全匹配；当精确度高于数据覆盖范围时，请使用此选项。