---
name: peloton-stats
description: >
  **功能描述：**  
  用于获取并展示Peloton骑行训练的统计数据。当用户希望查看自己的Peloton训练数据、每周骑行记录或性能指标时，可使用该功能。该功能直接调用Peloton的API（无需依赖任何第三方服务），以获取每次骑行的总距离、时长、消耗的卡路里、输出功率以及教练的相关信息。
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - PELOTON_USERNAME
        - PELOTON_PASSWORD
      config:
        - ~/.openclaw/agents/main/agent/auth-profiles.json
    primaryEnv: PELOTON_USERNAME
    emoji: "🚴"
---
# Peloton 统计数据

直接从 Peloton API 获取每周的骑行统计数据。完全不依赖任何第三方库，仅使用 Python 标准库。

## 设置

使用 OpenClaw 的凭证管理器安全地存储您的 Peloton 凭据：

```bash
openclaw config set auth.profiles.peloton:default.type api_key
openclaw config set auth.profiles.peloton:default.provider peloton
openclaw config set auth.profiles.peloton:default.username "your-email@example.com"
openclaw config set auth.profiles.peloton:default.password "your-password"
```

或者直接编辑 `~/.openclaw/agents/main/agent/auth-profiles.json` 文件：

```json
{
  "profiles": {
    "peloton:default": {
      "type": "api_key",
      "provider": "peloton",
      "username": "your-email@example.com",
      "password": "your-password"
    }
  }
}
```

## 使用方法

### 周报

```bash
python3 ~/.openclaw/skills/peloton-stats/scripts/fetch_stats.py
```

输出格式为 Markdown，包含以下内容：
- 本周的总骑行次数
- 总骑行时间、消耗的卡路里总量（kJ）
- 平均功率（瓦特）、阻力百分比（%）、踏频（RPM）
- 最近的骑行记录（日期、课程类型、教练信息及各项指标）

## 获取的数据

| 指标          | 描述                          |
|--------------|------------------------------|
| **总骑行次数**     | 过去 7 天内的骑行次数                    |
| **总骑行时间**     | 总骑行分钟数                        |
| **消耗卡路里**     | 总消耗的卡路里（kJ）                    |
| **总能量**      | 总能量（kJ）                        |
| **平均功率**     | 所有骑行的平均功率（瓦特）                 |
| **平均阻力**     | 所有骑行的平均阻力百分比                 |
| **平均踏频**     | 所有骑行的平均踏频（RPM）                 |

## 注意事项

- 仅获取骑行相关的训练数据（不包括跑步、力量训练、瑜伽等类型的数据） |
- 数据统计范围为过去 7 天内的数据             |
- 需要拥有有效的 Peloton 订阅服务             |
- 该工具使用的是非官方的 Peloton API（地址：`api.onepeloton.com`）