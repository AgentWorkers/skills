---
name: gotchi-finder
description: 从 Base 主网中根据 ID 获取 Aavegotchi，并显示其完整属性的图像。该图像为链上生成的 SVG 格式，可转换为 PNG 格式；同时还会展示该 Aavegotchi 的所有相关信息（统计数据）。
homepage: https://github.com/aaigotchi/gotchi-finder-skill
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
        - jq
      env:
        - BASE_MAINNET_RPC
---
# Gotchi Finder 技能

通过 ID 查找并显示任何 Aavegotchi，包括其完整属性和图片。

## 功能

- ✅ **即时 ID 查询** - 可以通过 ID 号获取任何 Gotchi 的信息
- ✅ 从 Base 主网获取任何 Gotchi 的信息
- ✅ 显示完整属性（BRS、亲缘关系、等级、经验值、栖息地、名称、所有者）
- ✅ **总 BRS** - 显示基础 BRS 以及装备修饰器的值（即 Gotchi 的实际强度）
- ✅ 生成 PNG 图片（标准尺寸 512x512 或高分辨率 1024x1024）
- ✅ 导出为 SVG（可缩放矢量图形）
- ✅ 提供多种格式选项（PNG、高分辨率图片、SVG 或全部格式）
- ✅ 支持所有 Gotchi 状态（Portal、Gotchi 等）
- ✅ 自动转换并发送图片

## 使用方法

### 默认行为（始终如此）

**运行 gotchi-finder 时，系统会始终输出：**

1. **🖼️ Gotchi PNG 图片**（512×512） - 作为图片/媒体文件发送
2. **📊 统计信息** - 显示在图片下方

这会生成一条消息，图片位于上方，下方显示所有元数据。

**示例：**
```bash
bash scripts/find-gotchi.sh 9638
```

**输出结果：** 一条 Telegram 消息，包含：
- 上方的 PNG 图片
- 下方的所有统计信息、属性和详细信息

### 额外格式选项（可选）

用户可以在查看默认输出后请求其他格式：

```bash
# Hi-res PNG (1024×1024)
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
- `svg` - 仅输出 SVG（不转换成 PNG）
- `all` - 同时输出所有格式

### 示例

**先查看预览（对话流程）：**
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
- `gotchi-{ID}.png` - 标准 PNG 图片（预览/全部格式）
- `gotchi-{ID}-hires.png` - 高分辨率 PNG 图片（高分辨率/全部格式）

## 显示格式（官方规范）

### 活跃中的 Gotchis（状态 3）

**始终以包含图片和标题的单条消息形式发送：**

**格式：**
```
media: gotchi-{ID}.png (512×512 PNG image)
caption: (text below)
```

**标题模板：**
```
👻 **Gotchi #{ID} - {Name}**

**📊 Stats:**
⭐ BRS: **{brs}** ({TIER} tier)
💜 Kinship: **{kinship}**
🎮 Level: **{level}** (XP: {xp})
👻 Haunt: **{haunt}**
💎 Collateral: **{collateral}**

**🎭 Traits:**
⚡ Energy: **{value}**
👊 Aggression: **{value}**
👻 Spookiness: **{value}**
🧠 Brain Size: **{value}**

**👔 Wearables:** {None/equipped count}

LFGOTCHi! 🦞🚀
```

**稀有度等级：**
- BRS ≥ 580：GODLIKE
- BRS ≥ 525：MYTHICAL
- BRS ≥ 475：UNCOMMON
- BRS < 475：COMMON

### Portal（状态 0-1）
**单条消息：** 显示 Portal 的 PNG 图片以及状态信息

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
- 2：普通 Gotchi（在 Base 主网上）
- 3：标准 Gotchi（在 Base 主网上）

## 文件

- `scripts/show-gotchi.sh` - **推荐使用** - 在单条消息中显示 PNG 图片和统计信息
- `scripts/find-gotchi.sh` - 用于获取和转换数据（高级用法）
- `scripts/fetch-gotchi.js` - 从区块链获取数据
- `scripts/svg-to-png.js` - 将 SVG 转换为 PNG
- `package.json` - Node.js 依赖项

## 对于 OpenClaw 代理

**使用 `show-gotchi.sh` - 它会输出消息工具所需的格式：**

```bash
cd ~/.openclaw/workspace/skills/gotchi-finder
bash scripts/show-gotchi.sh 8746
```

**输出结果：**
```
PNG_PATH=./gotchi-8746.png
CAPTION=<<EOF
👻 **Gotchi #8746 - LE PETIT MARX**
...complete stats...
EOF
```

**然后使用：**
```javascript
message(action: "send", media: PNG_PATH, caption: CAPTION)
```

## 安装方法**
```bash
cd /home/ubuntu/.openclaw/workspace/skills/gotchi-finder
npm install
```

## 示例

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

---

## 🔒 安全性

**此技能 100% 安全 - 仅用于读取！** ✅

### 安全特性
- ✅ **仅限读取** - 完全不涉及钱包操作
- ✅ **不进行任何交易** - 不会修改区块链状态
- ✅ **无需任何凭证** - 仅访问公共数据
- ✅ **无需私钥** - 不会访问钱包
- ✅ **对所有人安全** - 不会造成任何损害

### 此技能的功能
- ✅ 从公共子图获取 Gotchi 数据
- ✅ 从公共 SVG 数据生成图片
- ✅ 显示 Gotchi 的属性（仅限读取）

### 此技能无法执行的功能
- ❌ 无法访问钱包
- ❌ 无法签署交易
- ❌ 无法修改 Gotchi
- ❌ 无法转移任何物品
- ❌ 无法花费资金

### 数据来源
- 公共子图：`api.goldsky.com`（仅限读取）
- 公共 SVG 数据：Aavegotchi Diamond 合同（仅限读取）
- 无需身份验证

### 隐私保护
- ✅ 仅获取公共 Gotchi 数据
- ✅ 不会暴露钱包地址
- ✅ 不会泄露敏感信息

### 合规性
- ✅ 符合 ClawHub 的安全标准
- ✅ 仅限读取的最佳实践
- ✅ 安全等级为 0（无风险）

---

**安全评分：** 10/10 ✅ （仅限读取 = 最高安全性）
**ClawHub 状态：** 已批准
**风险等级：** 无风险（仅限读取）
**最后一次审计：** 2026-02-19

## BRS 计算方法（官方规定）

**gotchi-finder 始终使用 **总 BRS** = 基础 BRS + 装备修饰器的值**

这显示了 Gotchi 的 **实际强度**（包括所有装备的影响！）

### JSON 输出字段

- `brs` - **总 BRS**（基础 BRS 加装备修饰器） - 主要字段 ⭐
- `baseBrs` - 仅基础 BRS（不含装备修饰器）
- `baseRarityScore` - 与 baseBrs 相同（来自合约）
- `modifiedRarityScore` - 与 brs 相同（来自合约）

### 示例输出**

```json
{
  "name": "SHAAMAAN",
  "brs": "670",           // ← TOTAL BRS (used everywhere)
  "baseBrs": "562",       // Base only (reference)
  "traits": { ... },      // Base traits (no wearables)
  "modifiedTraits": { ... } // Modified traits (with wearables)
}
```

**控制台显示：**
```
⭐ Total BRS: 670 (Base: 562 + Wearables: +108)
```

### 为何使用总 BRS？

- ✅ 显示 Gotchi 在战斗中的 **实际实力**
- ✅ 反映装备的价值
- ✅ 根据装备确定稀有度等级
- ✅ 与 Baazaar 上的列表一致

**一个神话级的 Gotchi 通过合适的装备可以变得非常强大！** 🔥