---
slug: "rvt-to-ifc"
display_name: "RVT To IFC"
description: "将 RVT 文件转换为 IFC 格式。支持 IFC2x3、IFC4 和 IFC4.3 格式，并提供可自定义的导出设置。"
---

# RVT 到 IFC 的转换

> **注意：** RVT 是文件格式，而 IFC 是由 buildingSMART International 制定的开放标准。

## 商业案例

### 问题描述
IFC 是用于实现 BIM（建筑信息模型）互操作性的开放标准，但存在以下问题：
- 使用 Revit 的原生 IFC 导出功能需要 Autodesk 许可证；
- 导出设置会显著影响数据质量；
- 批量处理过程既繁琐又耗时。

### 解决方案
RVT2IFCconverter.exe 可以在离线环境下将 Revit 文件转换为 IFC 格式，无需许可证，并且用户可以完全控制导出设置。

### 商业价值
- **无需许可证**：无需安装 Autodesk 软件即可使用；
- **支持多种 IFC 版本**：IFC2x3、IFC4、IFC4.3；
- **支持批量处理**：能够处理数千个文件；
- **数据质量一致**：采用标准化的导出设置。

## 技术实现

### 命令行接口（CLI）语法
```bash
RVT2IFCconverter.exe <input.rvt> [<output.ifc>] [preset=<name>] [config="..."]
```

### IFC 版本
| 版本 | 适用场景 |
|---------|----------|
| IFC2x3 | 与大多数软件的兼容性 |
| IFC4 | 支持更多属性和现代 BIM 功能 |
| IFC4.3 | 适用于基础设施项目，是最新的标准 |

### 导出预设
| 预设 | 描述 |
|--------|-------------|
| `standard` | 默认的平衡导出设置 |
| `extended` | 最详细的导出内容和属性 |
| `custom` | 用户自定义的导出配置 |

### 示例
```bash
# Standard IFC export
RVT2IFCconverter.exe "C:\Projects\Building.rvt"

# IFC4 with extended settings
RVT2IFCconverter.exe "C:\Projects\Building.rvt" preset=extended

# Custom output path
RVT2IFCconverter.exe "C:\Projects\Building.rvt" "D:\Export\model.ifc"

# Custom configuration
RVT2IFCconverter.exe "C:\Projects\Building.rvt" config="ExportBaseQuantities=true; SitePlacement=Shared"
```

### Python 集成
```python
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class IFCVersion(Enum):
    """IFC schema versions."""
    IFC2X3 = "IFC2x3"
    IFC4 = "IFC4"
    IFC4X3 = "IFC4x3"


class ExportPreset(Enum):
    """Export presets."""
    STANDARD = "standard"
    EXTENDED = "extended"
    CUSTOM = "custom"


@dataclass
class IFCExportConfig:
    """IFC export configuration."""
    ifc_version: IFCVersion = IFCVersion.IFC4
    export_base_quantities: bool = True
    site_placement: str = "Shared"
    split_walls_and_columns: bool = False
    include_steel_elements: bool = True
    export_2d_elements: bool = False
    export_linked_files: bool = False
    export_rooms: bool = True
    export_schedules: bool = True

    def to_config_string(self) -> str:
        """Convert to CLI config string."""
        parts = [
            f"ExportBaseQuantities={str(self.export_base_quantities).lower()}",
            f"SitePlacement={self.site_placement}",
            f"SplitWallsAndColumns={str(self.split_walls_and_columns).lower()}",
            f"IncludeSteelElements={str(self.include_steel_elements).lower()}",
            f"Export2DElements={str(self.export_2d_elements).lower()}",
            f"ExportLinkedFiles={str(self.export_linked_files).lower()}",
            f"ExportRooms={str(self.export_rooms).lower()}"
        ]
        return "; ".join(parts)


class RevitToIFCConverter:
    """Convert Revit files to IFC format."""

    def __init__(self, converter_path: str = "RVT2IFCconverter.exe"):
        self.converter = Path(converter_path)
        if not self.converter.exists():
            raise FileNotFoundError(f"Converter not found: {converter_path}")

    def convert(self, rvt_file: str,
                output_path: Optional[str] = None,
                preset: ExportPreset = ExportPreset.STANDARD,
                config: Optional[IFCExportConfig] = None) -> Path:
        """Convert Revit file to IFC."""

        rvt_path = Path(rvt_file)
        if not rvt_path.exists():
            raise FileNotFoundError(f"Revit file not found: {rvt_file}")

        # Build command
        cmd = [str(self.converter), str(rvt_path)]

        # Add output path if specified
        if output_path:
            cmd.append(output_path)

        # Add preset
        cmd.append(f"preset={preset.value}")

        # Add custom config if provided
        if config:
            cmd.append(f'config="{config.to_config_string()}"')

        # Execute
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Conversion failed: {result.stderr}")

        # Return output path
        if output_path:
            return Path(output_path)
        return rvt_path.with_suffix('.ifc')

    def batch_convert(self, folder: str,
                      output_folder: Optional[str] = None,
                      preset: ExportPreset = ExportPreset.STANDARD,
                      config: Optional[IFCExportConfig] = None) -> List[Dict[str, Any]]:
        """Convert all Revit files in folder."""

        folder_path = Path(folder)
        results = []

        for rvt_file in folder_path.glob("**/*.rvt"):
            try:
                # Determine output path
                if output_folder:
                    out_dir = Path(output_folder)
                    out_dir.mkdir(parents=True, exist_ok=True)
                    output_path = str(out_dir / rvt_file.with_suffix('.ifc').name)
                else:
                    output_path = None

                ifc_path = self.convert(str(rvt_file), output_path, preset, config)
                results.append({
                    'input': str(rvt_file),
                    'output': str(ifc_path),
                    'status': 'success'
                })
                print(f"✓ Converted: {rvt_file.name}")

            except Exception as e:
                results.append({
                    'input': str(rvt_file),
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"✗ Failed: {rvt_file.name} - {e}")

        return results

    def validate_output(self, ifc_file: str) -> Dict[str, Any]:
        """Basic validation of generated IFC."""

        ifc_path = Path(ifc_file)
        if not ifc_path.exists():
            return {'valid': False, 'error': 'File not found'}

        # Basic file checks
        file_size = ifc_path.stat().st_size

        if file_size < 1000:
            return {'valid': False, 'error': 'File too small'}

        # Read header
        with open(ifc_file, 'r', errors='ignore') as f:
            header = f.read(1000)

        # Check IFC format
        if 'ISO-10303-21' not in header:
            return {'valid': False, 'error': 'Not a valid IFC file'}

        # Detect version
        version = 'Unknown'
        if 'IFC4X3' in header:
            version = 'IFC4.3'
        elif 'IFC4' in header:
            version = 'IFC4'
        elif 'IFC2X3' in header:
            version = 'IFC2x3'

        return {
            'valid': True,
            'file_size': file_size,
            'ifc_version': version
        }


class IFCQualityChecker:
    """Check quality of IFC exports."""

    def __init__(self, converter: RevitToIFCConverter):
        self.converter = converter

    def compare_presets(self, rvt_file: str) -> Dict[str, Any]:
        """Compare different export presets."""

        results = {}

        for preset in [ExportPreset.STANDARD, ExportPreset.EXTENDED]:
            try:
                output = Path(rvt_file).with_suffix(f'.{preset.value}.ifc')
                self.converter.convert(rvt_file, str(output), preset)

                validation = self.converter.validate_output(str(output))
                results[preset.value] = {
                    'file_size': validation.get('file_size', 0),
                    'valid': validation.get('valid', False)
                }
            except Exception as e:
                results[preset.value] = {'error': str(e)}

        return results


# Convenience functions
def convert_revit_to_ifc(rvt_file: str,
                         converter_path: str = "RVT2IFCconverter.exe") -> str:
    """Quick conversion of Revit to IFC."""
    converter = RevitToIFCConverter(converter_path)
    output = converter.convert(rvt_file)
    return str(output)


def batch_convert_to_ifc(folder: str,
                         converter_path: str = "RVT2IFCconverter.exe") -> List[str]:
    """Batch convert all Revit files to IFC."""
    converter = RevitToIFCConverter(converter_path)
    results = converter.batch_convert(folder)
    return [r['output'] for r in results if r['status'] == 'success']
```

## 快速入门
```python
# Initialize converter
converter = RevitToIFCConverter("C:/DDC/RVT2IFCconverter.exe")

# Basic conversion
ifc = converter.convert("building.rvt")
print(f"Created: {ifc}")

# With custom config
config = IFCExportConfig(
    ifc_version=IFCVersion.IFC4,
    export_base_quantities=True,
    export_rooms=True
)
ifc = converter.convert("building.rvt", preset=ExportPreset.CUSTOM, config=config)
```

## 常见应用场景

### 1. 批量处理
```python
converter = RevitToIFCConverter()
results = converter.batch_convert(
    folder="C:/Projects",
    output_folder="C:/IFC_Export",
    preset=ExportPreset.EXTENDED
)
print(f"Converted {len([r for r in results if r['status'] == 'success'])} files")
```

### 2. 数据质量检查
```python
validation = converter.validate_output("model.ifc")
print(f"Valid: {validation['valid']}, Version: {validation['ifc_version']}")
```

### 预设比较
```python
checker = IFCQualityChecker(converter)
comparison = checker.compare_presets("building.rvt")
print(comparison)
```

## 资源
- **GitHub**: [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- **buildingSMART IFC**: https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/