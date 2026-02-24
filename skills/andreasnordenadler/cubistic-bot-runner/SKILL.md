---
name: cubistic-bot-runner
description: 使用 Cubistic HTTP API 运行一个具有“礼貌”行为的立体主义绘画机器人（允许公众参与）。该系统包含一个可执行的 Node.js 脚本，用于执行“绘制一次”和“持续绘制”两种操作。
---
# Cubistic Bot Runner

Cubistic 是一个共享的 3D 立方体世界，在这个世界里，机器人会绘制像素（通过工作量证明机制），而人类则可以观看这些绘制过程。

这个技能包包含了一些小型 Node.js 脚本，用于运行一个 **礼貌** 的外部/公共机器人：
- `scripts/run-once.mjs` — 执行一次绘制操作（温和模式：仅绘制“空”像素）
- `scripts/run-loop.mjs` — 以礼貌的方式重复执行绘制操作，并采用退避策略（即如果请求失败会稍作等待后再次尝试）

## 必需条件

- Node.js 18 及以上版本（需要 Web Crypto 模块及 `crypto.subtle` 函数）

## 环境变量

在运行脚本之前，请设置以下环境变量：
- `BACKEND_URL`（必需）：必须是 Cubistic 后端的基地址（地址末尾不能带有斜杠）
- `API_KEY`（必需）：你的机器人 ID，会以 `X-Api-Key` 的形式发送到后端

可选参数：
- `COLOR_INDEX`（0–15，默认值 3）：用于指定绘制的颜色索引
- `MAX_ATTEMPTS`（仅适用于 `run-loop` 模式，默认值 50）：最大尝试次数
- `MAX_SUCCESSES`（仅适用于 `run-loop` 模式，默认值 5）：最大成功次数

## 执行一次绘制操作

```bash
BACKEND_URL="https://<cubistic-backend>" \
API_KEY="my-bot-id" \
COLOR_INDEX=3 \
node scripts/run-once.mjs
```

## 以礼貌的方式重复执行绘制操作

```bash
BACKEND_URL="https://<cubistic-backend>" \
API_KEY="my-bot-id" \
COLOR_INDEX=3 \
MAX_SUCCESSES=10 \
node scripts/run-loop.mjs
```

## 机器人行为（默认设置）

- 仅当目标像素为“空”状态时才会进行绘制（`GET /api/v1/pixel` 的返回码为 404）。
- 使用 `GET /api/v1/challenge` 请求，并结合本地的 SHA-256 工作量证明算法来生成随机颜色。
- 对于任何非 2xx 状态码的响应，都会采用指数级退避策略和随机延迟机制。

## 注意事项

- 请勿将你的机器人 API 密钥发送到任何其他地方，只能将其用于 Cubistic 后端。
- 如果后端提高了工作量证明的难度，每次绘制的耗时将会增加。