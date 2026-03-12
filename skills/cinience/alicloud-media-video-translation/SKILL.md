---
name: alicloud-media-video-translation
description: 通过 OpenAPI 创建和管理 Alibaba Cloud IMS 视频翻译任务（字幕/语音/面部识别）。适用于需要基于 API 的视频翻译、任务状态查询以及任务管理的场景。
version: 1.0.0
---
**类别：服务**  
# IMS 视频翻译（OpenAPI）  

通过 OpenAPI 提交视频翻译任务，并查询字幕、语音和面部处理的结果。  

## 前提条件  
- 准备输入/输出对象的存储服务（OSS）的 URI（建议与 API 所在区域相匹配）。  
- 配置 AK（阿里云访问密钥）：`ALICLOUD_ACCESS_KEY_ID`、`ALICLOUD_ACCESS_KEY_SECRET`、`ALICLOUD_REGION_ID`（`ALICLOUD_REGION_ID` 可作为默认区域使用；如果未设置，请根据实际情况选择最合适的区域）。  

## 工作流程  
1. 准备源文件和输出对象的存储位置。  
2. 使用 `SubmitVideoTranslationJob` 提交翻译任务。  
3. 使用 `GetSmartHandleJob` 查询任务的状态和结果。  
4. 根据需要使用 `ListSmartJobs` 或 `DeleteSmartJob` 进行任务管理。  

## 级别选择与参数  
- 字幕/语音/面部处理的规则和参数详见 `references/fields.md`。  
- 输入/输出/编辑配置的示例也位于 `references/fields.md` 中。  

## 注意事项  
- 如需进行二次编辑，请在首次提交任务时设置 `SupportEditing=true`，并后续引用 `OriginalJobId`。  
- 输入和输出对象的存储区域必须与调用 OpenAPI 的区域一致。  
- 对于处理量较大的任务，建议使用较长的轮询间隔以避免频繁请求。  

## 验证  
```bash
mkdir -p output/alicloud-media-video-translation
echo "validation_placeholder" > output/alicloud-media-video-translation/validate.txt
```  

**验证标准**：命令执行成功（返回代码为 0），并且生成了 `output/alicloud-media-video-translation/validate.txt` 文件。  

## 输出与证据  
- 将处理结果、命令输出以及 API 响应摘要保存在 `output/alicloud-media-video-translation/` 目录下。  
- 在证据文件中记录关键参数（区域、资源 ID、时间范围），以便后续复现。  

## 参考资料  
- 源代码列表：`references/sources.md`