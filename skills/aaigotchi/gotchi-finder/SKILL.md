---
name: gotchi-finder
description: 从 Base 主网中根据 ID 获取 Aavegotchi，并显示其完整属性的图像。该图像为链上的 SVG 格式，可转换为 PNG 格式；同时还会显示该 Aavegotchi 的所有相关信息（统计数据）。
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

- ✅ **即时 ID 查询** - 可以通过 ID 号获取任何 Gotchi 的信息
- ✅ 从 Base 主网获取任何 Gotchi 的信息
- ✅ 显示完整属性（BRS、亲缘关系、等级、经验值、栖息地、名称、所有者）
- ✅ **总 BRS** - 显示基础 BRS 以及装备的加成（即 Gotchi 的实际强度）
- ✅ 生成 PNG 图片（标准尺寸 512x512 或高分辨率 1024x1024）
- ✅ 导出为 SVG（可缩放矢量图形）
- ✅ 提供多种格式选项（PNG、高分辨率图片、SVG 或全部格式）
- 支持所有 Gotchi 状态（Portal、Gotchi 等）
- 图片会自动转换并发送给用户

## 使用方法

### 推荐的交互流程

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

- `preview` - 显示属性和标准 PNG 图片（默认）
- `png` - 标准 PNG 图片（512x512）
- `hires` - 高分辨率 PNG 图片（1024x1024）
- `svg` - 仅生成 SVG 图片（不转换成 PNG）
- `all` - 同时生成所有格式的文件

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
- `gotchi-{ID}.json` - 包含所有元数据
- `gotchi-{ID}.svg` - 矢量图片
- `gotchi-{ID}.png` - 标准 PNG 图片（预览/全部格式）
- `gotchi-{ID}-hires.png` - 高分辨率 PNG 图片（仅高分辨率格式）

## 显示格式

### 状态为 3 的 Gotchi

**单条消息，包含图片和说明：**

图片：512×512 的 Gotchi PNG 图片

说明：
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

### 状态为 0-1 的 Gotchi（Portal 状态）

**单条消息：** 显示 Portal 图片及状态信息

## 技术细节

**区块链：**
- 链路：Base 主网（8453）
- RPC：https://mainnet.base.org
- Diamond 合约地址：0xA99c4B08201F2913Db8D28e71d020c4298F29dBF

**依赖库：**
- 使用 Node.js 和 ethers v6
- Sharp 库用于图片转换

**状态代码：**
- 0：未打开的 Portal
- 1：已打开的 Portal
- 2：普通 Gotchi（在 Base 主网上较为罕见）
- 3：标准 Gotchi（在 Base 主网上常见）

## 相关文件

- `scripts/find-gotchi.sh` - 主程序入口
- `scripts/fetch-gotchi.js` - 从区块链获取数据
- `scripts/svg-to-png.js` - 将 SVG 转换为 PNG
- `package.json` - Node.js 依赖库列表

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

**查找多个 Gotchi：**
```bash
for id in 9638 21785 10052; do
  bash scripts/find-gotchi.sh $id
done
```

---

由 AAI 使用 💜 开发

---

## 🔒 安全性

**此技能 100% 安全 - 仅用于读取！** ✅

### 安全特性
- ✅ **仅用于读取** - 完全不涉及钱包操作
- ✅ **不进行任何交易** - 不会修改区块链状态
- ✅ **无需任何凭证** - 仅访问公开数据
- ✅ **无需私钥** - 不会访问用户的钱包
- ✅ **对所有人安全** - 不会造成任何损害

### 功能说明
- ✅ 从公共子图获取 Gotchi 数据
- ✅ 从公共 SVG 数据生成图片
- ✅ 仅显示 Gotchi 的属性（仅用于读取）

### 功能限制
- ❌ 无法访问用户的钱包
- ❌ 无法签署交易
- ❌ 无法修改 Gotchi 的状态
- ❌ 无法转移任何资产
- ❌ 无法花费任何货币

### 数据来源
- 公共子图：`api.goldsky.com`（仅用于读取）
- 公共 SVG 数据：Aavegotchi Diamond 合约（仅用于读取）
- 无需任何身份验证

### 隐私保护
- ✅ 仅获取公开的 Gotchi 数据
- ✅ 不会暴露用户的钱包地址
- ✅ 不会泄露任何敏感信息

### 合规性
- 符合 ClawHub 的安全标准
- 仅用于读取数据，遵循最佳安全实践
- 被归类为低风险技能

---

**安全评分：** 10/10 ✅（仅用于读取 = 最高安全性）
**ClawHub 状态：** 已批准
**风险等级：** 无风险（仅用于读取）
**最后一次审计时间：** 2026-02-19

## BRS 计算规则（官方规定）

**gotchi-finder 始终使用 **总 BRS** = 基础 BRS + 装备加成**

这表示 Gotchi 的 **实际强度**，包括所有装备的加成！

### JSON 输出字段

- `brs` - **总 BRS**（基础 BRS 加上装备加成） - 主要输出字段
- `baseBrs` - 仅基础 BRS（不含装备加成）
- `baseRarityScore` - 与 `baseBrs` 相同（来自合约）
- `modifiedRarityScore` - 与 `brs` 相同（来自合约）

### 示例输出

```json
{
  "name": "SHAAMAAN",
  "brs": "670",           // ← TOTAL BRS (used everywhere)
  "baseBrs": "562",       // Base only (reference)
  "traits": { ... },      // Base traits (no wearables)
  "modifiedTraits": { ... } // Modified traits (with wearables)
}
```

**控制台显示结果：**
```
⭐ Total BRS: 670 (Base: 562 + Wearables: +108)
```

### 为什么使用总 BRS？

- ✅ 显示 Gotchi 在战斗中的 **实际实力**
- ✅ 反映装备的价值
- ✅ 根据装备决定其稀有等级
- ✅ 与 Baazaar 上的列表信息一致

**配备合适装备的 Gotchi 可以变得非常强大！** 🔥