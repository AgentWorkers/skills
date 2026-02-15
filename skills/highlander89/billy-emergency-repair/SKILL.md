# Billy紧急修复技能

## 使用场景
- Neill明确请求对Billy系统进行修复
- Neill报告Billy的认证/网关问题
- Neill表示“修复Billy”或“Billy无法正常使用”
- Billy系统对Neill的指令无响应

## 不适用场景
- Billy运行正常
- 问题与认证无关
- 除Neill之外的其他人请求修复
- 常规维护（非紧急情况）

## 需要授权
⚠️ **仅限Neill使用** ⚠️
只有Neill有权授权对Billy进行紧急修复。未经Neill明确授权，严禁执行此操作。

## 使用方法

### 标准修复（推荐）
```bash
# Switch to Opus for enhanced diagnostics
export OPENCLAW_MODEL_OVERRIDE="anthropic/claude-opus-4-6"

# Run authorized repair
bash ~/.openclaw/workspace/scripts/emergency-repair/fix-billy-auth.sh --authorized-by Neill
```

### 设置（只需运行一次）
```bash
# Set up SSH keys first time
bash ~/.openclaw/workspace/scripts/emergency-repair/setup-billy-repair-keys.sh
```

## 功能流程
1. **验证Neill的授权**（安全检查）
2. 通过Tailscale连接到Billy（使用SSH）
3. 备份Billy的配置文件（确保数据安全）
4. 清除过期的认证令牌（删除`.token`和`device*.json`文件）
5. 删除硬编码的认证信息（防止问题重复发生）
6. 重启Billy的网关服务
7. 验证修复是否成功（测试认证功能）
8. 记录所有操作（生成完整审计日志）
9. 向Neill报告修复结果（成功/失败）

## 典型对话流程
**Neill:** “SAPCONET，Billy又出现了认证错误，请修复它。”
**SAPCONET回复:**
```
🚨 Emergency repair authorized by Neill
🔧 Switching to Opus model for enhanced diagnostics
🔗 Connecting to Billy via SSH...
📋 Backing up Billy's configuration...
🧹 Clearing stale authentication tokens...
⚠️  Found hardcoded token - removing...
🔄 Restarting Billy's gateway...
⏳ Waiting for startup...
🧪 Testing authentication...
✅ SUCCESS: Billy's authentication restored!
📊 Repair completed in 45 seconds
```

## 错误处理
- **SSH连接失败**：
  - 检查Billy是否在线
  - 确认Tailscale连接是否正常
  - 确认Billy上已安装SSH密钥

- **修复失败**：
  - 需要手动干预
  - 将完整错误日志提供给Neill
  - 根据具体诊断信息进行问题升级处理

- **结果不确定**：
  - 网关有响应，但状态不明确
  - 建议Neill手动检查
  - 提供修复日志供分析

## 安全特性
- **仅限Neill授权**：脚本会拒绝未经授权的访问
- **SSH密钥认证**：确保与Billy的安全连接
- **完整审计日志**：所有操作都会被记录
- **配置文件备份**：保留原始设置
- **非破坏性操作**：仅删除认证相关数据

## 前提条件
- Billy上必须已安装SSH密钥（一次性设置）
- SAPCONET与Billy之间需要建立Tailscale连接
- Billy必须处于在线状态且可访问

## 生成的文件
- `/home/neill/.openclaw/workspace/output/billy-repair-YYYYMMDD-HHMM.log`
- `~/.openclaw/openclaw.json.pre-repair-YYYYMMDD-HHMM`（Billy上的备份文件）

## 测试
```bash
# Test SSH connection
ssh -i ~/.ssh/billy-repair-key ubuntu@100.90.73.34 'echo "Connection works"'

# Dry run (check authorization)
bash ~/.openclaw/workspace/scripts/emergency-repair/fix-billy-auth.sh
# Should show: "UNAUTHORIZED: This repair requires Neill's explicit authorization"
```

## 故障排除
如果修复操作持续失败：
1. 检查Billy的系统日志
2. 验证OpenClaw的安装完整性
3. 考虑重新安装OpenClaw
4. 检查是否存在更深层次的系统问题（如磁盘空间不足、权限问题等）

**注意**：此技能仅用于处理**认证相关的紧急情况**。对于复杂的故障诊断，请使用Opus模型。