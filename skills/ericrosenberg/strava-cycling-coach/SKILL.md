---
name: strava-cycling-coach
description: 从 Strava 中跟踪和分析骑行表现。该工具可用于分析骑行数据、评估健康状况趋势、了解锻炼效果，或为骑行训练提供参考。它能自动监测新的骑行记录，并生成相应的表现分析报告。
---

# Strava 自行车训练助手

使用 Strava API 追踪骑行表现、分析骑行数据并监控健康状况的进步。

## 设置

### 1. 创建 Strava API 应用程序

访问 https://www.strava.com/settings/api 并创建一个应用程序：
- 应用程序名称：Clawdbot（或您喜欢的名称）
- 类别：数据导入器
- 俱乐部：（留空）
- 网站：http://localhost
- 授权回调域名：localhost

保存您的 **客户端 ID** 和 **客户端密钥**。

### 2. 运行设置脚本

```bash
cd skills/strava
./scripts/setup.sh
```

系统会提示您输入：
1. 客户端 ID
2. 客户端密钥
3. 访问 OAuth URL 进行授权
4. 复制授权代码，并使用以下代码完成设置：

```bash
./scripts/complete_auth.py YOUR_CODE_HERE
```

### 3. 配置自动监控（可选）

要在每次锻炼后自动接收骑行分析结果，请执行以下操作：

```bash
# Set your Telegram chat ID
export STRAVA_TELEGRAM_CHAT_ID="your_telegram_chat_id"

# Add to your shell profile for persistence
echo 'export STRAVA_TELEGRAM_CHAT_ID="your_telegram_chat_id"' >> ~/.bashrc

# Set up cron job (checks every 30 minutes)
crontab -l > /tmp/cron_backup.txt
echo "*/30 * * * * $(pwd)/scripts/auto_analyze_new_rides.sh" >> /tmp/cron_backup.txt
crontab /tmp/cron_backup.txt
```

### 4. 测试设置

分析您最近的骑行记录：

```bash
./scripts/analyze_rides.py --days 90 --ftp YOUR_FTP
```

## 使用方法

获取最新的骑行数据：

```bash
scripts/get_latest_ride.py
```

分析特定的骑行记录：

```bash
scripts/analyze_ride.py <activity-id>
```

监控新的骑行记录（在后台运行）：

```bash
scripts/monitor_rides.sh
```

## 自动监控功能

该工具可以自动：
1. 每 30 分钟检查一次新的骑行记录
2. 分析功率、心率和训练负荷
3. 提供关于表现和健康趋势的见解
4. 与最近的训练记录进行比较

## 分析的指标

- **功率**：平均值、标准化值、最大值、变化指数
- **心率**：平均值、最大值、在不同心率区间的时间
- **训练负荷**：TSS（训练负荷指数）估算值、强度系数
- **健康状况**：随时间的变化趋势
- **分段成绩**：个人最佳成绩及所付出的努力
- **对比**：与最近的骑行记录或个人最佳成绩进行对比

## 配置

编辑 `~/.config/strava/config.json` 文件以自定义以下设置：
- 监控频率
- 分析偏好
- 通知设置

## API 参考文档

请参阅 [references/api.md](references/api.md) 以获取完整的 Strava API 文档。