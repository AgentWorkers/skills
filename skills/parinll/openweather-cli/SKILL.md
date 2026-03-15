---
name: openweather-cli
description: 当用户希望运行、排查问题或扩展 owget CLI 以使用 OpenWeatherMap 进行地理编码、获取当前天气信息及 5 天天气预报时，请使用此技能。
homepage: https://github.com/ParinLL/OpenWeatherMap-script
metadata: {"openclaw":{"homepage":"https://github.com/ParinLL/OpenWeatherMap-script","requires":{"env":["OPENWEATHER_API_KEY"],"binaries":["go"]},"primaryEnv":"OPENWEATHER_API_KEY"}}
---
# OpenWeatherMap CLI 技能文档

本文档仅提供关于如何使用 `owget`（OpenWeatherMap CLI）以及解决相关问题的说明。

## 技能用途及使用场景

- 用户需要获取当前天气信息、天气预报或地理编码（geo）结果。
- 用户询问如何运行 `owget` 命令或如何使用参数。
- 用户报告 API 密钥问题、HTTP 错误或城市查询失败的情况。

## 从 GitHub 安装

- GitHub 链接：https://github.com/ParinLL/OpenWeatherMap-script

推荐的安装方式：

```bash
git clone https://github.com/ParinLL/OpenWeatherMap-script.git
cd OpenWeatherMap-script
go install .
```

这将 `owget` 安装到您的 Go 工具目录中（例如：`$GOPATH/bin` 或 `$HOME/go/bin`）。

## 所需环境变量/权限

所需的环境变量：

```bash
export OPENWEATHER_API_KEY="your-api-key"
```

- 安装和运行 `owget` 需要 `go` 工具链的支持。
- 如果将 `owget` 安装到系统全局目录（如 `/usr/local/bin`），则需要管理员权限，并事先审查源代码。
- 请勿在输出中显示完整的 API 密钥；调试请求日志应屏蔽敏感的查询参数（例如 `appid`）。

## 如何使用 `owget`

安装完成后，请确保 `owget` 可以在您的 shell 中使用：

```bash
owget --help
```

如果 shell 无法找到 `owget`，请将您的 Go 工具目录路径添加到 `PATH` 环境变量中：

```bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

**核心命令示例：**

- 根据坐标获取当前天气：
  - `owget weather <纬度> <经度>`
  - 例如：`owget weather 25.0330 121.5654`
- 根据城市名称获取当前天气：
  - `owget city "<城市,国家>"
  - 例如：`owget city "Taipei,TW"`
- 获取 5 天天气预报：
  - `owget forecast <纬度> <经度>`
  - 例如：`owget forecast 25.0330 121.5654`
- 根据城市名称获取 5 天天气预报：
  - `owget city "<城市,国家>" forecast`
  - 例如：`owget city "Taipei,TW" forecast`
- 进行地理编码查询：
  - `owget geo "<查询参数>"
  - 例如：`owget geo "New York,US"`

**常用参数：**

- `--detail`：显示更多详细信息（如气压、风速、日出/日落时间、能见度等）。
- `--debug`：打印 HTTP 调试信息以帮助排查问题。敏感的查询参数会被屏蔽。

**常见使用流程：**

1. 首先设置 `OPENWEATHER_API_KEY` 环境变量。
2. 如果需要验证地点名称，可以使用 `owget geo "<城市,国家>"` 命令。
3. 使用 `owget weather ...` 或 `owget forecast ...` 命令获取实际天气数据。
4. 如需更详细的输出，可以使用 `--detail` 参数；仅在排查问题时使用 `--debug` 参数。

## 常见问题及解决方法：

- **错误：需要设置 OPENWEATHER_API_KEY 环境变量**
  - 请确保已设置 `OPENWEATHER_API_KEY` 环境变量。示例：`export OPENWEATHER_API_KEY="..."`
- **API 返回 401 错误**
  - API 密钥无效、过期或输入错误。请重新检查您的 OpenWeatherMap 密钥。
- **API 返回 404 错误或城市未找到**
  - 请使用正确的格式（`<城市,国家>`），并先使用 `owget geo "<查询参数>"` 进行验证。
- **使用调试模式时担心敏感信息泄露**
  - 调试请求 URL 会屏蔽敏感参数，但在共享或日志记录的环境中请避免长时间运行调试模式。