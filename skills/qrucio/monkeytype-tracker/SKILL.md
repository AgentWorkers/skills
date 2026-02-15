---
name: monkeytype-tracker
description: **使用 Monkeytype 追踪和分析打字统计数据，并提供改进建议。**  
当用户提到“monkeytype”、“打字统计”、“打字速度”、“WPM（每分钟输入字数）”、“打字练习”或希望检查自己的打字表现时，可以使用该工具。  
该工具提供以下功能：  
- 按需查看统计数据  
- 测试历史分析  
- 个人最佳记录  
- 进度对比  
- 排行榜查询  
- 可选的自动生成报告  

**使用说明：**  
需要用户提供自己的 Monkeytype ApeKey 以访问 API。
---

# Monkeytype Tracker

跟踪您的Monkeytype打字统计数据，并获得个性化的改进建议。

## 预启动检查（务必首先执行）

在运行任何命令之前，请检查设置是否已完成：

**安全优先级：**
1. **环境变量**（最安全的方式）：`MONKEYTYPE_APE_KEY`
2. **配置文件备用路径**：`~/.openclaw/workspace/config/monkeytype.json`

```python
# Check environment variable first
ape_key = os.getenv('MONKEYTYPE_APE_KEY')
if not ape_key:
    # Check config exists and has valid key
    config_path = Path.home() / ".openclaw" / "workspace" / "config" / "monkeytype.json"
```

**如果不存在环境变量且没有配置文件** → 运行设置流程（步骤1）
**如果`apeKey`存在但API返回471“无效”** → 告知用户激活该密钥（勾选相应的复选框）
**如果`apeKey`有效** → 继续执行命令

## 设置流程（3个步骤）

### 步骤1：获取ApeKey

发送以下消息：

```
Hey! 👋 I see you want to track your Monkeytype stats. I'll need your API key to get started.

**🔑 How to get it:**
1. Go to monkeytype.com → **Account Settings** (click your profile icon)
2. Select **"Ape Keys"** from the left sidebar
3. Click **"Generate new key"**
4. ⚠️ **Activate it:** Check the checkbox next to your new key (keys are inactive by default!)
5. Copy the key and send it to me

Once you share the key, I'll ask about automation preferences 🤖

---

🔒 **Prefer to add it manually?** No problem!

**Option 1: Environment Variable (Recommended - Most Secure)**
Set in your system:
- Windows (PowerShell): `$env:MONKEYTYPE_APE_KEY="YOUR_KEY_HERE"`
- Linux/Mac: `export MONKEYTYPE_APE_KEY="YOUR_KEY_HERE"`

**Option 2: Config File**
Create this file: `~/.openclaw/workspace/config/monkeytype.json`
With this content:
{
  "apeKey": "YOUR_KEY_HERE"
}

Then just say "monkeytype stats" and I'll take it from there!
```

收到密钥后：
1. 将密钥保存到`~/.openclaw/workspace/config/monkeytype.json`文件中：
```json
{
  "apeKey": "USER_KEY_HERE",
  "automations": {
    "dailyReport": false,
    "weeklyReport": false,
    "reportTime": "20:00"
  }
}
```
2. **立即测试密钥**，运行`python scripts/monkeytype_stats.py stats`
3. 如果出现471错误 → 密钥无效，请让用户检查复选框是否已勾选
4. 如果成功 → 进入步骤2

### 步骤2：验证并询问自动化偏好设置

密钥验证成功后，发送以下消息：

```
Got it! Key saved and verified ✅

**📊 Quick Overview:**
• {tests} tests completed ({hours} hrs)
• 🏆 PB: {pb_15}WPM (15s) | {pb_30}WPM (30s) | {pb_60}WPM (60s)
• 🔥 Current streak: {streak} days

Now, would you like automated reports?

**Options:**
1️⃣ **Daily report** — Summary of the day's practice
2️⃣ **Weekly report** — Week-over-week comparison + tips
3️⃣ **Both**
4️⃣ **None** — On-demand only

⏰ What time should I send reports? (default: 8pm)
```

### 步骤3：完成设置

用户选择好偏好设置后：
1. 使用这些设置更新配置文件
2. 如果启用了自动化功能，创建cron作业：
   - 每日：`0 {小时} * * *`，作业名称为`monkeytype-daily-report`
   - 每周：`0 {小时} * * 0`，作业名称为`monkeytype-weekly-report`
3. 发送完成通知：

```
🎉 **You're all set!**

**✅ Config saved:**
• Weekly report: {status}
• Daily report: {status}

**💡 Try these anytime:**
• "show my typing stats"
• "how's my typing progress"
• "compare my typing this week"
• "monkeytype leaderboard"

Happy typing! May your WPM be ever higher 🚀⌨️
```

## 错误处理

| 错误类型 | 用户提示 |
|---------|-----------|
| 未找到配置文件 | “看起来Monkeytype尚未设置完成。让我帮助您开始使用吧！ 🔑” → 开始设置流程 |
| 配置文件中不存在`apeKey` | 同上 |
| API返回471“无效” | “您的API密钥无效。请前往Monkeytype → 账户设置 → Ape Keys，勾选密钥旁边的复选框以激活它 ✅” |
| API返回401“未经授权” | “您的API密钥似乎无效。让我们为您重新生成一个。” → 开始设置流程 |
| API请求次数达到上限 | “API请求次数达到上限。请稍后重试 ⏳” |
| 网络错误 | “无法连接到Monkeytype服务器。请检查网络连接后重试。”

## 命令

### 获取统计数据
**触发条件**：“显示我的Monkeytype统计数据”、“我的打字情况如何”、“查看打字统计”
1. 执行预启动检查（见上文）
2. 运行：`python scripts/monkeytype_stats.py stats`
3. 用表情符号美化输出结果

### 最近的打字记录与分析
**触发条件**：“分析我的近期打字情况”、“我最近的打字表现如何”
1. 执行预启动检查
2. 运行：`python scripts/monkeytype_stats.py history --limit 50`
3. 分析输出结果并提供2-3条改进建议

### 进度比较
**触发条件**：“比较我的打字进度”、“我的打字能力是否有提升”
1. 执行预启动检查
2. 运行：`python scripts/monkeytype_stats.py compare`

### 查看排行榜
**触发条件**：“查看Monkeytype排行榜”、“我的排名是多少”
1. 执行预启动检查
2. 运行：`python scripts/monkeytype_stats.py leaderboard [--mode time] [--mode2 60]`

## 改进建议逻辑

在获取统计数据后，根据以下情况提供改进建议：

| 问题 | 建议 |
|------|------|
| 标准差（STDDev）> 15 | “注重打字的一致性——放慢打字速度，争取每次测试的准确率达到95%以上” |
| 准确率< 95% | “提高准确率有助于提升打字速度。继续练习，直到准确率稳定在95%以上” |
| 60秒内的打字次数远少于30次 | “发现耐力不足。多练习长时间的单次打字测试以提高耐力” |
| 打字测试次数较少 | “多练习才能更快进步。建议每天进行5-10次测试” |
| 连续打字记录中断 | “保持一致性很重要！尽量每天都能进行一些打字练习” |

## API相关说明

- 基本URL：`https://api.monkeytype.com`
- 认证头：`Authorization: ApeKey {key}`
- 请求限制：全局每分钟30次请求；结果端点每天30次请求
- 尽可能将结果缓存到本地

## 相关文件

- `~/.openclaw/workspace/config/monkeytype.json`：用户配置文件
- `scripts/monkeytype_stats.py`：主要的数据获取脚本