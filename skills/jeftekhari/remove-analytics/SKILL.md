---
name: remove-analytics
description: **安全地从项目中移除 Google Analytics。**  
会清除所有跟踪代码、依赖项以及环境变量。
disable-model-invocation: true
---

# 移除分析功能（Remove Analytics Functionality）

您将在此项目中移除 Google Analytics。这是一个具有破坏性的操作，请在继续之前先与用户确认。

## 第一步：确认操作意图

请用户确认是否确实要移除分析功能：

> “这将从您的项目中移除所有 Google Analytics 的跟踪代码。此操作将：
> - 删除 `gtag` 脚本和组件
> - 删除与分析相关的实用工具文件
> - 从 `.env.example` 文件中移除相关环境变量
> - （如果有的话）删除相关的 npm 包
>
> 输入 ‘yes’ 以确认。”

## 第二步：查找所有与分析相关的代码

搜索以下内容：
- 包含 `gtag`、`dataLayer`、`GoogleAnalytics` 的文件
- 用于导入分析工具的导入语句
- 包含 `googletagmanager.com` 的脚本标签
- 环境变量：`GA_`、`GTAG_`、`MEASUREMENT_ID`
- `package.json` 中的依赖项：`@types/gtag.js`、`react-ga4`、`vue-gtag` 等

## 第三步：删除相关代码

对于每一处找到的代码或文件：
1. 显示需要删除的文件及其代码内容
2. 实际删除该代码或文件
3. 清理任何不再使用的导入语句（即那些不再引用的导入项）

## 第四步：进行清理

- 删除与分析相关的 npm 包：`npm uninstall @types/gtag.js`（或相应的包）
- 从 `.env.example` 文件中移除相关环境变量
- 更新所有引用分析功能的文档

## 第五步：总结

提供以下内容的总结：
- 被删除的文件
- 被修改的文件
- 被移除的包
- 被移除的环境变量
- 需要执行的任何手动操作（例如删除实际的环境变量值）