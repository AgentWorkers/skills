---
name: rednote
description: 当用户询问如何在终端中运行 `@skills-store/rednote` 的命令（如 `browser`、`search`、`env`、`status`、`check-login`、`login`、`home`、`get-feed-detail` 或 `get-profile`）时，请参考以下说明。
---
# Rednote 命令

请仅将以下内容用于 `@skills-store/rednote` 的命令行界面（CLI）。

重点在于告诉用户需要运行哪个命令、哪些参数是必需的，以及命令的执行顺序。

## 推荐的命令格式

优先展示已发布的包示例：

```bash
npx -y @skills-store/rednote <command> [...args]
```

如果用户需要全局安装，请显示以下命令：

```bash
npm install -g @skills-store/rednote
bun add -g @skills-store/rednote
```

全局安装完成后，可执行文件的名称为 `rednote`，而不是 `@skills-store/rednote`：

```bash
rednote <command> [...args]
```

仅当用户明确要开发 CLI 时，才显示与本地仓库相关的命令。

## 命令执行顺序

对于大多数操作任务，请按照以下顺序执行命令：

1. `env`
2. `browser list` 或 `browser create`
3. `browser connect`
4. `login` 或 `check-login`
5. `status`
6. `home`, `search`, `get-feed-detail`, 或 `get-profile`

## 快速参考

### `browser`

- 列出浏览器实例：
  ```bash
rednote browser list
```

- 创建浏览器实例：
  ```bash
rednote browser create --name seller-main --browser chrome --port 9222
```

- 连接到某个实例：
  ```bash
rednote browser connect --instance seller-main
```

- 使用指定的配置文件路径连接到实例：
  ```bash
rednote browser connect --browser edge --user-data-dir /tmp/edge-profile --port 9223
```

- 删除某个实例：
  ```bash
rednote browser remove --name seller-main
```

每当用户需要设置浏览器、管理配置文件或为后续命令创建可重用的实例时，可以使用 `browser` 命令。

### `env`

- 显示运行时和存储信息：
  ```bash
rednote env
rednote env --format json
```

当用户需要调试安装过程或进行本地配置时，请首先使用 `env` 命令。

### `status`

- 检查所选实例的状态：
  ```bash
rednote status --instance seller-main
```

使用 `status` 命令可以确认实例是否存在、是否正在运行以及用户是否已登录。

### `check-login`

- 仅用于检查登录状态：
  ```bash
rednote check-login --instance seller-main
```

当用户想要确认账户会话是否仍然有效时，可以使用此命令。

### `login`

- 打开实例的登录流程：
  ```bash
rednote login --instance seller-main
```

如果在执行 `browser connect` 后账户尚未认证，请使用 `login` 命令进行登录。

### `home`

- 读取主页内容：
  ```bash
rednote home --instance seller-main --format md --save
```

当用户想要查看当前的主页内容或将内容保存到磁盘时，可以使用 `home` 命令。

### `search`

- 按关键词搜索：
  ```bash
rednote search --instance seller-main --keyword 护肤
rednote search --instance seller-main --keyword 护肤 --format json --save ./output/search.jsonl
```

当用户希望根据关键词查找 RED 笔记，并且可以选择以机器可读的格式获取结果时，可以使用 `search` 命令。

### `get-feed-detail`

- 根据 URL 获取笔记详情：
  ```bash
rednote get-feed-detail --instance seller-main --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
```

当用户已经拥有 Xiaohongshu 笔记的 URL 并希望获取结构化的数据时，可以使用此命令。

### `get-profile`

- 根据用户 ID 获取个人资料：
  ```bash
rednote get-profile --instance seller-main --id USER_ID
```

当用户需要查看作者或账户的个人信息时，可以使用此命令。

## 参数说明

- `--instance NAME`：用于指定执行账户级操作的浏览器实例。
- `--format json`：适合脚本编写。
- `--format md`：适合直接阅读。
- `--save`：在用户需要将搜索结果或主页内容保存到磁盘时非常有用。
- `--keyword`：执行 `search` 命令时必需的参数。
- `--url`：执行 `get-feed-detail` 命令时必需的参数。
- `--id`：执行 `get-profile` 命令时必需的参数。

## 回答用户时的注意事项

- 在回答用户问题时，首先明确指出他们应该运行的具体命令。
- 仅提供完成任务所需的参数。
- 优先提供成功的操作示例。
- 如果命令需要用户登录，请务必提及 `browser connect` 和 `login` 命令。

## 故障排除

如果命令执行失败，请按以下顺序进行检查：

- 确保实例名称正确。
- 确保浏览器实例已经创建或成功连接。
- 确保用户已经为该实例完成了登录操作。
- 确认用户是否提供了必要的参数（如 `--keyword`、`--url` 或 `--id`）。