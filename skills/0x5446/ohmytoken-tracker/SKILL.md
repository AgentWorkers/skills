# ohmytoken-tracker

> 监控你的代币消耗情况——一个代币接一个代币地被“烧掉”。

该工具会自动追踪你通过 OpenClaw 网关使用的 LLM（大型语言模型）代币，并将这些数据以彩色像素珠子的形式展示在 [ohmytoken.dev](https://ohmytoken.dev) 上。

## 功能介绍

每次 LLM 发出响应后，该工具会将代币使用情况悄悄地发送到 ohmytoken.dev，这些数据会被实时可视化成一块像素珠子板：每个模型都有独特的颜色，每个珠子代表被消耗的代币数量。

## 主要特性

- 设置 API 密钥后即可立即使用（无需额外配置）
- 自动追踪所有模型（Claude、GPT、Gemini、DeepSeek、LLaMA 等）
- 在 ohmytoken.dev 上实时查看珠子板可视化效果
- 支持时间周期查看：每日、每月、每年、历史总计
- 提供 7 种珠子板形状（正方形、心形、星形、圆形、菱形、蘑菇形）
- 7 种填充图案（顺序排列、螺旋形、从中心向外扩散、随机分布、蛇形、对角线、雨滴状）
- 拥有 10 种徽章的成就系统
- 多维度排行榜
- 可分享包含 QR 代码的卡片
- 支持将 SVG 徽章嵌入到 GitHub 的 README 文件中

## 设置方法

1. 在 [ohmytoken.dev](https://ohmytoken.dev) 注册（支持 Google/GitHub OAuth）
2. 从欢迎页面复制你的 API 密钥
3. 将以下代码添加到你的 `openclaw.json` 文件中：

```json
{
  "skills": {
    "ohmytoken-tracker": {
      "enabled": true,
      "config": {
        "api_key": "omt_your_key_here"
      }
    }
  }
}
```

或者设置环境变量：`export OHMYTOKEN_API_KEY=omt_your_key_here`

## 相关链接

- 网站：https://ohmytoken.dev
- 代码仓库：https://github.com/0x5446/ohmytoken