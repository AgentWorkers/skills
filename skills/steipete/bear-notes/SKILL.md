---
name: bear-notes
description: 通过 grizzly CLI 创建、搜索和管理 Bear 笔记。
homepage: https://bear.app
metadata: {"clawdbot":{"emoji":"🐻","os":["darwin"],"requires":{"bins":["grizzly"]},"install":[{"id":"go","kind":"go","module":"github.com/tylerwince/grizzly/cmd/grizzly@latest","bins":["grizzly"],"label":"Install grizzly (go)"}]}}
---

# Bear 笔记管理

在 macOS 上，可以使用 `grizzly` 命令来创建、读取和管理 Bear 应用中的笔记。

**系统要求：**
- Bear 应用已安装并正在运行。
- 对于某些操作（如添加文本、添加标签、打开特定笔记），需要使用 Bear 应用的访问令牌（该令牌存储在 `~/.config/grizzly/token` 文件中）。

## 获取 Bear 访问令牌

对于需要访问令牌的操作（如添加文本、添加标签、打开特定笔记），您需要先获取一个认证令牌：
1. 打开 Bear 应用 → 帮助 → API 令牌 → 复制令牌。
2. 将令牌保存到文件：`echo "YOUR_TOKEN" > ~/.config/grizzly/token`

## 常用命令

- **创建笔记**：  
  ```bash
  grizzly create --title "新建笔记"
  ```

- **通过 ID 打开/读取笔记**：  
  ```bash
  grizzly open --id "note_id"
  ```

- **向笔记中添加文本**：  
  ```bash
  grizzly append --note_id "添加的文本"
  ```

- **列出所有标签**：  
  ```bash
  grizzly tags
  ```

- **搜索笔记**：  
  ```bash
  grizzly search --tag "关键词"
  ```

## 命令选项

- **--dry-run**：预览操作结果，不执行实际操作。
- **--print-url**：显示 x-callback URL。
- **--enable-callback**：等待 Bear 的响应（用于读取笔记数据）。
- **--json**：以 JSON 格式输出结果（当使用回调时）。
- **--token-file PATH**：指定 Bear API 令牌文件的路径。

## 配置

`grizzly` 会按照以下优先级读取配置信息：
1. 命令行参数。
2. 环境变量（`GRIZZLY_TOKEN_FILE`、`GRIZZLY_CALLBACK_URL`、`GRIZZLY_TIMEOUT`）。
3. 当前目录下的 `.grizzly.toml` 文件。
4. `~/.config/grizzly/config.toml` 文件。

**`.config/grizzly/config.toml` 文件示例：**
```toml
[grizzly]
token_file = ~/.config/grizzly/token
callback_url = https://your_bear_app/api/callback
timeout = 10
```

**注意事项：**
- 执行这些命令时，Bear 应用必须处于运行状态。
- 笔记 ID 是 Bear 的内部标识符，可以在笔记信息或回调结果中查看。
- 如果需要从 Bear 读取数据，请使用 `--enable-callback` 选项。
- 某些操作（如添加文本、添加标签、打开特定笔记）需要有效的访问令牌。