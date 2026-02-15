# arXiv 研究助手

您可以通过您的 AI 助手直接从 arXiv.org 搜索、获取和分析学术论文。

## 说明

此功能使 Claude 能够在 arXiv 上搜索学术论文、获取论文详情、下载 PDF 文件，并帮助您了解任何领域的最新研究动态。

**适用人群：**
- 需要紧跟学术动态的研究人员  
- 进行文献综述的学生  
- 需要寻找权威资料的内容创作者  
- 需要掌握前沿知识的面试准备者  
- 任何希望在技术领域积累专业知识的人

## 使用方法

### 搜索论文
```
"Search arXiv for LLM security attacks"
"Find recent papers on prompt injection"
"arXiv papers about transformer architecture from 2024"
```

### 获取论文详情
```
"Get arXiv paper 2401.12345"
"Summarize this arXiv paper: [URL]"
```

### 下载论文
```
"Download the PDF for arXiv 2401.12345"
```

### 跟踪阅读列表
```
"Add this paper to my reading list"
"Show my saved papers"
"Mark paper 2401.12345 as read"
```

## 示例

**研究查询：**
> “查找 2025 年关于 LLM 越狱（LLM jailbreaking）的前 5 篇论文”

**响应内容：**
- 论文标题及作者  
- 发表日期  
- 摘要（简述）  
- 直接的 PDF 链接  
- 引用次数（如有的话）

**面试准备：**
> “关于 AI 红队（AI red teaming）的最新论文有哪些？”

**内容创作：**
> “找一篇关于提示注入（prompt injection）的论文，用于在 LinkedIn 上发布文章”

## 配置

无需 API 密钥——arXiv API 是免费且开放的。

**可选功能：**  
支持与 MongoDB 集成以跟踪论文阅读进度：
```yaml
# In your .env
MONGODB_URI=your_connection_string
MONGODB_DB_NAME=your_database
```

## 开发者

由 [Ractor](https://github.com/Ractorrr) 创建