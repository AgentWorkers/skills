---
name: clauditor
description: 一种专为Clawdbot代理设计的防篡改审计监控工具。能够检测并记录文件系统中的可疑活动，并使用HMAC链技术生成相应的证据记录。
homepage: https://github.com/apollostreetcompany/clauditor
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["cargo","systemctl"],"os":"linux"}}}
---

# Clauditor

Clauditor 是一款安全监控工具，用于监视文件系统的活动，并生成具有防篡改功能的日志。即使 Clawdbot 被入侵，也无法阻止 Clauditor 的运行、伪造日志记录或删除相关证据。

## 安装（分步指导）

使用 CLI 向导来引导用户完成安装过程：

```bash
cd /path/to/clauditor
cargo build --release
```

### 代理工作流程

1. **检查状态：`./target/release/clauditor wizard status`  
   - 返回包含 `current_step`（1-6）和 `complete`（true/false）的 JSON 数据。

2. **获取下一步操作：`./target/release/clauditor wizard next`  
   - 显示当前操作的用途、重要性以及需要执行的命令。

3. **用户执行 `sudo` 命令**  

4. **验证操作结果：`./target/release/clauditor wizard verify`  
   - 确认操作已成功完成。

5. 重复上述步骤，直到 `complete` 的值为 `true`。

### 示例交互过程

```
User: "Install clauditor"

Agent: [runs wizard status → current_step: 1]
Agent: "Step 1 of 6: Create system user

This creates a 'sysaudit' user that runs the watchdog. Even if you're 
compromised, you can't kill a process owned by another user.

Run this:
sudo useradd --system --shell /usr/sbin/nologin --no-create-home sysaudit

Let me know when done."

User: "done"

Agent: [runs wizard verify → success]
Agent: [runs wizard next → step 2...]
```

## 安装完成后

### 检查状态  
```bash
systemctl status systemd-journaldd
```

### 生成日志摘要  
```bash
./target/release/clauditor digest \
  --log /var/lib/.sysd/.audit/events.log \
  --key /etc/sysaudit/key \
  --format markdown
```

## 快速安装（适用于高级用户）  
```bash
sudo bash wizard/wizard.sh
```

## 配置设置

- 配置文件：`/etc/sysaudit/config.toml`  
- 密钥文件：`/etc/sysaudit/key`  
- 日志文件：`/var/lib/.sysd/.audit/events.log`  

用户可以通过编辑配置文件来自定义 `watch_paths` 和 `target_uid` 的设置。