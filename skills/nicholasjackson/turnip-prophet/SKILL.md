---
name: turnip-prophet
description: 使用《动物森友会：新地平线》（Animal Crossing New Horizons, ACNH）中的精确算法来预测芜菁的价格。当用户询问芜菁的价格、芜菁的市场行情、如何预测芜菁价格、何时出售芜菁，或者如何通过芜菁获得最大利润时，可以使用此方法。
repository: https://github.com/nicholasjackson/openclaw-turnip-profit
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "jq"] },
        "install":
          [
            {
              "id": "python-deps",
              "kind": "shell",
              "label": "Install Python dependencies (matplotlib)",
              "command": "pip3 install matplotlib"
            },
            {
              "id": "jq-debian",
              "kind": "shell",
              "label": "Install jq (Debian/Ubuntu)",
              "command": "sudo apt-get update && sudo apt-get install -y jq",
              "when": "debian"
            },
            {
              "id": "jq-macos",
              "kind": "shell",
              "label": "Install jq (macOS)",
              "command": "brew install jq",
              "when": "darwin"
            }
          ]
      }
  }
---
# Turnip Prophet - 动物森友会萝卜价格预测器

该工具利用《动物森友会：新地平线》（Animal Crossing: New Horizons）中的实际算法来预测萝卜的价格。

## ⚠️ 重要提示：务必先读取内存数据！

**在执行任何操作之前**，请先读取每周的数据文件：
```
memory/turnip-week.json
```
该文件包含了当周的购买价格、之前的价格走势以及所有已知的萝卜价格。**不要向用户询问你已经掌握的数据**，只需询问新的或缺失的价格信息。

当用户提供新的价格信息时，请**立即使用新值更新 `memory/turnip-week.json` 文件**，然后再运行预测功能。

### 每周数据格式（`memory/turnip-week.json`）
```json
{
  "week_start": "2026-02-15",
  "buy_price": 96,
  "previous_pattern": 1,
  "prices": [84, 81, 78, null, null, null, null, null, null, null, null, null],
  "labels": ["Mon AM", "Mon PM", "Tue AM", "Tue PM", "Wed AM", "Wed PM", "Thu AM", "Thu PM", "Fri AM", "Fri PM", "Sat AM", "Sat PM"]
}
```

每周日，系统会创建一个新文件，记录新的购买价格，并将所有价格重置为 `null`。

## 触发条件

当用户提及以下内容时，该工具会自动启动：
- “萝卜价格”或“萝卜价格预测”
- “ACNH萝卜”或“动物森友会的萝卜”
- “萝卜市场”
- “萝卜预言家”或“萝卜价格预测”
- 任何与萝卜销售相关的问题

## 隐私与数据存储

该工具仅将配置数据存储在您的本地机器上的 `memory/turnip-config.json` 文件中，不会向外部服务器发送任何数据。

**如果启用提醒功能，将存储以下信息：**
- 频道名称（Telegram/WhatsApp/Discord/Signal）
- 您在该频道上的用户ID
- OpenClaw 的二进制路径
- 配置时间戳

**存储这些信息的原因是**：这样定时提醒功能才能根据正确的信息发送通知，而无需使用硬编码的值。

**数据存储位置：** 本地存储在您的 OpenClaw 实例的内存目录中，不会被共享或上传，其他人也无法查看。

## 如何禁用/重置配置：**
```bash
rm ~/.openclaw/workspace/skills/turnip-prophet/memory/turnip-config.json
```

**删除定时任务：**
```bash
# Edit crontab and remove the turnip-prophet lines
crontab -e
```

**重要提示：** 在保存任何配置之前，必须明确确认设置流程。如果拒绝设置，则不会保存任何数据。

## 凭据与权限

**该工具本身不会请求或存储任何 API 密钥或凭证。**

但是，**如果您启用了定时提醒功能**，安装的定时任务将：  
- 使用您本地的 `openclaw` CLI 二进制文件  
- 通过您现有的 OpenClaw 配置和凭证发送消息  
- 按照您的 OpenClaw 实例的权限进行操作  

**这意味着：**  
- 自动提醒将以您的身份发送  
- 定时任务需要 OpenClaw 正在运行且配置正确  
- 消息将通过您配置的渠道（Telegram/WhatsApp 等）发送  

**您正在授权：**  
- 以您的名义自动发送消息  
- 使用您现有的消息渠道凭证  
- 运行调用 `openclaw gateway call message.send` 的定时任务  

如果您不希望使用您的凭证进行自动消息发送，请**不要启用定时提醒功能**。即使不启用提醒功能，该工具的核心预测功能也能正常使用。

## 日常提醒（可选）

首次使用时，系统会提供设置每日提醒的交互式流程：

### 交互式设置流程（管理员指导）

**首次触发时（用户首次询问萝卜价格时）：**

1. **检查是否已配置：**
   ```bash
   test -f memory/turnip-config.json && echo "configured" || echo "not configured"
   ```

2. **如果未配置，提供设置选项：**
   > “想要每日萝卜价格提醒吗？我可以为您发送通知：
   > • 星期日早上 8 点：查看黛西·梅（Daisy Mae）的萝卜价格
   > • 周一至周六中午和晚上 8 点：查看努克（Nook）的萝卜价格  
   > • 周六晚上 9:45：最后提醒  
   > 
   > 回复“是”以设置提醒，或“否”以跳过设置。**

3. **如果用户同意设置：**
   - **频道：** 从传入的 JSON 数据中提取频道名称（`"channel"` 字段）
   - **目标用户 ID：** 从传入的 JSON 数据中提取用户 ID（`"sender_id"` 字段）
   - **OpenClaw 路径：** 运行 `which openclaw` 命令或使用 `/usr/local/bin/openclaw`
   - **技能目录：** 使用该技能的绝对路径

4. **如果自动检测失败：**
   - 明确询问用户缺失的配置信息  
   - 在继续之前验证这些信息

**将配置信息存储在 `memory/turnip-config.json` 中：**
```json
{
  "channel": "telegram",
  "target": "8577655544",
  "openclaw_bin": "/usr/local/bin/openclaw",
  "skill_dir": "/home/user/.openclaw/workspace/skills/turnip-prophet",
  "configured_at": "2026-02-23T10:30:00Z"
}
```

**生成并显示定时任务内容：**
向用户展示将要添加的配置内容，包括具体的参数值。例如：
```bash
# Turnip Prophet reminders for telegram:8577655544
0 8 * * 0 /usr/local/bin/openclaw gateway call message.send --params '{"channel":"telegram","target":"8577655544","message":"🔔 Sunday! Check Daisy Mae'\''s turnip price (90-110 bells) and buy your turnips 🥬"}' 2>&1 | logger -t turnip-prophet
0 12 * * 1-6 /usr/local/bin/openclaw gateway call message.send --params '{"channel":"telegram","target":"8577655544","message":"🔔 Time to check Nook'\''s Cranny turnip prices!"}' 2>&1 | logger -t turnip-prophet
0 20 * * 1-6 /usr/local/bin/openclaw gateway call message.send --params '{"channel":"telegram","target":"8577655544","message":"🔔 Evening price check: Check Nook'\''s Cranny!"}' 2>&1 | logger -t turnip-prophet
45 21 * * 6 /usr/local/bin/openclaw gateway call message.send --params '{"channel":"telegram","target":"8577655544","message":"⏰ FINAL CALL: Turnips expire at 10 PM! Sell now or they'\''ll rot 🗑️"}' 2>&1 | logger -t turnip-prophet
```

请将 `channel` 和 `target` 替换为实际检测到的值。确保单引号使用正确的方式。

**在用户确认之前，向用户展示将要存储的信息：**
```
This will save:
• Channel: telegram
• User ID: 8577655544
• Location: memory/turnip-config.json (local only)

This data is stored locally on your machine and is needed so cron reminders can send messages to you.
You can delete the config file anytime with: rm memory/turnip-config.json

Continue? Reply 'confirm' to proceed, or 'cancel' to skip.
```

**确认设置后：**
1. 将配置信息写入 `memory/turnip-config.json`
2. 生成一个安全的安装命令并展示给用户：
   ```bash
   # Save the cron entries to a temp file
   cat > /tmp/turnip-cron-$$.txt <<'TURNIP_EOF'
   [generated entries]
   TURNIP_EOF
   
   # Review the file
   cat /tmp/turnip-cron-$$.txt
   
   # If it looks good, install:
   (crontab -l 2>/dev/null; cat /tmp/turnip-cron-$$.txt) | crontab -
   ```
3. 请用户运行命令并确认操作完成
4. 回复：“✅ 提醒已设置。只有当数据缺失时才会收到通知。您可以通过 `crontab -l` 查看安装情况。如需删除提醒，请删除 `memory/turnip-config.json` 文件及相关的定时任务。”

**如果用户拒绝或取消设置：**
- 回复：“没问题。没有数据被保存。您随时可以通过询问萝卜价格来重新设置提醒。”

### 定时任务处理脚本（cron_handler.sh）

定时任务脚本会从 `memory/turnip-config.json` 中读取频道和目标用户的信息：

```bash
CONFIG_FILE="$SKILL_DIR/memory/turnip-config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Config not found: $CONFIG_FILE" >&2
    exit 1
fi

CHANNEL=$(jq -r '.channel' "$CONFIG_FILE")
TARGET=$(jq -r '.target' "$CONFIG_FILE")
OPENCLAW_BIN=$(jq -r '.openclaw_bin' "$CONFIG_FILE")
```

**任务类型：**

- **sunday-daisy：**  
  - 检查 `memory/turnip-week.json` 中是否包含当周的购买价格  
  - 如果缺失，发送提醒：“🔔 星期日！查看黛西·梅的萝卜价格（90-110 钟币），赶紧购买吧 🥬”  
  - 如果已设置，则不发送提醒

- **daily-check：**  
  - 确定当前活跃的价格时间段（周一上午/下午至周六下午）  
  - 检查该时间段的价格是否已记录在 `memory/turnip-week.json` 中  
  - 如果缺失，发送提醒：“🔔 [当天] [上午/下午]：查看努克商店的萝卜价格！”  
  - 如果已记录，则不发送提醒

- **saturday-final：**  
  - 检查仍有多少价格未填写  
  - 如果有缺失的价格或购买价格未知，发送提醒：“⏰ 最后机会：萝卜将在晚上 10 点过期！现在就卖出，否则会腐烂 🗑️”  
  - 如果所有价格都已记录，发送提醒：“⏰ 今晚是卖出萝卜的最后机会！”  

**发送方式：**  
  使用 `"$OPENCLAW_BIN" gateway call message.send --params "{\"channel\":\"$CHANNEL\",\"target\":\"$TARGET\",\"message\":\"...\"}"` 命令发送消息

## 工作原理

该工具使用 Python 实现了《动物森友会：新地平线》中的萝卜价格预测算法，根据以下信息来预测未来价格：  
- 您在星期日的购买价格（90-110 钟币）  
- 本周已知的出售价格  
- 上周的价格走势（如果已知）  

**存在四种价格走势模式：**  
- **模式 0（波动）**：价格呈高低高低的高潮波动  
- **模式 1（大幅上涨）**：价格先下降后大幅上涨（最多上涨 6 倍）  
- **模式 2（持续下跌）**：价格持续下跌（表示行情不佳）  
- **模式 3（小幅上涨）**：价格先下降后小幅上涨（最多上涨 2 倍）  

## 使用说明**

触发提醒后：  
1. **读取 `memory/turnip-week.json` 文件**，获取所有已知数据  
2. 如果用户提供了新的价格信息，更新文件  
3. 使用所有已知数据运行预测  
4. 生成价格图表并附上预测结果  

### 运行预测  

```bash
echo '{"buy_price": 96, "prices": [84, 81, 78, null, null, null, null, null, null, null, null, null], "previous_pattern": 1}' | python3 scripts/turnip_predict.py
```  
- `prices` 数组：[周一上午、周一下午、周二上午、周二下午、周三上午、周三下午、周四上午、周四下午、周五上午、周五下午、周六上午、周六下午]  
- 未知价格用 `null` 表示  

### 生成价格图表  

预测完成后，生成一张价格图表图片：  

```bash
python3 scripts/generate_chart.py <buy_price> '<known_json>' '<mins_json>' '<maxs_json>' /tmp/turnip-chart.png
```  
- `buy_price`：星期日的购买价格（整数）  
- `known_json`：包含 12 个价格值的数组，未知价格用 `null` 表示（来自 `memory/turnip-week.json`）  
- `mins_json`：包含 12 个最低价格值的数组  
- `maxs_json`：包含 12 个最高价格值的数组  
- 所有脚本路径均相对于技能目录 `skills/turnip-prophet/`  

然后通过消息工具发送图表图片，并附带预测结果的文字说明。  

**每次更新预测结果时，务必附带图表。**

## 展示结果**

通过消息工具发送图表图片，并附上文字分析。不要过于机械，要表现出一定的人性化交流风格。  

**格式建议：**  
1. 图表图片附带简短的文字说明（购买价格、已知价格）  
2. 文本回复包括：  
   - 用列表形式展示价格走势的概率（使用表情符号表示）  
   - 简单解释数据的含义  
   - “我的建议：” 提供具体的操作建议（建议查看哪些价格、何时卖出、何时持有）  

**示例：**  
```
Pattern odds:
📉 Decreasing: 84.7% 😬
📈 Large Spike: 15.1% 🤞
📊 Small Spike: 0.1%

Not great. Three consecutive drops is strongly pointing to a decreasing week. But there's still a 15% chance of a large spike hiding — if it happens, it'd be Wed-Fri with prices up to 576 bells.

My take: Check the Tuesday PM price. If it drops again, this week is almost certainly a bust — sell and cut your losses. If it jumps up, the spike is on. 🎰
```  
提供直接且具有个人见解的推荐，对于概率为 0% 的价格走势模式应予以忽略。  

## 向用户解释价格走势模式：**  
- **波动（模式 0）**：价格呈波动趋势——当价格超过 120-130 钟币时卖出  
- **大幅上涨（模式 1）**：价格先下跌后大幅上涨（最多上涨 400-600 钟币）——等待时机  
- **持续下跌（模式 2）**：价格整周持续下跌——尽快卖出以减少损失  
- **小幅上涨（模式 3）**：价格先下跌后小幅上涨（最多上涨 150-200 钟币）——在价格回升时卖出  

## 错误处理**

如果脚本失败或返回错误：  
- 用简单的语言解释问题所在  
- 请用户重新检查输入的数据  
- 建议用户使用正确的数据重新尝试  

**注意事项：**  
- 预测结果具有不确定性，并非绝对准确  
- 该算法基于游戏的实际代码实现  
- 知道的价格越多，预测越准确  
- 必须提供星期日的购买价格  
- 上周的价格走势有助于预测，但非必需