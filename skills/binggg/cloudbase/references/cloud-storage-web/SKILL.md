---
name: cloud-storage-web
description: 使用 Web SDK (@cloudbase/js-sdk) 的 CloudBase 云存储完整指南——包括上传、下载、临时 URL、文件管理以及最佳实践。
alwaysApply: false
---
# 云存储 Web SDK

在构建需要通过 `@cloudbase/js-sdk`（Web SDK）来上传、下载或管理文件的 Web 应用程序时，请使用此技能。

## 适用场景

当您在 Web 应用程序中需要进行以下文件存储操作时，请使用此技能：
- 从浏览器将文件上传到 CloudBase 云存储
- 为存储的文件生成临时下载链接
- 从云存储中删除文件
- 从云存储下载文件到本地浏览器

**不适用场景**：
- 小程序文件操作（请使用小程序专属的技能）
- 后端文件操作（请使用 Node SDK 技能）
- 数据库操作（请使用数据库技能）

## 使用方法（针对编程代理）

1. **初始化 CloudBase SDK**
   - 询问用户的 CloudBase 环境 ID
   - 始终使用以下标准初始化模式

2. **选择合适的存储方法**
   - `uploadFile`：用于将文件从浏览器上传到云存储
   - `getTempFileURL`：用于生成临时下载链接
   - `deleteFile`：用于从存储中删除文件
   - `downloadFile`：用于将文件下载到浏览器

3. **处理 CORS 需求**
   - 告知用户将他们的域名添加到 CloudBase 控制台的安全域名列表中
   - 这可以防止文件操作过程中出现 CORS 错误

4. **遵循文件路径规则**
   - 使用有效的字符：`[0-9a-zA-Z]`、`/`、`!`、`-`、`_`、`.`、`:`、`*`、中文字符
   - 使用 `/` 来构建文件夹结构（例如：`folder/file.jpg`）

---

## SDK 初始化

```javascript
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({
  env: "your-env-id", // Replace with your CloudBase environment ID
});
```

**初始化规则**：
- 始终使用上述同步初始化模式
- 不要通过动态导入来延迟加载 SDK
- 在整个应用程序中保持一个共享的 `app` 实例

## 文件上传（uploadFile）

### 基本用法

```javascript
const result = await app.uploadFile({
  cloudPath: "folder/filename.jpg", // File path in cloud storage
  filePath: fileInput.files[0],     // HTML file input element
});

// Result contains:
{
  fileID: "cloud://env-id/folder/filename.jpg", // Unique file identifier
  // ... other metadata
}
```

### 带进度显示的高级上传

```javascript
const result = await app.uploadFile({
  cloudPath: "uploads/avatar.jpg",
  filePath: selectedFile,
  method: "put", // "post" or "put" (default: "put")
  onUploadProgress: (progressEvent) => {
    const percent = Math.round(
      (progressEvent.loaded * 100) / progressEvent.total
    );
    console.log(`Upload progress: ${percent}%`);
    // Update UI progress bar here
  }
});
```

### 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `cloudPath` | 字符串 | 是 | 包含文件名的绝对路径（例如：“folder/file.jpg”） |
| `filePath` | 文件对象 | 是 | HTML 文件输入对象 |
| `method` | “post” \| “put” | 否 | 上传方法（默认：“put”） |
| `onUploadProgress` | 函数 | 否 | 进度回调函数 |

### 文件路径规则
- **有效字符**：`[0-9a-zA-Z]`、`/`、`!`、`-`、`_`、`.`、`:`、`*`、中文字符
- **无效字符**：其他特殊字符
- **结构**：使用 `/` 来创建文件夹层次结构
- **示例**：
  - `"avatar.jpg"`
  - `"uploads/avatar.jpg"`
  - `"user/123/avatar.jpg"`

### CORS 配置

**⚠️ 重要提示：** 为防止 CORS 错误，请将您的域名添加到 CloudBase 控制台：
1. 访问 CloudBase 控制台 → 环境 → 安全源 → 安全域名
2. 添加您的前端域名（例如：`https://your-app.com`、`http://localhost:3000`）
3. 如果出现 CORS 错误，请删除并重新添加该域名

## 临时下载链接（getTempFileURL）

### 基本用法

```javascript
const result = await app.getTempFileURL({
  fileList: [
    {
      fileID: "cloud://env-id/folder/filename.jpg",
      maxAge: 3600 // URL valid for 1 hour (seconds)
    }
  ]
});

// Access the download URL
result.fileList.forEach(file => {
  if (file.code === "SUCCESS") {
    console.log("Download URL:", file.tempFileURL);
    // Use this URL to download or display the file
  }
});
```

### 多个文件

```javascript
const result = await app.getTempFileURL({
  fileList: [
    {
      fileID: "cloud://env-id/image1.jpg",
      maxAge: 7200 // 2 hours
    },
    {
      fileID: "cloud://env-id/document.pdf",
      maxAge: 86400 // 24 hours
    }
  ]
});
```

### 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `fileList` | 数组 | 是 | 文件对象数组 |

#### 文件列表项结构

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `fileID` | 字符串 | 是 | 云存储文件 ID |
| `maxAge` | 数字 | 是 | URL 的有效期限（以秒为单位）

### 响应结构

```javascript
{
  code: "SUCCESS",
  fileList: [
    {
      code: "SUCCESS",
      fileID: "cloud://env-id/folder/filename.jpg",
      tempFileURL: "https://temporary-download-url"
    }
  ]
}
```

### 最佳实践
- 根据使用场景设置合适的 `maxAge`（1 小时到 24 小时）
- 在响应中处理 `SUCCESS`/`ERROR` 代码
- 使用临时链接进行私有文件访问
- 如有需要，可以缓存链接，但需尊重过期时间

## 文件删除（deleteFile）

### 基本用法

```javascript
const result = await app.deleteFile({
  fileList: [
    "cloud://env-id/folder/filename.jpg"
  ]
});

// Check deletion results
result.fileList.forEach(file => {
  if (file.code === "SUCCESS") {
    console.log("File deleted:", file.fileID);
  } else {
    console.error("Failed to delete:", file.fileID);
  }
});
```

### 多个文件

```javascript
const result = await app.deleteFile({
  fileList: [
    "cloud://env-id/old-avatar.jpg",
    "cloud://env-id/temp-upload.jpg",
    "cloud://env-id/cache-file.dat"
  ]
});
```

### 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `fileList` | 字符串数组 | 是 | 要删除的文件 ID 数组 |

### 响应结构

```javascript
{
  fileList: [
    {
      code: "SUCCESS",
      fileID: "cloud://env-id/folder/filename.jpg"
    }
  ]
}
```

### 最佳实践
- 在确认删除成功之前，请始终检查响应代码
- 用于清理操作（如旧头像、临时文件等）
- 考虑批量删除以提高效率

## 文件下载（downloadFile）

### 基本用法

```javascript
const result = await app.downloadFile({
  fileID: "cloud://env-id/folder/filename.jpg"
});

// File is downloaded to browser default download location
```

### 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `fileID` | 字符串 | 是 | 云存储文件 ID |

### 响应结构

```javascript
{
  // Success response (no specific data returned)
  // File is downloaded to browser
}
```

### 最佳实践
- 用于用户发起的下载（文件保存对话框）
- 对于程序化文件访问，请使用 `getTempFileURL`
- 适当处理下载错误

## 错误处理

所有存储操作都应包含适当的错误处理：

```javascript
try {
  const result = await app.uploadFile({
    cloudPath: "uploads/file.jpg",
    filePath: selectedFile
  });

  if (result.code) {
    // Handle error
    console.error("Upload failed:", result.message);
  } else {
    // Success
    console.log("File uploaded:", result.fileID);
  }
} catch (error) {
  console.error("Storage operation failed:", error);
}
```

### 常见错误代码
- `INVALID_PARAM`：参数无效
- `PERMISSION_DENIED`：权限不足
- `RESOURCE_NOT_FOUND`：文件未找到
- `SYS_ERR`：系统错误

## 最佳实践
1. **文件组织**：使用一致的文件夹结构（如 `uploads/`、`avatars/`、`documents/`）
2. **命名规范**：如有需要，使用包含时间戳的描述性文件名
3. **进度反馈**：显示上传进度以提升用户体验
4. **清理**：删除临时/未使用的文件以节省存储空间
5. **安全性**：上传前验证文件类型和大小
6. **缓存**：适当缓存下载链接，但需尊重过期时间
7. **批量操作**：尽可能使用数组进行多个文件的批量操作

## 性能考虑
1. **文件大小限制**：注意 CloudBase 的文件大小限制
2. **并发上传**：限制并发上传数量以防止浏览器过载
3. **进度监控**：对于大文件上传，使用进度回调
4. **临时链接**：仅在需要时生成链接，并设置合理的过期时间

## 安全性考虑
1. **域名白名单**：始终配置安全域名列表以防止 CORS 问题
2. **访问控制**：使用适当的文件权限（公共访问 vs 私有访问）
3. **URL 过期**：为临时链接设置合理的过期时间
4. **用户权限**：确保用户只能访问自己的文件