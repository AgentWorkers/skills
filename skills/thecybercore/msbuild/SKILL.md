# 技能：.NET / ASP.NET 的 80 个常用 MSBuild 命令（CLI）

## 目的
本技能提供了一组实用且按优先级排序的 80 个最常用的命令模板，用于通过命令行（使用 `dotnet msbuild` 或 `msbuild`）处理 .NET / ASP.NET 项目。这些命令反映了日常开发工作流程：恢复依赖项 → 构建 → 测试 → 发布/打包 → 诊断 → 持续集成（CI）优化。

## 典型的 ASP.NET 开发者工作流程（这些命令为何被优先考虑）
典型的 ASP.NET CLI 工作流程包括：
1. **恢复依赖项**（在持续集成（CI）过程中通常处于锁定模式）
2. **快速构建**（调试模式）并确保构建的可靠性（发布模式）
3. **反复测试**（包括过滤、日志记录和结果目录管理；在 CI 过程中可以选择不构建或不恢复依赖项）
4. **发布构建成果**（生成可执行的文件）
5. **打包库**（并设置版本信息）
6. **诊断构建问题**（通过分析二进制日志、调整日志详细程度等手段）
7. **优化持续集成流程**（确保构建过程的稳定性和可重复性）

命令的优先级基于其在工作流程中的使用频率和重要性。

## 常用约定：
- 建议使用跨平台的命令：`dotnet msbuild`
- 在安装了 Visual Studio Build Tools 的 Windows 系统上，也可以使用 `msbuild`
- 目标（Targets）的格式为：`/t:<Target>`
- 属性（Properties）的格式为：`/p:Name=value`
- 日志记录（Logging）的选项包括：`/v:<level>`、`/bl[:file]`、`/fl`、`/pp`
- 多线程构建（Multiproc）的选项为：`/m[:n]`
- 注意：`dotnet test` 也被包含在内，因为它是一个实用的测试命令行工具（实际上它会调用 MSBuild 来执行测试任务）。

---

## 前 80 个常用命令（1 代表最重要）

> 请根据实际情况替换 `MySolution.sln`、`src/MyWeb/MyWeb.csproj` 和 `tests/...` 等路径。

### A) 恢复依赖项 / 构建 / 清理 / 重新构建（日常操作）
1) 恢复解决方案的依赖项
```bash
dotnet msbuild MySolution.sln /t:Restore
```

2) 构建解决方案（调试模式）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Debug
```

3) 构建解决方案（发布模式）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release
```

4) 清理解决方案
```bash
dotnet msbuild MySolution.sln /t:Clean /p:Configuration=Debug
```

5) 重新构建解决方案（先清理再构建）
```bash
dotnet msbuild MySolution.sln /t:Rebuild /p:Configuration=Release
```

6) 一次性完成恢复和构建操作
```bash
dotnet msbuild MySolution.sln /restore /t:Build /p:Configuration=Debug
```

7) 在不恢复依赖项的情况下构建（适用于持续集成）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /p:Restore=false
```

8) 并行构建（充分利用 CPU 资源）
```bash
dotnet msbuild MySolution.sln /t:Build /m /p:Configuration=Release
```

9) 降低构建过程中的日志输出量（适合持续集成环境）
```bash
dotnet msbuild MySolution.sln /t:Build /nologo /v:minimal /p:Configuration=Release
```

10) 仅构建单个项目
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Build /p:Configuration=Debug
```

11) 明确指定构建平台
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /p:Platform="Any CPU"
```

12) 将警告视为错误
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /p:TreatWarningsAsErrors=true
```

13) 确保构建过程的稳定性（避免意外结果）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /p:Deterministic=true
```

14) 设置持续集成相关的构建模式（如 SourceLink 和版本控制行为）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /p:ContinuousIntegrationBuild=true
```

15) 禁用增量更新检查（强制执行完整构建）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /p:DisableFastUpToDateCheck=true
```

16) 在构建过程中使用预定义的常量
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Build /p:Configuration=Debug /p:DefineConstants="TRACE;DEBUG;MYFLAG"
```

17) 设置输出路径（以便存放构建成果）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Build /p:Configuration=Release /p:OutputPath=artifacts/bin/
```

18) 设置基础中间输出路径（用于隔离构建文件和缓存）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Build /p:Configuration=Release /p:BaseIntermediateOutputPath=artifacts/obj/
```

19) 禁用共享编译机制（避免某些奇怪的构建问题）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Debug /p:UseSharedCompilation=false
```

20) 显示 MSBuild 的版本信息
```bash
dotnet msbuild -version
```

### B) 测试（基于 MSBuild 的实用命令）
21) 运行整个解决方案的测试
```bash
dotnet test MySolution.sln -c Release
```

22) 仅运行测试而不构建整个解决方案
```bash
dotnet test MySolution.sln -c Release --no-build
```

23) 仅恢复依赖项而不构建解决方案
```bash
dotnet test MySolution.sln -c Release --no-restore
```

24) 仅测试单个测试项目
```bash
dotnet test tests/MyWeb.Tests/MyWeb.Tests.csproj -c Debug
```

25) 根据完整路径过滤测试用例
```bash
dotnet test MySolution.sln -c Release --filter "FullyQualifiedName~MyNamespace"
```

26) 按属性或类别过滤测试用例
```bash
dotnet test MySolution.sln -c Release --filter "TestCategory=Integration"
```

27) 使用 TRX 日志工具记录测试结果
```bash
dotnet test MySolution.sln -c Release --logger "trx"
```

28) 设置测试结果目录
```bash
dotnet test MySolution.sln -c Release --results-directory artifacts/testresults
```

29) 收集代码覆盖率数据（支持跨平台）
```bash
dotnet test MySolution.sln -c Release --collect "XPlat Code Coverage"
```

30) 增加日志的详细程度
```bash
dotnet test MySolution.sln -c Release -v normal
```

31) 显示详细的错误信息
```bash
dotnet test MySolution.sln -c Release --blame
```

32) 通过名称运行特定的测试用例
```bash
dotnet test MySolution.sln -c Release --filter "Name=MySpecificTest"
```

### C) 发布（针对 ASP.NET Core 的场景）
33) 发布解决方案（发布模式，依赖框架）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release
```

34) 将构建成果发布到指定目录
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:PublishDir=artifacts/publish/
```

35) 为发布成果添加运行时标识符（RID）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:RuntimeIdentifier=linux-x64
```

36) 生成自包含的可执行文件
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:RuntimeIdentifier=linux-x64 /p:SelfContained=true
```

37) 明确指定所需的框架版本
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:SelfContained=false
```

38) 生成单文件版本的发布成果
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:RuntimeIdentifier=win-x64 /p:PublishSingleFile=true
```

39) 生成可直接运行的发布成果
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:PublishReadyToRun=true
```

40) 使用特殊选项生成精简版的发布文件
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:PublishTrimmed=true
```

41) 生成包含环境信息的发布文件
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:RuntimeIdentifier=linux-x64 /p:PublishSingleFile=true /p:PublishTrimmed=true
```

42) 为发布成果添加版本标签
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:EnvironmentName=Production
```

43) 为多目标框架（TFM）项目指定正确的框架版本
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:TargetFramework=net8.0
```

44) 在发布过程中使用持续集成相关的属性
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:ContinuousIntegrationBuild=true /p:Deterministic=true
```

45) 同时发布 RID、自包含文件和构建日志
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:RuntimeIdentifier=linux-x64 /p:SelfContained=true /p:PublishDir=artifacts/publish/linux-x64/
```

### D) 打包 / NuGet 管理 / 版本控制
47) 将库打包成可执行的文件
```bash
dotnet msbuild src/MyLib/MyLib.csproj /t:Pack /p:Configuration=Release
```

48) 将打包结果保存到自定义路径
```bash
dotnet msbuild src/MyLib/MyLib.csproj /t:Pack /p:Configuration=Release /p:PackageOutputPath=artifacts/nuget/
```

49) 为打包文件设置版本信息
```bash
dotnet msbuild src/MyLib/MyLib.csproj /t:Pack /p:Configuration=Release /p:Version=1.2.3
```

50) 设置文件的版本号（AssemblyVersion 和 FileVersion）
```bash
dotnet msbuild src/MyLib/MyLib.csproj /t:Build /p:Configuration=Release /p:AssemblyVersion=1.2.0.0 /p:FileVersion=1.2.3.0
```

51) 为版本信息添加元数据（用于版本控制）
```bash
dotnet msbuild src/MyLib/MyLib.csproj /t:Build /p:Configuration=Release /p:InformationalVersion=1.2.3+sha.abcdef
```

52) 生成用于版本控制的 `packages.lock.json` 文件
```bash
dotnet msbuild MySolution.sln /t:Restore /p:RestorePackagesWithLockFile=true
```

53) 在锁定模式下恢复依赖项（如果锁定信息发生变化则停止构建）
```bash
dotnet msbuild MySolution.sln /t:Restore /p:RestoreLockedMode=true
```

54) 使用自定义的 `NuGet.config` 文件来控制依赖项的恢复过程
```bash
dotnet msbuild MySolution.sln /t:Restore /p:RestoreConfigFile=NuGet.config
```

55) 使用自定义的文件夹来存储打包后的文件（便于持续集成缓存）
```bash
dotnet msbuild MySolution.sln /t:Restore /p:RestorePackagesPath=artifacts/nuget-packages
```

### E) 诊断 / 故障排除
56) 查看二进制日志（binlog）——这是第一步应采取的措施
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /bl
```

57) 指定日志文件的路径
```bash
dotnet msbuild MySolution.sln /t:Build /p:Configuration=Release /bl:artifacts/logs/build.binlog
```

58) 调整日志的详细程度（详细或仅显示诊断信息）
```bash
dotnet msbuild MySolution.sln /t:Build /v:detailed
```

59) 仅在需要时显示诊断信息
```bash
dotnet msbuild MySolution.sln /t:Build /v:diag
```

60) 使用文本日志记录构建过程
```bash
dotnet msbuild MySolution.sln /t:Build /fl /flp:logfile=artifacts/logs/build.log;verbosity=normal
```

61) 在控制台显示构建过程的摘要信息及性能数据
```bash
dotnet msbuild MySolution.sln /t:Build /clp:Summary;PerformanceSummary
```

62) 在构建前预处理项目文件
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /pp:artifacts/logs/preprocessed.xml
```

63) 为整个解决方案生成构建过程图表
```bash
dotnet msbuild MySolution.sln /t:Build /graphBuild /p:Configuration=Release
```

64) 显式运行特定的构建目标（例如：仅执行清理操作）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Clean /p:Configuration=Release
```

65) 显示所有执行的命令行指令（有助于重现构建过程）
```bash
dotnet msbuild MySolution.sln /t:Build /m /v:minimal /clp:ShowCommandLine
```

66) 禁用节点的重用机制（提高持续集成的稳定性）
```bash
dotnet msbuild MySolution.sln /t:Build /nr:false /p:Configuration=Release
```

67) 限制构建过程中的并行度
```bash
dotnet msbuild MySolution.sln /t:Build /m:4 /p:Configuration=Release
```

### F) 高级构建控制选项
68) 定义自定义属性以满足特定需求
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Build /p:Configuration=Release /p:MyCustomProperty=Value
```

69) 快速恢复依赖项（便于进行测试）
```bash
dotnet msbuild MySolution.sln /t:Restore /p:RestoreSources="https://api.nuget.org/v3/index.json;https://myfeed/v3/index.json"
```

70) 禁用自动恢复依赖项的功能（实现完全的控制）
```bash
dotnet msbuild MySolution.sln /t:Build /p:Restore=false /p:BuildProjectReferences=true
```

71) 在不包含项目引用的情况下进行构建（便于调试）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Build /p:BuildProjectReferences=false
```

72) 使用 AppHost 运行应用程序（适用于 exe 格式的应用程序）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:RuntimeIdentifier=linux-x64 /p:SelfContained=true /p:UseAppHost=true
```

73) 在不使用 AppHost 的情况下进行发布（处理特殊情况）
```bash
dotnet msbuild src/MyWeb/MyWeb.csproj /t:Publish /p:Configuration=Release /p:UseAppHost=false
```

74) 在恢复依赖项时使用交互式身份验证机制（适用于私有环境）
```bash
dotnet msbuild MySolution.sln /t:Restore /p:NuGetInteractive=true
```

75) 修改 MSBuild 的 SDK 路径（处理特殊场景）
```bash
dotnet msbuild MySolution.sln /t:Build /p:MSBuildSDKsPath=/path/to/sdks
```

### G) msbuild.exe 的各种用法（适用于 Windows 和 Visual Studio Build Tools）
76) 使用 `msbuild.exe` 构建解决方案
```bash
msbuild MySolution.sln /t:Build /p:Configuration=Release /m
```

77) 使用 `msbuild.exe` 恢复依赖项
```bash
msbuild MySolution.sln /t:Restore
```

78) 使用 `msbuild.exe` 发布构建成果
```bash
msbuild src\MyWeb\MyWeb.csproj /t:Publish /p:Configuration=Release /p:PublishDir=artifacts\publish\
```

79) 使用 `msbuild.exe` 生成二进制日志
```bash
msbuild MySolution.sln /t:Build /p:Configuration=Release /bl:artifacts\logs\msbuild.binlog
```

80) 使用 `msbuild.exe` 对项目文件进行预处理
```bash
msbuild src\MyWeb\MyWeb.csproj /pp:artifacts\logs\preprocessed.xml
```

* * *

## 如何使用本技能
当您描述一个构建目标（例如：“发布一个适用于 Linux x64 系统的自包含单文件版本的应用程序”时，本技能会输出：
- 与此目标最相关的 3 个命令；
- 最重要的几个 MSBuild 属性；
- 以及一个用于在构建失败时生成二进制日志的诊断命令（通常为 `/bl`）。

## 注意事项：
- `Trim`、`ReadyToRun` 和 `SingleFile` 等选项可能会对应用程序的具体行为产生影响。
- 如果遇到构建问题，请使用 `/bl` 重新构建项目，并使用 MSBuild 的结构化日志查看器（MSBuild Structured Log Viewer）来排查问题。