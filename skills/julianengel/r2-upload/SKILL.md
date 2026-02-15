---
name: Send Me My Files - R2 upload with short lived signed urls
description: 将文件上传到 Cloudflare R2、AWS S3 或任何支持 S3 的存储服务，并生成具有可配置过期时间的安全预签名下载链接。
summary: TypeScript-based MCP skill for uploading files to cloud storage (R2, S3, MinIO) with secure, temporary download links. Features multi-bucket support, interactive onboarding, and 5-minute default expiration.
---

# 将文件上传至 Cloudflare R2 并生成临时签名链接

**功能：**  
- 将文件上传至 Cloudflare R2 或任何支持 S3 协议的存储服务；  
- 生成带有自定义过期时间的签名下载链接；  
- 支持多种 S3 兼容的存储服务（如 R2、AWS S3、MinIO 等）；  
- 支持配置多个存储桶；  
- 自动检测文件内容类型。  

**配置方法：**  
创建 `~/.r2-upload.yml` 文件（或设置环境变量 `R2_UPLOAD_CONFIG`）：  

### Cloudflare R2 的配置步骤：  
1. 登录 Cloudflare 控制台 → 进入 R2 界面；  
2. 创建一个新的存储桶；  
3. 访问 R2 API Tokens 页面（地址：`https://dash.cloudflare.com/<ACCOUNT_ID>/r2/api-tokens`）；  
4. 创建一个新的 API 令牌：  
   - **注意：** 请确保该令牌仅用于指定的存储桶；  
   - 授权权限：对象读写权限；  
5. 复制访问密钥（Access Key ID）和秘密访问密钥（Secret Access Key）；  
6. 使用以下格式的 API 端点：`https://<account_id>.r2.cloudflarestorage.com`；  
7. 将 `region` 设置为 `auto`。  

### AWS S3 的配置步骤：  
（具体配置方法请参考 AWS 官方文档。）  

**使用方法：**  
- 使用 `r2_upload` 命令上传文件并获取签名链接；  
- 使用 `r2_list` 命令查看最近上传的文件列表；  
- 使用 `r2_delete` 命令删除文件。  

**其他命令：**  
- `r2_upload`：上传文件并获取签名链接；  
- `r2_list`：列出最近上传的文件；  
- `r2_delete`：删除文件。  

**环境变量：**  
- `R2_UPLOAD_CONFIG`：配置文件的路径（默认值：`~/.r2-upload.yml`）；  
- `R2_DEFAULT_BUCKET`：覆盖默认存储桶；  
- `R2_DEFAULT_EXPIRES`：默认过期时间（单位：秒，默认值：300 秒 = 5 分钟）。  

**注意事项：**  
- 上传的文件将保留其原始文件名（除非指定了 `--key` 参数）；  
- 系统会自动为文件添加 UUID 前缀以防止文件名冲突（例如：`abc123/file.pdf`）；  
- 文件内容类型会根据文件扩展名自动检测；  
- 生成的签名链接会在配置的过期时间后失效。  

**相关工具：**  
- `r2_upload`：用于上传文件并获取签名链接；  
- `r2_list`：用于查看文件列表；  
- `r2_delete`：用于删除文件。