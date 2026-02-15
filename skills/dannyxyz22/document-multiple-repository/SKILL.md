---
name: document-multiple-repository
description: 为具有多个仓库（前端、后端、微服务、维基）的软件系统生成统一的技术文档。当用户需要多仓库的文档、统一的架构视图、仓库映射或从多个本地仓库中提取文档时，可使用该文档。
version: 0.1.0
---

# 技能：document-multiple-repository  
## 目的  
为由多个仓库（包括前端、后端、微服务、基础设施、文档和维基）组成的软件系统生成统一的技术文档。这些仓库都存储在共享的文件系统中。  

## 前提条件  
- 所有仓库（包括维基）均已克隆到本地。  
- 多个仓库可以构成一个逻辑上的完整系统。  
- 维基通常是以 `.wiki` 为后缀的 Git 仓库。  
- 可能使用的编程语言包括 Java、Python、JavaScript。  
- 没有严格的命名规范。  
- 执行过程需要通过人工智能代理（如 VS Code、Copilot、Gemini CLI 等）手动完成。  

## 输入参数  
- `ROOT_PATH`：包含多个系统的文件夹路径。  
- `OUTPUT_PATH`：生成文档的目标路径。  
- `TEMPLATES_PATH`：用于生成 README、ARCHITECTURE、API、CODE_COMMENTS 等文档的模板文件夹路径。  

## 处理流程  

### 1. 发现系统  
- 递归扫描 `ROOT_PATH`。  
- 识别 Git 仓库（带有 `.git` 文件夹的目录）。  
- 确定维基仓库（文件夹名以 `.wiki` 结尾）。  
- 根据文件系统的物理位置将仓库分组。  
- 将每个仓库组（代码仓库+维基仓库）视为一个逻辑上的独立系统。  

### 2. 分析仓库  
- 对每个仓库进行分析：  
  - 判断仓库类型（代码仓库、文档仓库或维基仓库）。  
  - 如果是代码仓库：  
    - 识别所使用的编程语言和框架（如 Spring、Django、Node.js 等）。  
    - 确定仓库的类型（后端、前端、微服务或基础设施）。  
    - 提取以下内容：README 文件、构建文件、配置文件、API 路由、数据模型、配置信息。  
  - 如果是维基仓库：  
    - 找到首页（Home.md、index.md）文件。  
    - 提取基础设施指南、设置教程、业务流程文档（DoR/DoD）以及外部法规或资源的链接。  
  - 如果是文档仓库：  
    - 识别使用的文档生成工具（如 MkDocs、Sphinx 等）。  
    - 提取用户手册和操作指南。  

### 3. 生成文档  
- 为每个系统生成以下文档：  
  - `SYSTEM_OVERVIEW.md`：包含业务和技术概览的文档。  
  - `ARCHITECTURE.md`：系统架构文档。  
  - `REPOSITORY_MAP.md`：仓库映射文档。  
  - `DEPLOYMENT.md`：结合代码配置和维基文档的信息。  
  - `PROCESSES_AND_GUIDELINES.md`：从维基中提取的业务流程和贡献指南。  

- 为每个仓库单独生成以下文档：  
  - `README.generated.md`：仓库的简介文档。  
  - `API GENERATED.md`：API 文档。  
  - `CODE_structure.md`：代码仓库的结构说明。  
  - `WIKI_SUMMARY.md`：维基仓库的摘要文档。  

### 输出结构  
输出文件将按照以下结构存储在 `OUTPUT_PATH` 目录下：  
```  
OUTPUT_PATH/  
  system-name/  
    SYSTEM_OVERVIEW.md  
    ARCHITECTURE.md  
    REPOSITORY_MAP.md  
    DEPLOYMENT.md  
    PROCESSES_AND_GUIDELINES.md  
  repos/  
       repo-name/  
         README.generated.md  
         API GENERATED.md  
         CODE_structure.md  
         WIKI_SUMMARY.md  
```  

## 执行方式  
通过运行以下命令来执行该技能：  
```  
"Run skill document-multiple-repository on <ROOT_PATH>"  
```  

## 限制条件  
- 该工具仅用于生成文档，不执行任何代码。  
- 不会修改原始仓库的内容。