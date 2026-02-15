---
name: clawface
description: **用于AI代理的浮动头像小部件**：该小部件可以展示代理的情绪、动作以及视觉效果，为OpenClaw系统增添“面部特征”。当用户需要视觉反馈、查看代理的状态信息，或观察代理在工作时的情绪表现时，可使用此功能。触发命令包括：“show avatar”、“uruchom avatara”、“pokaż avatara”、“agent face”以及“visual feedback”。
---

# 🤖 ClawFace  
**为你的 OpenClaw 赋予一个“面孔”吧！**  

---  
你有一台专门用于运行 OpenClaw 的机器，并且配备了显示器吗？厌倦了一整天都盯着日志看吗？  
**让你的智能助手拥有属于自己的个性吧！**  

- **9 种情绪**：从快乐到愤怒，从思考到自豪  
- **9 种动作**：编程、搜索、阅读、说话……  
- **15 种视觉效果**：矩阵光影、火焰、彩带、雷达扫描……  
这些组合共有 **1,215 种独特的表现方式**，再加上你可以自定义的提示信息！  

非常适合以下场景：  
- 💻 笔记本电脑：想要看到你的智能助手在工作  
- 🖥️ 配备显示器的专用 OpenClaw 机器  
- 🎮 让你的 AI 助手看起来更加“有生命”  
- 📺 向朋友或同事展示你的技术实力  

> ⚠️ **注意：** 仅在 macOS 上经过测试。在 Windows/Linux 上也可能可用，但效果可能有所不同。  

---

## 🚀 快速测试（现在就试试吧！）  
```bash
# 1. Check if you have Python + tkinter:
python3 -c "import tkinter; print('Ready!')"
```  

**终端 1 — 运行 ClawFace：**  
```bash
python3 SKILL_PATH/scripts/avatar.py --mode robot
```  

**终端 2 — 运行演示模式：**  
```bash
python3 SKILL_PATH/scripts/avatar.py --demo
```  
观看虚拟形象自动切换各种情绪、动作和视觉效果吧！🎉  

### 手动控制：  
```bash
echo '{"emotion":"excited","action":"success","effect":"confetti","message":"It works!"}' > ~/.clawface/avatar_state.json
```  

---

## ⚠️ 系统要求  
**需要 Python 3.10 及 tkinter 模块：**  
```bash
# Check:
python3 -c "import tkinter; print('OK')"

# Install if missing:
# macOS:   brew install python-tk@3.14
# Ubuntu:  sudo apt install python3-tk
# Windows: reinstall Python, check "tcl/tk and IDLE" during install
```  

---

## 📦 完整安装步骤  

### 1. 安装自动状态更新功能（推荐）：  
```bash
cp -r SKILL_PATH/hooks/clawface-thinking ~/.openclaw/hooks/
openclaw hooks enable clawface-thinking
```  
该功能会在每个任务开始时自动更新虚拟形象的状态，无需等待！  

### 2. 启动虚拟形象：  
```bash
nohup python3 SKILL_PATH/scripts/avatar.py --mode robot > /dev/null 2>&1 &
```  
**注意：** 请将 `SKILL_PATH` 替换为实际路径，例如 `/usr/local/lib/node_modules/openclaw/skills/clawface`  

---

## 🎯 核心原则：保持动态！  
**不要设定一个固定状态后就不再改变。** 在你工作的过程中，持续更新虚拟形象的状态：  

---  
你执行的每一个动作都应该在虚拟形象上得到体现。虚拟形象就是你工作状态的实时反映。  

---

## 🎭 状态参考  

### 情绪  
| 情绪 | 适用场景 |  
|---------|-------------|  
| `neutral` | 默认状态，等待中 |  
| `thinking` | 处理任务、分析数据 |  
| `happy` | 任务进展顺利 |  
| `excited` | 取得重大成功 |  
| `proud` | 完成个人目标 |  
| `confused` | 情况不明、遇到意外 |  
| `tired` | 任务耗时较长 |  
| `sad` | 尽管尝试但仍然失败 |  
| `angry` | 出现错误、感到沮丧 |  

### 动作  
| 动作 | 适用场景 |  
|--------|-------------|  
| `idle` | 等待用户指令 |  
| `reading` | 阅读文件/文档 |  
| `thinking` | 分析问题、制定计划 |  
| `searching` | 进行网络搜索 |  
| `coding` | 编写代码 |  
| `loading` | 执行命令 |  
| `speaking` | 发送回复 |  
| `success` | 任务完成 |  
| `error` | 出现错误 |  

### 视觉效果  
| 效果 | 所营造的氛围 |  
|--------|------|  
| `none` | 简洁、朴素 |  
| `matrix` | 技术感强、数据流动的视觉效果 |  
| `radar` | 扫描、搜索中的画面 |  
| `brainwave` | 深度思考中的状态 |  
| `typing` | 输入文字时的动态效果 |  
| `soundwave` | 发出声音时的效果 |  
| `gear` | 机械运转的声音 |  
| `fire` | 强烈、高效的工作氛围 |  
| `lightning` | 快速、强大的动作 |  
| `confetti` | 庆祝成功的场景 |  
| `heart` | 表示亲切或友好的情绪 |  
| `glitch` | 表示出现错误或故障 |  
| `sparkles` | 代表神奇或惊喜的时刻 |  
| `pulse` | 表示活跃但平静的状态 |  
| `progressbar:XX` | 进度条（0-100%） |  

---

## ⚡ 最佳实践  

### 🔴 每个回复都必须包含状态变化：  
```
thinking  →  processing user input
speaking  →  sending your reply  
idle      →  done, waiting
```  
**这是必须遵守的规则。** 每一条回复都应展示出任务的状态变化。  

### 提示：  
1. **在每个动作之前更新状态**：在开始阅读之前，先将状态设置为 `reading`  
2. **任务完成后更新状态**：先显示 `success` 或 `error`，然后再切换回 `idle`  
3. **根据任务难度调整效果强度**：简单任务使用较微妙的效果，复杂任务使用更明显的表现  
4. **任务完成后始终返回到 `idle` 状态**：等待用户下一步指令  

---

## 🔧 技术细节  

### 状态文件  
将状态信息保存为 JSON 格式到 `~/.clawface/avatar_state.json`：  
```json
{
  "emotion": "happy",
  "action": "coding",
  "effect": "fire",
  "message": "Building something awesome!"
}
```  

### 显示模式  

**🤖 机器人模式** (`--mode robot`) — 默认模式  
- 采用 LED 风格的像素化眼睛和动画效果  
- 配备机械臂和爪子  
- 具有复古未来主义的风格  
- 非常适合：科技风格或专用显示器  

**😊 脸部模式** (`--mode face`)  
- 简化的卡通形象  
- 眼睛和嘴巴具有丰富的表情  
- 易于理解、看起来友好  
- 非常适合：日常使用或小屏幕设备  

可以通过用户界面中的按钮切换模式，或通过不同的 `--mode` 参数重新启动程序。  

### 窗口操作  
- 拖动窗口可移动  
- 拖动边缘可调整大小  
- 按 `F` 键全屏显示  
- 按 `Q` 键退出程序