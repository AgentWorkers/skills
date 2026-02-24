---
name: skill-hunter
description: "查找、评估并安装 ClawHub 中的技能。支持对超过 10,000 种技能进行语义搜索，在安装前进行安全审查，并提供技能之间的对比功能。这些功能让技能真正变得实用。"
metadata:
  openclaw:
    tags:
      - clawhub
      - skills
      - discovery
      - search
      - install
      - security
      - utility
      - openclaw
      - agent-tool
    os:
      - darwin
      - linux
      - windows
---
# 技能猎人（Skill Hunter）

ClawHub 上拥有超过 10,000 种技能。然而，如何找到合适的技能、验证其安全性以及判断是否适合安装，一直是个难题。Skill Hunter 就为此而生。

## 三种模式

**搜索模式（Hunt）**：你知道自己需要什么技能，只需用简单的英语描述它，Skill Hunter 会搜索 ClawHub 的语义索引，并返回排名靠前的匹配结果。

```
curl -s "https://clawhub.ai/api/v1/search?q=code+review+security" | jq '.[] | {slug, displayName, summary, score}'
```

**探索模式（Scout）**：你可以浏览平台上最热门、最新或下载量最高的技能。

```
curl -s "https://clawhub.ai/api/v1/skills?sort=trending&limit=10" | jq '.items[] | {slug, displayName, summary}'
```

**验证模式（Vet）**：当你找到某项技能后，在安装之前，可以远程查看其对应的 SKILL.md 文件，检查其安全配置，了解该技能会在你的设备上执行哪些操作。

```
curl -s "https://clawhub.ai/api/v1/skills/kenoodl-synthesis/kenoodl-synthesis/file?path=SKILL.md"
```

完整的工作流程、API 参考文档以及安全评估框架，请参阅 `instructions.md`。

## 安全性保障

无需输入任何凭据，也不需要使用环境变量；所有 API 调用都通过 clawhub.ai 这一平台的公共端点进行。除了发送到 ClawHub 的搜索请求外，没有任何数据会离开你的系统环境。