---
name: cloudflare-dns-updater
description: "创建或更新一个代理的 Cloudflare DNS A 记录。当您需要通过编程方式将子域名指向某个 IP 地址时，请使用此功能。输入参数包括记录名称、区域名称和 IP 地址。"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      python: ["requests"]
---

# Cloudflare DNS 更新器

此技能用于创建或更新 Cloudflare 的 DNS “A” 记录，将其指向指定的 IP 地址，并确保该记录通过 Cloudflare 代理进行传输。它是自动化服务部署和 DNS 管理的基础工具。

## 前提条件

使用此技能之前，需要设置 `CLOUDFLARE_API_TOKEN` 环境变量，该变量应包含具有 DNS 编辑权限的有效 Cloudflare API Token。

模型应在尝试使用此技能之前验证这一前提条件。如果该变量未设置，应通知用户并停止操作。

## 核心操作：`scripts/update-record.py`

核心逻辑由 `update-record.py` 脚本处理。

### **输入参数（命令行参数）**

- `--zone`：（必填）根域名。示例：`example.com`
- `--record`：（必填）记录的名称（子域名）。使用 `@` 表示根域名本身。示例：`www`
- `--ip`：（必填）要指向的 IPv4 地址。
- `--proxyed`：（可选）布尔值（`true` 或 `false`），用于设置 Cloudflare 代理状态。默认值为 `true`。

### **输出**

脚本会将执行进度输出到标准输出（stdout）：
- 成功时，会打印确认消息以及创建/更新后的记录的 JSON 对象。
- 失败时，会向标准错误输出（stderr）打印详细的错误信息，并以非零的状态码退出。

### **执行流程**

使用此技能，请按照以下步骤操作：

1. **验证前提条件**：检查 `CLOUDFLARE_API_TOKEN` 环境变量是否已设置。如果没有设置，通知用户并中止操作。
2. **收集输入参数**：从用户请求中获取 `zone`（区域名称）、`record`（记录名称）和目标 `ip`（IP 地址）。
3. **构建命令**：生成用于执行脚本的完整 shell 命令。
4. **执行命令**：使用 `exec` 工具运行该命令。
5. **报告结果**：
    - 如果命令成功，向用户报告记录已成功创建或更新。
    - 如果命令失败，分析标准错误输出（stderr）中的错误信息，并以清晰易懂的方式向用户报告问题。

### **示例用法**

**用户请求**：“将 www.example.com 指向服务器的公共 IP。”

**AI 的处理流程**：
1. 用户希望更新 Cloudflare 上的 DNS 记录。`cloudflare-dns-updater` 技能非常适合完成此操作。
2. 我将使用 `update-record.py` 脚本。
3. 我需要获取区域名称、记录名称和目标 IP 地址。
    - 区域名称：`example.com`
    - 记录名称：`www`
    - IP 地址：我需要先获取服务器的公共 IP 地址。可以使用 `curl -s https://ipv4.icanhazip.com/` 来获取。
4. 我会先获取 IP 地址，然后构建最终的命令。
5. 我将执行命令并报告执行结果。

**AI 的具体操作**：
```bash
# Step 1: Get IP
PUBLIC_IP=$(curl -s https://ipv4.icanhazip.com/)

# Step 2: Run the skill's script
python3 skills/cloudflare-dns-updater/scripts/update-record.py \
  --zone "example.com" \
  --record "www" \
  --ip "$PUBLIC_IP"
```

### **失败处理策略**

- **如果 `CLOUDFLARE_API_TOKEN` 未设置**：不要尝试运行脚本。通知用户缺少必要的环境变量，并提示管理员进行配置。
- **如果脚本执行失败**：读取标准错误输出（stderr）中的错误信息。常见的错误包括无效的 API Token、错误的区域名称或权限不足。向用户报告具体的错误原因。