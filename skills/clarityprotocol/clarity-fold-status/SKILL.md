---
name: clarity-fold-status
description: 从 Clarity Protocol 获取概览和状态信息。当用户询问折叠状态、变体数量、研究概况、可用数据或 Clarity Protocol 的当前状态时，可以使用此功能。功能包括：API 信息、变体数量以及端点的可用性。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Optional CLARITY_API_KEY env var for 100 req/min (vs 10 req/min).
metadata:
  author: clarity-protocol
  version: "1.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity Fold Status Skill

本技能用于获取关于Clarity Protocol蛋白质折叠研究数据库的概览和状态信息，包括API功能、可用端点以及数据统计信息。

## 快速入门

- 获取完整状态报告：
  ```bash
  ```bash
python scripts/check_status.py
```
  ```

- 以JSON格式获取状态信息：
  ```bash
  ```bash
python scripts/check_status.py --format json
```
  ```

## 状态信息

状态检查提供以下内容：
- **API版本**：当前使用的API版本
- **API描述**：API提供的功能
- **总变体数量**：数据库中蛋白质变体的总数
- **可用端点**：所有API端点的列表
- **速率限制**：匿名用户和已认证用户的请求限制
- **数据更新时间**：数据最后一次更新的时间

## API端点

Clarity Protocol API v1提供以下端点：
- `GET /api/v1/`：API信息
- `GET /api/v1/variants`：列出所有蛋白质变体（支持过滤）
- `GET /api/v1/variants/{fold_id}`：获取特定变体的详细信息
- `GET /api/v1/variants/{fold_id}/findings`：获取与该变体相关的实验结果
- `GET /api/v1/literature`：列出相关研究论文
- `GET /api/v1/literature/{pmid}`：获取特定论文的详细信息
- `GET /api/v1/clinical`：列出临床相关的蛋白质变体
- `GET /api/v1/clinical/{gene}/{variant}`：获取特定基因和变体的临床详细信息

## 速率限制

- **匿名用户（无API密钥）**：每分钟10次请求
- **使用API密钥**：每分钟100次请求

要使用API密钥，请设置`CLARITY_API_KEY`环境变量：
```bash
```bash
export CLARITY_API_KEY=your_key_here
python scripts/check_status.py
```
```
您可以在[https://clarityprotocol.io]获取您的API密钥。

## 错误处理

- **429：速率限制**：您已超出请求限制。系统会显示需要等待的时间。
- **500：服务器错误**：API服务器出现故障，请稍后再试。
- **超时**：请求处理时间超过30秒。

## 使用场景

- 检查API是否可用
- 查看可用数据的概览
- 在发送请求前验证端点URL
- 监控速率限制状态
- 了解API功能以进行集成规划