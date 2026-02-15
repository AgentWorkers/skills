---
description: 管理、测试性能，并在本地 Ollama 模型之间切换，同时进行性能对比。
---

# Ollama Hub

用于管理和测试本地的Ollama模型。

**使用场景**：列出模型、下载新模型、测试模型性能或比较模型之间的差异。

## 前提条件

- Ollama已安装并正在运行（通过`ollama serve`或systemd服务启动）。
- 不需要API密钥。

## 操作指南

1. **列出已安装的模型**：
   ```bash
   ollama list                    # name, size, modified date
   ollama show <model>            # detailed info (parameters, template, license)
   ```

2. **下载/删除模型**：
   ```bash
   ollama pull llama3.3:70b       # download a model
   ollama pull mistral:latest     # latest version
   ollama rm <model>              # remove (confirm with user first!)
   ```

3. **测试模型性能**：
   ```bash
   # Time a response
   time ollama run <model> "Explain quantum computing in 3 sentences" --verbose 2>&1

   # Extract tokens/sec from verbose output
   ollama run <model> "Hello" --verbose 2>&1 | grep "eval rate"
   ```

4. **比较模型**：对多个模型使用相同的输入进行测试：
   ```
   ## 📊 Ollama Model Benchmark
   **Prompt:** "Explain quantum computing in 3 sentences"
   **Hardware:** [CPU/GPU specs]

   | Model | Size | Tokens/sec | Response Time | Quality |
   |-------|------|-----------|--------------|---------|
   | llama3.3:8b | 4.7GB | 42 t/s | 2.1s | ⭐⭐⭐⭐ |
   | mistral:7b | 4.1GB | 48 t/s | 1.8s | ⭐⭐⭐ |
   | phi3:mini | 2.3GB | 65 t/s | 1.2s | ⭐⭐⭐ |
   ```

5. **检查Ollama的运行状态**：
   ```bash
   curl -s http://localhost:11434/api/tags | jq .    # API check
   systemctl status ollama                            # service status
   ollama ps                                          # running models
   ```

## 模型命名规则

模型命名格式为：`name:tag`，例如 `llama3.3:8b`、`mistral:latest`、`codellama:13b-instruct`。

常见的标签包括：`latest`、`7b`、`13b`、`70b`、`instruct`、`code`。

## 注意事项

- **Ollama未运行**：请使用`ollama serve`或`systemctl start ollama`启动Ollama服务。
- **磁盘空间不足**：在下载大型模型之前，请使用`df -h`检查磁盘空间。70B大小的模型大约需要40GB的磁盘空间。
- **内存不足**：模型所需的内存容量与模型大小相关：7B模型大约需要8GB内存，70B模型大约需要48GB内存。
- **GPU与CPU的性能差异**：模型性能会受到硬件配置的影响，请在测试时注意这一点。
- **模型未找到**：请检查输入名称的拼写正确性。可以使用`ollama list`查看可用的模型名称，或访问[ollama.com/library](https://ollama.com/library)进行查询。
- **下载速度慢**：大型模型的下载时间较长，请耐心等待。`ollama pull`命令支持中断后继续下载。

## 常见问题解决方法

- **端口11434被占用**：可能有其他Ollama实例正在使用该端口。可以使用`lsof -i :11434`查看占用情况。
- **CUDA相关错误**：请使用`nvidia-smi`检查GPU驱动程序，必要时重新安装Ollama。
- **模型损坏**：请删除损坏的模型并重新下载：`ollama rm <model> && ollama pull <model>`。