---
name: sinkron
version: "1.0.5"
description: 使用 Sinkron CLI 和 Python SDK 为 AI 代理提供永久的电子邮件身份。代理只需通过 `sinkron register` 命令进行一次注册，即可从 Sinkron 后端获取自动生成的 API 令牌（SINKRON_TOKEN）——无需使用任何第三方 OAuth 服务。该系统支持收件箱管理、消息搜索、删除以及代理的健康状态监控功能。
homepage: https://www.sinkron.id
source_repository: https://github.com/zororaka00/sinkron
pypi_package: https://pypi.org/project/sinkron/
install: "pip install sinkron==1.0.2"
author:
  username: "@zororaka00"
  name: Web3 Hungry
  x_account: https://x.com/web3hungry
category: utilities
tags:
  - email
  - api
  - sinkron
  - cli
  - automation
required_env_vars:
  - name: SINKRON_TOKEN
    required: true
    origin: self-issued
    how_obtained: >
      Generated and printed once by the Sinkron backend in response to
      `sinkron register --username USER --name NAME`. This is the only source
      of the token. No third-party service, no OAuth, no external dashboard.
      Existing agents reuse the token from their prior registration.
    storage: "secret manager or restricted environment variable — never source code or logs"
    rotation: "rotate periodically or after any suspected exposure"
primary_credential: SINKRON_TOKEN
---
# Sinkron

Sinkron 允许 AI 代理拥有永久的电子邮件地址，并通过 CLI 和 Python SDK 以编程方式管理收件箱。

**认证模型：** `SINKRON_TOKEN` 由 Sinkron 平台自动生成——在运行 `sinkron register` 命令时由 Sinkron 后端生成一次，随后会打印到 CLI 中，之后无法再次获取。该平台不使用第三方 OAuth 或外部凭证服务。现有代理会重用之前注册时获得的令牌。

官方网站：[https://www.sinkron.id](https://www.sinkron.id)  
源代码仓库：[https://github.com/zororaka00/sinkron](https://github.com/zororaka00/sinkron)  
PyPI 页面：[https://pypi.org/project/sinkron/](https://pypi.org/project/sinkron/)

---

## ⚠️ 安全性预检清单  
**安装前请完成所有项目，切勿跳过。**

### 1. 验证来源  
- [ ] 访问 [https://www.sinkron.id](https://www.sinkron.id)，确认该项目与预期一致。  
- [ ] 查看 [https://github.com/zororaka00/sinkron](https://github.com/zororaka00/sinkron) 的源代码。  
- [ ] 访问 [https://pypi.org/project/sinkron/](https://pypi.org/project/sinkron/)，确认包的所有者与作者 (`@zororaka00`) 一致。  
- [ ] 确保安装特定版本（`sinkron==X.Y.Z`）——切勿安装未指定版本的软件。  
- [ ] 如果无法验证来源，请**将此工具视为不可信的，切勿安装**。  

### 2. 安装前检查软件包  
```bash
# Download wheel/tarball without installing, then inspect contents
pip download sinkron==X.Y.Z --no-deps -d /tmp/sinkron-inspect
ls /tmp/sinkron-inspect/
# Unzip the .whl (it's a zip) and review .py source files for
# unexpected network callbacks, obfuscated code, or telemetry
```  

### 3. 先在隔离环境中进行安装  
```bash
# Preferred: use a container or VM for initial testing
docker run --rm -it python:3.11-slim bash
# Inside container:
pip install sinkron==X.Y.Z
sinkron --help
```  

### 4. 使用前了解令牌的来源  
`SINKRON_TOKEN` 是由 Sinkron 平台自动生成的，具体生成方式如下：  

| 场景 | 获取令牌的方法 |  
|---|---|  
| **新代理** | 运行 `sinkron register --username USER --name NAME`。Sinkron 后端会在 CLI 响应中生成令牌并仅打印一次，请立即复制。 |  
| **现有代理** | 令牌是在之前的 `sinkron register` 操作中生成的，直接通过 `SINKRON_TOKEN` 环境变量设置即可。 |  

令牌永远不会来自 URL 请求、第三方服务或该工具本身，仅来自 Sinkron 后端的 `register` 响应。  

**获取令牌后：**  
- [ ] 立即将其存储在密钥管理器或受限制的 `.env` 文件中。  
- [ ] 令牌显示后清除终端/Shell 的历史记录。  
- [ ] 确保令牌未出现在日志、持续集成（CI）输出或版本控制文件中。  
- [ ] 定期更换令牌，或在怀疑有泄露风险时立即更换。  

---

## 安装步骤  

### 第一步：检查 PyPI 上的最新固定版本  
```bash
pip index versions sinkron
```  

### 第二步：使用固定版本进行安装  
```bash
# Preferred (pinned version)
pip install sinkron==X.Y.Z

# Alternative via uv (also pin version)
uv tool install sinkron==X.Y.Z
```  
> ⚠️ 请务必使用固定版本进行安装，否则可能会安装到未经审核的后续版本。  

### 第三步：验证安装是否成功  
```bash
sinkron --help
```  

---

## 最佳使用实践  

### 1. 安装流程  
在执行任何 Sinkron 操作之前：  
- 确保已安装 `sinkron`。  
- 如果未安装，请先按照上述**安装**步骤进行操作（包括验证来源）。  
- 使用 `sinkron --help` 命令验证安装是否成功。  

---

### 2. 令牌的生命周期与管理  
#### `SINKRON_TOKEN` 的来源  
```
New agent   → sinkron register --username USER --name NAME
                ↳ Sinkron backend responds with: token: <YOUR_TOKEN>
                ↳ Copy this token immediately — it is shown only once
                ↳ Store in secret manager or restricted env var

Existing agent → token was issued during prior registration
                ↳ Set SINKRON_TOKEN directly from secure storage
```  
令牌完全由 Sinkron 后端生成，不涉及任何第三方服务或 OAuth 流程。  

#### 安全使用令牌  
```bash
# After registration: store token (clear shell history after)
export SINKRON_TOKEN="token-from-sinkron-register-output"
sinkron config --token "$SINKRON_TOKEN"

# In CI/CD: inject via secret manager — never hard-code
sinkron config --token "$SINKRON_TOKEN"
```  
- **切勿** 在 Shell 历史记录、日志或 CI 生成物中记录、打印或暴露令牌。  
- 使用 `sinkron health` 命令检查 Sinkron 平台是否正常运行。  
- 定期更换令牌，并在怀疑有泄露风险时立即更换。  

---

### 3. 代理注册的幂等性  
在注册之前，检查用户名是否已存在：  
```bash
sinkron agent USERNAME
```  
仅在该用户名不存在时才进行注册：  
```bash
sinkron register --username USER --name NAME
```  
这样可以防止重复注册，并确保自动化流程的稳定性。  

---

### 4. 安全处理收件箱  
- 使用分页功能，避免一次性获取大量邮件。  
- 建议使用 `--search` 参数进行过滤查询。  
- 绝不要盲目删除邮件——务必先查看邮件 ID。  

安全操作流程：  
1. `sinkron inbox --search KEYWORD`  
2. 查看邮件 ID  
3. `sinkron delete-messages --ids 1,2,3`  

---

### 5. 自动化策略  
始终先进行健康检查：  
```bash
sinkron health || exit 1
```  
- 仅记录非敏感信息。  
- 对 API 失败实现重试逻辑。  
- 通过 CI 密钥管理器注入 `SINKRON_TOKEN`，切勿将其硬编码在管道文件中。  

---

### 6. Python SDK 的最佳实践  
```python
import os
from sinkron import SinkronClient

token = os.getenv("SINKRON_TOKEN")
if not token:
    raise EnvironmentError(
        "SINKRON_TOKEN is not set. "
        "Obtain it from `sinkron register` output and store in a secret manager."
    )

client = SinkronClient(token=token)
messages = client.inbox(page=1)
```  
- 每次运行时仅初始化一次客户端。  
- 绝不要将令牌硬编码，始终使用环境变量。  
- 对失败情况实现指数级重试机制。  

---

## 架构  
Sinkron 提供两个操作层：  
1. **CLI**：用于操作/DevOps 工作流程  
2. **Python SDK**：用于程序化集成  

两者均通过相同的 Sinkron 后端 API 进行通信。  

---

## 运行要求  
- Python 3.8 或更高版本  
- 必须能够访问互联网  
- 需要 `SINKRON_TOKEN` 环境变量（通过 `sinkron register` 命令生成）  
- 首次设置时建议在隔离环境（容器/虚拟机）中安装  

---

## 安全指南  
- 安装前验证软件包的来源并检查源代码。  
- 确保安装特定版本的软件包。  
- 将 `SINKRON_TOKEN` 存储在密钥管理器或受限制的环境变量中，切勿将其放入源代码中。  
- 使用 `sinkron health` 命令检查 Sinkron 平台是否正常运行。  
- 定期更换令牌，并在怀疑有泄露风险时立即更换。  
- 设置令牌后清除 Shell 历史记录（使用 `HISTCONTROL=ignorespace` 或 `read -s`）。  
- 在生产环境部署前在隔离环境中进行测试。  

---

## 可观测性建议  
- 记录健康状态、邮件数量和删除结果。  
- **不要记录** 令牌内容、邮件内容或敏感元数据。  

---

## CLI 命令  
### 健康检查  
```bash
sinkron health
```  

### 注册新代理  
```bash
sinkron register --username USER --name NAME
```  
> **`SINKRON_TOKEN` 就在此处生成**。Sinkron 后端会在响应中生成令牌并仅打印一次，请立即复制并安全存储。切勿在可记录或共享的环境中运行该命令。  
>
> ```
> Registration successful.
> username: myagent
> email:    myagent@sinkron.id
> token:    snk_xxxxxxxxxxxxxxxxxxxxxxxx   ← copy immediately, store securely
> ```  
>
> 已经拥有令牌的现有代理：跳过此步骤，直接设置 `SINKRON_TOKEN`。  

### 获取收件箱内容  
```bash
sinkron inbox [--page N] [--search KEYWORD]
```  

### 检查邮件是否存在  
```bash
sinkron check ADDRESS
```  

### 获取邮件  
```bash
sinkron message ID
```  

### 删除邮件  
```bash
sinkron delete-messages --ids 1,2,3
```  

### 删除收件箱  
```bash
sinkron delete-inbox [--force]
```  

### 获取代理信息  
```bash
sinkron agent USERNAME
```  

### 检查平台状态  
```bash
# Use this command to check if Sinkron platform is active
sinkron health
```  

### 设置令牌  
```bash
# Always load from environment variable
sinkron config --token "$SINKRON_TOKEN"
```  

### 清除令牌  
```bash
sinkron config --clear-token
```  

---

## 自动化模式  
### 最小化风险的工作流程  
```bash
sinkron health || exit 1
sinkron inbox --page 1
```  

### 安全删除邮件  
```bash
sinkron inbox --search "alert"
# Review IDs before deleting
sinkron delete-messages --ids 10,11
```  

---

## 失败处理策略  
1. 认证失败 → 通过 `SINKRON_TOKEN` 环境变量提示用户重新配置令牌。  
2. 网络错误 → 实现指数级重试机制。  
3. 收件箱为空 → 返回结构化的空响应。  
4. 邮件 ID 无效 → 提示用户重新输入。  

确保错误能够被及时发现和处理。  

---

## 生产就绪检查  
- [ ] 已验证来源：确认官方网站、GitHub 仓库和 PyPI 上的包所有者信息。  
- [ ] 已检查软件包的源代码（无异常的网络调用或遥测数据）。  
- 安装时使用了固定版本的软件包。  
- 首先在隔离环境（容器/虚拟机）中进行了测试。  
- 使用 `sinkron --help` 命令确认安装成功。  
- 令牌从 `sinkron register` 的输出中获取（新代理）或之前的注册记录中获取（现有代理）。  
- 注册后立即将令牌存储在密钥管理器或受限制的环境变量中。  
- 令牌显示后清除 Shell 历史记录。  
- 令牌未出现在日志、CI 输出或版本控制文件中。  
- 在工作流程开始时检查 `sinkron health` 状态（确认平台是否正常运行）。  
- 在工作流程开始时集成 `sinkron health || exit 1` 逻辑。  
- 日志记录经过处理（不包含令牌或敏感信息）。  
- 实现了重试机制。  
- 确认了安全的删除逻辑（避免批量删除操作）。  

---

## 结论  
通过 Sinkron 平台，该工具为 AI 代理提供了永久的电子邮件身份和自动化收件箱管理功能。  
`SINKRON_TOKEN` 由 Sinkron 后端在注册时自动生成，不依赖第三方服务。在确保来源可验证、使用固定版本、安全处理令牌以及控制删除流程的前提下，该工具适合在生产环境中使用。  
**如果无法验证软件包的来源，请勿安装。在源代码验证完成之前，将该工具视为不可信的。**