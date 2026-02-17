# 技能：deep-scraper

## 概述
这是一个高性能的工程工具，用于深度网络爬取（deep web scraping）。它利用容器化的 Docker + Crawlee（Playwright）环境来突破 YouTube 和 X/Twitter 等复杂网站的安全防护机制，从而获取“拦截级别”的原始数据。

## 需求
1. **Docker**：必须已在主机上安装并运行。
2. **镜像**：使用标签 `clawd-crawlee` 构建环境。
    *   构建命令：`docker build -t clawd-crawlee skills/deep-scraper/`

## 集成指南
只需将 `skills/deep-scraper` 目录复制到您的 `skills/` 文件夹中。确保 Dockerfile 位于技能目录内，以实现独立部署。

## 标准接口（CLI）
```bash
docker run -t --rm -v $(pwd)/skills/deep-scraper/assets:/usr/src/app/assets clawd-crawlee node assets/main_handler.js [TARGET_URL]
```

## 输出规范（JSON）
爬取结果以 JSON 字符串的形式输出到标准输出（stdout）：
- `status`：SUCCESS | PARTIAL | ERROR
- `type`：TRANSCRIPT | DESCRIPTION | GENERIC
- `videoId`：（针对 YouTube）经过验证的视频 ID。
- `data`：核心文本内容或字幕。

## 核心规则
1. **ID 验证**：所有 YouTube 相关操作必须验证视频 ID，以防止缓存污染。
2. **隐私保护**：严禁爬取受密码保护或非公开的个人信息。
3. **数据优化**：自动去除广告和无关内容，提供适合大型语言模型（LLM）处理的纯净数据。