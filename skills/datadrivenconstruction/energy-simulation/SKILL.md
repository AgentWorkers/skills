---
slug: "energy-simulation"
display_name: "Energy Simulation"
description: "为建筑项目提供能源模拟与分析服务。包括计算供暖/制冷负荷、评估建筑围护结构的性能、优化暖通空调（HVAC）系统的规模设计，并确保项目符合相关能源法规的要求。"
---

# 能源模拟

## 概述

该技能用于实现建筑能源的模拟与分析，包括计算热负荷、评估建筑围护结构的性能，并优化系统以提高能源效率和符合相关规范要求。

**功能包括：**
- 供暖/制冷负荷计算
- 围护结构热分析
- HVAC（暖通空调）系统设计
- 能源规范合规性检查
- 可再生能源集成
- 生命周期成本分析

## 快速入门

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import numpy as np

class WallType(Enum):
    CONCRETE = "concrete"
    BRICK = "brick"
    WOOD_FRAME = "wood_frame"
    STEEL_FRAME = "steel_frame"
    CURTAIN_WALL = "curtain_wall"

@dataclass
class BuildingEnvelope:
    wall_area_m2: float
    wall_u_value: float  # W/m²K
    roof_area_m2: float
    roof_u_value: float
    floor_area_m2: float
    floor_u_value: float
    window_area_m2: float
    window_u_value: float
    window_shgc: float  # Solar Heat Gain Coefficient

@dataclass
class ClimateData:
    location: str
    heating_degree_days: float  # HDD base 18°C
    cooling_degree_days: float  # CDD base 18°C
    design_temp_winter: float
    design_temp_summer: float

def calculate_heat_loss(envelope: BuildingEnvelope, climate: ClimateData,
                       indoor_temp: float = 21) -> float:
    """Calculate design heat loss (W)"""
    delta_t = indoor_temp - climate.design_temp_winter

    # Transmission losses
    wall_loss = envelope.wall_area_m2 * envelope.wall_u_value * delta_t
    roof_loss = envelope.roof_area_m2 * envelope.roof_u_value * delta_t
    floor_loss = envelope.floor_area_m2 * envelope.floor_u_value * delta_t * 0.5  # Ground factor
    window_loss = envelope.window_area_m2 * envelope.window_u_value * delta_t

    total_loss = wall_loss + roof_loss + floor_loss + window_loss

    # Add infiltration estimate (simplified)
    volume = envelope.floor_area_m2 * 3  # Assume 3m height
    infiltration = volume * 0.5 * 0.33 * delta_t  # 0.5 ACH, 0.33 Wh/m³K

    return total_loss + infiltration

# Example
envelope = BuildingEnvelope(
    wall_area_m2=500, wall_u_value=0.35,
    roof_area_m2=200, roof_u_value=0.25,
    floor_area_m2=200, floor_u_value=0.30,
    window_area_m2=100, window_u_value=1.4, window_shgc=0.4
)

climate = ClimateData(
    location="Moscow",
    heating_degree_days=5000,
    cooling_degree_days=300,
    design_temp_winter=-25,
    design_temp_summer=30
)

heat_loss = calculate_heat_loss(envelope, climate)
print(f"Design heat loss: {heat_loss/1000:.1f} kW")
```

## 全面能源分析

### 建筑热模型

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import numpy as np
from datetime import datetime

@dataclass
class MaterialLayer:
    name: str
    thickness_m: float
    conductivity: float  # W/mK
    density: float  # kg/m³
    specific_heat: float  # J/kgK

    @property
    def resistance(self) -> float:
        """Thermal resistance R (m²K/W)"""
        return self.thickness_m / self.conductivity if self.conductivity > 0 else 0

@dataclass
class WallAssembly:
    name: str
    layers: List[MaterialLayer]
    inside_surface_resistance: float = 0.13  # m²K/W
    outside_surface_resistance: float = 0.04

    @property
    def total_resistance(self) -> float:
        return (self.inside_surface_resistance +
                sum(layer.resistance for layer in self.layers) +
                self.outside_surface_resistance)

    @property
    def u_value(self) -> float:
        return 1 / self.total_resistance if self.total_resistance > 0 else 0

@dataclass
class Window:
    name: str
    u_value: float
    shgc: float
    visible_transmittance: float = 0.6
    frame_fraction: float = 0.2

@dataclass
class Zone:
    zone_id: str
    name: str
    floor_area_m2: float
    volume_m3: float
    occupancy: int
    lighting_power_density: float  # W/m²
    equipment_power_density: float  # W/m²
    ventilation_rate: float  # L/s per person
    setpoint_heating: float = 21
    setpoint_cooling: float = 24

@dataclass
class BuildingGeometry:
    zones: List[Zone]
    walls: List[Dict]  # {zone, orientation, area, assembly}
    windows: List[Dict]  # {zone, orientation, area, window_type}
    roofs: List[Dict]  # {zone, area, assembly}
    floors: List[Dict]  # {zone, area, assembly, is_ground}

class ThermalCalculator:
    """Calculate building thermal loads"""

    # Standard climate data (simplified)
    CLIMATE_DB = {
        'moscow': {
            'hdd': 5000, 'cdd': 300,
            'design_winter': -25, 'design_summer': 30,
            'latitude': 55.75
        },
        'new_york': {
            'hdd': 2500, 'cdd': 800,
            'design_winter': -12, 'design_summer': 33,
            'latitude': 40.71
        },
        'dubai': {
            'hdd': 50, 'cdd': 3000,
            'design_winter': 15, 'design_summer': 45,
            'latitude': 25.20
        }
    }

    def __init__(self, building: BuildingGeometry, location: str):
        self.building = building
        self.location = location.lower()
        self.climate = self.CLIMATE_DB.get(self.location, self.CLIMATE_DB['moscow'])

    def calculate_design_heating_load(self) -> Dict:
        """Calculate design heating load for each zone"""
        delta_t = 21 - self.climate['design_winter']
        results = {}

        for zone in self.building.zones:
            # Transmission losses
            wall_loss = 0
            window_loss = 0
            roof_loss = 0
            floor_loss = 0

            for wall in self.building.walls:
                if wall['zone'] == zone.zone_id:
                    u_value = wall['assembly'].u_value
                    wall_loss += wall['area'] * u_value * delta_t

            for window in self.building.windows:
                if window['zone'] == zone.zone_id:
                    window_loss += window['area'] * window['window_type'].u_value * delta_t

            for roof in self.building.roofs:
                if roof['zone'] == zone.zone_id:
                    u_value = roof['assembly'].u_value
                    roof_loss += roof['area'] * u_value * delta_t

            for floor in self.building.floors:
                if floor['zone'] == zone.zone_id:
                    u_value = floor['assembly'].u_value
                    factor = 0.5 if floor.get('is_ground', False) else 1.0
                    floor_loss += floor['area'] * u_value * delta_t * factor

            # Infiltration
            infiltration_loss = zone.volume_m3 * 0.5 * 0.33 * delta_t

            # Ventilation (if mechanical)
            ventilation_loss = zone.occupancy * zone.ventilation_rate * 1.2 * delta_t

            total = wall_loss + window_loss + roof_loss + floor_loss + infiltration_loss + ventilation_loss

            results[zone.zone_id] = {
                'zone_name': zone.name,
                'wall_loss_w': wall_loss,
                'window_loss_w': window_loss,
                'roof_loss_w': roof_loss,
                'floor_loss_w': floor_loss,
                'infiltration_w': infiltration_loss,
                'ventilation_w': ventilation_loss,
                'total_w': total,
                'total_kw': total / 1000,
                'w_per_m2': total / zone.floor_area_m2
            }

        return results

    def calculate_design_cooling_load(self) -> Dict:
        """Calculate design cooling load for each zone"""
        delta_t = self.climate['design_summer'] - 24
        results = {}

        for zone in self.building.zones:
            # Transmission gains
            transmission_gain = 0
            for wall in self.building.walls:
                if wall['zone'] == zone.zone_id:
                    u_value = wall['assembly'].u_value
                    # Apply sol-air temperature correction for orientation
                    sol_air_delta = delta_t + self._get_sol_air_correction(wall['orientation'])
                    transmission_gain += wall['area'] * u_value * sol_air_delta

            # Window solar gains
            solar_gain = 0
            for window in self.building.windows:
                if window['zone'] == zone.zone_id:
                    shgc = window['window_type'].shgc
                    irradiance = self._get_solar_irradiance(window['orientation'])
                    solar_gain += window['area'] * shgc * irradiance

            # Window conduction
            window_conduction = 0
            for window in self.building.windows:
                if window['zone'] == zone.zone_id:
                    window_conduction += window['area'] * window['window_type'].u_value * delta_t

            # Internal gains
            lighting_gain = zone.floor_area_m2 * zone.lighting_power_density
            equipment_gain = zone.floor_area_m2 * zone.equipment_power_density
            people_gain = zone.occupancy * 75  # W per person sensible

            # Ventilation
            ventilation_gain = zone.occupancy * zone.ventilation_rate * 1.2 * delta_t

            total = (transmission_gain + solar_gain + window_conduction +
                    lighting_gain + equipment_gain + people_gain + ventilation_gain)

            results[zone.zone_id] = {
                'zone_name': zone.name,
                'transmission_gain_w': transmission_gain,
                'solar_gain_w': solar_gain,
                'window_conduction_w': window_conduction,
                'lighting_gain_w': lighting_gain,
                'equipment_gain_w': equipment_gain,
                'people_gain_w': people_gain,
                'ventilation_gain_w': ventilation_gain,
                'total_w': total,
                'total_kw': total / 1000,
                'w_per_m2': total / zone.floor_area_m2
            }

        return results

    def _get_sol_air_correction(self, orientation: str) -> float:
        """Get sol-air temperature correction by orientation"""
        corrections = {
            'north': 0, 'south': 8, 'east': 4, 'west': 6,
            'northeast': 2, 'northwest': 3, 'southeast': 6, 'southwest': 7
        }
        return corrections.get(orientation.lower(), 3)

    def _get_solar_irradiance(self, orientation: str) -> float:
        """Get design solar irradiance W/m² by orientation"""
        # Simplified peak values
        irradiance = {
            'north': 150, 'south': 450, 'east': 350, 'west': 350,
            'northeast': 200, 'northwest': 200, 'southeast': 400, 'southwest': 400
        }
        return irradiance.get(orientation.lower(), 300)
```

### HVAC系统设计

```python
class HVACSizer:
    """Size HVAC systems based on loads"""

    def __init__(self, calculator: ThermalCalculator):
        self.calculator = calculator

    def size_heating_system(self, safety_factor: float = 1.15) -> Dict:
        """Size heating system"""
        heating_loads = self.calculator.calculate_design_heating_load()

        total_load = sum(z['total_kw'] for z in heating_loads.values())
        sized_capacity = total_load * safety_factor

        # Recommend system type
        if sized_capacity < 15:
            system_type = "Split system heat pump"
        elif sized_capacity < 50:
            system_type = "Packaged rooftop unit"
        elif sized_capacity < 200:
            system_type = "Central boiler with radiators"
        else:
            system_type = "Central plant with multiple boilers"

        return {
            'total_load_kw': total_load,
            'sized_capacity_kw': sized_capacity,
            'safety_factor': safety_factor,
            'recommended_system': system_type,
            'zone_loads': heating_loads
        }

    def size_cooling_system(self, safety_factor: float = 1.1) -> Dict:
        """Size cooling system"""
        cooling_loads = self.calculator.calculate_design_cooling_load()

        total_load = sum(z['total_kw'] for z in cooling_loads.values())
        sized_capacity = total_load * safety_factor

        # Convert to tons
        capacity_tons = sized_capacity / 3.517

        # Recommend system type
        if capacity_tons < 5:
            system_type = "Split system DX"
        elif capacity_tons < 20:
            system_type = "VRF system"
        elif capacity_tons < 100:
            system_type = "Chilled water with AHUs"
        else:
            system_type = "Central chiller plant"

        return {
            'total_load_kw': total_load,
            'total_load_tons': capacity_tons,
            'sized_capacity_kw': sized_capacity,
            'sized_capacity_tons': capacity_tons * safety_factor,
            'safety_factor': safety_factor,
            'recommended_system': system_type,
            'zone_loads': cooling_loads
        }

    def estimate_annual_energy(self) -> Dict:
        """Estimate annual energy consumption"""
        climate = self.calculator.climate

        heating_loads = self.calculator.calculate_design_heating_load()
        cooling_loads = self.calculator.calculate_design_cooling_load()

        total_heating_load = sum(z['total_kw'] for z in heating_loads.values())
        total_cooling_load = sum(z['total_kw'] for z in cooling_loads.values())

        # Simplified degree-day calculation
        # Heating energy = load * HDD * 24 / delta_t_design
        delta_t_heating = 21 - climate['design_winter']
        heating_kwh = total_heating_load * climate['hdd'] * 24 / delta_t_heating / 1000

        delta_t_cooling = climate['design_summer'] - 24
        cooling_kwh = total_cooling_load * climate['cdd'] * 24 / delta_t_cooling / 1000 if delta_t_cooling > 0 else 0

        # Apply efficiency factors
        heating_fuel_efficiency = 0.9  # Gas boiler
        cooling_cop = 3.5  # Chiller COP

        heating_consumption = heating_kwh / heating_fuel_efficiency
        cooling_consumption = cooling_kwh / cooling_cop

        return {
            'heating_load_kw': total_heating_load,
            'cooling_load_kw': total_cooling_load,
            'annual_heating_kwh': heating_kwh,
            'annual_cooling_kwh': cooling_kwh,
            'heating_fuel_kwh': heating_consumption,
            'cooling_electricity_kwh': cooling_consumption,
            'total_hvac_energy_kwh': heating_consumption + cooling_consumption
        }
```

### 能源规范合规性检查

```python
@dataclass
class EnergyCodeRequirements:
    code_name: str
    climate_zone: str
    wall_u_max: float
    roof_u_max: float
    floor_u_max: float
    window_u_max: float
    window_shgc_max: float
    lighting_lpd_max: float  # W/m²

class ComplianceChecker:
    """Check energy code compliance"""

    CODES = {
        'ASHRAE_90.1_2019_4A': EnergyCodeRequirements(
            code_name="ASHRAE 90.1-2019",
            climate_zone="4A",
            wall_u_max=0.45,
            roof_u_max=0.27,
            floor_u_max=0.32,
            window_u_max=2.0,
            window_shgc_max=0.40,
            lighting_lpd_max=9.0
        ),
        'IECC_2021_5A': EnergyCodeRequirements(
            code_name="IECC 2021",
            climate_zone="5A",
            wall_u_max=0.35,
            roof_u_max=0.20,
            floor_u_max=0.30,
            window_u_max=1.7,
            window_shgc_max=0.40,
            lighting_lpd_max=8.5
        )
    }

    def __init__(self, code_key: str):
        self.requirements = self.CODES.get(code_key)
        if not self.requirements:
            raise ValueError(f"Unknown code: {code_key}")

    def check_envelope(self, building: BuildingGeometry) -> Dict:
        """Check envelope compliance"""
        results = {
            'code': self.requirements.code_name,
            'climate_zone': self.requirements.climate_zone,
            'compliant': True,
            'issues': []
        }

        # Check walls
        for wall in building.walls:
            u_value = wall['assembly'].u_value
            if u_value > self.requirements.wall_u_max:
                results['compliant'] = False
                results['issues'].append({
                    'element': f"Wall {wall['zone']} {wall['orientation']}",
                    'actual': u_value,
                    'required': self.requirements.wall_u_max,
                    'issue': 'Exceeds maximum U-value'
                })

        # Check windows
        for window in building.windows:
            u_value = window['window_type'].u_value
            shgc = window['window_type'].shgc

            if u_value > self.requirements.window_u_max:
                results['compliant'] = False
                results['issues'].append({
                    'element': f"Window {window['zone']} {window['orientation']}",
                    'actual': u_value,
                    'required': self.requirements.window_u_max,
                    'issue': 'Exceeds maximum U-value'
                })

            if shgc > self.requirements.window_shgc_max:
                results['compliant'] = False
                results['issues'].append({
                    'element': f"Window {window['zone']} {window['orientation']}",
                    'actual': shgc,
                    'required': self.requirements.window_shgc_max,
                    'issue': 'Exceeds maximum SHGC'
                })

        # Check roof
        for roof in building.roofs:
            u_value = roof['assembly'].u_value
            if u_value > self.requirements.roof_u_max:
                results['compliant'] = False
                results['issues'].append({
                    'element': f"Roof {roof['zone']}",
                    'actual': u_value,
                    'required': self.requirements.roof_u_max,
                    'issue': 'Exceeds maximum U-value'
                })

        return results

    def check_lighting(self, zones: List[Zone]) -> Dict:
        """Check lighting power density compliance"""
        results = {
            'compliant': True,
            'issues': []
        }

        for zone in zones:
            if zone.lighting_power_density > self.requirements.lighting_lpd_max:
                results['compliant'] = False
                results['issues'].append({
                    'zone': zone.name,
                    'actual_lpd': zone.lighting_power_density,
                    'required_max': self.requirements.lighting_lpd_max
                })

        return results
```

## 参考信息

| 组件 | 最佳U值（W/m²K） | 规范允许的最大值（W/m²K） |
|-----------|--------------|--------------|
| 墙体 | < 0.25 | 0.35–0.45 |
| 屋顶 | < 0.15 | 0.20–0.27 |
| 地板 | < 0.20 | 0.25–0.32 |
| 窗户 | < 1.2 | 1.7–2.0 |

## 资源参考

- **ASHRAE 90.1**: 建筑能源标准
- **IECC**: 国际节能规范
- **EnergyPlus**: 美国能源部（DOE）的建筑模拟工具
- **DDC网站**: https://datadrivenconstruction.io

## 下一步操作

- 如需进行碳排放分析，请参考`co2-estimation`模块。
- 如需进行能源成本建模，请参考`cost-prediction`模块。
- 如需进行模型集成，请参考`bim-validation-pipeline`模块。