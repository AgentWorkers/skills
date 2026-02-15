# Feishu 视频会议功能

用于管理 Feishu 视频会议（VC）。

## 使用方法

### 预订会议
创建会议预订。
```bash
node skills/feishu-vc/reserve.js --subject "Meeting Title" --time "2026-02-04T10:00:00+08:00"
```

## API 参考
- `reserve` API: `POST /open-apis/vc/v1/reserve`
- 所需权限: `vc:meeting:request`（更新会议预订信息）

## 设置要求
需要 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。