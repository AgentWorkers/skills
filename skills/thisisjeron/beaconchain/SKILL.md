---
name: beaconchain
description: 通过 V2 API 在 beaconcha.in 上监控以太坊验证器的运行状态，重点关注每日一次的检查结果以及基于 BeaconScore 的故障排查机制。当用户需要查询验证器的运行状况、BeaconScore、未完成的任务，或设置针对 beaconcha.in 仪表盘的每日监控/警报时，可以使用此功能。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["python3"],
            "env": ["BEACONCHAIN_API_KEY", "BEACONCHAIN_DASHBOARD_ID"],
          },
        "disableModelInvocation": true,
      },
  }
---

# Beaconchain

使用此技能可以减少对验证器检查的焦虑：每天进行一次简洁的健康检查，仅在发现问题时才进行详细处理。

## 快速入门

1. 将凭据设置为环境变量：
   - `BEACONCHAIN_API_KEY`
   - `BEACONCHAIN_DASHBOARD_ID`
2. 运行以下命令：

```bash
python3 skills/beaconchain/scripts/check_dashboard.py --json
```

3. 解释退出代码：
   - `0` = 一切正常
   - `2` = 存在问题（需要关注）
   - `1` = 出现错误（认证问题/速率限制/端点故障）

## 监控工作流程

1. 每天运行一次 `scripts/check_dashboard.py` 脚本。
2. 如果 `status` 为“正常”，只需发送简短的确认信息，无需提供额外细节。
3. 如果 `status` 为“有问题”，则报告以下内容：
   - BeaconScore（如果可用）
   - 触发问题的具体信号（未检测到信号/受到惩罚）
   - 下一步操作：查看仪表板详细信息和验证器日志。
4. 如果 `status` 为“错误”，则报告以下关键检查结果：
   - API 密钥的有效性
   - 仪表板 ID
   - 计划/速率限制权限

## 命令模式

### 基本检查

```bash
python3 skills/beaconchain/scripts/check_dashboard.py
```

### JSON 输出（用于定时任务/解析）

```bash
python3 skills/beaconchain/scripts/check_dashboard.py --json
```

### 自定义阈值

```bash
python3 skills/beaconchain/scripts/check_dashboard.py --warn-threshold 75
```

## 注意事项

- 脚本使用 `POST /api/v2/ethereum/validators/performance-aggregate` 请求，并直接读取 `data.beaconscore.total` 数据。
- 默认时间窗口为 24 小时；支持的时间窗口：`24h`、`7d`、`30d`、`90d`、`all_time`。
- 当系统运行正常时，响应信息会尽量简洁，以降低操作者的焦虑。

## 安全性与透明度

- 运行环境：仅使用 Python 3，并使用 Python 标准库（`argparse`、`json`、`urllib`、`datetime`）。
- 凭据：读取 `BEACONCHAIN_API_KEY` 和 `BEACONCHAIN_DASHBOARD_ID`（或相应的 CLI 参数）。
- 网络请求目标：仅限于 `https://beaconcha.in/api/v2/ethereum/validators/performance-aggregate`。
- 本地文件系统：无写入操作，不执行 shell 命令，也不启动子进程。

## 参考资料

- API 说明：`references/api-notes.md`