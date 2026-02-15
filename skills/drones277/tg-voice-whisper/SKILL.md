---

**名称：tg-voice-whisper**  
**描述：** 使用本工具可将 Telegram 中的音频消息（.ogg 格式，采用 Opus 编码）自动转录为文本。该工具基于 OpenAI 的 Whisper 模型（tiny 版本）进行转录，并在转录完成后自动删除相关文件以保护用户隐私。无需使用 API 密钥，安装完成后可完全离线使用。  
**图标：** 🎙️🔊  

**依赖软件：**  
- `whisper`  
- `ffmpeg`  

**安装方法：**  
  - 使用 `apt` 包管理器：  
    ```bash
    sudo apt install ffmpeg
    ```  
  - 使用 `pip` 包管理器：  
    ```bash
    sudo pip install openai-whisper
    ```  
  （安装时需使用 `--break-system-packages` 选项以避免破坏系统包的依赖关系。）  

**系统要求：**  
建议服务器配备至少 4GB 的内存，以确保快速稳定的转录性能（在 1 核 CPU 上，缓存模型可在 1 秒内完成转录）。  

**安全性说明：**  
- 该工具仅在本机运行，不会存储任何外部 API 密钥或用户数据。  

**使用方法（作为代理服务）：**  
当音频文件（.ogg 格式）被上传到 `/root/.openclaw/media/inbound/` 目录时，系统会自动启动转录流程。  

**自动配置方案：**  
- 可以每隔 5 秒启动一个子进程或定时任务来执行转录任务：  
  ```bash
  # 使用子进程：
  python tg-voice-whisper.py
  ```  
  或者使用 `cron` 定时任务：  
  ```bash
  crontab -e
  0 5 * * * /path/to/tg-voice-whisper.py
  ```  

**测试命令：**  
```bash
  whisper /path/to/your/ogg/file --model tiny --language ru
  ```  

**注意事项：**  
- 首次运行时，模型文件（`tiny.bin`）的下载时间约为 15 秒（文件大小约 72MB，存储在 `~/.cache/whisper` 目录中）。  
- 在 1 核 CPU 和 4GB 内存的环境下，转录速度可达到 1 秒以内。  
- 最适合的语种为俄语（`ru`）和英语（`en`）；系统会自动检测语言。  
- 转录准确率：对于俄语语音，tiny 模型的准确率约为 85–95%；如需更高准确率，可升级到 `base` 或 `small` 模型。