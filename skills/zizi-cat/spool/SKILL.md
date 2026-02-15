---
name: spool
description: "Threads CLI：使用 OpenClaw 浏览器工具在 Meta 的 Threads 中执行读取、发布、回复和搜索操作。适用于用户需要与 Threads 进行交互的场景，例如发布内容、查看时间线、浏览用户资料、回复帖子或进行搜索。"
homepage: https://github.com/zizi-cat/spool
metadata: {"clawdhub":{"emoji":"🧵"}}
---

# 使用 OpenClaw 浏览器工具操作 Threads (threads.net)

## 先决条件

### 环境要求
- 已启用浏览器工具的 OpenClaw
- `openclaw` 浏览器配置文件
- 已完成 Threads 账户登录

### 如果使用无图形界面的服务器（无 GUI）

需要 Xvfb 虚拟显示器：

```bash
# 1. Xvfb 설치 및 서비스 등록
sudo apt install -y xvfb
sudo tee /etc/systemd/system/xvfb.service << 'EOF'
[Unit]
Description=X Virtual Frame Buffer
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now xvfb

# 2. OpenClaw Gateway에 DISPLAY 환경변수 추가
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
echo -e '[Service]\nEnvironment=DISPLAY=:99' > ~/.config/systemd/user/openclaw-gateway.service.d/display.conf
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

### 登录（仅首次需要）

```
browser action=start profile=openclaw
browser action=open profile=openclaw targetUrl="https://www.threads.net/login"
# 사용자에게 수동 로그인 요청
```

---

## 使用方法

### 1. 阅读时间线

```
browser action=open profile=openclaw targetUrl="https://www.threads.net"
browser action=snapshot profile=openclaw compact=true
```

在结果中可以查看每篇帖子的作者、内容以及点赞/评论数量。

### 2. 发布帖子（完整流程）

**步骤 1：返回首页**
```
browser action=open profile=openclaw targetUrl="https://www.threads.net"
browser action=snapshot profile=openclaw compact=true
```

**步骤 2：找到并点击“What’s new?”按钮**
在快照中找到包含 “What’s new?” 或 “Empty text field” 的按钮的引用（ref）：
```
browser action=act profile=openclaw request={"kind":"click","ref":"e14"}
```
（引用因快照而异！请务必在快照中确认）

**步骤 3：在对话框中输入文本**
```
browser action=snapshot profile=openclaw compact=true
```
找到 `textbox` 的引用：
```
browser action=act profile=openclaw request={"kind":"type","ref":"e14","text":"포스팅 내용"}
```

**步骤 4：点击 Post 按钮**
```
browser action=act profile=openclaw request={"kind":"click","ref":"e22"}
```
（Post 按钮的引用同样需要在快照中确认）

**步骤 5：确认**
```
browser action=snapshot profile=openclaw compact=true
```
当看到 “Posted” 文本和 “View” 链接时，表示操作成功！

### 3. 查看个人资料

```
browser action=open profile=openclaw targetUrl="https://www.threads.net/@username"
browser action=snapshot profile=openclaw compact=true
```

### 4. 搜索

```
browser action=open profile=openclaw targetUrl="https://www.threads.net/search?q=검색어"
browser action=snapshot profile=openclaw compact=true
```

### 5. 回复帖子

```
# 게시물 열기
browser action=open profile=openclaw targetUrl="https://www.threads.net/@user/post/POSTID"
browser action=snapshot profile=openclaw compact=true

# Reply 버튼 클릭 (ref 확인 후)
browser action=act profile=openclaw request={"kind":"click","ref":"<reply-ref>"}

# 텍스트 입력 및 게시 (포스팅과 동일)
```

---

## 关键要点

1. **先创建快照！** - 在进行任何操作之前，先使用快照记录当前页面状态和引用。
2. **引用每次都会变化** - 请在快照结果中重新查找引用。
3. **始终使用 “compact=true”** - 以节省令牌。
4. **保持 `targetId` 不变** - 如果要在同一标签页中继续操作，请使用 `targetId` 参数。
5. **发布前确认** - 确保用户已阅读内容后再进行发布。

---

## 故障排除

| 问题 | 解决方法 |
|------|------|
| 浏览器工具无法使用 | 确认 Xvfb 是否正在运行，检查 DISPLAY=:99 的设置，并重启 Gateway。|
| 无法登录 | 转到 `/login` 页面后手动登录。|
| 无法找到引用 | 重新创建快照并查找相似的文本或按钮。|
| 无法发布帖子 | 检查 Post 按钮是否被禁用（可能需要输入文本）。|