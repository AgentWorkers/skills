---
name: openclaw-trakt
description: 使用 Trakt.tv 来跟踪和推荐电视剧及电影。当用户请求节目/电影推荐、想要查看自己正在观看的内容、查看自己的观看列表，或根据观看历史获得个性化建议时，可以使用该服务。请注意：要使用全部功能，需要拥有 Trakt.tv 的 Pro 订阅账户。
---

# OpenClaw 的 Trakt.tv 集成

通过集成 Trakt.tv，您可以追踪用户的观看历史，并获得个性化的剧集/电影推荐。

**📚 Trakt API 文档：** <https://trakt.docs.apiary.io/>

## 首次设置要求

**在使用此功能之前，请运行交互式设置程序：**

### 自动设置（推荐）
```bash
python3 scripts/setup.py
```

该程序将指导您完成以下步骤：
1. 安装所需依赖项
2. 创建 Trakt 应用程序
3. 配置凭证
4. 通过 PIN 进行身份验证
5. 测试集成效果

### 手动设置
如果自动设置失败，请按照下面的手动步骤进行操作。

### OpenClaw 的交互式设置
当用户请求“安装 Trakt”或“设置 Trakt 集成”时，OpenClaw 应该：
1. 读取 `INSTALL.md` 文件以获取详细的交互式操作流程
2. 或者运行 `python3 scripts/setup.py` 并根据提示指导用户完成设置

---

## 功能

- 自动追踪用户的观看历史（Trakt 会从流媒体服务同步这些数据）
- 根据用户的观看习惯提供个性化推荐
- 访问用户的观看列表和收藏夹
- 搜索剧集和电影
- 查看热门内容

## 先决条件

1. **Python 依赖项：**
   ```bash
   # Install via pip (with --break-system-packages if needed)
   pip3 install requests
   
   # OR use a virtual environment (recommended)
   python3 -m venv ~/.openclaw-venv
   source ~/.openclaw-venv/bin/activate
   pip install requests
   ```

   或者，如果可用，可以通过 Homebrew 安装：
   ```bash
   brew install python-requests
   ```

2. **Trakt.tv 账户**（需订阅 Pro 订阅才能自动追踪观看记录）

3. **Trakt API 应用程序** - 在 <https://trakt.tv/oauth/applications> 创建

4. **配置文件：`~/.openclaw/trakt_config.json`（请参见下面的设置说明）

## 设置

### 1. 创建 Trakt 应用程序

1. 访问 <https://trakt.tv/oauth/applications>
2. 点击“新建应用程序”
3. 填写表单：
   - 名称：OpenClaw Assistant
   - 描述：个人 AI 助手集成
   - 重定向 URI：`urn:ietf:wg:oauth:2.0:oob`（用于 PIN 验证）
   - 权限：勾选所有适用的权限
4. 保存并记下您的客户端 ID（Client ID）和客户端密钥（Client Secret）

### 2. 创建配置文件

创建 `~/.openclaw/trakt_config.json` 文件，并填写您的凭证：

```json
{
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "access_token": "",
  "refresh_token": ""
}
```

将 `YOUR_CLIENT_ID_HERE` 和 `YOUR_CLIENT_SECRET_HERE` 替换为步骤 1 中的实际值。

**注意：** `access_token` 和 `refresh_token` 可以留空——它们会在身份验证后自动填充。

### 3. 身份验证

运行身份验证脚本：

```bash
python3 scripts/trakt_client.py auth
```

该脚本会生成一个 PIN 验证链接。访问该链接，完成授权后，运行以下命令：

```bash
python3 scripts/trakt_client.py auth <PIN>
```

身份验证令牌将保存到 `~/.openclaw/trakt_config.json` 文件中。

## 使用方法

### 获取推荐

当用户请求剧集/电影推荐时：

```bash
python3 scripts/trakt_client.py recommend
```

系统会根据用户的观看历史和评分返回个性化推荐。

### 查看观看历史

```bash
python3 scripts/trakt_client.py history
```

显示用户最近的观看记录。

### 查看观看列表

```bash
python3 scripts/trakt_client.py watchlist
```

显示用户保存的、待观看的剧集内容。

### 搜索

```bash
python3 scripts/trakt_client.py search "Breaking Bad"
```

搜索特定的剧集或电影。

### 热门内容

```bash
python3 scripts/trakt_client.py trending
```

获取当前的热门剧集和电影列表。

## 推荐工作流程

当用户询问“我应该看什么？”时：

1. **获取个性化推荐：**
   ```bash
   python3 scripts/trakt_client.py recommend
   ```

2. **解析推荐结果**并以自然的方式展示：
   - 显示剧集名称、年份、评分
   - 简短描述/类型
   - 推荐理由（如果有的话）

3. **可选：检查用户的观看列表**，避免推荐用户已经计划观看的剧集
4. **参考最近的历史记录**，避免重复推荐最近观看过的内容

## API 参考

详细了解 Trakt API 的端点文档，请参阅 `references/api.md`。

## 常见使用场景

**“我今晚应该看什么？”**
- 获取推荐，可根据心情或类型进行筛选
- 如果用户喜欢热门内容，可以查看热门推荐

**“将 [剧集] 添加到我的观看列表”**
- 搜索剧集
- 将剧集添加到 Trakt 的观看列表（需要实现额外的 API 功能）

**“我最近看了什么？”**
- 获取观看历史记录
- 总结用户最近观看的剧集/电影

**“[剧集] 是热门的吗？”**
- 获取热门剧集列表
- 搜索特定的剧集

## 限制

- 需要 Trakt Pro 订阅才能自动从流媒体服务追踪观看记录
- 随着观看历史的积累，推荐效果会逐渐改善
- API 有请求限制：每 5 分钟最多 1000 次请求（已认证用户）
- 完整的 API 文档：<https://trakt.docs.apiary.io/>

## 故障排除

**“身份验证失败”**
- 确保 `~/.openclaw/trakt_config.json` 中的 CLIENT_ID 和 CLIENT_SECRET 设置正确
- 确认 PIN 验证码准确无误（区分大小写）
- 检查 Trakt 应用程序是否具有正确的权限

**“没有返回推荐”**
- 用户可能还没有足够的观看记录
- 可以尝试查看热门内容
- 确保用户已在 Trakt 上对某些内容进行了评分

**“API 请求失败”**
- 检查身份验证令牌是否过期
- 确认网络连接正常
- 查看 Trakt API 的状态：https://status.trakt.tv