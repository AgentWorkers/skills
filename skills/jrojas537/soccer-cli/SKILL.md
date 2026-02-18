---
name: "soccer-cli"
version: "1.0.0"
author: "J R"
description: "这是一个命令行工具（CLI），用于从终端查看足球比赛的比分、比赛详情以及球员数据。"
requires:
  bins:
    - name: "go"
      version: ">=1.18"
install: "install.sh"
usage: |
  soccer-cli scores "Manchester United"
  soccer-cli game <fixture_id>
  soccer-cli squad <fixture_id>
---
## soccer-cli

这是一个命令行工具，用于通过 API-Football 服务查询足球比赛比分、比赛详情和球员统计数据。

### 描述

该工具提供了一组命令，可让您在终端中快速获取足球相关数据。您可以查询您喜爱的球队的最新比分，查看特定比赛的详细事件（如进球和犯规情况），以及查看包含球员评分和出场时间的完整阵容信息。

### 安装

1. **运行安装程序：**
    ```bash
    ./install.sh
    ```
    这将编译 Go 程序，并将 `soccer-cli` 可执行文件复制到 `~/.local/bin/` 目录中。

2. **配置 API 密钥：**
    该工具需要从 [API-Football](https://www.api-football.com/) 获取 API 密钥。
    在 `~/.config/soccer-cli/config.yaml` 文件中创建配置文件：
    ```bash
    mkdir -p ~/.config/soccer-cli
    touch ~/.config/soccer-cli/config.yaml
    ```

    按照以下格式将您的 API 密钥添加到文件中：
    ```yaml
    apikey: YOUR_API_KEY_HERE
    ```

### 使用方法

- **查询球队的最新比分：**
    ```bash
    soccer-cli scores "<team-name>"
    ```
    例如：`soccer-cli scores "Real Madrid"`

- **查询比赛的详细事件：**
    （使用 `scores` 命令获取的比赛 ID）
    ```bash
    soccer-cli game <fixture_id>
    ```
    例如：`soccer-cli game 123456`

- **查询比赛的阵容和球员统计数据：**
    ```bash
    soccer-cli squad <fixture_id>
    ```
    例如：`soccer-cli squad 123456`