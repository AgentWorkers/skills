---
name: docker-ctl
description: "通过 `podman` 检查容器、日志和镜像"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐳",
        "requires": { "bins": ["podman"] },
        "install": [],
      },
  }
---

# Docker Ctl

通过 `podman` 检查容器、日志和镜像。在 Bazzite/Fedora 系统中，`podman` 是默认的容器运行时环境，并且始终可用。

## 命令

```bash
# List running containers
docker-ctl ps

# View container logs
docker-ctl logs <container>

# List local images
docker-ctl images

# Inspect a container
docker-ctl inspect <container>
```

## 安装

无需额外安装。Bazzite 使用 `podman` 作为其容器运行时环境，因此 `podman` 已经预装好了。