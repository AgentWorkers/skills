---
name: firebase
description: >
  **Firebase管理API与托管OAuth的集成**  
  该功能支持对Firebase项目、Web应用、Android应用及iOS应用进行管理。  
  当用户需要列出Firebase项目、创建或管理应用、获取应用配置信息，或关联Google Analytics时，可使用此功能。  
  对于其他第三方应用，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Firebase

使用托管的 OAuth 认证来访问 Firebase Management API。您可以全面执行 CRUD 操作来管理 Firebase 项目及其应用程序（Web、Android、iOS）。

## 快速入门

```bash
# List Firebase projects
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/firebase/v1beta1/projects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/firebase/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Firebase Management API 端点路径。该网关会将请求代理到 `firebase.googleapis.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Firebase OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=firebase&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'firebase'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "firebase",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Firebase 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/firebase/v1beta1/projects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 项目操作

#### 列出项目

列出当前用户可访问的所有 Firebase 项目。

```bash
GET /firebase/v1beta1/projects
```

**响应：**
```json
{
  "results": [
    {
      "projectId": "my-firebase-project",
      "projectNumber": "123456789",
      "displayName": "My Firebase Project",
      "name": "projects/my-firebase-project",
      "resources": {
        "hostingSite": "my-firebase-project"
      },
      "state": "ACTIVE",
      "etag": "1_bc06d94f-cf77-4689-be01-576702b23f6a"
    }
  ]
}
```

#### 获取项目信息

```bash
GET /firebase/v1beta1/projects/{projectId}
```

#### 更新项目

```bash
PATCH /firebase/v1beta1/projects/{projectId}?updateMask=displayName
Content-Type: application/json

{
  "displayName": "Updated Project Name"
}
```

#### 列出可添加 Firebase 的 Google Cloud 项目

```bash
GET /firebase/v1beta1/availableProjects
```

#### 为项目添加 Firebase 服务

```bash
POST /firebase/v1beta1/projects/{projectId}:addFirebase
Content-Type: application/json

{}
```

此操作需要较长时间才能完成。您可以使用以下链接检查操作状态：

```bash
GET /firebase/v1beta1/operations/{operationId}
```

#### 获取管理员 SDK 配置

```bash
GET /firebase/v1beta1/projects/{projectId}/adminSdkConfig
```

### Web 应用程序操作

#### 列出 Web 应用程序

```bash
GET /firebase/v1beta1/projects/{projectId}/webApps
```

#### 获取 Web 应用程序信息

```bash
GET /firebase/v1beta1/projects/{projectId}/webApps/{appId}
```

#### 创建 Web 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/webApps
Content-Type: application/json

{
  "displayName": "My Web App"
}
```

#### 更新 Web 应用程序

```bash
PATCH /firebase/v1beta1/projects/{projectId}/webApps/{appId}?updateMask=displayName
Content-Type: application/json

{
  "displayName": "Updated Web App Name"
}
```

#### 获取 Web 应用程序配置

```bash
GET /firebase/v1beta1/projects/{projectId}/webApps/{appId}/config
```

**响应：**
```json
{
  "projectId": "my-firebase-project",
  "appId": "1:123456789:web:abc123",
  "apiKey": "AIzaSy...",
  "authDomain": "my-firebase-project.firebaseapp.com",
  "storageBucket": "my-firebase-project.firebasestorage.app",
  "messagingSenderId": "123456789",
  "measurementId": "G-XXXXXXXXXX",
  "projectNumber": "123456789"
}
```

#### 删除 Web 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/webApps/{appId}:remove
Content-Type: application/json

{
  "immediate": true
}
```

#### 恢复已删除的 Web 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/webApps/{appId}:undelete
Content-Type: application/json

{}
```

### Android 应用程序操作

#### 列出 Android 应用程序

```bash
GET /firebase/v1beta1/projects/{projectId}/androidApps
```

#### 获取 Android 应用程序信息

```bash
GET /firebase/v1beta1/projects/{projectId}/androidApps/{appId}
```

#### 创建 Android 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/androidApps
Content-Type: application/json

{
  "displayName": "My Android App",
  "packageName": "com.example.myapp"
}
```

#### 更新 Android 应用程序

```bash
PATCH /firebase/v1beta1/projects/{projectId}/androidApps/{appId}?updateMask=displayName
Content-Type: application/json

{
  "displayName": "Updated Android App Name"
}
```

#### 获取 Android 应用程序配置

此操作会返回 `google-services.json` 配置文件。

```bash
GET /firebase/v1beta1/projects/{projectId}/androidApps/{appId}/config
```

#### 删除 Android 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/androidApps/{appId}:remove
Content-Type: application/json

{
  "immediate": true
}
```

#### 列出 SHA 证书

```bash
GET /firebase/v1beta1/projects/{projectId}/androidApps/{appId}/sha
```

#### 添加 SHA 证书

```bash
POST /firebase/v1beta1/projects/{projectId}/androidApps/{appId}/sha
Content-Type: application/json

{
  "shaHash": "1234567890ABCDEF1234567890ABCDEF12345678",
  "certType": "SHA_1"
}
```

#### 删除 SHA 证书

```bash
DELETE /firebase/v1beta1/projects/{projectId}/androidApps/{appId}/sha/{shaId}
```

### iOS 应用程序操作

#### 列出 iOS 应用程序

```bash
GET /firebase/v1beta1/projects/{projectId}/iosApps
```

#### 获取 iOS 应用程序信息

```bash
GET /firebase/v1beta1/projects/{projectId}/iosApps/{appId}
```

#### 创建 iOS 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/iosApps
Content-Type: application/json

{
  "displayName": "My iOS App",
  "bundleId": "com.example.myapp"
}
```

#### 更新 iOS 应用程序

```bash
PATCH /firebase/v1beta1/projects/{projectId}/iosApps/{appId}?updateMask=displayName
Content-Type: application/json

{
  "displayName": "Updated iOS App Name"
}
```

#### 获取 iOS 应用程序配置

此操作会返回 `GoogleService-Info.plist` 配置文件。

```bash
GET /firebase/v1beta1/projects/{projectId}/iosApps/{appId}/config
```

#### 删除 iOS 应用程序

```bash
POST /firebase/v1beta1/projects/{projectId}/iosApps/{appId}:remove
Content-Type: application/json

{
  "immediate": true
}
```

### Google Analytics 操作

#### 获取 Analytics 详细信息

```bash
GET /firebase/v1beta1/projects/{projectId}/analyticsDetails
```

#### 添加 Google Analytics

```bash
POST /firebase/v1beta1/projects/{projectId}:addGoogleAnalytics
Content-Type: application/json

{
  "analyticsAccountId": "123456789"
}
```

#### 删除 Google Analytics

```bash
POST /firebase/v1beta1/projects/{projectId}:removeAnalytics
Content-Type: application/json

{
  "analyticsPropertyId": "properties/123456789"
}
```

### 可用的位置

#### 列出可用位置

```bash
GET /firebase/v1beta1/projects/{projectId}/availableLocations
```

## 分页

使用 `pageSize` 和 `pageToken` 进行分页：

```bash
GET /firebase/v1beta1/projects?pageSize=10&pageToken={nextPageToken}
```

当还有更多结果时，响应中会包含 `nextPageToken`：

```json
{
  "results": [...],
  "nextPageToken": "..."
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/firebase/v1beta1/projects',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/firebase/v1beta1/projects',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### 创建 Web 应用程序

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/firebase/v1beta1/projects/my-project/webApps',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'displayName': 'My New Web App'}
)
data = response.json()
```

## 注意事项

- 项目 ID 是 Firebase 项目的全球唯一标识符。
- 应用程序 ID 的格式为 `1:PROJECT_NUMBER:PLATFORM:HASH`。
- `PATCH` 请求需要一个 `updateMask` 查询参数来指定要更新的字段（例如：`?updateMask=displayName`）。
- 创建操作是异步的，并会返回一个 `Operation` 对象。
- 您可以在 `/firebase/v1beta1/operations/{operationId}` 处检查操作状态。
- 被删除的应用程序可以在 30 天内通过 `undelete` 端点恢复。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 可以防止全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量（如 `$MATON_API_KEY`）。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 Firebase 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 没有足够的权限执行请求的操作 |
| 404 | 项目或应用程序未找到 |
| 429 | 请求次数超出限制 |
| 4xx/5xx | 来自 Firebase API 的传递错误 |

## 资源

- [Firebase Management API 概述](https://firebase.google.com/docs/projects/api/workflow_set-up-and-manage-project)
- [Firebase Management REST API 参考](https://firebase.google.com/docs/reference/firebase-management/rest)
- [项目资源](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects)
- [Web 应用程序资源](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.webApps)
- [Android 应用程序资源](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.androidApps)
- [iOS 应用程序资源](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.iosApps)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)