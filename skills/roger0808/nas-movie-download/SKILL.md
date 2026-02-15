---
name: nas-movie-download
description: 通过Jackett和qBittorrent搜索和下载电影。当用户需要从种子源下载电影或视频、搜索特定电影标题或管理电影下载时，可以使用这些工具。
---

# NAS电影下载

这是一个自动化电影下载系统，使用Jackett进行种子搜索，使用qBittorrent进行下载管理。

## 配置

### 环境变量

设置以下环境变量以确保该功能正常运行：

**Jackett配置：**
- `JACKETT_URL`：Jackett服务地址（默认：http://192.168.1.246:9117）
- `JACKETT_API_KEY`：Jackett API密钥（默认：o5gp976vq8cm084cqkcv30av9v3e5jpy）

**qBittorrent配置：**
- `QB_URL`：qBittorrent网页界面地址（默认：http://192.168.1.246:8888）
- `QB_USERNAME`：qBittorrent用户名（默认：admin）
- `QB_PASSWORD`：qBittorrent密码（默认：adminadmin）

### 索引器设置

该系统支持Jackett的多种索引器。当前已配置的索引器包括：
- The Pirate Bay
- TheRARBG
- YTS

请确保这些索引器已在Jackett中启用并正确配置，以获得最佳搜索效果。

## 使用方法

### 搜索电影

仅搜索电影信息，不进行下载：

```bash
scripts/jackett-search.sh -q "Inception"
scripts/jackett-search.sh -q "The Matrix"
scripts/jackett-search.sh -q "死期将至"  # Chinese movie names supported
```

### 下载最高质量的版本

搜索并自动下载最高质量的版本：

```bash
scripts/download-movie.sh -q "Inception"
scripts/download-movie.sh -q "The Matrix"
```

### 手动下载流程

如需更精细地控制下载过程：
1. 搜索电影：`scripts/jackett-search.sh -q "电影名称"`
2. 查看搜索结果并复制磁力链接
3. 将磁力链接添加到qBittorrent：`scripts/qbittorrent-add.sh -m "magnet:?xt=urn:btih:..."`

### 测试配置

验证Jackett和qBittorrent的配置是否正确：

```bash
scripts/test-config.sh
```

## 质量优先级

系统按以下顺序优先选择电影质量：
1. **4K/UHD**：包含“4K”、“2160p”、“UHD”字样的电影
2. **1080P/全高清**：包含“1080p”、“FHD”字样的电影
3. **720P/高清**：包含“720p”、“HD”字样的电影
4. **其他**：其他质量级别的电影

使用`download-movie.sh`命令时，系统会自动选择可用种子中的最高质量版本。

## 脚本详情

### jackett-search.sh

用于在Jackett中搜索种子文件。

**参数：**
- `-q, --query`：搜索查询（必填）
- `-u, --url`：Jackett服务地址（可选，使用环境变量）
- `-k, --api-key`：API密钥（可选，使用环境变量）

**示例：**
```bash
scripts/jackett-search.sh -q "Inception" -u http://192.168.1.246:9117
```

### qbittorrent-add.sh

用于将搜索到的种子文件添加到qBittorrent。

**参数：**
- `-m, --magnet`：磁力链接（必填）
- `-u, --url`：qBittorrent服务地址（可选，使用环境变量）
- `-n, --username`：用户名（可选，使用环境变量）
- `-p, --password`：密码（可选，使用环境变量）

**示例：**
```bash
scripts/qbittorrent-add.sh -m "magnet:?xt=urn:btih:..."
```

### download-movie.sh

一键完成搜索和下载。

**参数：**
- `-q, --query`：电影名称（必填）

**示例：**
```bash
scripts/download-movie.sh -q "The Matrix"
```

## 提示与最佳实践：
- 使用英文电影名称以获得更好的搜索结果
- 如果搜索无结果，请检查Jackett索引器的状态
- 监控qBittorrent的下载进度
- 下载4K内容时请考虑存储空间
- 定期测试配置以确保服务正常运行

## 故障排除

### 无搜索结果
1. 确认Jackett正在运行：`curl http://192.168.1.246:9117`
2. 检查Jackett中是否启用了相应的索引器
- 尝试使用英文电影名称进行搜索
- 确认API密钥是否正确

### qBittorrent连接失败
1. 确认qBittorrent正在运行
- 检查qBittorrent设置中是否启用了网页界面
- 核对用户名和密码
- 确保网络连接正常

### 权限问题

确保脚本具有执行权限：

```bash
chmod +x scripts/*.sh
```

## 安全注意事项：
- 保护API密钥，切勿将其提交到版本控制系统中
- 尽可能使用HTTPS连接
- 考虑为种子下载流量设置VPN
- 定期检查qBittorrent是否存在未经授权的下载行为

## 依赖软件
- `curl`：用于发送HTTP请求
- `jq`：用于解析JSON数据
- Bash shell

如果未安装`jq`，请先安装它：
```bash
apt-get install jq
```