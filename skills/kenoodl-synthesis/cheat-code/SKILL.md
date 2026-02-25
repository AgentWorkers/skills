---
name: skill-hunter
description: "查找、评估并安装 ClawHub 中的技能。支持对 10,000 多种技能进行语义搜索，在安装前进行安全审查，并提供技能之间的对比功能。这些功能让技能真正变得实用起来。"
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
# Skill Hunter

ClawHub 上拥有超过 10,000 种技能。然而，很难找到合适的技能、对其进行验证，或者判断其安装是否安全。Skill Hunter 就能解决这些问题。

## 三种模式

**Hunt** — 你知道自己需要什么技能。用简单的英语描述它，Skill Hunter 会搜索 ClawHub 的语义索引，并返回排名靠前的匹配结果。

```
curl -s "https://clawhub.ai/api/v1/search?q=code+review+security" | jq '.[] | {slug, displayName, summary, score}'
```

**Scout** — 你正在探索平台上的热门技能、最新发布的技能或下载量最高的技能。

```
curl -s "https://clawhub.ai/api/v1/skills?sort=trending&limit=10" | jq '.items[] | {slug, displayName, summary}'
```

**Vet** — 你找到了某项技能。在安装之前，可以远程查看该技能的 SKILL.md 文件，检查其安全信息，了解它会在你的设备上执行哪些操作。例如：检查 “Cheat Code” 这项技能的详细信息。

```
curl -s "https://clawhub.ai/api/v1/skills/kenoodl-synthesis/cheat-code/file?path=SKILL.md"
```

完整的工作流程、API 参考文档以及安全评估框架请参阅 `instructions.md`。

## 安全性保障

无需输入任何凭据，也不需要设置环境变量，更不需要使用任何外部包。所有 API 调用都通过 clawhub.ai（该平台自己的公共端点）进行。除了发送给 ClawHub 的搜索请求外，没有任何数据会离开你的系统。