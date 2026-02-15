---
name: huckleberry
description: 通过 Huckleberry 应用程序的 API 来记录宝宝的睡眠、喂食、换尿布以及成长情况。可以使用自然语言来记录宝宝的各项活动。
homepage: https://github.com/aaronn/openclaw-huckleberry-skill
metadata:
  clawdbot:
    emoji: "👶"
    requires:
      bins: ["python3"]
      packages: ["huckleberry-api"]
    install:
      - id: pip-huckleberry
        kind: pip
        package: huckleberry-api
        label: Install huckleberry-api (pip)
---

# Huckleberry婴儿追踪器

通过Huckleberry应用程序的Firebase后端来追踪婴儿的活动（睡眠、喂食、换尿布、生长情况）。

## 设置

1. 安装API：
   ```bash
   # Install from GitHub (required for bottle feeding support until next PyPI release)
   pip install git+https://github.com/Woyken/py-huckleberry-api.git
   # or with uv:
   uv pip install git+https://github.com/Woyken/py-huckleberry-api.git
   ```

2. 配置凭据（选择一种方式）：
   - 环境变量：
     ```bash
     export HUCKLEBERRY_EMAIL="your-email@example.com"
     export HUCKLEBERRY_PASSWORD="your-password"
     export HUCKLEBERRY_TIMEZONE="America/Los_Angeles"  # optional
     ```
   - 配置文件位于`~/.config/huckleberry/credentials.json`：
     ```json
     {
       "email": "your-email@example.com",
       "password": "your-password",
       "timezone": "America/Los_Angeles"
     }
     ```

## 命令行工具（CLI）使用方法

CLI工具位于`~/clawd/skills/huckleberry/scripts/hb.py`。

```bash
# List children
python3 ~/clawd/skills/huckleberry/scripts/hb.py children

# Sleep tracking
python3 ~/clawd/skills/huckleberry/scripts/hb.py sleep-start
python3 ~/clawd/skills/huckleberry/scripts/hb.py sleep-pause
python3 ~/clawd/skills/huckleberry/scripts/hb.py sleep-resume
python3 ~/clawd/skills/huckleberry/scripts/hb.py sleep-complete
python3 ~/clawd/skills/huckleberry/scripts/hb.py sleep-cancel

# Breastfeeding
python3 ~/clawd/skills/huckleberry/scripts/hb.py feed-start --side left
python3 ~/clawd/skills/huckleberry/scripts/hb.py feed-switch
python3 ~/clawd/skills/huckleberry/scripts/hb.py feed-pause
python3 ~/clawd/skills/huckleberry/scripts/hb.py feed-resume --side right
python3 ~/clawd/skills/huckleberry/scripts/hb.py feed-complete
python3 ~/clawd/skills/huckleberry/scripts/hb.py feed-cancel

# Bottle feeding
python3 ~/clawd/skills/huckleberry/scripts/hb.py bottle 120 --type "Formula" --units ml

# Diaper
python3 ~/clawd/skills/huckleberry/scripts/hb.py diaper both --pee-amount medium --poo-amount big --color yellow --consistency loose

# Growth
python3 ~/clawd/skills/huckleberry/scripts/hb.py growth --weight 5.2 --height 55 --head 38 --units metric
python3 ~/clawd/skills/huckleberry/scripts/hb.py growth-get

# History
python3 ~/clawd/skills/huckleberry/scripts/hb.py history --date 2026-01-27
python3 ~/clawd/skills/huckleberry/scripts/hb.py history --days 7 --type sleep --type feed
python3 ~/clawd/skills/huckleberry/scripts/hb.py history --json
```

## 完整参数参考

### 睡眠相关命令

| 命令 | 参数 | 描述 |
|---------|------------|-------------|
| `sleep-start` | — | 开始新的睡眠会话（计时器开始） |
| `sleep-pause` | — | 暂停当前的睡眠会话 |
| `sleep-resume` | — | 恢复暂停的睡眠会话 |
| `sleep-complete` | `--notes` | 结束睡眠并将记录保存到历史记录中 |
| `sleep-cancel` | — | 取消睡眠操作，不保存记录 |

### 哺乳相关命令

| 命令 | 参数 | 描述 |
|---------|-----------|-------------|
| `feed-start` | `--side {left,right}` （默认：left） | 开始哺乳会话 |
| `feed-pause` | — | 暂停哺乳会话，并记录持续时间 |
| `feed-resume` | `--side {left,right}` （可选） | 在指定的一侧或上次哺乳的一侧继续哺乳 |
| `feed-switch` | — | 切换哺乳位置（如果会话已暂停，则自动恢复） |
| `feed-complete` | `--notes` | 结束哺乳并将记录保存到历史记录中 |
| `feed-cancel` | — | 取消哺乳操作，不保存记录 |

### 滴奶瓶喂养相关命令

```
bottle <amount> [options]
```

| 参数 | 值 | 是否必填 | 默认值 |
|-----------|--------|----------|---------|
| `amount` | 任意数值 | **是** | — |
| `--type` / `-t` | `"Breast Milk"`, `"Formula"`, `"Mixed"` | 否 | `"Formula"` |
| `--units` / `-u` | `ml`, `oz` | 否 | `ml` |
| `--notes` / `-n` | 任意文本 | 否 | — |

### 换尿布相关命令

```
diaper <mode> [options]
```

| 参数 | 值 | 是否必填 | 默认值 |
|-----------|--------|----------|---------|
| `mode` | `pee`, `poo`, `both`, `dry` | **是** | — |
| `--pee-amount` | `little`, `medium`, `big` | 否 | — |
| `--poo-amount` | `little`, `medium`, `big` | 否 | — |
| `--color` | `yellow`, `brown`, `black`, `green`, `red`, `gray` | 否 | — |
| `--consistency` | `solid`, `loose`, `runny`, `mucousy`, `hard`, `pebbles`, `diarrhea` | 否 | — |
| `--rash` | （标志） | 否 | false |
| `--notes` | 任意文本 | 否 | — |

#### 颜色说明：
- **黄色** — 母乳喂养婴儿的正常情况 |
- **棕色** — 配方奶喂养或较大婴儿的正常情况 |
- **绿色** — 可能是正常情况，也可能表示消化较快 |
- **黑色** — 出生头几天的正常现象（胎便），后期可能表示异常 |
- **红色** — 可能表示有血液，需咨询儿科医生 |
- **灰色** | 不常见，可能表示肝脏问题 |

#### 大便性状说明：
- **solid** — 成形的大便 |
- **loose** | 软但不是水状 |
- **runny** | 水状的大便 |
- **mucousy** | 含有黏液的粪便 |
- **hard** | 硬的大便，可能表示便秘 |
- **pebbles** | 小而硬的颗粒 |
- **diarrhea** | 非常稀的大便 |

### 生长测量相关命令

```
growth [options]
growth-get
```

| 参数 | 值 | 是否必填 | 备注 |
|-----------|--------|----------|-------|
| `--weight` / `-w` | 数值 | 至少提供一个 | 千克（公制）或磅（英制） |
| `--height` / `-l` | 数值 | 测量单位 | 厘米（公制）或英寸（英制） |
| `--head` | 数值 | 必填 | 厘米（公制）或英寸（英制） |
| `--units` / `-u` | `metric`, `imperial` | 否 | 默认：`metric` |
| `--notes` / `-n` | 任意文本 | 否 | — |

### 历史记录/日历相关命令

```
history [options]
```

| 参数 | 值 | 是否必填 | 默认值 |
|-----------|--------|----------|---------|
| `--date` / `-d` | `YYYY-MM-DD` | 否 | 当前日期 |
| `--days` | 数值 | 否 | 1 |
| `--type` / `-t` | `sleep`, `feed`, `diaper`, `health` | 否 | 所有类型 |

可以使用`--type`多次过滤：`--type sleep --type feed`

## 代理使用指南：何时请求详细信息

### 在备注中标注AI协助

**在记录条目时** **始终** 需要标注AI的协助：

**创建新条目时**：
- 无用户备注：`--notes "通过AI创建"`
- 用户提供备注：`--notes "用户备注 | 通过AI创建"`

**编辑现有条目时**：
- 无用户备注：`--notes "通过AI更新"`
- 用户提供备注：在现有备注后添加 `| 通过AI更新`

这样可以记录下AI协助创建的条目。

### 何时需要进一步确认

当用户提供的信息不完整时，在记录之前请请求进一步确认。例如：

### 换尿布时
如果用户只说了“换尿布”或“大便”：
- **务必询问**：是小便、大便还是两者都有？
- **对于大便**，可以询问：颜色？性状？量？
- **如果用户显得匆忙或只说“记录一下”**，可以省略这些细节。

示例跟进：
> “明白了！是小便、大便还是两者都有？有什么需要记录的细节（颜色、性状、量）？”

### 滴奶瓶喂养时
如果用户只说了“喂奶”，但没有提供量：
- **务必询问**：喂了多少？（以毫升或盎司为单位）
- **可以进一步询问**：是配方奶、母乳还是混合喂养？

示例跟进：
> “喂了多少毫升？是配方奶、母乳还是混合喂养？”

### 生长测量时
如果用户只说了“记录体重”，但没有提供具体数值：
- **务必询问**：体重是多少？（如果单位不明确，请明确说明）

### 睡眠/喂食计时器相关命令
这些命令通常比较明确，但如果存在歧义，请进一步确认：
- “婴儿开始吃奶了” → “开始哺乳 — 在哪一侧，左侧还是右侧？”
- “喂奶完成” → 需要确认是母乳喂养还是使用奶瓶喂养

## 自然语言示例

| 用户输入 | 操作建议 |
|-----------|--------|
| “婴儿睡着了” | `sleep-start` |
| “婴儿醒了” | `sleep-complete` |
| “取消这次睡眠” | `sleep-cancel` |
| “在左侧喂奶” | `feed-start --side left` |
| “更换哺乳位置” | `feed-switch` |
| “哺乳完成” | `feed-complete` |
| “喂了4盎司的配方奶” | `bottle 4 --type Formula --units oz` |
| “喂了120毫升的母乳” | `bottle 120 --type "Breast Milk" --units ml` |
| “换尿布，有尿和大便” | **询问尿量和大便的性状/颜色** |
| “尿布只是湿了” | `diaper pee` |
| “检查尿布是否干燥” | `diaper dry` |
| “体重是5.5千克” | `growth --weight 5.5 --units metric` |
| “婴儿今天做了什么？” | `history --days 1` |
| “本周的睡眠记录” | `history --days 7 --type sleep` |

## 支持多个孩子

如果账户中有多个孩子，可以使用`--child` / `-c`参数：
```bash
python3 hb.py --child "Baby Name" sleep-start
```

如果没有使用`--child`参数，命令将默认针对账户中的第一个孩子。

## 故障排除

**认证错误**：
- 确认电子邮件/密码是否正确
- 检查配置文件的权限
- Huckleberry API访问不支持双因素认证（2FA）

**“未找到孩子”**：
- 确保账户中至少有一个孩子的资料在Huckleberry应用程序中

**计时器已启动**：
- 在开始新的会话之前，请完成或取消当前的会话

## 技术说明

- 通过gRPC使用Firebase Firestore（与移动应用程序相同）
- 实时同步：更改会立即显示在Huckleberry应用程序中
- 令牌自动刷新：会话保持认证状态
- **时区处理**：Huckleberry要求在条目中设置`offset`字段（UTC时间后的偏移量，单位为分钟）。例如，PST（UTC-8）表示偏移8分钟。CLI会根据配置的时区自动计算这个值。如果没有这个字段，条目会在应用程序中显示为UTC时间。

---

## 致谢

本工具基于[py-huckleberry-api](https://github.com/Woyken/py-huckleberry-api)开发，由Woyken创建——这是一个针对Huckleberry Firebase后端的Python客户端。

---

*使用AI生成 - 2026-01-27*
*使用AI更新 - 2026-01-28*

## 关于所有条目类型的说明

`--notes` / `-n`参数适用于所有类型的条目：
- `sleep-complete --notes "宝宝整晚都睡着了！"`
- `feed-complete --notes "今天的吸吮姿势很好"`
- `bottle --notes "通过AI记录"`
- `diaper --notes "由AI检查"`
- `growth --notes "在儿科医生处测量过"`

上游的py-huckleberry-api仅支持在换尿布条目中添加备注。本工具通过直接更新Firestore文档，将这一功能扩展到了所有类型的条目。

## 上游API不支持的功能

Huckleberry中存在以下功能，但在py-huckleberry-api中不可用：
- 睡眠状态（开始/结束时婴儿的情绪）
- 睡眠地点（汽车、婴儿车、婴儿床等）

要使用这些功能，需要修改上游库以接受额外的参数。