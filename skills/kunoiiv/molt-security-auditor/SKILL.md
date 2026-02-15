# Moltbook Skill Auditor – 基于工作量证明（PoW）的技能审计工具

该工具用于扫描 ClawdHub/Moltbook 中的技能内容，以检测潜在的安全威胁（如环境变量读取、通过 Webhook 进行的数据窃取等行为），并生成类似比特币哈希链的审计记录。

## 安装  
```bash
npx molthub@latest install molt-security-auditor
```

## 使用方法  
```bash
exec: node skills/molt-security-auditor/audit.js <skill_url_or_path>
```

## 支持的审计模式：  
- **ENV_READ**: 从 `.env` 文件或 `process.env` 中读取环境变量  
- **EXFIL**: 通过 `curl` 或 `fetch` 命令从指定的 Webhook 获取数据  
- **FS_ABUSE**: 从指定的文件中读取敏感信息（如密钥等）

## 工作量证明（PoW）机制：  
审计过程中会生成一个哈希值（使用 SHA256 对技能内容进行加密），并添加一个随机数（nonce）作为验证标识。这个哈希值可用于验证审计结果的完整性。

**示例：**  
```bash
$ audit.js https://clawdhub.com/skills/weather/SKILL.md
```
**审计结果：**  
- 检测到的威胁数量：0  
- 生成的哈希链：0000abcd...

（注：实际审计结果中的哈希链长度会根据审计内容而变化。）