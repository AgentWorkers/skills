---
name: feishu-user
description: Feishu 文档操作（用户访问令牌版本）：使用用户访问令牌进行身份验证。当您需要读取、创建、写入或追加 Feishu 文档时，请使用该令牌。
---
# 使用 useru 访问 Feishu 文档的操作

需要使用 Feishu 的访问令牌（`user_access_token`）进行身份验证。可以通过 REST API 直接调用 Feishu 的开放 API。

## 安装依赖项

```bash
pip install requests
```

## 快速入门

```python
from feishu_client import FeishuClient

# 初始化客户端
client = FeishuClient(user_access_token="u-xxx")
```

## 获取用户访问令牌

### 第一步：从 Feishu Open 平台获取应用凭据

准备以下信息：
- **APP_ID**：应用 ID（来自 Feishu Open 平台的应用设置）
- **APP_SECRET**：应用密钥（来自 Feishu Open 平台的应用设置）
- **REDIRECT_URI**：授权回调 URL

启用以下权限：
- `docx:document`：文档操作
- `drive:drive.search:readonly`：云盘搜索
- `search:docs:read`：文档搜索

### 第二步：生成授权 URL

```bash
https://accounts.feishu.cn/open-apis/authen/v1/authorize?client_id={YOUR_APP_ID}&response_type=code&redirect_uri={YOUR_REDIRECT_URI}&scope=docx%3Adocument%20drive%3Adrive.search%3Areadonly%20search%3Adocs%3Aread
```

### 第三步：交换获取令牌

```bash
curl -X POST "https://open.feishu.cn/open-apis/authen/v1/access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "authorization_code",
    "code": "{YOUR_CODE}",
    "app_id": "{YOUR_APP_ID",
    "app_secret": "{YOUR_APP_SECRET}"
  }
```

返回的 `access_token` 即为您的 `user_access_token`。

---

## 使用示例

```python
from feishu_client import FeishuClient

# 初始化客户端
client = FeishuClient(user_access_token="u-xxx")

# 读取文档
content = client.read_doc("doc_token")
print(content)

# 创建文档
new_token = client.create_doc("我的新文档")
print(f"新文档的令牌：{new_token}")

# 写入文档
client.write_doc("doc_token", "# 标题\n\n内容")

# 添加内容
client.append_doc("doc_token", "## 新章节\n\n更多内容")

# 列出所有文档块
blocks = client.list_blocks("doc_token")
for block in blocks:
    print(block)

# 获取特定文档块
block = client.get_block("doc_token", "block_id")

# 更新文档块
client.update_block("doc_token", "block_id", "新内容")

# 删除文档块
client.delete_block("doc_token", "block_id")
```

---

## 方便函数

如果不想手动创建客户端，可以直接使用以下函数：

```python
from feishu_client import read_document, create_document, write_document, append_document

# 读取文档
content = read_document("doc_token", user_access_token="u-xxx")

# 创建文档
new_token = create_document("标题", user_access_token="u-xxx")

# 写入文档
write_document("doc_token", "# 内容", user_access_token="u-xxx")

# 添加内容
append_document("doc_token", "## 更多内容", user_access_token="u-xxx")
```

---

## API 参考

### FeishuClient

| 方法 | 描述 |
|--------|-------------|
| `read_doc(doc_token)` | 读取文档内容 |
| `create_doc(title, folder_token)` | 创建新文档 |
| `write_doc(doc_token, content)` | 写入文档（覆盖现有内容） |
| `append_doc(doc_token, content)` | 在文档末尾添加内容 |
| `list_blocks(doc_token)` | 列出所有文档块 |
| `get_block(doc_token, block_id)` | 获取特定文档块 |
| `update_block(doc_token, block_id, content)` | 更新文档块内容 |
| `delete_block(doc_token, block_id)` | 删除文档块 |

---

## 注意事项

1. `user_access_token` 有有效期，需要定期刷新。
2. 授权 URL 中的 `scope` 必须在 Feishu Open 平台上启用。
3. 该功能使用用户身份访问个人云文档。

---

## 相关链接

- Feishu Open 平台：https://open.feishu.cn
- 文档 API：https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDMzCM4ATm

---

## 令牌自动刷新

使用 `feishu_token.py` 脚本实现令牌自动刷新。

### 安装依赖项

```bash
pip install requests
```

### 首次授权

```bash
# 1. 生成授权 URL
python feishu_token.py --app-id YOUR_APP_ID --app-secret YOUR_SECRET --redirect-uri YOUR_REDIRECT_URI --url
```

用户授权后，系统会回调到 `YOUR_REDIRECT_URI?code=XXX`。

```bash
# 2. 使用授权码获取令牌
python feishu_token.py --app-id YOUR_APP_ID --app-secret YOUR_SECRET --code AUTH_CODE
```

令牌会自动保存到 `~/.config/claw-feishu-user/config.json` 文件中。

### 刷新令牌

```bash
python feishu_token.py --app-id YOUR_APP_ID --app-secret YOUR_SECRET --refresh
```

### 在代码中获取令牌

```python
import json
import os

# 读取缓存的令牌
config_path = os.path.expanduser("~/.config/claw-feishu-user/config.json")
with open(config_path) as f:
    config = json.load(f)

# 使用令牌
client = FeishuClient(user_access_token=config["access_token"])
```