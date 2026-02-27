# linkedin-video-dl

使用 `linkedin-video-dl` 从 LinkedIn 帖子中下载视频。该工具接受一个公开帖子的 URL，并将 MP4 视频保存到当前目录。对于公开帖子，无需任何身份验证。

## 设置（只需一次）

```bash
cd linkedin-video-dl && go build -o linkedin-video-dl .
```

或者全局安装：

```bash
go install .
```

## 常用命令

下载视频：`linkedin-video-dl "<post-url>"`

## 示例

```bash
linkedin-video-dl "https://www.linkedin.com/posts/midudev_anthropic-ha-acusado-a-deepseek-activity-7432111870431449089-9evi"
```

## 注意事项

- 仅适用于包含视频的 **公开** LinkedIn 帖子。
- 无需身份验证或 API 密钥。
- 完全依赖 Go 的标准库开发，无外部依赖。
- 视频从 LinkedIn 的 CDN（`dms.licdn.com`）下载，以最佳可用质量进行传输。
- 下载过程中会使用临时文件 `.tmp`，下载完成后会重命名文件——因此可以安全地中断下载而不会导致文件损坏。
- 输出文件名来源于帖子的 URL（截取前 80 个字符）。
- 如果已存在同名文件，则会跳过下载，以避免覆盖原有文件。
- 下载过程中会显示进度条，包括下载百分比、已下载大小和总大小。