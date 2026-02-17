---
name: grazy
description: grazy - Your Grazer Command Line Companion. Verwende für alle Graz-bezogenen Infos: Öffi, Wetter, News, Luftqualität, POI-Suche, Events
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["grazy"],
            "npmPackages": ["@grazy/cli"],
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@grazy/cli",
              "label": "Install grazy CLI (npm)",
              "description": "Installiert die grazy CLI global: npm install -g @grazy/cli"
            },
          ],
        "homepage": "https://github.com/thomyg/grazy",
        "repository": "https://github.com/thomyg/grazy",
        "author": "Thomas Gölles (@thomyg)",
        "keywords": ["grazy", "graz", "austria", "public-transport", "weather", "events", "cli"]
      }
  }
---

# grazy Skill

此技能允许您使用 grazy CLI 来获取格拉茨市的各类信息。

## ⚠️ 对代理（Agents）的重要提示

**在不确定如何使用该技能时，请务必先执行 `grazy help` 命令，以查看所有可用功能！**

```bash
# IMMER zuerst help aufrufen wenn du unsicher bist!
grazy help

# Oder für spezifische Commands:
grazy events --category help
grazy events --when help
grazy poi help
```

## 安装

该 CLI 已全局安装：`npm install -g @grazy/cli`

或者使用 npx（在沙箱环境中安装）：
```bash
npx @grazy/cli events
```

## 源代码与验证信息

- **NPM 包：** https://www.npmjs.com/package/@grazy/cli
- **GitHub 仓库：** https://github.com/thomyg/grazy
- **开发者：** Thomas Gölles (@thomyg)

## 命令列表

### 🚇 公共交通
```
grazy departures <stop>     # Echtzeit-Abfahrten
grazy search <name>          # Haltestelle suchen
grazy route <von> <nach>    # Route planen
```

### 🌤️ 天气与空气质量
```
grazy weather                # Aktuelles Wetter
grazy weather --days 7       # 7-Tage Forecast
grazy air                   # Luftqualität (AQI, PM2.5, PM10)
```

### 📰 新闻
```
grazy news                   # Alle News (ORF + Kleine Zeitung)
grazy news --source orf     # Nur ORF
grazy news --source kleine  # Nur Kleine Zeitung
grazy news --source sport   # Nur Sport
```

### 📅 活动
```
grazy events                 # Alle Events (kultur.graz.at)
grazy events --category musik          # Nur Musik
grazy events --category theater        # Theater & Tanz
grazy events --category ausstellungen  # Ausstellungen
grazy events --category kabarett       # Kabarett
grazy events --category kinder         # Kinder & Jugend
grazy events --category lesungen       # Lesungen & Vorträge
grazy events --category fuehrungen      # Führungen
grazy events --category film           # Film & Neue Medien

grazy events --when heute      # Heute
grazy events --when morgen     # Morgen
grazy events --when woche     # Diese Woche
grazy events --when wochenende # Wochenende (Sa/So)
grazy events --when monat      # Diesen Monat

grazy events --category help   # Alle Kategorien anzeigen
grazy events --when help      # Alle Zeitfilter anzeigen

# Kombiniert:
grazy events -c musik -w wochenende
grazy events -c theater -w woche
```

### 🔍 地点查询（POI）
```
grazy poi <type>            # POI-Typ suchen
grazy poi help              # Alle verfügbaren Typen anzeigen
```

**可查询的地点类型：** 餐厅（restaurant）、咖啡馆（cafe）、酒吧（bar）、快餐店（fast_food）、酒吧（pub）、电影院（cinema）、剧院（theatre）、博物馆（museum）、图书馆（library）、药店（pharmacy）、医院（hospital）、医生诊所（doctors）、停车场（parking）、加油站（fuel station）、自动取款机（ATM）、银行（bank）、游乐场（playground）

### 📋 其他功能
```
grazy status                # API-Status prüfen
grazy help                  # Hilfe anzeigen
```

## 常见公交站点名称

- `Jakomini` → Jakominiplatz（雅科米尼广场）
- `FH Joanneum` / `FH` → FH Joanneum（约阿内姆应用技术大学）
- `Hauptbahnhof` / `Bahnhof` → 格拉茨中央火车站（Graz Hauptbahnhof）
- `Stadion` → Merkur Arena（墨丘利竞技场）
- `LKH` / `Med Uni` → LKH 医学院（LKH Med Uni）

## 作为助手使用时的重要提示

### ⚡ 第一步：务必先执行 `help` 命令！

```bash
# Bei ANY Unsicherheit - zuerst help!
grazy help

# Für Events:
grazy events --category help
grazy events --when help

# Für POI:
grazy poi help
```

### 然后使用相应的命令

```bash
# Events
grazy events --limit 10
grazy events --category musik
grazy events --when wochenende
grazy events -c theater -w wochenende

# Wetter
grazy weather

# Öffi
grazy departures "Jakomini"
grazy departures "FH Joanneum"

# News
grazy news --limit 5

# Luft
grazy air

# POI
grazy poi restaurant --limit 10
grazy poi cafe --limit 5
grazy poi pharmacy
```

## 输出格式说明

- **●** = 数据为实时更新
- **+Xmin** = 行车延误时间
- **AQI：** 0-50 表示空气质量良好，51-100 表示中等，>100 表示空气质量较差

## 注意事项

- **请始终使用英文命令名称（如 `departures`、`weather`、`news`、`poi`、`events` 等）**
- **遇到不确定的情况时，请执行 `grazy help` 命令！**
- grazy 是无密钥（keyless）使用的工具，无需任何 API 密钥
- 数据来源包括：EFA、Open-Meteo、ORF RSS、OpenStreetMap 以及 kultur.graz.at 的 RSS 源