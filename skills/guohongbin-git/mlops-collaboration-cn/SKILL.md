---
name: mlops-collaboration-cn
version: 1.0.0
description: 准备项目以供共享、协作和社区使用
license: MIT
---
# MLOps协作 🤝  
让项目具备协作性和社区适用性。  

## 功能  

### 1. README模板 📖  
专业文档：  
```bash
cp references/README-template.md ../your-project/README.md
# Edit with your project details
```  
包含：  
- 徽章（PyPI、CI、许可证）  
- 快速入门指南  
- 安装步骤  
- 使用示例  
- 贡献指南  

### 2. 必需文件清单 ✅  
社区文件：  
- `LICENSE` - MIT/Apache/GPL许可证  
- `CODE_OF_CONDUCT.md` - 贡献者准则  
- `CONTRIBUTING.md` - 如何贡献代码  
- `CHANGELOG.md` - 版本历史记录  

### 3. 开发容器 📦  
VS Code开发容器：  
```json
// .devcontainer/devcontainer.json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/astral-sh/uv:latest": {}
  }
}
```  

## 快速入门  
```bash
# Copy README template
cp references/README-template.md ./README.md

# Create required files
touch LICENSE CODE_OF_CONDUCT.md CONTRIBUTING.md CHANGELOG.md

# Setup dev container
mkdir -p .devcontainer
# Add devcontainer.json

# Protect main branch (GitHub UI)
# Settings → Branches → Add rule
```  

## 发布流程  
1. 在`pyproject.toml`中更新版本号  
2. 更新`CHANGELOG.md`  
3. 创建Git标签：`git tag v1.0.0`  
4. 推送代码：`git push --tags`  
5. 在GitHub上发布项目  

## 语义版本控制  
- `1.0.0` → `1.0.1`：修复错误（PATCH版本）  
- `1.0.0` → `1.1.0`：新增功能（MINOR版本）  
- `1.0.0` → `2.0.0`：重大变更（MAJOR版本）  

## 作者  
该项目改编自[MLOps编程课程](https://github.com/MLOps-Courses/mlops-coding-skills)  

## 版本历史记录  
### v1.0.0 (2026-02-18)  
- 首次将项目转换为MLOps格式  
- 添加了README模板