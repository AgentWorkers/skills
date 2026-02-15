---
name: bookstack
description: "BookStack Wiki与文档API集成：通过编程方式管理您的知识库——可以创建、读取、更新和删除书籍、章节、页面以及分类目录。支持对所有内容进行全文搜索。适用于以下场景：  
(1) 创建或编辑Wiki页面和文档；  
(2) 对内容进行分类（放入不同的书籍或章节中）；  
(3) 在知识库中搜索信息；  
(4) 自动化文档处理流程；  
(5) 在不同系统之间同步内容。  
该集成同时支持HTML和Markdown格式的内容。"
metadata:
  openclaw:
    requires:
      env:
        - BOOKSTACK_URL
        - BOOKSTACK_TOKEN_ID
        - BOOKSTACK_TOKEN_SECRET
---

# BookStack 技能

**BookStack** 是一个开源的 wiki 和文档平台。通过这个技能，您可以使用 API 管理您的整个知识库——非常适合自动化和集成。

## 功能

- 📚 **书籍** – 创建、编辑、删除书籍
- 📑 **章节** – 在书籍中组织内容
- 📄 **页面** – 使用 HTML 或 Markdown 创建/编辑页面
- 🔍 **全文搜索** – 在所有内容中进行搜索
- 📁 **书架** – 将书籍分类到不同的集合中

## 快速入门

```bash
# List all books
python3 scripts/bookstack.py list_books

# Search the knowledge base
python3 scripts/bookstack.py search "Home Assistant"

# Get a page
python3 scripts/bookstack.py get_page 123

# Create a new page (Markdown)
python3 scripts/bookstack.py create_page --book-id 1 --name "My Page" --markdown "# Title\n\nContent here..."
```

## 所有命令

### 书籍
```bash
python3 scripts/bookstack.py list_books                    # List all books
python3 scripts/bookstack.py get_book <id>                 # Book details
python3 scripts/bookstack.py create_book "Name" ["Desc"]   # New book
python3 scripts/bookstack.py update_book <id> [--name] [--description]
python3 scripts/bookstack.py delete_book <id>
```

### 章节
```bash
python3 scripts/bookstack.py list_chapters                 # List all chapters
python3 scripts/bookstack.py get_chapter <id>              # Chapter details
python3 scripts/bookstack.py create_chapter --book-id <id> --name "Name"
python3 scripts/bookstack.py update_chapter <id> [--name] [--description]
python3 scripts/bookstack.py delete_chapter <id>
```

### 页面
```bash
python3 scripts/bookstack.py list_pages                    # List all pages
python3 scripts/bookstack.py get_page <id>                 # Page preview
python3 scripts/bookstack.py get_page <id> --content       # With HTML content
python3 scripts/bookstack.py get_page <id> --markdown      # As Markdown

# Create page (in book or chapter)
python3 scripts/bookstack.py create_page --book-id <id> --name "Name" --markdown "# Content"
python3 scripts/bookstack.py create_page --chapter-id <id> --name "Name" --html "<p>HTML</p>"

# Edit page
python3 scripts/bookstack.py update_page <id> [--name] [--content] [--markdown]
python3 scripts/bookstack.py delete_page <id>
```

### 搜索
```bash
python3 scripts/bookstack.py search "query"                # Search everything
python3 scripts/bookstack.py search "query" --type page    # Pages only
python3 scripts/bookstack.py search "query" --type book    # Books only
```

### 书架
```bash
python3 scripts/bookstack.py list_shelves                  # List all shelves
python3 scripts/bookstack.py get_shelf <id>                # Shelf details
python3 scripts/bookstack.py create_shelf "Name" ["Desc"]  # New shelf
```

## 配置

设置以下环境变量：

```bash
export BOOKSTACK_URL="https://your-bookstack.example.com"
export BOOKSTACK_TOKEN_ID="your-token-id"
export BOOKSTACK_TOKEN_SECRET="your-token-secret"
```

或者通过您的网关配置文件（位于 `skills.entries.bookstack.env` 下）进行配置。

### 创建 API 令牌

1. 登录到您的 BookStack 实例
2. 转到 **编辑个人资料** → **API 令牌**
3. 点击 **创建令牌**
4. 复制令牌 ID 和密钥

⚠️ 用户需要具有 **“访问系统 API”** 的权限！

## API 参考

- **基础 URL**：`{BOOKSTACK_URL}/api`
- **认证头**：`Authorization: Token {ID}:{SECRET}`
- **官方文档**：https://demo.bookstackapp.com/api/docs

---

**作者**：xenofex7 | **版本**：1.0.2