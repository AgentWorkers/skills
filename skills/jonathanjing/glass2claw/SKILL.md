---
name: glass2claw
description: "雷朋眼镜 → 语音指令 → WhatsApp → OpenClaw 会自动将你的照片导入正确的数据库中。实现免提式的日志记录功能。"
version: "2.3.3"
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "tools": ["sessions_send", "message"]
      }
  }
---
# glass2claw：从你的眼睛到你的数据库——瞬间完成

## 🛠️ 安装

### 1. 建议使用 OpenClaw
告诉 OpenClaw：“安装 glass2claw 功能。”代理会自动处理安装和配置。

### 2. 手动安装（通过 CLI）
如果你更喜欢使用终端，可以运行以下命令：
```bash
clawhub install glass2claw
```

你戴着 **Meta Ray-Ban 眼镜**。你看到一张葡萄酒标签、一张名片或一个茶叶罐，然后你说：
> “嘿 Meta，拍张照片并发送到我的 WhatsApp 上。”

就这样，OpenClaw 会完成剩下的所有工作。

照片会直接发送到你的 WhatsApp 账户中。OpenClaw 的视觉识别系统会识别照片内容，并将其存储到你指定的数据库中——无论是葡萄酒收藏、联系人信息还是茶叶记录等。

**无需输入任何信息，无需切换应用程序，没有任何操作上的麻烦。**

---

## 📸 工作原理

你的唯一操作就是发出语音指令，其余的所有流程都是自动完成的。

---

## 🔧 需要准备的设置

这个功能实际上是一个 **路由协议**，它定义了数据传输的规则，但不涉及具体的实现细节。你需要自行准备以下内容：
- **Meta AI 与 WhatsApp 的连接**：在 Ray-Ban 眼镜上启用 Meta AI 并将其与 WhatsApp 连接（只需在 Meta View 应用中进行一次设置）
- **OpenClaw 与 WhatsApp 的通信通道**：你的 OpenClaw 实例需要一个 WhatsApp 会话来接收传入的图片
- **目标数据库**：你可以选择任何数据库进行存储：Notion、Airtable、本地文件或 Discord 频道等。该功能会根据你的配置将数据发送到指定的位置
- **数据库访问权限**：你需要自行设置目标数据库的访问权限（例如 Notion 的 API 密钥、Airtable 的访问令牌等）

> 该软件包中的示例模板展示了使用 Notion 和 Discord 的实现方式。你可以根据自己的需求进行调整。

---

## 🔒 隐私政策

该功能会处理 **来自你个人相机的照片**。照片会先传输到 OpenClaw 实例，然后再被存储到你配置的目标数据库中。你连接的任何外部服务（如 Notion、Discord 等）都遵循它们各自的隐私政策。所有的数据传输逻辑都在你的 OpenClaw 实例上完成。

---

## 📦 包含的内容

- `SAMPLE_AGENT.md`：用于 Hub 代理的路由逻辑示例
- `SAMPLE_SOUL_WINE.md`：用于葡萄酒专家角色的示例代码

你可以将这些文件作为起点，根据自己的需求进行定制和扩展。

---

*创建者：JonathanJing | AI 可靠性架构师*