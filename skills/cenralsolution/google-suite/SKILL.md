# Google Suite Skill

**版本：** 1.0.0  
**类别：** 生产力工具  
**描述：** 提供统一访问Gmail、Google Calendar和Google Drive API的功能，支持发送/接收邮件、管理日历事件以及处理文件。

## 功能  

### Gmail  
- 发送邮件  
- 查看邮件（列表、搜索、获取详细信息）  
- 删除邮件  
- 将邮件标记为已读/未读  

### Google Calendar  
- 列出日历事件  
- 创建日历事件  
- 更新日历事件  
- 删除日历事件  

### Google Drive  
- 列出文件  
- 上传文件  
- 下载文件  
- 删除文件  
- 搜索文件  

## 设置  

### 先决条件  
- Python 3.8及以上版本  
- 拥有Google Cloud项目及相应的OAuth2凭证  
- 在Google Cloud Console中启用Gmail、Calendar和Drive API  

### 环境变量  
- `GOOGLE_OAUTH_CLIENT_ID`：OAuth2客户端ID  
- `GOOGLE_OAUTH_CLIENT_SECRET`：OAuth2客户端密钥  
- `GOOGLE_OAUTH_REDIRECT_URI`：OAuth2重定向URI（例如：http://localhost:8080/callback）  

### 所需权限  
- `https://www.googleapis.com/auth/gmail.readonly`  
- `https://www.googleapis.com/auth/gmail.send`  
- `https://www.googleapis.com/auth/gmail.modify`  
- `https://www.googleapis.com/auth/calendar`  
- `https://www.googleapis.com/auth/drive`  

### 令牌存储  
- 令牌默认存储在`google_suite_tokens.json`文件中  

### 安装  
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```  

## 使用方法  

### 认证  
- 首次使用时，该工具会请求进行OAuth2认证。  
- 访问提供的URL，登录后粘贴授权代码。  
- 令牌会自动保存以供后续使用。  

### 示例代码  

#### 发送邮件  
```python
skill.execute({
    "service": "gmail",
    "action": "send",
    "to": "user@example.com",
    "subject": "测试邮件",
    "body": "来自OpenClaw的消息！"
})
```  

#### 查看邮件  
```python
skill.execute({
    "service": "gmail",
    "action": "list",
    "query": "from:boss@company.com"
})
```  

#### 删除邮件  
```python
skill.execute({
    "service": "gmail",
    "action": "delete",
    "message_id": "XYZ123..."
})
```  

#### 列出日历事件  
```python
skill.execute({
    "service": "calendar",
    "action": "list",
    "days": 7
})
```  

#### 创建日历事件  
```python
skill.execute({
    "service": "calendar",
    "action": "create",
    "summary": "团队会议",
    "start": "2024-03-01T10:00:00",
    "end": "2024-03-01T11:00:00"
})
```  

#### 列出Drive文件  
```python
skill.execute({
    "service": "drive",
    "action": "list",
    "query": "name contains 'report'"
})
```  

#### 上传文件到Drive  
```python
skill.execute({
    "service": "drive",
    "action": "upload",
    "file_path": "./myfile.pdf"
})
```  

## 安全性  
- OAuth2令牌会被安全存储，不会被记录。  
- 所有凭证均从环境变量中读取。  
- 不会打印或记录任何敏感数据。  

## 故障排除  
- 确保在Google Cloud Console中启用了所有必要的API。  
- 检查OAuth2凭证是否正确，并确保重定向URI设置正确。  
- 如需强制重新认证，可删除`google_suite_tokens.json`文件。  

## 参考资料  
- [Google API Python客户端](https://github.com/googleapis/google-api-python-client)  
- [Gmail API文档](https://developers.google.com/gmail/api)  
- [Calendar API文档](https://developers.google.com/calendar/api)  
- [Drive API文档](https://developers.google.com/drive/api)