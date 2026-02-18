---
name: gotchi-finder
description: 从 Base 主网中根据 ID 获取 Aavegotchi，并显示其完整属性的图像（包括链上的 SVG 图像）。该图像会被转换为 PNG 格式，并同时展示 Aavegotchi 的所有相关信息。
homepage: https://github.com/aavegotchi/gotchi-finder-skill
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
      env:
        - BASE_MAINNET_RPC
---
# Gotchi Finder 技能

通过 ID 查找并显示任何 Aavegotchi，包括其完整属性和图片。

## 特点

- ✅ **即时 ID 查询** - 可以通过 ID 号获取任何 Gotchi
- ✅ 从 Base 主网获取任何 Gotchi
- ✅ 显示完整属性（BRS、亲缘关系、等级、经验值、栖息地、名称、所有者）
- ✅ 生成 PNG 图片（标准尺寸 512x512 或高分辨率 1024x1024）
- ✅ 导出为 SVG（可缩放矢量图形）
- ✅ 提供多种格式选项（PNG、高分辨率图片、SVG 或全部格式）
- ✅ 支持所有 Gotchi 状态（Portal、Gotchi 等）
- ✅ 自动转换并发送图片

## 使用方法

### 推荐的交互式工作流程

**步骤 1：预览 Gotchi**
```bash
bash scripts/find-gotchi.sh 9638
```

**显示顺序：**
1. 🖼️ Gotchi 图片（512x512 标准 PNG 预览） - **首先显示**
2. 📊 完整的属性信息 - **图片下方显示**
3. 📥 下载选项菜单 - **在页面底部**

**步骤 2：用户选择格式**
用户可以选择所需的格式：
```bash
# Hi-res PNG
bash scripts/find-gotchi.sh 9638 --format hires

# SVG vector
bash scripts/find-gotchi.sh 9638 --format svg

# All formats
bash scripts/find-gotchi.sh 9638 --format all
```

### 格式选项

- `preview` - 显示属性 + 标准 PNG（默认）
- `png` - 标准 PNG（512x512）
- `hires` - 高分辨率 PNG（1024x1024）
- `svg` - 仅 SVG（不转换成 PNG）
- `all` - 同时显示所有格式

### 示例

**先预览（对话式流程）：**
```bash
# Show gotchi info + preview image
bash scripts/find-gotchi.sh 9638

# Then user picks format
bash scripts/find-gotchi.sh 9638 --format hires
```

**直接下载（跳过预览）：**
```bash
# Get hi-res immediately
bash scripts/find-gotchi.sh 9638 --format hires

# Get all formats at once
bash scripts/find-gotchi.sh 9638 --format all
```

**输出文件：**
- `gotchi-{ID}.json` - 完整的元数据（始终生成）
- `gotchi-{ID}.svg` - 矢量图片（始终生成）
- `gotchi-{ID}.png` - 标准 PNG（预览/全部格式）
- `gotchi-{ID}-hires.png` - 高分辨率 PNG（高分辨率/全部格式）

## 显示格式

### 活跃的 Gotchis（状态 3）

**单条消息，包含图片和标题：**

图片：512×512 的 Gotchi PNG 图片

标题：
```
👻 Gotchi #{ID} "{Name}"

📊 Stats:
⭐ BRS: {brs} (Modified: {modifiedBrs})
💜 Kinship: {kinship}
🎯 Level: {level}
✨ XP: {xp}
🏰 Haunt: {haunt}
🔒 Locked: {Yes/No}

🎭 Traits:
• Energy: {value}
• Aggression: {value}
• Spookiness: {value}
• Brain Size: {value}
• Eye Shape: {value}
• Eye Color: {value}

📥 Download options:
• Standard PNG (512×512)
• Hi-res PNG (1024×1024)
• SVG (vector)
• All formats
```

### Portal（状态 0-1）
**单条消息：** Portal 图片，标题中包含状态信息

## 技术细节

**区块链：**
- 链路：Base 主网（8453）
- RPC：https://mainnet.base.org
- Diamond：0xA99c4B08201F2913Db8D28e71d020c4298F29dBF

**依赖项：**
- 使用 ethers v6 的 Node.js
- Sharp 库用于图片转换

**状态代码：**
- 0：未打开的 Portal
- 1：打开的 Portal
- 2：Gotchi（在 Base 主网上较为罕见）
- 3：标准的 Gotchi（在 Base 主网上常见）

## 文件结构

- `scripts/find-gotchi.sh` - 主入口脚本
- `scripts/fetch-gotchi.js` - 从区块链获取数据
- `scripts/svg-to-png.js` - 将 SVG 转换为 PNG
- `package.json` - Node.js 依赖项列表

## 安装方法
```bash
cd /home/ubuntu/.openclaw/workspace/skills/gotchi-finder
npm install
```

## 使用示例

**查找你的 Gotchi：**
```bash
bash scripts/find-gotchi.sh 9638
```

**查找任意 Gotchi：**
```bash
bash scripts/find-gotchi.sh 5000
```

**查找多个 Gotchis：**
```bash
for id in 9638 21785 10052; do
  bash scripts/find-gotchi.sh $id
done
```

---

由 AAI 使用 💜 构建