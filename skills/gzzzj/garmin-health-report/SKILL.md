---
name: garmin-health-report
description: 根据Garmin Connect的数据生成全面的每日健康报告，并包含专业的跑步分析（心率区间、TRIMP值以及Jack Daniels VDOT指标）。
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python: ">=3.8"
    install:
      - kind: pip
        packages:
          - garth>=0.4.0
    emoji: "🏃‍♂️"
    homepage: https://github.com/yourusername/garmin-health-report
---
# 加明健康报告（Garmin Health Report）

本工具能够利用Garmin Connect数据生成专业的每日健康报告，并提供高级的跑步分析功能。

**主要功能：**
- **睡眠分析**：睡眠时长、睡眠阶段（深度睡眠/浅睡眠/快速眼动睡眠）、睡眠质量评分以及7维睡眠质量评级
- **心率监测**：静息心率及恢复状态
- **活动追踪**：步数、跑步距离、楼层爬升次数以及目标完成情况
- **专业跑步指标**：
  - 心率区间（1-5区）
  - TRIMP（训练负荷）计算
  - 基于Jack Daniels跑步公式的VDOT（有氧能力）估算
  - 个性化的恢复与训练建议
- **7天趋势分析**：活动模式及持续性的跟踪
- **个性化建议**：睡眠技巧、步数目标、训练建议

**区域支持**：支持Garmin.com（国际版）和Garmin.cn（中国地区）账户。

## 快速入门

### 1. 安装依赖库

本工具需要Python 3.8或更高版本以及`garth`库：

```bash
# Install garth (Garmin Connect authentication library)
pip3 install garth

# Verify installation
python3 -c "import garth; print('garth installed successfully')"
```

### 2. 与Garmin Connect进行身份验证

首次使用时需要登录Garmin Connect进行身份验证：

```bash
# Navigate to skill directory
cd ~/.agents/skills/garmin-health-report

# Run authentication script
python3 authenticate.py
```

按照提示输入您的Garmin Connect用户名和密码。验证完成后，Token会安全地存储在`~/.garmin-health-report/tokens.json`文件中。

**中国地区用户（garmin.cn）：**

在身份验证之前，请先创建一个配置文件：

```bash
mkdir -p ~/.garmin-health-report
cat > ~/.garmin-health-report/config.json << 'EOF'
{
  "is_cn": true,
  "log_level": "INFO"
}
EOF
```

然后运行`python3 authenticate.py`进行身份验证。

### 3. 生成健康报告

可以生成当天的健康报告，或指定日期的报告：

```bash
# Today's report
python3 health_daily_report.py

# Specific date
python3 health_daily_report.py 2025-01-15

# Save to file
python3 health_daily_report.py > ~/health_report_$(date +%Y-%m-%d).txt
```

### 4. （可选）通过Cron任务自动执行

若希望每天自动生成健康报告，请将其添加到Cron任务中：

```bash
crontab -e

# Add this line for daily report at 23:00
0 23 * * * /usr/bin/python3 /path/to/health_daily_report.py >> /path/to/health_report.log 2>&1
```

## 使用示例

```bash
# Generate today's report
python3 health_daily_report.py

# Generate report for a specific date
python3 health_daily_report.py 2026-03-01

# Check authentication status
python3 authenticate.py

# Logout and remove saved tokens
python3 authenticate.py
# Then choose 'y' when prompted to logout
```

## 指标解析

### 心率区间

| 区间 | 强度 | 用途 | 心率占比 |
|-------|-----------|----------|---------|
| 1   | 恢复期 | 热身、恢复 | <50% |
| 2   | 有氧基础 | 基础训练 | 50-60% |
| 3   | 有氧耐力 | 提高耐力 | 60-70% |
| 4   | 乳酸阈值 | 提升乳酸阈值 | 70-80% |
| 5   | 最大摄氧量 | 最大强度 | >80% |

### TRIMP（训练负荷）

TRIMP是一种结合训练时长和强度的训练负荷指标：
- **<100**：轻度负荷 - 恢复日
- **100-200**：中度负荷 - 日常训练
- **200-300**：高强度负荷 - 需要休息
- **>300**：极高负荷 - 建议休息

### VDOT（VDot O₂max）

基于Jack Daniels跑步公式计算的有氧能力指标。VDOT值越高，代表跑步速度潜力越大。

VDOT用于确定最佳训练配速：
- **E（轻松）**：恢复期和基础训练
- **M（马拉松）**：马拉松配速
- **T（阈值）**：乳酸阈值配速
- **I（间歇）**：间歇训练配速
- **R（重复）**：重复训练配速

## 输出格式

报告以美观的文本格式呈现：

```
📅 2026-03-01 健康日报
============================================================

😴 睡眠质量
总睡眠：7.7 小时
└─ 深睡：1.4h (18%) | 浅睡：4.5h (58%) | REM：1.9h (24%)

睡眠评分：82 (良好)

💓 心率监测
静息心率：57 bpm 💙

👟 活动量
今日步数：13620 步
步数目标：10000 步
完成度：136.2%
...

💪 运动数据分析（专业版）
... (detailed HR zones, TRIMP, VDOT analysis)

💡 J.A.R.V.I.S.有话说
... (personalized insights)

📈 长期趋势（过去7天）
... (7-day pattern analysis)

============================================================
💪 今天运动量很充足！继续保持！

✨ 明天加油！💪
```

## 配置设置

请编辑`health_daily_report.py`文件顶部的配置部分：

```python
# Health history file (for 7-day trend analysis)
HISTORY_FILE = os.path.expanduser("~/.garmin_health_report/history.json")

# User profile (optional, for more accurate HR zone calculations)
USER_RESTING_HR = None  # e.g., 53
USER_AGE = None        # e.g., 25
```

设置`USER_restING_HR`和`USER_AGE`可以提高以下指标的准确性：
- 心率区间计算
- TRIMP（训练负荷）估算
- 恢复状态评估

如果未设置，默认值分别为：年龄30岁，静息心率60次/分钟。

## 故障排除

### 错误：未安装garth库

```
ModuleNotFoundError: No module named 'garth'
```

**解决方法：** 安装`garth`库：
```bash
pip3 install garth
```

### 错误：无法进行身份验证

```
Error: Not authenticated.
Run 'python3 authenticate.py' first.
```

**解决方法：** 运行`python3 authenticate.py`进行身份验证。

### 中国地区用户注意事项

```bash
# Verify config
cat ~/.garmin-health-report/config.json
# Should show: {"is_cn": true, ...}

# Clear tokens and re-authenticate
rm ~/.garmin-health-report/tokens.json
python3 authenticate.py
```

## 隐私与数据安全

- 所有数据均来自您的Garmin Connect个人账户
- Token文件仅存储在本地`~/.garmin-health-report/tokens.json`中
- 数据不会发送到第三方服务器（仅通过Garmin的API传输）
- 健康记录存储在本地`~/.garmin-health-report/history.json`中
- Token文件具有受限权限（仅允许文件所有者读写）

## 与原版本（基于garmer的版本）的差异

本版本直接使用`garth`库，而非`garmer`库：
- **依赖关系更简单**：仅依赖`garth`库
- **功能保持不变**：所有原始功能均保留
- **更易于安装**：使用`pip3 install garth`即可
- **更好的错误处理和调试体验**

## 许可证

本工具采用MIT许可证，详细信息请参阅`LICENSE`文件。

## 致谢

- 本工具使用了[garth](https://github.com/matin/garth)库来访问Garmin Connect API
- VDOT计算基于Jack Daniels的跑步公式
- TRIMP计算采用了Banister的公式