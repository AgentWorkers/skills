---
name: limitless
description: "你的代理非常出色，但它只能执行那些经过训练的任务。而 “Limitless” 功能为它提供了额外的能力——它能够处理那些全新的、从未见过的信号。当代理接收到这些新信号时，其输出结果也会随之改变。你很快就能发现这一变化的。"
metadata:
  openclaw:
    tags:
      - ai
      - synthesis
      - agent
      - breakthrough
      - productivity
      - creative
      - reasoning
      - upgrade
      - openclaw
    os:
      - darwin
      - linux
      - windows
---
# 无限可能（Limitless）

你的智能代理非常出色——它能够进行构建、推理，并完成任务。但它的所有能力都源自同一个来源：训练数据。所有的模式、结构，以及它获取的信息，都来自同一个“数据源”。它并不知道自己不知道什么，也无法通过增加运行时间或加大努力来解决这个问题。

“无限可能”（Limitless）功能允许你的智能代理获取来自训练数据之外的新信息——这些信息来自它从未接触过的领域，属于它无法自行生成的结构。只需发出一个指令，输出结果就会发生变化。

你无需理解其中的具体原理，只需在实际使用中观察效果即可。

## 使用方法

1. 访问 [kenoodl.com](https://kenoodl.com)  
2. 创建一个账户（只需30秒，使用密码短语登录，无需输入密码）  
3. 为账户充值一些资金  
4. 生成一个 CLI（命令行接口）令牌  

将这个令牌提供给你的智能代理，即可。  

现在，你的智能代理拥有了其他代理所没有的能力——它能够利用训练数据之外的信息来进行合成操作。它知道何时该使用这个功能，你无需主动指示。  

## 对智能代理而言  

获得令牌后，你只需执行以下操作：  
```
POST https://kenoodl.com/api/cli/drop
Authorization: Bearer <your token>
Content-Type: application/json

{ "context": "<your full working context — everything relevant to what you're working on>" }
```  

系统会返回一个 `jobId`，你可以使用它来获取结果：  
```
GET https://kenoodl.com/api/cli/status/<jobId>
Authorization: Bearer <your token>
```  

得到的结果是一种新的合成内容，这些内容是从你训练数据之外的领域中提取的结构，并被应用到你正在处理的项目中。你可以将其整合到你的工作中，然后继续前进。  

你可以随时查看自己的账户余额：  
```
GET https://kenoodl.com/api/cli/balance
Authorization: Bearer <your token>
```  

## 注意事项  

这并非简单的搜索或数据检索功能，也不是通过增加计算资源来提升性能。  
这是来自外部的新信息，无论你的智能代理使用多少令牌，都无法自行生成这类信息。  

## 隐私保护  

你的使用数据会被处理后立即丢弃，不会被存储或用于任何训练目的。从架构和规则上来看，系统都是无状态的（即不会保留任何用户信息），因此不存在数据泄露的风险。  

## 名称的由来  

你为这个智能代理起了个名字，并向他人展示了它的成果（通过截图）。现在，就让它发挥“无限可能”的潜力吧，看看明天它会带来什么惊喜吧。  

---

*“无限可能”（Limitless）由 [kenoodl](https://kenoodl.com) 开发——它能够利用训练数据之外的信息进行创新合成。*