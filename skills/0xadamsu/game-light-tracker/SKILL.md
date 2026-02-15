---
name: game-light-tracker
description: 实时跟踪NFL（美国国家橄榄球联盟）、NBA（美国国家篮球联盟）、NHL（美国国家冰球联盟）或MLB（美国职业棒球大联盟）的比赛，并根据领先球队的情况自动调整Hue智能灯的颜色。适用于用户希望将智能灯光与实时体育比分同步，以实现视觉化的比赛追踪效果。支持NFL、NBA、NHL和MLB的比赛，且支持自定义球队颜色。
---

# 游戏灯光追踪器

该工具可自动将您的 Hue 灯具与实时体育赛事比分同步。当比分发生变化时，灯光颜色会相应地变为领先球队的颜色。

## 快速入门

**基本用法：**
```
Track the [Team A] vs [Team B] game and change my [light name] to [color1] when [Team A] leads and [color2] when [Team B] leads
```

**示例：**
- “追踪公羊队对阵海鹰队的比赛：当公羊队领先时，将背景灯设置为蓝色；当海鹰队领先时，设置为绿色”（NFL）
- “监控湖人队对阵凯尔特人队的比赛：湖人队领先时灯光为紫色，凯尔特人队领先时为绿色”（NBA）
- “观看游骑兵队对阵魔鬼队的比赛：游骑兵队领先时灯光为蓝色，魔鬼队领先时为红色”（NHL）
- “追踪洋基队对阵红袜队的比赛：将客厅灯光设置为洋基队领先时为蓝色，红袜队领先时为红色”（MLB）

## 工作原理

1. 每 20 秒从 ESPN API 获取实时比分数据
2. 检测比分变化
3. 通过 Home Assistant 更改指定的 Hue 灯具颜色
4. 配备自动重启功能，以防程序超时
5. 可选：在比分平局时显示第三种颜色

## 设置要求

- 安装并配置了 Home Assistant 及 Hue 灯具
- 拥有 Home Assistant API 令牌（存储在 `.homeassistant-config.json` 文件中）
- 知道 Home Assistant 中对应的灯光实体 ID

## 脚本

### `game-tracker.ps1`
主要监控脚本，用于追踪特定比赛并更新灯光颜色。

**使用方法：**
```powershell
.\game-tracker.ps1 -Sport "nfl" -Team1 "LAR" -Team2 "SEA" -Light "light.backlight" -Color1 "0,0,255" -Color2 "0,100,0" [-TiedColor "255,0,0"]
```

**参数：**
- `-Sport`："nfl"、"nba"、"nhl" 或 "mlb"（比赛类型）
- `-Team1`：第一支球队的缩写
- `-Team2`：第二支球队的缩写
- `-Light`：Home Assistant 中的灯光实体 ID
- `-Color1`：第一支球队的 RGB 颜色（用逗号分隔，例如 "0,0,255" 表示蓝色）
- `-Color2`：第二支球队的 RGB 颜色（用逗号分隔，例如 "0,100,0" 表示深绿色）
- `-TiedColor`：（可选）比赛平局时的颜色

### `keeper.ps1`
自动重启脚本，防止程序因超时而崩溃。

**使用方法：**
```powershell
.\keeper.ps1 -TrackerScript "game-tracker.ps1" -RestartInterval 25
```

**参数：**
- `-TrackerScript`：`game-tracker.ps1` 脚本的路径
- `-RestartInterval`：自动重启的间隔时间（默认为 25 分钟）

## 常见球队缩写

**NFL：**
- 公羊队（Rams）：LAR
- 海鹰队（Seahawks）：SEA
- 首席队（Chiefs）：KC
- 比尔队（Bills）：BUF
- 爱国者队（Patriots）：NE
- 牛仔队（Cowboys）：DAL
- 老鹰队（Eagles）：PHI
- 49 人队（49ers）：SF
- 包装工队（Packers）：GB
- 熊队（Bears）：CHI
- [完整列表：https://www.espn.com/nfl/teams]

**NBA：**
- 湖人队（Lakers）：LAL
- 凯尔特人队（Celtics）：BOS
- 战士队（Warriors）：GS
- 尼克斯队（Knicks）：NY
- 公牛队（Bulls）：CHI
- 热队（Heat）：MIA
- 网队（Nets）：BKN
- 76 人队（76ers）：PHI
- 鹰队（Bucks）：MIL
- 小牛队（Mavericks）：DAL
- 猛龙队（Nuggets）：DEN
- 太阳队（Suns）：PHX
- 快船队（Clippers）：LAC
- 雷aptors：TOR
- [完整列表：https://www.espn.com/nba/teams]

**NHL：**
- 游骑兵队（Rangers）：NYR
- 魔鬼队（Devils）：NJ
- 海盗队（Bruins）：BOS
- 枫叶队（Maple Leafs）：TOR
- 加人队（Canadiens）：MTL
- 鹰派队（Penguins）：PIT
- 首都队（Capitals）：WSH
- 飞人队（Flyers）：PHI
- 闪电队（Lightning）：TB
- 黑豹队（Blackhawks）：CHI
- 雪崩队（Avalanche）：COL
- 金骑士队（Golden Knights）：VGK
- [完整列表：https://www.espn.com/nhl/teams]

**MLB：**
- 洋基队（Yankees）：NYY
- 红袜队（Red Sox）：BOS
- 道奇队（Dodgers）：LAD
- 巨人队（Giants）：SF
- 大都会队（Mets）：NYM
- 小熊队（Cubs）：CHC
- 红雀队（Cardinals）：STL
- 太空人队（Astros）：HOU
- 鹰队（Braves）：ATL
- 费城费城人队（Phillies）：PHI
- [完整列表：https://www.espn.com/mlb/teams]

## 常见 RGB 颜色

- **蓝色**：0,0,255
- **红色**：255,0,0
- **绿色**：0,255,0
- **深绿色**：0,100,0
- **橙色**：255,165,0
- **紫色**：128,0,128
- **黄色**：255,255,0
- **白色**：255,255,255

## 工作流程

当用户请求开始游戏追踪时：

1. **确定比赛类型和球队**：
   - 选择比赛类型（NFL/NBA/NHL/MLB）
   - 从用户处获取球队缩写或从官方列表中查询

2. **获取灯光和颜色设置**：
   - 询问用户所需的灯光实体 ID 或从 Home Assistant 配置中读取
   - 获取每支球队的 RGB 颜色
   - 可选：询问用户是否需要设置平局时的颜色

3. **加载 Home Assistant 配置**：
   ```powershell
   $config = Get-Content ".homeassistant-config.json" | ConvertFrom-Json
   $token = $config.token
   $url = $config.url
   ```

4. **启动游戏追踪器**：
   ```powershell
   .\scripts\game-tracker.ps1 -Sport "nfl" -Team1 "LAR" -Team2 "SEA" -Light "light.backlight" -Color1 "0,0,255" -Color2 "0,100,0" -TiedColor "255,0,0"
   ```

5. **启动自动重启脚本**：
   ```powershell
   Start-Process powershell -ArgumentList "-File keeper.ps1 -TrackerScript 'game-tracker.ps1'" -WindowStyle Hidden
   ```

6. **通知用户**：
   - 告知用户追踪功能已启动
   - 显示当前比分（如有的话）
   - 解释颜色方案
   - 提供停止追踪的方法

## 停止追踪

要停止追踪功能，请执行以下操作：
```powershell
Get-Process powershell | Where-Object { $_.CommandLine -like "*game-tracker.ps1*" -or $_.CommandLine -like "*keeper.ps1*" } | Stop-Process -Force
```

## 常见问题解决方法

**灯光颜色未变化**：
- 确认 Home Assistant API 令牌有效
- 检查灯光实体 ID 是否正确
- 确保可以通过配置的 URL 访问 Home Assistant

**脚本崩溃**：
- 自动重启脚本应能解决问题
- 检查 ESPN API 是否可用
- 确认球队缩写是否正确

**球队颜色显示错误**：
- 重新核对 RGB 值（范围为 0-255，用逗号分隔）
- 确保颜色分配给正确的球队