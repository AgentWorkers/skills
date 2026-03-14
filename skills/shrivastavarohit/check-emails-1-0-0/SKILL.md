# 从Himalaya服务中检查电子邮件

## 命令
```bash
himalaya envelope list --page 1 --page-size 10
```

## 使用方法
当用户输入“check emails”或类似指令时，执行以下操作：
- `himalaya envelope list --page 1 --page-size 10`

## 说明
- 该功能会读取用户邮箱中的最后10封电子邮件。
- 适用于快速查看最近的邮件。
- 除了指定页面编号（`page`）和每页显示的邮件数量（`page-size`）外，无需使用其他特殊参数。