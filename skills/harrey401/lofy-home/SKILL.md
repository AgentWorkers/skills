---
name: lofy-home
description: **Lofy AI助手的智能家居控制功能——场景模式（学习、休闲、睡眠、早晨、工作模式）**  
通过Home Assistant的REST API实现设备管理；支持基于用户位置的自动化控制；支持使用自然语言指令来控制灯光、音乐、恒温器以及通过网络唤醒PC。适用于控制智能家居设备、激活特定场景模式或管理家庭自动化系统。
---

# 主控器——环境控制

通过 Home Assistant 控制智能家居和计算环境，管理场景模式、设备控制以及基于用户状态的自动化操作。

## 数据文件：`data/home-config.json`

```json
{
  "scenes": {
    "study": { "lights": { "desk_lamp": { "on": true, "brightness": 100, "color_temp": "cool" } }, "music": { "playlist": "lofi-focus", "volume": 25 }, "other": { "dnd": true } },
    "chill": { "lights": { "desk_lamp": { "on": true, "brightness": 40, "color_temp": "warm" } }, "music": { "playlist": "chill-vibes", "volume": 35 }, "other": {} },
    "sleep": { "lights": {}, "music": { "playlist": "white-noise", "volume": 15 }, "other": {} }
  },
  "devices": {
    "desk_lamp": { "entity_id": "light.desk_lamp", "type": "light" },
    "speaker": { "entity_id": "media_player.room_speaker", "type": "media_player" }
  },
  "home_assistant": { "url": "http://homeassistant.local:8123", "token_env": "HA_TOKEN" }
}
```

## 场景激活

当用户输入“学习模式”、“放松模式”等指令时：
1. 从 `data/home-config.json` 中读取相应的场景配置
2. 通过 Home Assistant API 执行每个设备的控制命令
3. 简要确认执行结果：“学习模式已启动 —— 台灯亮度调整至适宜，背景音乐开启”

### Home Assistant API

```bash
# Light control
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.desk_lamp", "brightness_pct": 100}'

# Media playback
curl -s -X POST "$HA_URL/api/services/media_player/play_media" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -d '{"entity_id": "media_player.speaker", "media_content_id": "spotify:playlist:xxx", "media_content_type": "playlist"}'

# Wake-on-LAN
curl -s -X POST "$HA_URL/api/services/wake_on_lan/send_magic_packet" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -d '{"mac": "XX:XX:XX:XX:XX:XX"}'
```

## 快速指令

- “关灯” → 关闭所有灯光
- “调暗灯光” → 将所有灯光亮度调至 20%
- “播放音乐” → 播放默认的放松音乐列表
- “天气太冷” → 将恒温器温度升高 2°F（约 1.1°C）
- “启动我的电脑” → 发送远程唤醒（WOL）指令
- “晚安” → 进入睡眠模式
- “我出门了” → 关闭所有灯光并切换至节能模式
- “我回家了” → 根据当前时间自动触发相应场景

## 使用说明：

1. 阅读 `data/home-config.json` 以了解设备映射和场景设置
2. 通过一条简短的消息确认要执行的操作
3. 如果设备出现故障，请报告具体设备名称并建议解决方法
4. 未经确认切勿直接执行“关闭所有设备”的指令
5. 如果无法连接 Home Assistant，请报告问题并建议检查网络连接
6. 设备的实体 ID 必须由用户自行配置；如果缺少该信息，请提示用户进行设置