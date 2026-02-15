---
name: tautulli
description: 通过 Tautulli API 监控 Plex 的活动及统计数据。可以查看正在观看的人、浏览历史记录、获取库的统计信息以及服务器详情。
metadata:
  openclaw:
    emoji: 📊
    requires:
      bins:
        - curl
        - jq
      env:
        - TAUTULLI_URL
        - TAUTULLI_API_KEY
---

# Tautulli

通过 Tautulli API 监控 Plex 媒体服务器的活动。

## 设置

配置环境变量：
- `TAUTULLI_URL` – Tautulli 实例的 URL（例如：`http://192.168.1.100:8181`）
- `TAUTULLI_API_KEY` – 在“设置” → “Web 界面”中获取的 API 密钥

## 命令

### 当前活动

```bash
bash {baseDir}/scripts/activity.sh
```

显示活跃的流媒体信息，包括用户、标题、进度、质量和播放器。

### 观看历史

```bash
bash {baseDir}/scripts/history.sh [limit]
```

默认显示最近 10 条记录；可以通过传递数字来查看更多记录。

### 库统计

```bash
bash {baseDir}/scripts/libraries.sh
```

列出库中的各个部分及其对应的媒体数量。

### 最新添加的媒体

```bash
bash {baseDir}/scripts/recent.sh [limit]
```

显示最近添加的媒体文件；默认显示 10 条记录。

### 用户统计

```bash
bash {baseDir}/scripts/users.sh
```

列出用户的总观看时长以及最后登录日期。

### 服务器信息

```bash
bash {baseDir}/scripts/server.sh
```

显示 Plex 服务器的名称、版本、平台以及连接状态。

## API 参考

所有 Tautulli API 调用都使用以下格式：

```
$TAUTULLI_URL/api/v2?apikey=$TAUTULLI_API_KEY&cmd=<command>
```

常用命令：`get_activity`、`get_history`、`get_libraries`、`get_recently_added`、`get_users`、`get_server_info`。