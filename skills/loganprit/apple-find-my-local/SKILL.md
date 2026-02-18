---
name: find-my
description: 通过“Peekaboo”功能控制Apple的“Find My”应用程序，以定位人员、设备以及AirTags（无线标签）。当需要寻找钥匙、钱包、AirTags，或者定位家人和朋友的位置时，或者需要向丢失的物品发送声音提示，或者检查设备的位置时，都可以使用该功能。该功能直接通过原生应用程序进行控制，无需使用任何第三方API或共享凭证。
---
# 使用“Find My”应用

通过“Peekaboo”来控制原生的“Find My”应用程序，无需使用任何不可靠的API或共享凭证。

**脚本执行路径：** `cd {skillDir}`

## 已知限制

1. 在“Peekaboo”中执行`--app "Find My"`时可能会出现卡顿现象——请改用`--window-id`参数。
2. 侧边栏中的项目名称无法通过辅助功能API获取。
3. 项目只能通过位置（如第1个、第2个等）来选择，无法通过名称选择。
4. 仅支持macOS系统，需要“Peekaboo”和“OpenClaw.app”作为桥梁工具。
5. 在脚本运行期间，用户无法与Mac进行交互（因为鼠标或点击操作会与脚本产生冲突）。

## 快速参考

| 脚本 | 功能 |
|--------|---------|
| `fm-window.sh` | 获取窗口ID和边界信息（以JSON格式） |
| `fm-screenshot.sh [路径]` | 截取“Find My”窗口的截图 |
| `fm-tab.sh <标签页>` | 切换标签页（“人员”、“设备”、“物品”） |
| `fm-list.sh [标签页]` | 截取窗口截图并显示侧边栏项目位置 |
| `fm-select-item.sh <位置> [标签页>` | 根据位置（如第1个、第2个等）选择项目 |
| `fm-locate.sh <位置> [标签页>` | 选择项目并截取其位置截图 |
| `fm-info.sh [路径]` | 打开信息面板并显示项目详情 |
| `fm-play-sound.sh <位置>` | 尝试对选中的项目播放声音 |
| `fm-click.sh <x> <y>` | 在窗口的相对坐标位置进行点击 |

## 工作流程示例

### 列出可用项目

```bash
./scripts/fm-list.sh items
# Screenshots the Items tab - view image to see your AirTags/items
```

### 查找钥匙（如果钥匙是列表中的第2个项目）

```bash
./scripts/fm-locate.sh 2 items
# Shows location on map, outputs screenshot path
```

### 对钥匙播放声音

```bash
./scripts/fm-play-sound.sh 2
# Selects 2nd item, attempts to click Play Sound
# May require manual click if button not found
```

### 检查家庭成员的位置

```bash
./scripts/fm-list.sh people
# View screenshot to see who's listed

./scripts/fm-locate.sh 1 people
# Shows first person's location
```

## 用户界面布局参考

### 标签栏（距离窗口顶部约68像素）
| 标签页 | X坐标 |
|-----|------------|
| 人员 | ~63 |
| 设备 | ~154 |
| 物品 | ~243 |

### 侧边栏项目（距离窗口左侧约150像素）
| 位置 | Y坐标 |
|----------|--------------|
| 第1个项目 | ~120 |
| 第2个项目 | ~174 |
| 第3个项目 | ~228 |
| 第4个项目 | ~282 |
| （项目间距） | 每个项目之间相隔54像素 |

## 手动坐标点击方法

当自动化操作失败时，可以手动计算坐标：

```bash
# Get window position
./scripts/fm-window.sh
# Output: {"x": 824, "y": 62, "width": 1024, "height": 768, "window_id": 2248}

# Click at relative position within window
./scripts/fm-click.sh 150 174   # 2nd sidebar item
./scripts/fm-click.sh 243 68    # Items tab
```

## 信息面板操作

选择项目后，点击地图弹窗上的 ⓘ 按钮以打开信息面板：

| 操作 | 功能 |
|--------|-------------|
| **播放声音** | 使AirTag发出提示音（仅适用于可播放声音的项目） |
| **路线指引** | 打开地图并显示导航路线 |
| **分享位置** | 与其他用户分享当前位置 |
| **丢失模式** | 启用位置信息共享功能 |
| **通知设置** | 配置通知方式 |

## 故障排除

**“Find My”窗口未找到**
- 确保“Find My.app”已打开。
- 检查“OpenClaw.app”是否正在运行（它提供了与“Peekaboo”的交互接口）。

**点击操作无效**
- 窗口可能已经移动——重新运行`fm-window.sh`以获取最新的窗口坐标。
- 点击前请确保“Find My”应用程序处于最前面。

**找不到“播放声音”按钮**
- 手动打开信息面板（点击地图弹窗上的 ⓘ 按钮）。
- 然后重新运行`fm-play-sound.sh`脚本。

## 未来改进计划

当“Peekaboo”修复`--app "Find My"`的问题后：
- 将实现无需计算坐标的直接元素定位功能。
- 侧边栏项目的辅助功能信息将更加可靠。
- 自动化流程将更加简洁易用。