---
name: trein
description: 通过 `trein` CLI 查询荷兰铁路（NS）的列车发车信息、行程规划、列车延误情况以及车站搜索服务。
homepage: https://github.com/joelkuijper/trein
metadata: {"clawdbot":{"emoji":"🚆","requires":{"bins":["trein"],"env":["NS_API_KEY"]},"primaryEnv":"NS_API_KEY","install":[{"id":"npm","kind":"node","package":"trein","bins":["trein"],"label":"Install trein (npm)"},{"id":"download-mac-arm","kind":"download","url":"https://github.com/joelkuijper/trein/releases/latest/download/trein-darwin-arm64","bins":["trein"],"label":"Download (macOS Apple Silicon)","os":["darwin"]},{"id":"download-mac-x64","kind":"download","url":"https://github.com/joelkuijper/trein/releases/latest/download/trein-darwin-x64","bins":["trein"],"label":"Download (macOS Intel)","os":["darwin"]},{"id":"download-linux","kind":"download","url":"https://github.com/joelkuijper/trein/releases/latest/download/trein-linux-x64","bins":["trein"],"label":"Download (Linux x64)","os":["linux"]}]}}
---

# trein - 荷兰铁路（NS）命令行界面（CLI）

这是一个用于荷兰铁路（NS）API的命令行工具，提供实时列车发车信息、行程规划、列车延误情况以及车站查询功能。

## 安装

推荐使用 npm：
```bash
npm i -g trein
```

或者从 [GitHub 仓库](https://github.com/joelkuijper/trein/releases) 下载独立的二进制文件。

## 设置

从 [https://apiportal.ns.nl/](https://apiportal.ns.nl/) 获取 API 密钥，并进行配置：
```bash
export NS_API_KEY="your-api-key"
```

或者创建 `~/.config/trein/trein.config.json` 文件：
```json
{ "apiKey": "your-api-key" }
```

## 命令

### 列车发车信息
```bash
trein departures "Amsterdam Centraal"
trein d amsterdam
trein d amsterdam --json  # structured output
```

### 行程规划
```bash
trein trip "Utrecht" "Den Haag Centraal"
trein t utrecht denhaag --json
```

### 列车延误情况
```bash
trein disruptions
trein disruptions --json
```

### 车站查询
```bash
trein stations rotterdam
trein s rotterdam --json
```

### 别名（快捷方式）
```bash
trein alias set home "Amsterdam Centraal"
trein alias set work "Rotterdam Centraal"
trein alias list
trein d home  # uses alias
```

## 提示
- 对所有命令使用 `--json` 标志可获取结构化输出，便于进一步处理。
- 车站名称支持模糊匹配（例如：“adam” 可匹配 “Amsterdam Centraal”）。
- 别名存储在配置文件中，可以替代车站名称使用。