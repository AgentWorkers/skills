---
name: openweathermap-cli
description: 当用户希望运行、排查问题或扩展 owget CLI 以使用 OpenWeatherMap 进行地理编码、查询当前天气以及获取 5 天的天气预报时，请使用此技能。
homepage: https://github.com/ParinLL/OpenWeatherMap-script
metadata: {"openclaw":{"homepage":"https://github.com/ParinLL/OpenWeatherMap-script","requires":{"env":["OPENWEATHER_API_KEY"],"binaries":["go"]},"primaryEnv":"OPENWEATHER_API_KEY"}}
---
# OpenWeatherMap CLI 技能文档

本文档仅用于说明如何使用 `owget`（OpenWeatherMap CLI）以及解决相关问题。

## 技能用途及使用场景

- 用户需要获取当前天气信息、天气预报或地理编码（geo）结果。
- 用户希望了解如何运行 `owget` 命令或使用其参数。
- 用户遇到 API 密钥问题、HTTP 错误或城市查询失败的情况。

## 安装命令（或 GitHub 安装链接）

- GitHub: [https://github.com/ParinLL/OpenWeatherMap-script](https://github.com/ParinLL/OpenWeatherMap-script)

安装前建议先查看最近的提交记录，并在可能的情况下将特定提交或标签固定下来（以防止供应链风险）：

```bash
git clone git@github.com:ParinLL/OpenWeatherMap-script.git
cd OpenWeatherMap-script
git log --oneline -n 5
```

推荐使用非特权用户权限进行安装：

```bash
go install .
```

系统全局安装（可选，需要 `sudo` 权限）：

```bash
CGO_ENABLED=0 go build -ldflags="-s -w" -o owget .
sudo install owget /usr/local/bin/
```

## 所需环境变量/权限

所需环境变量：

```bash
export OPENWEATHER_API_KEY="your-api-key"
```

- 安装和运行该工具需要 `go` 工具链。
- 如果使用 `sudo install ... /usr/local/bin/`，则需要系统管理员权限，并且应先审查源代码。
- 请勿在输出中泄露完整的 API 密钥；调试请求日志应屏蔽敏感的凭证参数（例如 `appid`）。

## 常见问题及解决方法

- **错误：OPENWEATHER_API_KEY 环境变量未设置**  
  - 请先运行 `export OPENWEATHER_API_KEY="..."` 来设置该环境变量。

- **API 返回 401 错误**  
  - API 密钥无效、已过期或输入错误。请重新检查您的 OpenWeatherMap 密钥。

- **API 返回 404 错误或城市未找到**  
  - 请使用 `City,Country` 的格式（例如 `Taipei,TW`），并先使用 `owget geo "<query>"` 进行测试。

- **担心使用调试模式时会导致凭证泄露**  
  - 调试请求 URL 会屏蔽敏感参数，但在共享或日志记录的环境中应避免长时间运行调试模式。