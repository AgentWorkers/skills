# Urban Sports Scanner

该工具可以扫描您的Urban Sports Club场馆信息，显示带有直接预订链接的课程，并支持课程的预订与取消功能。

## 设置

### 1. Python环境

```bash
cd /pfad/zu/urban-sports
python3 -m venv venv
venv/bin/pip install playwright
venv/bin/playwright install chromium
venv/bin/playwright install-deps chromium
```

### 2. 登录凭据

请输入您的Urban Sports Club登录凭据：

```json
{
  "email": "deine-email@beispiel.de",
  "password": "dein-passwort"
}
```

`credentials.json`文件被包含在`.gitignore`中，因此不会被提交到代码仓库。
这些凭据仅用于`--book`、`--cancel`和`--bookings`命令。

### 3. 配置场馆信息

请将您的场馆信息填写到`config.py`文件中。场馆ID可以在urbansportsclub.com的网址中找到：

```
https://urbansportsclub.com/de/venues/20818
                                       ^^^^^
```

示例：

```python
VENUES = {
    "storm": {
        "name": "STORM Cycling Berlin - Mitte",
        "url": "https://urbansportsclub.com/de/venues/20818",
        "type": "cycling",
        "keywords": ["Performance", "Groove", "Cycling"],
    },
    "fitboxing": {
        "name": "Brooklyn Fitboxing",
        "url": "https://urbansportsclub.com/de/venues/27355",
        "type": "boxing",
        "keywords": ["Boxing", "Fitboxing", "HIIT"],
    },
}
```

- `name`：显示名称
- `url`：场馆在urbansportsclub.com上的页面地址
- `type`：可自由选择，会显示在输出结果中
- `keywords`：有助于在页面文本中识别课程名称

### URL参数

该工具会自动在场馆URL中添加以下参数：

- `plan_type`：会员等级。用于确定显示哪些课程（仅显示可预订的课程）：
  - Private: 1=Essential, 2=Classic, 3=Premium, 6=Max
  - Company: 1=S, 2=M, 3=L, 6=XL
  默认值：`3`
- `business_type`：`b2c`（个人会员）或`b2b`（企业会员）
  默认值：`b2c`

这些参数可以在`config.py`文件中的`PLAN_TYPE`和`BUSINESS_TYPE`字段进行配置。

## 使用方法

### 扫描课程

```bash
# Alle Venues fuer heute
venv/bin/python scan.py

# Bestimmtes Datum
venv/bin/python scan.py --date 2026-02-10

# Nur eine Venue
venv/bin/python scan.py --venue storm

# JSON-Ausgabe (fuer Weiterverarbeitung)
venv/bin/python scan.py --json
```

每个课程都会附带一个直接的预订链接返回：
```
  07:30  STORM Cycling Berlin - Mitte    45 Min STORM Ride - Performance
         https://www.urbansportsclub.com/de/activities?class=98049323
```

### 预订课程

```bash
venv/bin/python scan.py --book 98049323
```

### 取消预订

```bash
venv/bin/python scan.py --cancel 98049323
```

### 查看即将进行的预订

```bash
venv/bin/python scan.py --bookings
venv/bin/python scan.py --bookings --json
```

## 文件结构

```
urban-sports/
├── SKILL.md                  # Diese Doku
├── scan.py                   # Scanner + Buchen + CLI
├── config.py                 # Venue-Konfiguration
├── credentials.json          # Login-Daten (nicht im Repo)
├── credentials.example.json  # Vorlage
├── .gitignore
└── venv/                     # Python virtualenv (nicht im Repo)
```

## 错误处理

### “未配置任何场馆”
请在`config.py`中至少配置一个场馆。

### “未找到credentials.json”
请将`credentials.example.json`复制到`credentials.json`文件中，并填写您的凭据信息。

### 扫描器未找到课程
- 请检查日期是否正确（不要选择过去的日期）
- 某些场馆在特定日期可能没有课程
- 需要安装Chromium相关依赖库：`venv/bin/playwright install-deps chromium`