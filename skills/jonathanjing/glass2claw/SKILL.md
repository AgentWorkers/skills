---
name: glass2claw
description: "雷朋眼镜 → 语音指令 → WhatsApp → OpenClaw 会自动将你的照片导入正确的数据库中。实现免提式的日常记录功能。"
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

你戴着你的**Meta Ray-Ban眼镜**。当你看到一张葡萄酒标签、一张名片或一个茶叶罐时，你可以这样说道：

> “嘿，Meta，拍张照片然后发到我的WhatsApp上。”

就这样，OpenClaw会完成剩下的所有工作。

照片会直接发送到你的WhatsApp账户中。OpenClaw的视觉识别系统会识别照片的内容，并将其存储到你配置好的数据库中——无论是葡萄酒收藏、联系人信息还是茶叶记录。

**无需输入任何文字，无需切换应用程序，没有任何操作上的麻烦。**

---

## 📸 工作原理

```
Meta Ray-Ban glasses
  → "Hey Meta, take a picture and send this to myself on WhatsApp"
      → Meta AI delivers the photo to your WhatsApp
          → OpenClaw (WhatsApp session) receives the image
              → classifies intent: Wine | Tea | Contacts | Cigar | ...
                  → routes to the matching specialist agent
                      → writes structured entry to your database
```

你唯一需要做的就是发出语音指令，其余的所有步骤都是自动完成的。

---

## 🔧 需要准备的设置

这个功能实际上是一个**路由协议**——它定义了数据传输的规则，但不涉及具体的实现细节。你需要自行准备以下内容：

- **Meta AI与WhatsApp的连接**：在Ray-Ban眼镜上启用Meta AI功能，并将其与WhatsApp关联起来（只需在Meta View应用程序中进行一次设置）。
- **OpenClaw与WhatsApp的集成**：你的OpenClaw实例需要具备接收照片的能力。
- **目标数据库**：你可以选择任何数据库进行存储（如Notion、Airtable或本地文件）；该功能会自动将照片发送到你配置的目标位置。
- **数据库访问权限**：你需要自行设置数据库的访问权限（例如Notion的API密钥或Airtable的访问令牌）。

> 该软件包中的示例模板展示了使用Notion和Discord的实现方式。你可以根据自己的需求进行调整。

---

## 🔒 隐私保护

该功能仅处理来自你个人相机的照片。照片会先传输到OpenClaw实例，然后再被存储到你指定的数据库中。你连接的任何外部服务（如Notion或Discord）都遵循它们自己的隐私政策。所有的数据传输逻辑都在你的OpenClaw实例上完成。

---

## 📦 包含的内容

- `SAMPLE_AGENT.md`：用于Hub代理的路由逻辑示例。
- `SAMPLE_SOUL_WINE.md`：用于葡萄酒专家角色的示例代码。

你可以将这些模板作为起点，根据自己的需求进行定制。

---

*创建者：JonathanJing | AI可靠性架构师*