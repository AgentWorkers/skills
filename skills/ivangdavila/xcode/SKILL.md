---
name: Xcode
description: 避免常见的 Xcode 错误：签名问题、构建设置错误以及缓存损坏问题。
metadata: {"clawdbot":{"emoji":"🔨","requires":{"bins":["xcodebuild"]},"os":["darwin"]}}
---

## 签名问题  
- “自动”签名功能仍需手动选择团队（在“签名与权限”设置中进行配置）  
- 配置文件（provisioning profile）不匹配：捆绑ID（bundle ID）必须完全一致（包括大小写）  
- “没有签名证书”：打开钥匙链（Keychain），检查证书是否有效且未过期  
- 设备未注册：在开发者门户中添加设备的UDID，然后重新生成配置文件  
- 在持续集成/持续部署（CI/CD）过程中需要手动签名，因为自动签名功能在无界面（headless）构建环境中无法正常工作  

## 派生数据（Derived Data）损坏问题  
- 更新Xcode后出现随机构建失败：删除`~/Library/Developer/Xcode/DerivedData`文件夹  
- 报告“模块未找到”（Module not found），但实际上模块存在：清理Derived Data文件夹并重新启动Xcode  
- 缓存问题：构建过程时有时会失败，但随后又能正常运行  
- 单纯使用`xcodebuild clean`命令可能不够，有时需要手动删除Derived Data文件夹  

## 构建设置（Build Settings）的层级结构  
- 设置顺序为：项目（Project）→ 目标（Target）→ xcconfig → 命令行（command line）；后续设置会覆盖之前的设置  
- 使用`$(inherited)`命令是为了在现有设置的基础上进行添加，而不是替换原有设置  
- Swift相关的配置应使用`SWIFT_ACTIVE_COMPILATION_CONDITIONS`，而非`OTHER_SWIFT_FLAGS`  
- Objective-C相关的配置应使用`GCC_PREPROCESSOR DEFINITIONS`，并添加到现有设置中，而非替换原有设置  

## 归档（Archive）与构建（Build）的区别  
- 默认情况下，归档使用发布（Release）配置；而构建使用调试（Debug）配置  
- 在模拟器中可以正常运行，但在归档模式下失败：检查发布模式的构建设置  
- 归档文件需要有效的签名证书；而模拟器构建不需要签名证书  
- 对于框架（frameworks），应将`SKIP_INSTALL`设置为`YES`，否则归档文件可能包含无效的框架  

## 权限（Capabilities）与 entitlements 文件  
- Xcode中的权限设置必须与entitlements文件内容一致；不一致会导致程序崩溃  
- 推送通知（Push notifications）功能需要同时满足App ID权限和provisioning profile的要求  
- 相关域名（associated domains）需要通过`apple-app-site-association`文件进行配置，并托管在服务器上  
- 共享钥匙链（Keychain）功能需要指定特定的用户组；默认情况下仅允许当前应用程序访问  

## 依赖项（Dependencies）  
- SPM（Spotify Package Manager）和CocoaPods之间可能存在冲突，请注意检查是否存在重复的符号  
- 更新Pod与安装Pod的区别：`install`命令会使用`Podfile.lock`文件，而`update`命令会忽略该文件  
- 报告“框架未找到”：检查框架的搜索路径（Framework Search Paths），并确认框架是嵌入（embed）还是链接（link）到项目中  
- 如果SPM包解析失败，请删除`Package.resolved`文件并重置包缓存  

## 常见问题解决方法  
- 如果构建失败但没有明确的错误信息，可以通过“报告导航器”（Report Navigator）获取详细信息  
- 如果模拟器卡住，可以使用`xcrun simctl shutdown all`和`xcrun simctl erase all`命令进行恢复  
- 如果索引生成失败，可以删除Derived Data文件夹中的索引文件  
- 如果自动补全功能失效，可以重启Xcode；如果问题仍然存在，可以删除Derived Data文件夹  

## 命令行构建（CLI Builds）  
- 使用`xcodebuild -showBuildSettings`命令查看具体的构建设置  
- 在持续集成过程中使用`-allowProvisioningUpdates`选项以实现自动签名功能（需要钥匙链访问权限）  
- 使用`-destination`参数指定构建目标，例如`platform=iOS Simulator,name=iPhone 15`  
- `xcrun altool`命令已被弃用，建议使用`xcrun notarytool`进行代码签名验证