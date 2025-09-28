# 🎨 DataVisualization Workspace

[English](#english-version) | [中文](#中文版本)

---

## English Version

A collection of astronomical and space data visualization projects that transform scientific datasets into artistic and interactive visualizations.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## 📂 Projects Overview

### 🌌 Galaxy Morphology Art
**Location**: `GalaxyMorphologyArt/galaxy_morphology_art.py`

Creates artistic visualizations from SDSS (Sloan Digital Sky Survey) galaxy data, focusing on morphological classification and redshift distributions.

**Features**:
- Real SDSS DR16 data integration with synthetic fallback
- 4 artistic visualization styles: Sky Map, Redshift Field, Bubble Art, Concentration Spiral
- 3D interactive galaxy distribution viewer
- Morphological classification (spiral vs elliptical galaxies)

**Quick Start**:
```bash
cd GalaxyMorphologyArt
python galaxy_morphology_art.py
```

### 🛰️ Satellite Constellation Trails
**Location**: `SatelliteConstellationTrails/satellite_visualizer.py`

Real-time satellite tracking and orbital pattern visualization tool with artistic trail effects.

**Features**:
- Live satellite data from CelesTrak (ISS, Starlink, GPS, Weather satellites)
- Real-time animated tracking with orbital trails
- 1-hour orbital art pattern generation
- Static constellation maps
- 5 satellite categories with distinct colors

**Quick Start**:
```bash
cd SatelliteConstellationTrails  
python satellite_visualizer.py
```

### ⭐ Star Atlas
**Location**: `StarAtlas/StarAtlas.ipynb`

Interactive Jupyter notebook for creating beautiful star maps from the HYG-Athyg star catalog.

**Features**:
- 117,000+ star database visualization
- Magnitude-based sizing and color index mapping
- Interactive Bokeh plots with zoom/pan
- Customizable filtering and edge detection
- Static and interactive visualization modes

**Quick Start**:
```bash
cd StarAtlas
jupyter notebook StarAtlas.ipynb
```

## 🚀 Setup Instructions

### Environment Setup (Windows PowerShell)

1) Create and activate virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:
```powershell
pip install -U pip
pip install -r requirements.txt
```

3) Open in VS Code:
```powershell
code .
```

## 📊 Output Examples

Each project generates high-quality visualizations:
- **Galaxy Art**: `galaxy_art_output/` - Morphological art and 3D distributions
- **Satellite Trails**: `orbital_art.png`, `constellation_map.png` - Real-time satellite data
- **Star Atlas**: Interactive plots and static star maps

## 🛠️ Technical Stack

- **Data Processing**: NumPy, Pandas, SciPy
- **Visualization**: Matplotlib, Bokeh, Seaborn
- **Astronomical Data**: Skyfield, SDSS, CelesTrak, HYG-Athyg
- **Interactive**: Jupyter Notebooks, Real-time animations

## 📁 Project Structure

```
DataVisualization/
├── README.md
├── requirements.txt
├── GalaxyMorphologyArt/
│   ├── galaxy_morphology_art.py
│   ├── README.md
│   └── SDSS_Data_Guide.md
├── SatelliteConstellationTrails/
│   ├── satellite_visualizer.py
│   ├── README.md
│   └── requirements.txt
└── StarAtlas/
    ├── StarAtlas.ipynb
    └── hyglike_from_athyg_v32.csv.gz
```

---

## 中文版本

# 🎨 数据可视化工作区

天文和太空数据可视化项目集合，将科学数据集转化为艺术性和交互式可视化。

## 📂 项目概览

### 🌌 星系形态艺术
**位置**: `GalaxyMorphologyArt/galaxy_morphology_art.py`

基于SDSS（斯隆数字巡天）星系数据创建艺术化可视化，专注于形态学分类和红移分布。

**功能特色**:
- 真实SDSS DR16数据接入，合成数据备份
- 4种艺术可视化风格：天空图、红移场、气泡图、浓度螺旋
- 3D交互式星系分布查看器
- 形态学分类（螺旋星系 vs 椭圆星系）

**快速开始**:
```bash
cd GalaxyMorphologyArt
python galaxy_morphology_art.py
```

### 🛰️ 卫星轨道轨迹
**位置**: `SatelliteConstellationTrails/satellite_visualizer.py`

实时卫星追踪和轨道模式可视化工具，具有艺术轨迹效果。

**功能特色**:
- 来自CelesTrak的实时卫星数据（国际空间站、星链、GPS、气象卫星）
- 带轨道轨迹的实时动画追踪
- 1小时轨道艺术图案生成
- 静态星座地图
- 5个卫星类别，不同颜色区分

**快速开始**:
```bash
cd SatelliteConstellationTrails  
python satellite_visualizer.py
```

### ⭐ 星图集
**位置**: `StarAtlas/StarAtlas.ipynb`

用于从HYG-Athyg恒星目录创建美丽星图的交互式Jupyter笔记本。

**功能特色**:
- 117,000+恒星数据库可视化
- 基于星等的尺寸和色指数映射
- 具有缩放/平移的交互式Bokeh图表
- 可定制过滤和边缘检测
- 静态和交互式可视化模式

**快速开始**:
```bash
cd StarAtlas
jupyter notebook StarAtlas.ipynb
```

## 🚀 安装说明

### 环境设置（Windows PowerShell）

1) 创建并激活虚拟环境：
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) 安装依赖：
```powershell
pip install -U pip
pip install -r requirements.txt
```

3) 在VS Code中打开：
```powershell
code .
```

## 📊 输出示例

每个项目都生成高质量可视化：
- **星系艺术**: `galaxy_art_output/` - 形态学艺术和3D分布
- **卫星轨迹**: `orbital_art.png`, `constellation_map.png` - 实时卫星数据
- **星图集**: 交互式图表和静态星图

## 🛠️ 技术栈

- **数据处理**: NumPy, Pandas, SciPy
- **可视化**: Matplotlib, Bokeh, Seaborn
- **天文数据**: Skyfield, SDSS, CelesTrak, HYG-Athyg
- **交互式**: Jupyter Notebooks, 实时动画

## 📁 项目结构

```
DataVisualization/
├── README.md
├── requirements.txt
├── GalaxyMorphologyArt/
│   ├── galaxy_morphology_art.py
│   ├── README.md
│   └── SDSS_Data_Guide.md
├── SatelliteConstellationTrails/
│   ├── satellite_visualizer.py
│   ├── README.md
│   └── requirements.txt
└── StarAtlas/
    ├── StarAtlas.ipynb
    └── hyglike_from_athyg_v32.csv.gz
```
