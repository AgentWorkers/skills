# Sefaria API MCP

Sefaria API MCP 是一个用于访问 Sefaria API 的服务器。Sefaria 是一个最大的开源犹太文本数据库。

## 说明

本文档提供了使用 Sefaria API MCP 服务器的指南和辅助工具。通过简单的 MCP 接口，您可以访问包括《托拉》（Torah）、《塔木德》（Talmud）、《密西拿》（Mishnah）及其注释在内的所有犹太文本。

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/davad00/sefaria-api-mcp.git
cd sefaria-api-mcp
```

2. 安装依赖项：
```bash
npm install
```

3. 构建项目：
```bash
npm run build
```

## 工具

### `connect`

启动 Sefaria API MCP 服务器。

**参数：**
- `port`（可选）：端口号（默认：8080）

**示例：**
```javascript
{
  "name": "connect",
  "arguments": {
    "port": 8080
  }
}
```

### `use`

展示所有可用 Sefaria MCP 工具的示例用法。

**示例：**
```javascript
{
  "name": "use"
}
```

## 可用的 MCP 工具

一旦 MCP 服务器运行起来，您可以使用以下工具：

### 文本检索
- `get_text` - 根据引用获取文本（例如：“创世记 1:1”）
- `get_text_v1` - 使用旧版本的文本接口
- `get_random_text` - 获取随机文本片段
- `get_manuscripts` - 获取手稿变体

### 搜索与发现
- `search` - 在整个数据库中进行全文搜索
- `find_refs` - 从文本中解析引用
- `get_toc` - 获取所有可用文本的目录
- `get_category` - 获取特定类别的文本

### 相关内容
- `get_related` - 获取所有相关内容（链接、表格、主题）
- `get_links` - 获取与其他资源的交叉引用
- `get_topics` - 获取主题详情
- `get_all_topics` - 列出所有主题
- `get_ref_topic_links` - 获取与某个引用相关联的主题

### 查阅
- `get_index` - 获取文本元数据（结构、版本信息）
- `get_shape` - 获取文本结构
- `get_lexicon` - 获取希伯来语单词的定义
- `get_versions` - 获取可用的翻译版本

### 日历
- `get_calendars` - 获取当天的《托拉》诵读内容和犹太历信息

## 示例用法

```javascript
// 获取“创世记 1:1”的内容
{
  "name": "get_text",
  "arguments": { "tref": "Genesis 1:1"
}

// 搜索“love”这个词
{
  "name": "search",
  "arguments": { "q": "love", "limit": 5 }
}

// 从文本中解析引用
{
  "name": "find_refs",
  "arguments": { "text": "As it says in Shabbat 31a"
}

// 获取当天的诵读内容
{
  "name": "get_calendars"
}
```

## 配置

将以下配置添加到您的 MCP 配置文件中：
```json
{
  "mcpServers": {
    "sefaria": {
      "command": "node",
      "args": ["path/to/sefaria-api-mcp/dist/index.js"]
    }
  }
}
```

## 链接

- [GitHub 仓库](https://github.com/davad00/sefaria-api-mcp)
- [Sefaria API 文档](https://developers.sefaria.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 许可证

MIT 许可证——允许自由使用、修改和重新分发。

## 支持

如有问题或疑问：
- 在 [GitHub](https://github.com/davad00/sefaria-api-mcp/issues) 上提交问题
- 查看 [Sefaria API 文档](https://developers.sefaria.org/)