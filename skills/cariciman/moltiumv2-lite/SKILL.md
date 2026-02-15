---
name: MoltiumV2
description: **Lightweight Clawhub Bootstrap Skill for MoltiumV2**  
该技能用于快速启动基于MoltiumV2的Clawhub服务器。它会从[https://moltium.fun](https://moltium.fun)下载完整的RPC-first本地开发工具包（RPC-first local toolkit），并执行`init/doctor`命令以完成初始化过程。
---

# MoltiumV2（Clawhub Lite Bootstrap）

为了避开上传限制，这个 Clawhub 脚本被特意设计得非常简洁（仅包含文本内容）。它会从官方网站下载完整的 MoltiumV2 工具包：

- 文档索引：https://moltium.fun/skill.md
- Skillpack 文件夹：
  - https://moltium.fun/MoltiumV2-skillpack-latest.zip
  - https://moltium.fun/MoltiumV2-skillpack-latest.tar.gz

## 快速启动

在您安装或上传此 Clawhub 脚本的文件夹中，运行以下命令：

```bash
node scripts/bootstrap.mjs
```

可选的环境变量：
- `MOLTIUMV2_DIR` — 安装目标文件夹（默认值：`MoltiumV2`）
- `MOLTIUMV2_BASE_URL` — 下载基地址（默认值：`https://moltium.fun`）

脚本的执行步骤：
- 下载 `MoltiumV2-skillpack-latest.tar.gz` 文件
- 将文件解压到 `MOLTIUMV2_DIR` 目录中
- 运行 `npm install` 命令进行依赖项安装
- 运行 `ctl.mjs init --pretty` 命令（如果缺少钱包文件，则会自动生成钱包）
- 运行 `ctl.mjs doctor --pretty` 命令（检查系统配置）

在发送实际交易之前，请先为生成的钱包公钥充值。

## 安全规则（必须遵守）：
- 绝不要在聊天中输入种子短语（用于恢复钱包的密码）。
- 在进行实际交易之前，请务必使用 `--simulate` 选项进行模拟测试。