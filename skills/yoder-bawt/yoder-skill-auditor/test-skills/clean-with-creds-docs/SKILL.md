# API客户端辅助工具

## 说明
这是一组用于执行经过身份验证的API调用的辅助工具。

## 配置
请设置以下环境变量：
- `API_KEY`：来自提供商控制台的API密钥
- `SECRET_KEY`：用于签名请求的秘密密钥
- `AUTH_TOKEN`：用于身份验证的OAuth令牌

## 使用方法
```bash
# Set your credentials
export API_KEY="your-api-key-here"
export AUTH_TOKEN="your-token"
bash client.sh
```

## 安全注意事项
切勿将`.env`文件或`.aws/credentials`文件提交到版本控制系统中。
请将`password`和`credential`值存储在安全密钥管理器中。