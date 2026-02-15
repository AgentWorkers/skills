---
name: radarr-sonarr
description: Radarr与Sonarr的集成功能，支持通过自动化服务器自动下载电影和电视剧资源。
metadata:
  openclaw:
    emoji: 🎬
    requires:
      bins: ["python3"]
    install:
      - id: deps
        kind: apt
        packages: ["python3"]
        label: Install Python 3
    config:
      - id: radarr_url
        label: Radarr URL
        type: string
        default: "http://localhost:7878"
      - id: radarr_api_key
        label: Radarr API Key
        type: secret
      - id: sonarr_url
        label: Sonarr URL
        type: string
        default: "http://localhost:8989"
      - id: sonarr_api_key
        label: Sonarr API Key
        type: secret
---
