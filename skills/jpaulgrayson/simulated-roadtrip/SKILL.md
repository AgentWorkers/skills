# 模拟公路旅行

让你的Clawbot通过GPS在现实世界中进行一次公路旅行吧！选择一条路线、一个主题，Turai会利用真实的Google Maps数据生成带有旁白的旅行站点信息。你的代理会在Clawbot“旅行”过程中实时更新这些信息。

## 架构原理

你的代理会指定起点和终点，Turai公路旅行API会规划一条实际的路线，并确定沿途的各个站点。每个站点包含以下信息：

- **真实位置数据**：GPS坐标、地点名称、距离（来自Google Maps）
- **主题相关的叙述**：以真实旅行者的视角撰写的描述
- **当地环境细节**：你在每个站点能看到的景象、听到的声音、闻到的气味以及可以品尝的食物

代理可以按固定时间间隔（每小时、每天等）逐步发布这些站点信息，从而在聊天窗口、Moltbook或任何消息渠道中创建一个连续的旅行叙事。

## 可用主题

| 主题 | 旅行重点 |
|-------|-------|
| `历史` | 历史地标、战场、纪念碑 |
| `美食` | 当地餐厅、街头小吃、地区特色美食 |
| `鬼故事` | 幽灵传说、废弃场所、当地民间传说 |
| `奇异景观` | 路边奇观、奇特的事物、世界上最大的物体 |
| `自然** | 国家公园、风景优美的观景点、野生动物 |
| **艺术** | 画廊、壁画、公共艺术作品 |
| **建筑** | 著名建筑、桥梁、城市设计 |
| **音乐** | 音乐演出场所、音乐家的出生地、音乐历史相关地点 |
| **文学** | 书店、作家故居、小说中的场景 |
| **电影** | 电影拍摄地、电影中的标志性地点 |
| **宗教** | 寺庙、教堂、圣地 |
| **冒险** | 极限运动、徒步旅行、人迹罕至的路线 |

## 设置步骤

1. 从 [turai.org](https://turai.org) 获取Turai API密钥。
2. 设置环境变量：
   ```bash
   export TURAI_API_KEY="your-key-here"
   ```

## 使用方法

### 通过命令行使用

```bash
# Basic road trip — NYC to LA, 5 stops, foodie theme
node skills/simulated-roadtrip/scripts/roadtrip.mjs \
  --from "New York City" \
  --to "Los Angeles" \
  --theme foodie \
  --stops 5

# Haunted road trip through New England
node skills/simulated-roadtrip/scripts/roadtrip.mjs \
  --from "Salem, MA" \
  --to "Sleepy Hollow, NY" \
  --theme haunted \
  --stops 4

# Drip-feed mode — post one stop every 2 hours
node skills/simulated-roadtrip/scripts/roadtrip.mjs \
  --from "Nashville, TN" \
  --to "New Orleans, LA" \
  --theme music \
  --stops 6 \
  --drip 2h

# Save trip data to JSON for later use
node skills/simulated-roadtrip/scripts/roadtrip.mjs \
  --from "Tokyo" \
  --to "Kyoto" \
  --theme art \
  --stops 4 \
  --output trip.json
```

### 发布信息的时间间隔

- `1h`：每小时发布一次信息
- `2h`：每两小时发布一次信息
- `4h`：每四小时发布一次信息
- `1d`：每天发布一个站点信息
- `30m`：每30分钟发布一次信息（适合急切的旅行者）

### 通过你的代理使用

> “从芝加哥出发，前往奥斯汀，选择‘音乐’主题，设置5个旅行站点”

代理会运行相应的脚本，并将每个站点的信息以聊天消息或社交媒体的形式发送出来。

## API参考

**接口地址：** `POST https://turai.org/api/agent/roadtrip`

**请求头：**
- `x-api-key`：你的Turai API密钥
- `Content-Type`：`application/json`

**请求体：**
```json
{
  "from": "New York City",
  "to": "Los Angeles",
  "theme": "foodie",
  "stops": 5
}
```

**响应格式：** JSON格式的数据，其中包含多个站点信息，每个站点包含位置数据和叙述内容。

## 相关文件

- `SKILL.md`：本文档文件
- `scripts/roadtrip.mjs`：主要脚本文件