**SKILL.md**  
**specter-cli**  
通过 `specter-cli`，您可以丰富、搜索和管理来自 Specter 智能平台的公司及人员数据。您可以按域名查找公司，通过 LinkedIn 丰富个人资料，管理列表，查询保存的搜索记录，以及追踪人才和投资者动态。  

## 安装  
克隆并安装该命令行工具（CLI）：  
```bash
git clone git@github.com:FroeMic/tryspecter-cli.git
cd tryspecter-cli
npm install
npm run build
npm link
```  

设置 `SPECTER_API_KEY` 环境变量（从 [Specter 设置 > API 控制台](https://app.tryspecter.com/settings/api-console) 获取）：  
- **推荐方式：** 将其添加到 `~/.claude/.env` 文件中（适用于 Claude Code）  
- **备用方式：** 将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：`export SPECTER_API_KEY="your-api-key"`  

仓库地址：`git@github.com:FroeMic/tryspecter-cli.git`  

## 命令  
### 公司信息丰富与查询：  
```
specter companies enrich --domain <domain>            # Enrich company by domain
specter companies enrich --linkedin <url>             # Enrich company by LinkedIn URL
specter companies enrich --website <url>              # Enrich company by website
specter companies get <companyId>                     # Get company details by Specter ID
specter companies similar <companyId>                 # Find similar companies
specter companies people <companyId>                  # Get team members
specter companies search <query>                      # Search companies by name or domain
```  

### 人员信息丰富与查询：  
```
specter people enrich --linkedin <url>                # Enrich person by LinkedIn identifier
specter people get <personId>                         # Get person details by Specter ID
specter people email <personId>                       # Get person's email address
specter people find-by-email <email>                  # Reverse lookup person by email
```  

### 列表管理：  
```
specter lists companies list                          # List all company lists
specter lists companies create <name>                 # Create a company list
specter lists companies get <listId>                  # Get list metadata
specter lists companies results <listId>              # Get companies in a list
specter lists companies add <listId>                  # Add companies to a list
specter lists companies remove <listId>               # Remove companies from a list
specter lists companies delete <listId>               # Delete a company list
specter lists people list                             # List all people lists
specter lists people create <name>                    # Create a people list
specter lists people results <listId>                 # Get people in a list
specter lists people delete <listId>                  # Delete a people list
```  

### 保存的搜索记录：  
```
specter searches list                                 # List all saved searches
specter searches delete <searchId>                    # Delete a saved search
specter searches companies get <searchId>             # Get company search details
specter searches companies results <searchId>         # Get company search results
specter searches people get <searchId>                # Get people search details
specter searches people results <searchId>            # Get people search results
specter searches talent get <searchId>                # Get talent search details
specter searches talent results <searchId>            # Get talent signal results
specter searches investor-interest get <searchId>     # Get investor interest details
specter searches investor-interest results <searchId> # Get investor interest results
```  

### 人才与投资者动态：  
```
specter talent get <signalId>                         # Get talent signal details
specter investor-interest get <signalId>              # Get investor interest signal
```  

### 实体提取：  
```
specter entities search --text "..."                  # Extract companies/investors from text
specter entities search --file <path>                 # Extract entities from a file (max 1000 chars)
```  

### 全局选项：  
```
--api-key <key>       # Override SPECTER_API_KEY
--format <format>     # Output format: json (default), table, csv
--help                # Show help
--version             # Show version
```  

## 关键概念  
| 概念                          | 功能                                      | 示例                                        |  
| --------------------------- | -------------------------------------- | ------------------------------------------- |  
| 公司                          | 公司情报记录                                  | 包含资金信息、团队成员等详细信息的公司资料           |  
| 个人                          | 个人资料                                    | 通过 LinkedIn 丰富后的个人数据                         |  
| 列表                          | 经过筛选的公司/人员集合                             | 如 “目标账户”、“招聘流程” 等分类                |  
| 保存的搜索记录                    | 在 Specter 平台上保存的搜索查询                         | 可用于查询公司或人员信息                         |  
| 人才动态                        | 人员跳槽的信号                                | 人员跳槽到新公司的信息                         |  
| 投资者关注                      | 投资者关注的信号                                | 受到投资者关注的公司                         |  
| 实体提取                        | 从文本中提取的实体名称                             | 文本中的公司/投资者名称                         |  

## API 参考  
- **基础 URL：** `https://app.tryspecter.com/api/v1`  
- **认证方式：** `X-API-KEY: $SPECTER_API_KEY`  
- **请求限制：** 每个 API 密钥每秒最多 15 次请求（采用指数级退避策略自动重试）  
- **信用额度：** 每个团队分配一定信用额度，每个成功结果消耗 1 个信用额度，每月重置  

### 常用 API 操作  
- **按域名丰富公司信息：**  
  ```bash
curl -X POST https://app.tryspecter.com/api/v1/companies/enrich \
  -H "X-API-KEY: $SPECTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```  

- **通过 LinkedIn 丰富个人资料：**  
  ```bash
curl -X POST https://app.tryspecter.com/api/v1/people/enrich \
  -H "X-API-KEY: $SPECTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"linkedin": "https://www.linkedin.com/in/johndoe"}'
```  

- **搜索公司：**  
  ```bash
curl -X GET "https://app.tryspecter.com/api/v1/companies/search?query=acme" \
  -H "X-API-KEY: $SPECTER_API_KEY"
```  

- **获取公司搜索结果：**  
  ```bash
curl -X GET "https://app.tryspecter.com/api/v1/searches/companies/<searchId>/results?page=0&limit=50" \
  -H "X-API-KEY: $SPECTER_API_KEY"
```  

## 注意事项：  
- 保存的搜索记录必须在 Specter 平台上启用 “通过 API 共享” 功能后，才能通过 API 访问。  
- 通过 API 创建的列表默认可共享；平台创建的列表需要手动开启 “通过 API 共享” 功能。  
- 无法通过 API 创建保存的搜索记录，只能查询和删除。  
- 公司 ID 采用 `comp_` 格式，个人 ID 采用 `per_` 格式。  
- 分页使用 `page` 和 `limit` 参数（最大 5000 条结果）。  
- CLI 会自动尝试最多 3 次请求（采用指数级退避策略）。  
- 在排查问题时，可将 `DEBUG_API_errors=true` 设置为开启详细错误日志记录。