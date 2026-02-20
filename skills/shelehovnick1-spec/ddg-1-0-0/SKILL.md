---
name: ddg
description: 使用 `ddgr`（即终端中的 DuckDuckGo）从命令行执行以隐私保护为导向的网络搜索。适用于以下场景：  
1. 从终端中进行网络搜索；  
2. 在不打开浏览器的情况下使用 DuckDuckGo；  
3. 以文本格式快速获取搜索结果；  
4. 进行无痕搜索（避免被追踪）；  
5. 通过终端使用 DuckDuckGo 的特殊搜索指令（如 `!`）。
---

# ddgr - 通过终端使用 DuckDuckGo

**ddgr** 是一个命令行工具，用于通过终端搜索 DuckDuckGo。它提供了快速且注重隐私的网页搜索功能，无需打开浏览器。

## 安装

### 通过 Snap（推荐用于 Ubuntu）：
```bash
sudo snap install ddgr
```

### 通过 PPA（Package Archive）：
```bash
sudo add-apt-repository ppa:twodopeshaggy/jarun
sudo apt-get update
sudo apt-get install ddgr
```

### 从源代码安装：
```bash
git clone https://github.com/jarun/ddgr.git
cd ddgr
sudo make install
```

**依赖项：** Python 3.8 或更高版本

## 基本用法

### 简单搜索（非交互式）：
```bash
snap run ddgr "search query" --np
```

### 指定搜索结果数量：
```bash
snap run ddgr "search query" --num 5 --np
```

### 设置搜索时间限制：
```bash
snap run ddgr "query" --time w --np    # past week
snap run ddgr "query" --time m --np    # past month
snap run ddgr "query" --time y --np    # past year
```

### 搜索特定网站：
```bash
snap run ddgr "query" --site github.com --np
```

### 以 JSON 格式输出结果：
```bash
snap run ddgr "query" --json --np
```

### 在浏览器中打开第一个搜索结果：
```bash
snap run ddgr "query" --ducky
```

## 交互式模式

不使用 `--np` 选项即可进入交互式模式：
```bash
snap run ddgr "search query"
```

**交互式命令：**
- `1`, `2`, `3`... → 在浏览器中打开搜索结果
- `n` → 切换到下一页结果
- `p` → 切换到上一页结果
- `q` 或 `Ctrl+D` → 退出
- `?` → 显示帮助信息

## 高级选项

| 选项 | 描述 |
|--------|-------------|
| `-n N`, `--num N` | 每页显示 N 个结果（0-25，默认为 10） |
| `-r REG`, `--reg REG` | 按地区搜索（例如：'us-en', 'uk-en'） |
| `-t SPAN`, `--time SPAN` | 时间限制：d（天）、w（周）、m（月）、y（年） |
| `-w SITE`, `--site SITE` | 搜索特定网站 |
| `-x`, `--expand` | 显示完整的 URL |
| `--json` | 以 JSON 格式输出结果 |
| `--ducky` | 在浏览器中打开第一个搜索结果 |
| `--np`, `--noprompt` | 非交互式模式 |
| `--unsafe` | 禁用安全搜索功能 |

## 使用 DuckDuckGo 的特殊搜索指令（“Bangs”）

可以使用特殊的搜索指令来搜索特定网站：
```bash
snap run ddgr "!w Linux" --np        # Wikipedia search
snap run ddgr "!yt music" --np       # YouTube search
snap run ddgr "!gh python" --np      # GitHub search
snap run ddgr "!a books" --np        # Amazon search
```

## 通过别名简化使用

将以下命令添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：
```bash
alias ddg='snap run ddgr'
```

然后使用：
```bash
ddg "search query" --np
```

## 隐私特性

- 不会跟踪用户行为或生成用户画像
- 默认启用“不跟踪”功能
- 支持通过 Tor 网络进行搜索（需使用代理）
- 支持 HTTPS 代理
- 不会保存搜索历史记录

## 示例

### 搜索科技新闻：
```bash
snap run ddgr "latest AI news 2025" --num 5 --np
```

### 查找 Ubuntu 教程：
```bash
snap run ddgr "Ubuntu tutorial" --site askubuntu.com --np
```

### 搜索最新的 Python 文档：
```bash
snap run ddgr "Python 3.12 features" --time m --np
```

### 使用特殊指令搜索 Wikipedia：
```bash
snap run ddgr "!w OpenClaw" --np
```

## 故障排除

**命令未找到：**
- 确保已通过 Snap 安装了 ddgr：`sudo snap install ddgr`
- 使用完整命令：`snap run ddgr` 而不是仅输入 `ddgr`

**没有搜索结果：**
- 检查网络连接
- 尝试不使用 `--np` 选项以查看是否可以进入交互式模式
- 确认在您的地区可以访问 DuckDuckGo

**响应缓慢：**
- DuckDuckGo 的 HTML 界面可能比主网站响应更慢
- 使用 `--time` 选项按时间范围限制搜索结果以加快查询速度

## 更多信息

- GitHub：https://github.com/jarun/ddgr
- DuckDuckGo：https://duckduckgo.com
- 特殊搜索指令（Bangs）：https://duckduckgo.com/bang