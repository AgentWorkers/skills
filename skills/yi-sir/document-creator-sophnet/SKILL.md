# 自动上传到SophNet的文档创建工具

## 描述

这是一个集成的文档创建功能，支持生成Word文档（DOCX）和PowerPoint演示文稿（PPTX），并能够自动将生成的文档上传到开源软件仓库（OSS），同时返回文档的URL。

## 使用方法

```bash
# Create document using skill
openclaw document-creator /path/to/your/file.txt

# Or call via session
# In OpenClaw session: Create document /path/to/file.png
```

## 配置要求

- 设置 `SOPH_API_KEY` 环境变量
- 或者在OpenClaw的配置文件中配置SophNet的API密钥

## 支持的参数

- `file_path`：要上传的本地文件路径（必需）

## 返回值

- 成功：返回带有签名信息的URL字符串
- 失败：抛出异常并显示错误信息

## 依赖项

- Python 3.7及以上版本
- requests库
- OpenClaw的配置文件及相应的访问权限