---
name: hustle
description: "ZeroEx Hustle：套利智能与运营引擎。用于管理资金库、支付流程以及游戏自动化监控。"
---

# Hustle 操作

该技能提供了对 **Hustle** 引擎的访问权限，用于游戏套利和金融操作。

## 功能

1. **金库管理**：访问用于套利账户的安全凭证。
2. **市场情报**：用于价格检查的自动化脚本。
3. **支付流程**：管理 GUNZ 钱包和 Odealo 的集成。

## 工具

### `hustle_vault`

用于访问安全金库以检索或存储凭证。
**使用方法：**

```bash
python3 /Users/lowkey/Desktop/game-compare/hustle/engine/vault.py --action retrieve --key <key_name>
```

### `hustle_status`

用于检查套利机器人和监听器的状态。
**使用方法：**

```bash
# Check running processes for hustle engine
ps aux | grep hustle
```

## 工作流程

### 1. 初始化会话

在开始套利任务之前：

1. 确保 `.vault/secrets.json` 可以被访问。
2. 从金库中加载 `ACTIVE_IDENTITY`。
3. 检查与 GUNZ 钱包的连接是否正常。

### 2. 图片验证码处理

如果在网络自动化过程中遇到图片验证码：

1. 暂停执行。
2. 提示用户输入验证码，或使用 `captcha-solver` 技能（如果可用）。
3. 如果需要手动干预，使用 `browser_subagent` 等待用户输入。

## 资源

- **代码库：** `/Users/lowkey/Desktop/game-compare/hustle/`
- **配置文件：** `/Users/lowkey/Desktop/game-compare/.vault/`