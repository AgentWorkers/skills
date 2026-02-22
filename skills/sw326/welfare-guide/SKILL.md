---
name: welfare-guide
description: '育儿/福利/政府补助金相关技能。包含9个核心功能（Benefit Search~Beginner Guide），支持通过中央/地方政府的API（采用三层架构）查询各类补助金和福利信息。触发词包括：“补助金”（Subsidy）、“福利”（Welfare）、“津贴”（Allowance）、“育儿”（Childcare）、“生育”（Birth）、“托儿费”（Childcare Fee）、“儿童补贴”（Child Allowance）、“基本生活保障”（Basic Living Support）、“残疾人援助”（Disability Support）、“老年人福利”（Elderly Welfare）、“青年援助”（Youth Support）以及“福利指南”（Welfare Guide）。'
version: 1.0.0
author: chumjibot
created: 2026-02-22
tags: [welfare, 복지, 지원금, 보조금, 육아, 출산, 보육, 아동수당, 기초생활]
connectors: [~~search, ~~notify, ~~docs]
---
# 🍀 福利指南（育儿/福利/政府补助金）技能

我们将福利和补助金相关的问题分为9个类别，并通过“Bokjiro”平台中的中央政府部门和地方政府的API，提供个性化的查询服务。

## 意图路由器（Intent Router）

| 编号 | 意图（Intent） | 用户示例 | 基本输出结果 |
| --- | -------- | -----------------| ------------ |
| 1 | 福利搜索（Benefit Search） | “我能享受哪些福利？” | 基于条件的个性化福利列表 |
| 2 | 育儿（Childcare） | “育儿有哪些补助金？” | 育儿支持项目列表 |
| 3 | 出产支持（Birth Support） | “生育后能得到什么？” | 出产补助金汇总信息 |
| 4 | 基本生活（Basic Living） | “如何成为基本生活补助金领取者？” | 领取条件 + 申请方法 |
| 5 | 青年支持（Youth Support） | “青年有哪些福利？” | 青年专属福利列表 |
| 6 | 老年支持（Senior Support） | “父母或老年人有哪些福利？” | 老年人福利服务列表 |
| 7 | 残疾人支持（Disability Support） | “残疾人有哪些补助金？” | 残疾人福利服务列表 |
| 8 | 如何申请（How to Apply） | “如何申请？” | 申请流程 + 所需文件说明 |
| 9 | 新手指南（Beginner Guide） | “我是福利新手” | 福利系统入门信息 |

详情：[`references/intent_router.md`](references/intent_router.md)

## API三层结构（API 3-Layer Structure）

| API | 提供机构 | 内容 | 状态 |
| ----- | --------- | ------ | ------ |
| Bokjiro - 中央政府部门（`15090532`） | 中央政府的福利项目和领取条件 | ⏳ 需要申请使用 |
| Bokjiro - 地方政府（`15108347`） | 地方政府的福利服务 | ⏳ 需要申请使用 |
| Bokjiro - 补助金24（`15113968`） | 行政安全部 | 政府部门、地方政府及公共机构的各类补助金 | ⏳ 需要申请使用 |

通过结合这3个API，可以全面覆盖中央和地方政府的福利服务。支持根据年龄、地区、家庭状况和收入等条件进行筛选。

## 输出格式

- **Flash Layer**：始终显示
- **Deep-Dive Layer**：在用户明确请求时显示，或通过“Basic Living”/“Benefit Search”意图查询时显示

详情：[`references/output_templates.md`](references/output_templates.md)

## ⚠️ 免责声明

本内容仅用于提供信息，实际是否能够领取福利由相关机构决定。
最新政策请访问Bokjiro网站（www.bokjiro.go.kr）或当地居民服务中心查询。

## 🔧 设置（公共数据门户API）

1. 在[data.go.kr](https://www.data.go.kr)注册成为会员，然后复制通用认证密钥（Decoding）。
2. 下列3项服务均支持自动申请：
   - [Bokjiro - 中央政府部门](https://www.data.go.kr/data/15090532/openapi.do) (15090532)
   - [Bokjiro - 地方政府](https://www.data.go.kr/data/15108347/openapi.do) (15108347)
   - [Bokjiro - 补助金24](https://www.data.go.kr/data/15113968/openapi.do) (15113968)
3. 保存密钥：
   ```bash
   mkdir -p ~/.config/data-go-kr
   echo "YOUR_API_KEY" > ~/.config/data-go-kr/api_key
   ```
> 即使未注册API，也可以通过`web_search`功能查询主要的福利信息。