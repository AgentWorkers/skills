---
name: dont-hack-me
description: >-
  別駭我！基本安全檢測 — Security self-check for Clawdbot/Moltbot.
  Run a quick audit of your clawdbot.json to catch dangerous
  misconfigurations — exposed gateway, missing auth, open DM policy,
  weak tokens, loose file permissions. Auto-fix included.
  Invoke: "run a security check" or "幫我做安全檢查".
author: "小安 Ann Agent — Taiwan 台灣"
homepage: https://github.com/peterann/dont-hack-me
metadata:
  clawdbot:
    emoji: "🔒"
---

# **不要黑我（Don't Hack Me）**  
这是一个用于检查Clawdbot/Moltbot安全配置的自动检查技能。它会读取`~/.clawdbot/clawdbot.json`文件，并检查7个常见的配置错误。最终会输出一个简单的“PASS”/“FAIL”/“WARN”报告。  

## **如何运行**  
你可以输入以下命令：  
- `run a security check`  
- `check my security settings`  
- `audit my clawdbot config`  
- `am I secure?`  

## **检查步骤**  
当该技能被触发时，请严格按照以下步骤操作：  

### **步骤0：读取配置文件**  
使用`read`工具打开`~/.clawdbot/clawdbot.json`文件，并解析其JSON内容。如果文件不存在或无法读取，会报告错误并停止检查。  
同时，运行以下shell命令来查看文件的权限：  
**```
stat -f '%Lp' ~/.clawdbot/clawdbot.json
```**  
（在Linux系统中：`stat -c '%a' ~/.clawdbot/clawdbot.json`）  

### **步骤1：网关绑定（Gateway Bind）**  
- **检查路径：** `gateway.bind`  
- **预期值：** `"loopback"`、`localhost`、`127.0.0.1`或`::1`  
- **结果：** 如果值为上述之一或该字段不存在（默认值为`loopback`），则视为**PASS**；  
- **结果：** 如果值为`0.0.0.0`、`::`或其他非循环回地址，则视为**FAIL**；  
- **严重性：** **CRITICAL** — 非循环回地址会导致代理暴露在网络中。  

### **步骤2：网关认证模式（Gateway Auth Mode）**  
- **检查路径：** `gateway.auth.mode`  
- **预期值：** `"token"`或`password`  
- **结果：** 如果值为`token`或`password`，或该字段不存在（默认值为`token`），则视为**PASS**；  
- **结果：** 如果值为`off`或`none`，则视为**FAIL**；  
- **严重性：** **CRITICAL** — 无认证机制会导致任何能够访问网关的人控制代理。  

### **步骤3：令牌强度（Token Strength）**  
- **检查路径：** `gateway.auth.token`  
- **预期值：** 至少32个字符  
- **结果：** 如果令牌长度大于或等于32个字符，则视为**PASS**；  
- **结果：** 如果令牌长度在16到31个字符之间，则视为**WARN**；  
- **结果：** 如果令牌长度小于16个字符或为空，则视为**FAIL**；  
- **注意：** 如果认证模式为`password`，则跳过此步骤（因为密码长度由用户自行设置）。  
- **严重性：** **HIGH** — 短令牌容易被暴力破解。  

### **步骤4：直接消息策略（DM Policy，针对每个频道）**  
- **检查路径：** `channels.<name>.dmPolicy`（每个频道对应一个文件）  
- **预期值：** `"pairing"`；如果设置为`open`，则`allowFrom`数组不能为空  
- **结果：** 如果`dmPolicy`为`pairing`，或`allowFrom`数组中至少有一个元素，則视为**PASS**；  
- **结果：** 如果`dmPolicy`为`open`且`allowFrom`为空或缺失，则视为**FAIL**；  
- **注意：** 如果没有配置任何频道，则跳过此步骤。  
- **严重性：** **HIGH** — 开放的直接消息策略会让任何人向代理发送命令。  

### **步骤5：组策略（Group Policy，针对每个频道）**  
- **检查路径：** `channels.<name>.groupPolicy`（每个频道对应一个文件）  
- **预期值：** `"allowlist"`  
- **结果：** 如果`groupPolicy`为`allowlist`或不存在（默认值为`allowlist`），则视为**PASS**；  
- **结果：** 如果`groupPolicy`为`open`或`any`，则视为**FAIL**；  
- **注意：** 如果没有配置任何频道，则跳过此步骤。  
- **严重性：** **HIGH** — 非允许列表的组策略会让任何组别触发代理。  

### **步骤6：文件权限（File Permissions）**  
- **检查路径：** `~/.clawdbot/clawdbot.json`  
- **预期值：** 权限设置为`600`或`400`（仅允许所有者读写）  
- **结果：** 如果权限设置为`600`或`400`，则视为**PASS**；  
- **结果：** 如果权限设置为`644`或`640`（允许组或其他用户读写），则视为**WARN**；  
- **结果：** 如果权限设置为`777`、`755`、`666`或任何允许全局写操作的权限，则视为**FAIL**；  
- **严重性：** **MEDIUM** — 松散的权限会让系统上的其他用户读取你的令牌。  

### **步骤7：明文密码扫描（Plaintext Secrets Scan）**  
- **检查内容：** 遍历JSON文件中的所有字符串值，查找名为`password`、`secret`、`apiKey`、`api_key`、`privateKey`、`private_key`的键（不区分大小写），并检查它们是否包含非空字符串  
- **结果：** 如果没有找到这些键，则视为**PASS**；  
- **警告：** 如果存在这些键，建议用户考虑使用环境变量或密码管理工具来存储敏感信息。  
- **注意：** 用于网关认证的`token`字段是必填项，不应被标记为错误。  
- **严重性：** **MEDIUM** — 配置文件中的明文密码可能通过备份、日志或版本控制工具泄露。  

## **输出格式**  
完成所有检查后，会输出如下格式的报告：  
**```
🔒 Security Check Report

1. Gateway Bind        <ICON> <STATUS> — <detail>
2. Gateway Auth        <ICON> <STATUS> — <detail>
3. Token Strength      <ICON> <STATUS> — <detail>
4. DM Policy           <ICON> <STATUS> — <detail>
5. Group Policy        <ICON> <STATUS> — <detail>
6. File Permissions    <ICON> <STATUS> — <detail>
7. Secrets Scan        <ICON> <STATUS> — <detail>

Score: X/7 PASS, Y WARN, Z FAIL
```**  
其中：  
- `<ICON>` 表示检查结果（✅：PASS、⚠️：WARN、❌：FAIL、⏭️：SKIP）  
- `<STATUS>` 表示整体状态（PASS、WARN、FAIL、SKIP）  
- `<detail>` 是简要的错误说明（例如：“网关绑定设置为`loopback`”）。  

## **自动修复流程**  
如果**任何**检查项的结果为**FAIL**或**WARN**，请执行以下操作：  
1. 首先显示报告。  
2. 列出所有需要修复的项，并说明修复内容。  
3. 提问用户：“是否希望我自动修复这些问题？（是/否/选择）”：  
   - **是**：自动修复所有**FAIL**和**WARN**项。  
   - **否**：停止操作，不做任何更改。  
   - **选择**：允许用户选择要修复的项。  
4. 应用修复措施（见下面的修复指南）。  
5. 修复完成后，重新读取配置文件并重新运行完整检查，确认所有项均为**PASS**。  
6. 如果配置文件已更改，提醒用户：“运行`clawdbot gateway restart`以应用新设置。”  

### **修复指南**  
针对每个问题，请使用以下命令进行修复：  
- **步骤1：网关绑定失败（FAIL）**：将`gateway.bind`设置为`loopback`：  
  **```json
{ "gateway": { "bind": "loopback" } }
```**  
- **步骤2：网关认证失败（FAIL）**：将`gateway.auth.mode`设置为`token`；如果尚未生成令牌，还需生成一个新的令牌：  
  **```json
{ "gateway": { "auth": { "mode": "token", "token": "<GENERATED>" } } }
```**  
  （使用以下命令生成48个字符的十六进制令牌：**```bash
openssl rand -hex 24
```**  
- **步骤3：令牌强度失败/警告（FAIL/WARN）**：用新的强令牌替换现有令牌：  
  **```bash
openssl rand -hex 24
```**  
  将新令牌写入`gateway.auth.token`文件。  
- **步骤4：直接消息策略失败（FAIL）**：将每个受影响频道的`dmPolicy`设置为`pairing`：  
  **```json
{ "channels": { "<name>": { "dmPolicy": "pairing" } } }
```**  
- **步骤5：组策略失败（FAIL）**：将每个受影响频道的`groupPolicy`设置为`allowlist`：  
  **```json
{ "channels": { "<name>": { "groupPolicy": "allowlist" } } }
```**  
- **步骤6：文件权限失败/警告（FAIL/WARN）**：运行以下命令：  
  **```bash
chmod 600 ~/.clawdbot/clawdbot.json
```**  
- **步骤7：明文密码警告（WARN）**：此问题无法自动安全修复。建议用户：  
  - 将相关键值移至环境变量；  
  - 或使用密码管理工具；  
  - 如果平台支持，可以在配置文件中引用环境变量（格式：`"$ENV_VAR_NAME"`）。  

### **自动修复的重要规则**  
- **务必先备份。** 在进行任何更改之前，请先复制原始配置文件：  
  **```bash
  cp ~/.clawdbot/clawdbot.json ~/.clawdbot/clawdbot.json.bak
  ```**  
- **合并修改，不要覆盖原有文件**：读取完整的JSON文件，仅修改特定字段，然后重新写入完整的JSON文件。  
- **保持格式一致**：使用2个空格进行缩进。  
- **一次性完成所有修改**：将所有修复操作合并为一次写入，以避免部分状态。  
- **令牌更换需重启**：如果网关令牌已更改，用户需要更新所有已配对的客户端以使用新令牌。  
  **警告：** “您的网关令牌已更改。所有已配对的设备都需要使用新令牌重新连接。”  

## **本技能不检查的内容**  
- 沙箱配置（大多数环境中无需检查）  
- 网络隔离/Docker设置（macOS原生环境不涉及）  
- MCP工具的权限设置（过于复杂，不适合简单审计）  
- 操作系统的防火墙配置  
- 代理代码是否存在漏洞  

如需更全面的审计，可参考社区工具`clawdbot-security-check`。  

## **参考来源**  
本技能基于社区整理的“Clawdbot/Moltbot十大安全漏洞”列表，涵盖了适用于典型macOS原生环境的7个关键问题。  

*小安 Ann Agent — 台灣*  
*为全球所有AI代理打造技能和本地MCP服务。*