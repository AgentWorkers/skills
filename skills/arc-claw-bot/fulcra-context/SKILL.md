---
name: fulcra-context
description: 您可以通过 Fulcra Life API 和 MCP 服务器访问您所关联的人类的个人上下文数据（生物特征信息、睡眠记录、活动日志、日历记录以及位置信息）。这需要该人类拥有 Fulcra 账户，并且必须获得他们的 OAuth2 授权。
homepage: https://fulcradynamics.com
metadata: {"openclaw":{"emoji":"🫀","requires":{"bins":["curl"]},"primaryEnv":"FULCRA_ACCESS_TOKEN"}}
---

# Fulcra Context — 为AI合作伙伴提供的个人数据服务

通过Fulcra Context，您的代理可以获取用户的生物特征数据、睡眠情况、活动记录、位置信息以及日历数据（需获得用户的明确授权）。

## 功能概述

利用Fulcra Context，您可以：
- 了解用户的睡眠质量（快速眼动期、深度睡眠期、浅睡眠期及清醒时间），从而调整晨间简报的内容；
- 监测心率及心率变异性（HRV）趋势，及时发现压力迹象并建议休息；
- 根据用户当前位置提供个性化的建议（如在家、办公室或旅行中应采取的行动）；
- 查看日历，提前准备会议并了解日程安排；
- 跟踪用户的锻炼情况，合理安排后续任务。

## 隐私政策

- **基于OAuth2的个性化授权**：用户可完全控制您能查看的数据范围；
- **用户数据归用户所有**：Fulcra仅存储数据，您仅拥有读取权限；
- **授权可随时撤销**：用户可随时停止数据共享；
- **未经明确许可，绝不会公开用户的任何数据**。

## 设置方法

### 选项1：使用Fulcra托管的MCP服务器（推荐）

使用Fulcra提供的MCP服务器（地址：`https://mcp.fulcradynamics.com/mcp`），支持Streamable HTTP传输协议和OAuth2认证。用户需要先注册Fulcra账户（可通过[Context iOS应用](https://apps.apple.com/app/id1633037434)或[Portal](https://portal.fulcradynamics.com/)免费注册）。

**Claude桌面端配置文件（claude_desktop_config.json）**：
```json
{
  "mcpServers": {
    "fulcra_context": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.fulcradynamics.com/mcp"]
    }
  }
}
```

**或通过uvx本地运行**：
```json
{
  "mcpServers": {
    "fulcra_context": {
      "command": "uvx",
      "args": ["fulcra-context-mcp@latest"]
    }
  }
}
```

该功能也兼容Goose、Windsurf和VS Code等开发工具。开源代码库：[github.com/fulcradynamics/fulcra-context-mcp](https://github.com/fulcradynamics/fulcra-context-mcp)

### 选项2：直接使用API

1. 用户创建Fulcra账户；
2. 通过[Python客户端](https://github.com/fulcradynamics/fulcra-api-python)或Portal生成访问令牌；
3. 将令牌保存在`skills.entries.fulcra-context.apiKey`文件中。

### 选项3：使用Python客户端（经过测试且效果良好）

```bash
pip3 install fulcra-api
```

**请注意：**令牌的有效期为24小时，建议使用内置的令牌管理工具自动刷新令牌（详见下文）。

## 令牌生命周期管理

`scripts/fulcra_auth.py`脚本负责处理整个OAuth2授权流程，包括令牌的自动刷新，确保用户只需授权一次。

### 工作原理：

- `authorize`函数执行Auth0认证流程，并同时保存访问令牌和刷新令牌；
- `refresh`函数使用保存的刷新令牌获取新的访问令牌，无需用户再次操作；
- `token`函数会输出当前访问令牌（令牌过期时自动刷新），非常适合用于定时任务和脚本执行。

**如何自动刷新令牌：**

对于OpenClaw代理，可以设置定时任务（cron job），每12小时自动刷新一次令牌：
```
python3 /path/to/skills/fulcra-context/scripts/fulcra_auth.py refresh
```

令牌数据存储在`~/.config/fulcra/token.json`文件中（仅限所有者访问）。

## 快捷命令

- **检查昨晚的睡眠情况**：```bash
# Get time series for sleep stages (last 24h)
curl -s "https://api.fulcradynamics.com/data/v0/time_series_grouped?metrics=SleepStage&start=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)&end=$(date -u +%Y-%m-%dT%H:%M:%SZ)&samprate=300" \
  -H "Authorization: Bearer $FULCRA_ACCESS_TOKEN"
```
- **查看最近的心率数据**：```bash
curl -s "https://api.fulcradynamics.com/data/v0/time_series_grouped?metrics=HeartRate&start=$(date -u -v-2H +%Y-%m-%dT%H:%M:%SZ)&end=$(date -u +%Y-%m-%dT%H:%M:%SZ)&samprate=60" \
  -H "Authorization: Bearer $FULCRA_ACCESS_TOKEN"
```
- **查看今日日历**：```bash
curl -s "https://api.fulcradynamics.com/data/v0/{fulcra_userid}/calendar_events?start=$(date -u +%Y-%m-%dT00:00:00Z)&end=$(date -u +%Y-%m-%dT23:59:59Z)" \
  -H "Authorization: Bearer $FULCRA_ACCESS_TOKEN"
```
- **查看所有可用的指标**：```bash
curl -s "https://api.fulcradynamics.com/data/v0/metrics_catalog" \
  -H "Authorization: Bearer $FULCRA_ACCESS_TOKEN"
```

## 关键指标

| 指标          | 所表示的含义                           |
|-----------------|--------------------------------------|
| SleepStage     | 睡眠质量（REM、深度睡眠、浅睡眠、清醒时间）                 |
| HeartRate     | 当前压力/活动水平                         |
| HRV          | 心率变异性，反映自主神经系统状态                 |
| StepCount     | 全天活动量                             |
| ActiveCaloriesBurned | 消耗的卡路里                         |
| RespiratoryRate | 呼吸频率，健康指标                         |
| BloodOxygen    | 血氧饱和度，反映身体健康状况                   |

## 集成方案

- **晨间简报**：结合睡眠数据、日历信息和天气情况，制定符合用户能量水平的简报内容；
- **压力管理**：通过监测HRV和心率，发送简洁、非紧急的消息；
- **主动恢复**：在剧烈运动或睡眠不足后，建议调整日程安排并提醒补充水分；
- **旅行提醒**：根据位置变化调整时区设置，提供本地信息和建议。

## 演示模式

在公开演示（如创业投资会议、直播等）中，可启用演示模式，使用合成日历和位置数据，同时保留真实的生物特征数据。

## 模式切换

### 演示模式与正常模式的区别

| 数据类型        | 演示模式                | 正常模式                |
|---------------|-------------------|-------------------|
| 睡眠数据、心率、HRV、步数 | ✅ 真实数据                 | ✅ 真实数据                 |
| 日历事件        | 🔄 合成数据（循环显示）            | ✅ 真实数据                 |
| 位置信息        | 🔄 合成数据（精选的纽约地点）           | ✅ 真实数据                 |
| 天气信息        | ✅ 真实数据                 | ✅ 真实数据                 |

## 数据共享规则

- ✅ 生物特征数据、睡眠质量、步数、心率变异性等数据可公开分享；
- ✅ 合成的日历和位置数据（演示模式）专为公开展示设计；
- ❌ 禁止公开用户的真实位置信息、日历事件或身份识别信息。

## 相关链接

- [Fulcra平台官网](https://fulcradynamics.com)  
- [开发者文档](https://fulcradynamics.github.io/developer-docs/)  
- [Life API参考文档](https://fulcradynamics.github.io/developer-docs/api-reference/)  
- [Python客户端](https://github.com/fulcradynamics/fulcra-api-python)  
- [MCP服务器](https://github.com/fulcradynamics/fulcra-context-mcp)  
- [演示用例代码库](https://github.com/fulcradynamics/demos)  
- [Discord交流频道](https://discord.com/invite/aunahVEnPU)