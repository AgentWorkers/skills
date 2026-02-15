# MCP求职技能

该技能使AI代理能够使用JobSpy MCP服务器在多个招聘平台上搜索职位信息。

JobSpy将来自LinkedIn、Indeed、Glassdoor、ZipRecruiter、Google Jobs等来源的职位信息汇总到一个统一的界面中。

## 何时使用此技能

当您需要执行以下操作时，请使用此技能：
- 根据特定条件（职位类型、地点、公司）查找职位信息
- 搜索远程或现场工作的职位
- 在多个招聘平台之间比较职位信息
- 获取可用的薪资信息
- 查找最近发布的职位
- 筛选“易于申请”的职位

## 先决条件
- Python 3.10及以上版本
- 已安装并配置了JobSpy MCP服务器

## 安装与设置

### macOS环境下的设置（使用Homebrew安装Python）

Homebrew管理的Python版本遵循PEP 668规范。在安装依赖项之前，请先创建并激活一个虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mcp python-jobspy pandas pydantic

```