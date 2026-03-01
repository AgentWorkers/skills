---
name: openclaw-gpu-bridge
description: "将计算密集型的机器学习任务（如 BERTScore 计算、嵌入向量生成等）卸载到一个或多个远程 GPU 机器上进行处理。"
---
# @elvatis_com/openclaw-gpu-bridge

OpenClaw插件用于将机器学习任务（BERTScore和嵌入计算）卸载到一个或多个远程GPU主机上。

## v0.2 主要特性

- 支持多GPU主机池（`hosts[]`）：
  - 采用轮询或最小负载均衡策略
  - 具有自动故障转移功能
  - 定期检查主机健康状况
- 与v0.1版本向后兼容（`serviceUrl` / `url`配置选项）
- 支持根据请求灵活选择模型（`model` / `model_type`）
- 提供GPU服务模型缓存机制（按需加载）
- 通过 `/status` 端点提供传输状态信息及批量处理进度日志

---

## 所使用的工具

- `gpu_health`
- `gpu_info`
- `gpu_status`（v0.2新增）
- `gpu_bertscore`
- `gpu_embed`

---

## OpenClaw插件配置

### v0.2推荐配置

```json
{
  "plugins": {
    "@elvatis_com/openclaw-gpu-bridge": {
      "hosts": [
        {
          "name": "rtx-2080ti",
          "url": "http://your-gpu-host:8765",
          "apiKey": "gpu-key-1"
        },
        {
          "name": "rtx-3090",
          "url": "http://your-second-gpu-host:8765",
          "apiKey": "gpu-key-2"
        }
      ],
      "loadBalancing": "least-busy",
      "healthCheckIntervalSeconds": 30,
      "timeout": 45,
      "models": {
        "embed": "all-MiniLM-L6-v2",
        "bertscore": "microsoft/deberta-xlarge-mnli"
      }
    }
  }
}
```

### v0.1版本兼容性配置

```json
{
  "plugins": {
    "@elvatis_com/openclaw-gpu-bridge": {
      "serviceUrl": "http://your-gpu-host:8765",
      "apiKey": "gpu-key",
      "timeout": 45
    }
  }
}
```

### 配置参数说明

- `hosts`：GPU主机列表（v0.2版本）
- `serviceUrl` / `url`：旧版本使用的单主机配置方式
- `loadBalancing`：轮询（`round-robin`）或最小负载均衡（`least-busy`）
- `healthCheckIntervalSeconds`：主机健康检查间隔时间
- `timeout`：计算端点的请求超时时间
- `apiKey`：为未配置主机密钥的主机提供的备用API密钥
- `models.embed`、`models.bertscore`：插件默认使用的模型

---

## GPU服务（Python实现）

```bash
cd gpu-service
pip install -r requirements.txt
uvicorn gpu_service:app --host 0.0.0.0 --port 8765
```

插件启动时会预加载默认模型：
- 嵌入计算模型：`all-MiniLM-L6-v2`
- BERTScore模型：`microsoft/deberta-xlarge-mnli`

其他模型会根据需求动态加载并缓存到内存中。

### 环境变量

- `API_KEY`：除 `/health` 端点外，所有端点都需要设置此环境变量
- `GPU_MAX_CONCURRENT`：最大并发作业数（默认值：2）
- `GPU_EMBED_BATCH`：用于进度日志记录的嵌入数据块大小（默认值：32）
- `MODEL_BERTSCORE`：BERTScore任务的默认模型
- `MODEL_EMBED`：嵌入计算的默认模型
- `TORCH_DEVICE`：指定使用的GPU设备（`cuda`、`cpu` 或 `cuda:1`）

---

## GPU服务API端点

- `GET /health`：获取主机健康状态
- `GET /info`：获取服务信息
- `GET /status`：查看任务队列、活跃任务及处理进度
- `POST /bertscore`：提交BERTScore计算请求
- `POST /embed`：提交嵌入计算请求

### 请求级别的模型配置

- `/bertscore`端点支持模型覆盖：
```json
{
  "candidates": ["a"],
  "references": ["b"],
  "model_type": "microsoft/deberta-xlarge-mnli"
}
```

- `/embed`端点支持模型覆盖：
```json
{
  "texts": ["hello world"],
  "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
}
```

---

## 在互联网上公开服务

如果需要将GPU服务暴露到外部网络，请采取以下安全措施：

1. **预共享密钥认证（强制要求）**
   - 在服务端设置 `API_KEY`
   - 在插件配置中配置相同的密钥（`apiKey`）
   - 所有请求都必须包含 `X-API-Key` 参数

2. **使用TLS/HTTPS（公共网络必备）**
   - 推荐方案：使用Nginx反向代理并配置Let’s Encrypt证书
   - 替代方案：直接使用uvicorn服务器并配置SSL证书/密钥

### Nginx反向代理配置示例

```nginx
server {
  listen 443 ssl http2;
  server_name gpu.example.com;

  ssl_certificate /etc/letsencrypt/live/gpu.example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/gpu.example.com/privkey.pem;

  location / {
    proxy_pass http://127.0.0.1:8765;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

### uvicorn服务器的SSL配置示例

```bash
uvicorn gpu_service:app --host 0.0.0.0 --port 8765 \
  --ssl-keyfile /path/key.pem \
  --ssl-certfile /path/cert.pem
```

3. **可选方案：使用WireGuard VPN进行私有网络保护**
   - 将服务部署在VPN网络中
   - 在插件配置的 `hosts` 列表中指定使用私有WireGuard IP地址

4. **增强安全性**
   - 防火墙仅允许OpenClaw服务器的IP地址通过
   - 在反向代理上设置速率限制
   - 定期检查和更新安全密钥

---

## 开发环境

该项目使用TypeScript编写，并以严格模式运行。

## 许可证

MIT许可证