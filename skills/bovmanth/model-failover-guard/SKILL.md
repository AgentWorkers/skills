# OpenClaw 模型故障转移保护机制

为 OpenClaw 提供的自动模型故障转移及回滚保护功能。

## 描述

当主模型出现不稳定情况时，该保护机制会自动切换到可用的备用模型，并在主模型恢复正常后再次切换回主模型。

## 特点

- 定期监控模型运行状态
- 如果主模型连续失败 N 次，则触发故障转移
- 备用模型从所有已配置的模型中自动选择
- 支持设置优先使用的备用模型
- 在备用模型稳定运行 N 次后，尝试进行回滚操作
- 如果回滚测试失败，立即恢复到备用模型状态

## 安装

```bash
npx skills add BovmantH/openclaw-model-failover-guard --skill model-failover-guard
```

## 使用方法

```bash
# Run once
python3 skills/model-failover-guard/scripts/failover.py once

# Run as daemon
python3 skills/model-failover-guard/scripts/failover.py loop
```

## 配置

将 `skills/model-failover-guard/config.example.json` 复制到 `config.json` 文件中，并根据需要调整配置参数：

| 参数 | 说明 |
|-------|--------|
| `primaryModel` | 需要监控的主模型 |
| `failThreshold` | 连续失败次数（触发故障转移的条件） |
| `recoverThreshold` | 备用模型稳定运行的次数（触发回滚的条件） |
| `checkIntervalSec` | 健康检查间隔（秒） |

## 开发者

- 开发者：BovmantH |
- 版本：1.0.0 |

## 许可证

MIT 许可证