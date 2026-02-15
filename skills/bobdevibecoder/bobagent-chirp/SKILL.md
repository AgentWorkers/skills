---
name: chirp
description: "**X/Twitter CLI（命令行界面）：使用 OpenClaw 浏览器工具**  
当用户需要与 X/Twitter 进行交互时（如阅读时间线、发布推文、点赞、转发、回复或搜索），可以使用该 CLI。它适用于没有 Homebrew 的环境，是 bird CLI 的替代方案。"
homepage: https://github.com/zizi-cat/chirp
metadata: {"clawdhub":{"emoji":"🐦"}}
---

# chirp

使用 OpenClaw 浏览器工具来操作 X/Twitter。这是 bird CLI 的基于浏览器的替代方案。

## 先决条件

### 环境要求
- 已启用浏览器工具的 OpenClaw
- `openclaw` 浏览器配置文件
- 已完成 X/Twitter 账户登录

### 如果使用无头服务器（Headless server）

需要 Xvfb 虚拟显示器（请参考 `spool` 技能的先决条件）

### 登录（仅首次需要）

```
browser action=start profile=openclaw
browser action=open profile=openclaw targetUrl="https://x.com/login"
# 사용자에게 수동 로그인 요청
```

---

## 使用方法

### 1. 查看时间线

```
browser action=open profile=openclaw targetUrl="https://x.com/home"
browser action=snapshot profile=openclaw compact=true
```

可以在每条推文上查看作者、内容以及点赞/转发/回复的数量。

### 2. 发布推文

**步骤 1：在首页找到文本输入框**
```
browser action=open profile=openclaw targetUrl="https://x.com/home"
browser action=snapshot profile=openclaw compact=true
```
→ 查找 `textbox "Post text"` 的引用（reference）

**步骤 2：输入内容**
```
browser action=act profile=openclaw request={"kind":"click","ref":"<textbox-ref>"}
browser action=act profile=openclaw request={"kind":"type","ref":"<textbox-ref>","text":"트윗 내용"}
```

**步骤 3：点击“发布”按钮**
```
browser action=snapshot profile=openclaw compact=true
```
→ 查找 `button "Post"` 的引用（确保该按钮未被禁用）
```
browser action=act profile=openclaw request={"kind":"click","ref":"<post-ref>"}
```

### 点赞

在时间线上找到推文中的 `button "Like"` 或 `button "X Likes. Like"` 并点击：
```
browser action=act profile=openclaw request={"kind":"click","ref":"<like-ref>"}
```

### 转发推文

找到 `button "Repost"` 或 `button "X reposts. Repost"` 并点击：
```
browser action=act profile=openclaw request={"kind":"click","ref":"<repost-ref>"}
browser action=snapshot profile=openclaw compact=true
# "Repost" 옵션 선택
browser action=act profile=openclaw request={"kind":"click","ref":"<repost-option-ref>"}
```

### 回复推文

**方法 1：在时间线上回复**
```
browser action=act profile=openclaw request={"kind":"click","ref":"<reply-button-ref>"}
browser action=snapshot profile=openclaw compact=true
# 답글 입력창에 텍스트 입력 후 Reply 버튼 클릭
```

**方法 2：在推文页面回复**
```
browser action=open profile=openclaw targetUrl="https://x.com/username/status/1234567890"
browser action=snapshot profile=openclaw compact=true
# 답글 입력창 찾아서 입력
```

### 查看个人资料

```
browser action=open profile=openclaw targetUrl="https://x.com/username"
browser action=snapshot profile=openclaw compact=true
```

### 搜索

```
browser action=open profile=openclaw targetUrl="https://x.com/search?q=검색어&src=typed_query"
browser action=snapshot profile=openclaw compact=true
```

### 关注

在个人资料页面找到 `button "Follow"` 并点击：
```
browser action=act profile=openclaw request={"kind":"click","ref":"<follow-ref>"}
```

---

## 关键要点

1. **先创建快照（Snapshot）** - 在执行任何操作前先查看当前状态。
2. **引用（References）会随每次操作而变化** - 必须在每次操作后重新查找引用。
3. **设置 `compact=true`** - 以节省令牌（tokens）。
4. **推文结构**：每条推文都包含一个 `article` 元素，其中包含作者、内容和按钮。
5. **发布前确认内容** - 确保用户已看到你要发布的推文内容。

---

## 故障排除

| 问题 | 解决方案 |
|------|------|
| 浏览器无法使用 | 检查 Xvfb 是否正常运行，设置 DISPLAY=:99，然后重启 Gateway。|
| 无法登录 | 转到 `/login` 页面后手动登录。|
| “发布”按钮被禁用 | 确认文本输入是否正确。|
| 遭到发送限制（Rate limit） | 稍等片刻后再尝试。|

---

## 与 bird CLI 的比较

| 功能 | bird CLI | chirp (浏览器) |
|------|----------|-----------------|
| 安装 | 需要 brew 工具 | 只需要 Xvfb 即可。|
| 认证方式 | 通过提取 cookie 进行认证 | 依赖浏览器会话（可更改）。|
| 稳定性 | 基于 API 运行 | 依赖于用户界面（可能发生变化）。|
| 执行速度 | 速度较快 | 速度稍慢。|