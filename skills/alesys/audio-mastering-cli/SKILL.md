---

**名称：audio-mastering-cli**  
**描述：** 一个基于命令行的音频处理工具，无需参考音轨即可使用 `ffmpeg` 进行音频剪辑；支持音频或视频输入，输出格式为 WAV/MP3 或重新封装后的 MP4。  

**元数据：**  
```json
{
  "openclaw": {
    "emoji": "🎚️",
    "homepage": "https://github.com/alesys/openclaw-skill-audio-mastering-cli",
    "os": ["win32"],
    "requires": {
      "bins": ["ffmpeg", "powershell"]
    }
  }
}
```

---

## **音频剪辑 CLI**

当用户希望通过命令行对音频文件进行剪辑（无需参考音轨）时，可以使用此工具。

**支持的输入格式：**  
- 音频：`wav`, `aiff`, `flac`, `mp3`, `m4a`  
- 视频：`mp4`, `mov`, `m4v`, `mkv`, `webm`

**工作流程：**  
1. 检查输入文件是否存在。  
2. 执行以下命令：  
   ```powershell
   -ExecutionPolicy Bypass -File "{baseDir}/scripts/master_media.ps1" -InputFile "<ruta-archivo>" -MakeMp3
   ```  
3. 输出结果：  
   - 音频剪辑后的文件：`<base>_master.wav`  
   - 如果选择了 `-MakeMp3` 选项，输出文件为 `<base>_master.mp3`  
   - 如果输入为视频文件，输出文件为 `<base>_master.mp4`（包含原始视频和剪辑后的 AAC 320k 音频）  
4. 日志中会显示音量的峰值（loudness）信息。  

**应用的音频处理步骤：**  
- 首先应用高通滤波（highpass）和低通滤波（lowpass）处理。  
- 使用均衡器（EQ）进行轻微的音质调整和优化。  
- 接着使用压缩器（compressor）进行音量压缩。  
- 最后使用 `loudnorm` 工具进行两次音量标准化处理（确保跨平台的音量一致性）。  

**可选验证步骤：**  
```powershell
ffmpeg -hide_banner -i "<archivo_master.wav>" -af "loudnorm=I=-14:TP=-1:LRA=7:print_format=summary" -f null NUL
```  
此命令可用于验证音频处理的准确性。  

**注意事项：**  
- 对于视频文件，仅替换音频部分，视频流保持不变。  
- 如果在均衡器处理过程中出现音频削波（clipping）现象，建议降低输入音量或调整均衡器参数后再重新处理。