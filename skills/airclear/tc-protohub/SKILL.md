---
name: tc-protohub
description: 在 ProtoHub 上管理原型。当用户需要上传目录或 ZIP 文件作为原型、更新现有原型、列出所有原型或获取预览链接时，请使用此功能。该功能支持自动打包文件夹、强制校验入口文件（index.html），并允许用户通过名称搜索原型以进行更新。
---
# 技能：ProtoHub AI 代理集成

## 目的
该技能允许 AI 代理在 ProtoHub 上管理原型。它提供了自动化工具，用于打包、发布以及在 ProtoHub 私有沙箱中查找原型（文件夹或 ZIP 文件）。

## 功能
- **自动化发布：** 使用目录或 ZIP 文件来创建/更新原型。
- **入口点验证：** 在上传前自动检查是否存在 `index.html` 文件。
- **原型查找：** 列出现有的原型或通过名称搜索以获取原型 ID。
- **预览管理：** 获取公共 URL 以供演示使用。

## 必需配置
在执行任何操作之前，AI 代理必须验证以下环境变量是否已设置：
- `PROTOHUB_API_KEY`：用于身份验证。
- `PROTOHUB_URL`：ProtoHub 服务器的基地址（默认值：`http://localhost:48080`）。

**严格验证规则：**
如果这些环境变量中的任何一个缺失，或者用户当前会话中没有提供这些变量，代理 **严禁** 尝试运行脚本，也不允许使用占位符值进行重试。相反，应立即要求用户提供缺失的配置信息。

### 设置方法：
```bash
export PROTOHUB_API_KEY="your-api-key"
export PROTOHUB_URL="http://localhost:48080"
```

## 推荐工具：publish.py

### 使用示例

#### 1. 上传目录作为新原型
```bash
python skills/tc-protohub/scripts/publish.py publish ./my-dist-folder --name "My Prototype Name"
```

#### 2. 更新现有原型
在保持相同 ID 和 URL 的情况下覆盖原有内容。
```bash
python skills/tc-protohub/scripts/publish.py publish ./my-dist-folder --id 1024
```

#### 3. 列出原型（按名称搜索）
当用户请求“更新‘登录页面’原型”时，此功能非常有用。
```bash
python skills/tc-protohub/scripts/publish.py list --name "Login Page"
```

#### 4. 获取预览链接
```bash
python skills/tc-protohub/scripts/publish.py get-link 1024
```

## 最佳实践
- **文件夹结构：** 确保 `index.html` 文件位于目录或 ZIP 文件的根目录中。
- **智能更新：**
  - 如果用户请求更新某个原型但未提供 ID，先使用 `publish.py list --name "..."` 来查找匹配的原型。
  - 如果找到唯一匹配项，则使用其 ID 进行更新。
  - 如果找不到匹配项或找到多个匹配项，应要求用户提供更多信息或创建一个新的原型。
- **API 基地址：** 默认值为 `http://localhost:48080`。可以通过 `PROTOHUB_URL` 环境变量或 `--url` 标志进行覆盖。
- **错误处理：**
  - `401 未授权`：API 密钥缺失或无效。
  - `404 未找到`：指定的 `prototypeId` 不存在。
  - `缺少 index.html`：脚本将中止上传，以防止预览页面显示错误。