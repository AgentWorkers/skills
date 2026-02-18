---
name: katok
description: macOS版KakaoTalk自动化CLI工具。支持查看好友列表、聊天室列表、读取消息以及发送消息等功能。当您需要执行与KakaoTalk相关的操作时，可以使用该工具。
allowed-tools: Bash(katok *)
---
# 使用 katok 实现 KakaoTalk 自动化

通过使用 macOS 的辅助功能 API（Accessibility API），您可以实现 KakaoTalk 的自动化操作。请确保已安装 KakaoTalk 应用，并且已授予相应的辅助功能权限。

## 快速入门

```bash
# 채팅방 목록 보기 (기본 명령)
katok chats
# 친구 목록 보기
katok friends
# 특정 채팅방 메시지 읽기
katok messages "홍길동"
# 메시지 보내기
katok send "홍길동" "안녕하세요"
```

## 命令

### chats （基本命令）

以 CSV 格式输出聊天室列表。

```bash
# 기본 (최근 50개)
katok chats
# 개수 제한
katok chats --limit 10
katok chats -l 10
# 건너뛰기 (페이지네이션)
katok chats --offset 20
katok chats -o 20
# 조합
katok chats -l 10 -o 20
```

输出格式：`name, time, member_count, unread_count`

### friends

以 CSV 格式输出好友列表。每个好友项之间用 `#` 分隔。

```bash
katok friends
```

输出格式：`name, status_message`

### messages

以 CSV 格式输出特定聊天室中的消息。系统消息以 `#` 开头。

```bash
# 기본 (최근 50개)
katok messages "채팅방 이름"
# 개수 제한
katok messages "채팅방 이름" --limit 20
katok messages "채팅방 이름" -l 20
```

输出格式：`sender, content, time`

- 自己发送的消息的发送者显示为 `나`（即 “我”）
- 图片会显示为 `[이미지]`（即 “[图片]”）
- 系统消息会以 `# 메시지 내용` 的格式显示

### send

向特定聊天室发送消息。

```bash
katok send "채팅방 이름" "보낼 메시지"
```

## 示例：查看未读消息

```bash
katok chats -l 10
# 출력에서 unread_count > 0인 채팅방 확인 후 메시지 읽기
katok messages "친구이름" -l 5
```

## 示例：阅读消息并回复

```bash
katok messages "친구이름" -l 10
katok send "친구이름" "확인했습니다!"
```

## 先决条件

- **必须安装 katok CLI**：
  - 如果未安装，请执行：`brew install sunghyun-k/tap/katok`
- **必须安装 KakaoTalk macOS 应用**：
  - 如果未安装，请访问 [KakaoTalk 下载页面](https://apps.apple.com/kr/app/kakaotalk/id869223134?mt=12) 进行安装，或使用 `mas install 869223134`（需要 mas-cli）。
  - 如果未运行 KakaoTalk，katok 会自动启动它。
- **终端（或运行环境）必须具有 macOS 辅助功能权限**：
  - 在系统设置 → 个人信息与安全 → 辅助功能中，允许终端应用程序访问相关功能。
- **该工具在屏幕保护程序或屏幕锁定状态下无法正常工作**。
- 聊天室名称必须与实际名称完全匹配。