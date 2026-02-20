---
name: ulanzi-tc001
description: 通过本地HTTP协议控制Ulanzi TC001（Pixel Clock设备）。可以执行以下操作：列出tc1/tc001相关的命令、读取设备状态、启用/禁用各种功能（如时间显示、日期显示、YouTube视频播放、矩阵显示屏等），以及调整设备设置（亮度、夜间模式、时区、切换速度、滚动速度等）。所有以“tc1”或“tc001”开头的命令均可被执行。
---
# Ulanzi TC001

您可以通过其本地HTTP端点来控制Ulanzi TC001的像素时钟（无需使用浏览器）。

## 快速入门

1) 在`config.json`中设置设备IP地址（推荐方式）：
```json
{ "host": "192.168.1.32" }
```

（如果配置文件中未设置IP地址，系统会使用环境变量`TC001_HOST`作为默认值。）

2) 使用辅助脚本进行操作：
```bash
python3 scripts/tc001.py status
python3 scripts/tc001.py gadgets list
python3 scripts/tc001.py gadget on youtube
python3 scripts/tc001.py brightness manual 80
python3 scripts/tc001.py nightmode on
python3 scripts/tc001.py timezone GMT-3
```

## 支持的命令（通过脚本执行）

- `status` → 显示系统设置及各个小工具的开关状态（以JSON格式）
- `gadgets list` | `gadgets on` | `gadgets off`  
- `gadget on` | `gadget off <名称>`  
- `brightness auto` | `brightness manual <0-100>`  
- `nightmode on` | `nightmode off` | `nightmode start HH:MM` | `nightmode end HH:MM`  
- `timezone GMT-3` | `timezone AUTO` （具体设置请参考脚本说明）  
- `switch <10|15|20|25|30|35|40|45|50|55|60` | `switch no`  
- `scroll <0-10>`  

### 完整系统配置（sys）

`sys <字段> <值>`：
- `language`：`english` | `chinese`  
- `autobrightness`：`auto` | `manual`  
- `brightness`：`0-100`  
- `nightbrightness`：`0-100`  
- `switchspeed`：`no` | `10` | `15` | `20` | `25` | `30` | `35` | `40` | `45` | `50` | `55` | `60`  
- `scrollspeed`：`0-10`  
- `timezone`：`GMT-3` 或 `AUTO`  
- `timeformat`：`HH:mm` | `HH:mm:ss`  
- `dateformat`：`DD/MM` | `MM/DD`  
- `showweek`：`show` | `hide`  
- `firstday`：`sunday` | `monday`  
- `nightmode`：`on` | `off`  
- `nightstart`：`HH:MM`  
- `nightend`：`HH:MM`  

### 完整应用配置（app）

`app <字段> <值>`：
- `citycode`  
- `bilibili_uid` / `bilibili_animation` / `bilibili_color` / `bilibili_format`  
- `weibo_uid` / `weibo_animation` / `weibo_color` / `weibo_format`  
- `youtube_uid` / `youtube_apikey` / `youtube_animation` / `youtube_color` / `youtube_format`  
- `douyin_uid` / `douyin_animation` / `douyin_color` / `douyin_format`  
- `awtrix_server` / `awtrix_port`  
- `showlocalip`：`on` | `off`  

支持的操作类型：`swipe` | `scroll`  
可选的颜色：`default` | `red` | `orange` | `yellow` | `green` | `cyan` | `blue` | `purple`  
可选的显示格式：`none` | `format`  

## 小工具列表（名称）

- `time` | `date` | `weather` | `bilibili` | `weibo` | `youtube` | `douyin` | `scoreboard` | `chronograph` | `tomato` | `battery` | `matrix` | `awtrix` | `localip`  

## 注意事项

- 使用`POST /`和`POST /app_switch`方法发送请求，并需要携带相应的表单数据。详情请参阅`references/tc001-api.md`。  
- 如果使用了YouTube API密钥，请确保其保密性。