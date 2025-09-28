# 🌌 Galaxy Morphology Art Visualizer

[English](#english-version) | [中文](#中文版本)

---

## English Version

A scientific art visualization tool that creates artistic representations from SDSS (Sloan Digital Sky Survey) galaxy data, focusing on morphological characteristics and redshift distributions.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Real SDSS Data Integration**: Fetches live galaxy data from SDSS DR16 database
- **Morphological Classification**: Distinguishes between spiral and elliptical galaxies  
- **Artistic Visualizations**: Creates 4 different art styles based on galaxy properties
- **3D Distribution View**: Interactive 3D representation of galaxy positions
- **Redshift Color Mapping**: Consistent color coding based on redshift values
- **Fallback Synthetic Data**: Generates realistic synthetic data when SDSS is unavailable

## 🎨 Visualization Types

1. **Morphological Sky Map**: Galaxy shapes based on spiral/elliptical classification
2. **Redshift Gradient Field**: Interpolated redshift distribution with cosmic web
3. **Size-Redshift Bubble Art**: Bubble chart showing galaxy size vs redshift correlation
4. **Concentration Spiral**: Artistic spiral arrangement based on galaxy concentration indices

## 📋 Requirements

```bash
pip install numpy matplotlib pandas requests scipy seaborn
```

## 🚀 Quick Start

```bash
python galaxy_morphology_art.py
```

The program will:
1. Attempt to fetch real galaxy data from SDSS DR16
2. Create artistic visualizations
3. Save outputs to `galaxy_art_output/` directory
4. Display interactive plots

## ⚙️ Configuration

### Data Parameters
- **Galaxy limit**: Default 50 galaxies (adjustable in `main()`)
- **Magnitude range**: 15-18 (bright galaxies)
- **Sky region**: Declination -1.2° to -0.8°

### Output Files
- `galaxy_morphology_art.png`: Main 4-panel artistic visualization
- `galaxy_3d_distribution.png`: 3D galaxy distribution plot  
- `sdss_galaxy_data_*.csv`: Raw SDSS data (when available)
- `galaxy_data_summary.txt`: Data statistics

### Color Scheme
- **Redshift mapping**: Plasma colormap (warm colors, 0.3-1.0 range)
- **Morphology colors**: Redshift-based with shape differentiation
- **Background**: Dark space theme (#0a0a0a, #000814)

## 🔧 Technical Details

### SDSS Query
```sql
SELECT TOP {limit}
    objid, ra, dec, u, g, r, i, z,
    petroR50_r, petroR90_r, deVAB_r, expAB_r, petroMag_r
FROM PhotoObj 
WHERE type = 3 AND petroMag_r BETWEEN 15 AND 18
```

### Galaxy Classification
- **Spiral**: `fracDeV_r < 0.5` (disk-dominated)
- **Elliptical**: `fracDeV_r >= 0.5` (bulge-dominated)
- **Concentration Index**: `petroR90_r / petroR50_r`

## 🛠️ Troubleshooting

**SDSS Connection Issues**: Program automatically switches to synthetic data if SDSS is unreachable.

**Empty Visualizations**: Check network connection or increase galaxy limit in `main()`.

**Performance**: For large datasets (>200 galaxies), increase timeout or reduce query limit.

---

## 中文版本

# 🌌 星系形态艺术可视化工具

基于SDSS（斯隆数字巡天）星系数据的科学艺术可视化工具，专注于星系形态特征和红移分布的艺术化展示。

## ✨ 功能特色

- **真实SDSS数据接入**：从SDSS DR16数据库获取实时星系数据
- **形态学分类**：区分螺旋星系和椭圆星系
- **艺术化可视化**：基于星系属性创建4种不同艺术风格
- **3D分布视图**：星系位置的交互式三维表示
- **红移颜色映射**：基于红移值的一致性颜色编码
- **合成数据备份**：SDSS不可用时生成真实的合成数据

## 🎨 可视化类型

1. **形态学天空图**：基于螺旋/椭圆分类的星系形状
2. **红移梯度场**：插值红移分布与宇宙网络
3. **尺寸-红移气泡图**：显示星系大小与红移相关性的气泡图
4. **浓度指数螺旋**：基于星系浓度指数的艺术螺旋排列

## 📋 环境要求

```bash
pip install numpy matplotlib pandas requests scipy seaborn
```

## 🚀 快速开始

```bash
python galaxy_morphology_art.py
```

程序将会：
1. 尝试从SDSS DR16获取真实星系数据
2. 创建艺术化可视化
3. 将输出保存到 `galaxy_art_output/` 目录
4. 显示交互式图表

## ⚙️ 配置参数

### 数据参数
- **星系数量**：默认50个星系（可在`main()`中调整）
- **星等范围**：15-18（明亮星系）
- **天区范围**：赤纬-1.2°到-0.8°

### 输出文件
- `galaxy_morphology_art.png`：主要4面板艺术可视化
- `galaxy_3d_distribution.png`：3D星系分布图
- `sdss_galaxy_data_*.csv`：原始SDSS数据（如果可用）
- `galaxy_data_summary.txt`：数据统计信息

### 颜色方案
- **红移映射**：Plasma色彩图（暖色调，0.3-1.0范围）
- **形态学颜色**：基于红移的形状区分
- **背景**：深空主题（#0a0a0a, #000814）

## 🔧 技术细节

### SDSS查询
```sql
SELECT TOP {limit}
    objid, ra, dec, u, g, r, i, z,
    petroR50_r, petroR90_r, deVAB_r, expAB_r, petroMag_r
FROM PhotoObj 
WHERE type = 3 AND petroMag_r BETWEEN 15 AND 18
```

### 星系分类
- **螺旋星系**：`fracDeV_r < 0.5`（盘主导）
- **椭圆星系**：`fracDeV_r >= 0.5`（核球主导）
- **浓度指数**：`petroR90_r / petroR50_r`

## 🛠️ 故障排除

**SDSS连接问题**：程序在SDSS无法访问时自动切换到合成数据。

**可视化为空**：检查网络连接或在`main()`中增加星系数量限制。

**性能问题**：对于大型数据集（>200个星系），增加超时时间或减少查询限制。