---
name: alicloud-compute-fc-serverless-devs
description: **Alibaba Cloud Function Compute (FC 3.0) 技能**：用于指导用户如何使用 Serverless Devs 来创建、部署、调用以及删除 Python 函数。适用于需要基于命令行界面（CLI）的 FC 快速入门指南或 Serverless Devs 设置帮助的用户。
version: 1.0.0
---
**类别：工具**  
# Function Compute (FC 3.0) 无服务器开发（Serverless Devs）  

## 目标  
- 安装并验证 Serverless Devs 工具。  
- 配置凭据，初始化示例项目，进行部署、调用以及删除操作。  
- 提供包含 Python 运行时示例的命令行界面（CLI）流程。  

## 快速入门流程  
1. 安装 Node.js（14 及以上版本）和 npm。  
2. 安装并验证 Serverless Devs。  
3. 通过引导式设置配置凭据。  
4. 初始化示例项目并进入项目目录。  
5. 进行部署、调用操作（如需要，也可执行删除操作）。  

## 安装 Serverless Devs（使用 npm）  
**全局安装（需要 sudo 权限）：**  
```bash
sudo npm install @serverless-devs/s -g
sudo s -v
```  

**无需 sudo 权限的替代方案（推荐在受限环境中使用）：**  
```bash
npx -y @serverless-devs/s -v
```  

## 配置凭据（引导式设置）  
选择 “Alibaba Cloud (alibaba)”，输入 `AccountID`、`AccessKeyID`、`AccessKeySecret`，并设置别名。  

## 配置凭据（通过命令行）  
使用命令行参数一次性配置凭据别名（非交互式操作）：  
```bash
s config add -a default --AccessKeyID <AK> --AccessKeySecret <SK> -f
```  

**如果使用环境变量，请将其添加到命令中（示例）：**  
```bash
s config add -a default -kl AccessKeyID,AccessKeySecret -il ${ALIBABA_CLOUD_ACCESS_KEY_ID},${ALIBABA_CLOUD_ACCESS_KEY_SECRET} -f
```  

**或者使用 Serverless Devs 规定的 JSON 格式配置环境变量（示例）：**  
```bash
export default_serverless_devs_key='{\"AccountID\":\"<AccountID>\",\"AccessKeyID\":\"<AK>\",\"AccessKeySecret\":\"<SK>\"}'
```  

**在 `s.yaml` 文件中的配置参考：**  
```yaml
access: default_serverless_devs_key
```  

## 初始化示例项目（使用 Python）  
初始化操作会创建 `s.yaml`、`code/` 和 `readme.md` 文件；请编辑 `code/index.py` 文件以编写函数逻辑。  

## 部署、调用及删除操作  
```bash
sudo s deploy
sudo s invoke -e "test"
sudo s remove
```  

## 自定义域名绑定（避免使用默认域名导致文件自动下载）  
> 注意：FC 默认域名会设置 `Content-Disposition: attachment`，导致浏览器自动下载文件。  
> 请使用自定义域名以避免此问题。  

### 第一步：为你的域名配置 CNAME 记录  
配置 DNS 的 CNAME 记录以指向 FC 的公共域名：  
```
<account_id>.<region_id>.fc.aliyuncs.com
```  

**示例（杭州地区）：**  
```
1629965279769872.cn-hangzhou.fc.aliyuncs.com
```  

**注意：** 如果使用 apex 域名（例如 `animus.run`），且 DNS 服务提供商不支持在 apex 下配置 CNAME 记录，  
请使用 ALIAS/ANAME 记录，或切换到子域名（如 `www.animus.run`）。  

### 第二步：在 Serverless Devs 中创建自定义域名  
**选项 A：** 在 `s.yaml` 文件中添加 `fc3-domain` 资源：  
```yaml
resources:
  newsDomain:
    component: fc3-domain
    props:
      region: cn-hangzhou
      domainName: animus.run
      protocol: HTTP
      routeConfig:
        routes:
          - functionName: honnold-taipei101-news
            qualifier: LATEST
            methods:
              - GET
              - HEAD
            path: /*
```  
`region` 为示例默认值；如果不确定最佳区域，请询问用户。  
之后执行部署操作：  
```bash
printf 'y\n' | npx -y @serverless-devs/s deploy
```  

**选项 B：** 通过控制台（高级功能 > 自定义域名）创建并配置自定义域名。  

### 常见错误  
- `DomainNameNotResolved`：域名未解析为正确的 FC CNAME 记录。  
- `InvalidICPLicense`：中国大陆地区需要完成与 Alibaba Cloud 相关的 ICP 注册流程。  

## 参考资料  
- 详细官方步骤请参阅 `references/install_serverless_devs_and_docker.md`。  
- HTTP 触发器的限制及响应头行为（默认域名会设置 `Content-Disposition: attachment`）：  
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/http-triggers-overview  
- 自定义域名绑定及 CNAME 配置指南：  
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names  
- 官方资源列表：`references/sources.md`  

## 验证  
通过以下条件判断配置是否成功：  
- 命令执行成功（返回状态码 0），并且生成 `output/alicloud-compute-fc-serverless-devs/validate.txt` 文件。  

## 输出结果与证据  
- 将所有生成的结果文件、命令输出以及 API 响应内容保存到 `output/alicloud-compute-fc-serverless-devs/` 目录下。  
- 确保证据文件中包含关键参数（如区域、资源 ID、时间范围等），以便后续复现操作。  

## 先决条件  
- 在执行操作前，请配置最低权限的 Alibaba Cloud 凭据。  
- 建议使用环境变量：`ALICLOUD_ACCESS_KEY_ID`、`ALICLOUD_ACCESS_KEY_SECRET`（可选）以及 `ALICLOUD_REGION_ID`。  
- 如果不确定使用哪个区域，请在执行修改操作前询问用户。  

## 工作流程  
1. 确认用户的操作意图、所选区域、相关标识信息，以及操作类型（只读或修改）。  
2. 先执行一个最小的只读查询以验证连接性和权限。  
3. 使用明确的参数和受限范围执行目标操作。  
4. 验证操作结果，并保存输出文件及证据文件。