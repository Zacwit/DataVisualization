# 🛰️ Satellite Constellation Visualizer

[English](#english-version) | [中文](#中文版本)

---

## English Version

A real-time satellite constellation visualization tool that creates artistic orbital patterns and tracks satellite positions in real time.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## ✨ Features

- 🔴 **Real-time Satellite Tracking**: Dynamic display of satellite positions and orbital trails
- 🎨 **Orbital Art Patterns**: Generate artistic satellite orbital patterns over 1-hour periods
- 🗺️ **Constellation Map**: Static position map showing all current satellite locations
- 🌈 **Multi-category Data**: Support for 5 different types of satellite data sources
- ⚡ **Performance Optimized**: Intelligent data sampling and limits ensure smooth operation

## 🛰️ Supported Satellite Categories

| Category | Color | Description | Data Source |
|----------|-------|-------------|-------------|
| ISS & Crew Vehicles | 🔴 Red | International Space Station and crewed vehicles | CelesTrak |
| Starlink | 🟢 Green | SpaceX Starlink satellites | CelesTrak |
| GPS Constellation | 🔵 Blue | GPS navigation satellites | CelesTrak |
| Bright Satellites | 🟡 Yellow | Bright visible satellites | CelesTrak |
| Weather Satellites | 🟣 Purple | Weather monitoring satellites | CelesTrak |

## 📋 System Requirements

- Python 3.7+
- Internet connection (for satellite orbital data retrieval)
- Graphics environment supporting matplotlib

## 🔧 Installation

```bash
pip install numpy matplotlib requests skyfield
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

### Main Dependencies

- **numpy**: Numerical computations
- **matplotlib**: Data visualization and animation
- **requests**: HTTP requests for satellite data
- **skyfield**: Celestial mechanics calculations and satellite orbit prediction

## 🚀 Quick Start

### Basic Usage

```bash
python satellite_visualizer.py
```

### Interactive Menu

After running the program, you'll see the following options:

```
Choose visualization mode:
1. Real-time satellite tracking (animated)    # Real-time satellite tracking
2. Create orbital art pattern (1-hour paths)  # Create orbital art patterns
3. Current constellation map (static)         # Current constellation map
4. Exit                                       # Exit
```

### Programmatic Usage

```python
from satellite_visualizer import SatelliteVisualizer

# Create visualizer
viz = SatelliteVisualizer(trail_length=30, update_interval=2000)

# Generate orbital art
viz.create_orbital_art()

# Create constellation map
viz.create_constellation_map()

# Start real-time tracking
viz.start_real_time_visualization()
```

## 📊 Data Sources and Limitations

### Data Acquisition
- All satellite data from [CelesTrak](https://celestrak.com/)
- Uses Two-Line Element (TLE) format orbital data
- Real-time data fetched from internet ensuring accurate orbital information

### Performance Optimization
- Each category limited to 10-50 satellites
- Orbital art mode selects 4 representative satellites per category
- Total satellite count controlled under 200
- 1-hour time window with 1-minute sampling intervals

## 🎨 Output Files

The program generates the following files in the current directory:

- `orbital_art.png`: 1-hour orbital art pattern (300 DPI)
- `constellation_map.png`: Current satellite position map (300 DPI)

## 🎯 Feature Details

### 1. Real-time Satellite Tracking
- **Function**: Animated display of real-time satellite positions and orbital trails
- **Features**:
  - Real-time satellite position updates
  - Orbital trail display (configurable length)
  - Timestamp and active satellite count
  - Interactive graphical interface

### 2. Orbital Art Patterns
- **Function**: Generate artistic satellite orbital patterns over 1-hour periods
- **Features**:
  - 4 representative satellites selected per category
  - 1-hour time range with 60 time points
  - Colored orbital trajectories with different colors per category
  - High-resolution PNG output

### 3. Constellation Map
- **Function**: Display current positions of all satellites
- **Features**:
  - Static scatter plot display
  - Includes all loaded satellites
  - Timestamp annotation
  - Categorized legend

## ⚙️ Configuration Options

### SatelliteVisualizer Parameters

```python
SatelliteVisualizer(
    trail_length=50,      # Orbital trail length (number of points)
    update_interval=1000  # Animation update interval (milliseconds)
)
```

### Custom Color Scheme

Modify the `category_colors` dictionary to customize colors:

```python
self.category_colors = {
    'ISS & Crew Vehicles': '#FF4444',  # Red
    'Starlink': '#44FF44',             # Green
    'GPS Constellation': '#4444FF',    # Blue
    'Bright Satellites': '#FFFF44',   # Yellow
    'Weather Satellites': '#FF44FF'   # Purple
}
```

## 🔍 Technical Details

### Coordinate System
- Uses Earth-Centered Cartesian coordinate system
- X-Y plane projection display
- Units: kilometers (km)

### Time Handling
- Uses UTC time
- Precise celestial mechanics calculations with Skyfield library
- Supports orbital prediction over arbitrary time ranges

### Data Processing Pipeline
1. Fetch TLE data from CelesTrak
2. Parse TLE format to create satellite objects
3. Calculate orbital positions using SGP4 model
4. Convert to Earth-centered coordinates
5. Visualization rendering

## 🐛 Troubleshooting

### Common Issues

**1. Network Connection Error**
```
Failed to load [Category]: HTTPSConnectionPool...
```
- Check network connection
- Verify firewall settings
- Try using a proxy

**2. No Satellite Data**
```
No satellites loaded. Please check your internet connection.
```
- Check network connection
- Verify CelesTrak website accessibility

**3. Graphics Display Issues**
- Ensure matplotlib backend is configured correctly
- SSH environments may require X11 forwarding
- Windows users ensure GUI environment is available

### Debug Mode

Uncomment the following line to enable verbose logging:
```python
# warnings.filterwarnings('ignore')  # Comment this line
```

## 📈 Performance Notes

### Resource Usage
- **Memory**: ~50-100MB (depending on satellite count)
- **CPU**: Moderate (continuous calculation in real-time mode)
- **Network**: ~1-2MB data download during initialization

### Optimization Tips
- Reduce `trail_length` to improve animation performance
- Increase `update_interval` to reduce CPU usage
- Disable unnecessary satellite categories

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Development Setup

```bash
git clone [repository_url]
cd SatelliteConstellationTrails
pip install -r requirements.txt
python satellite_visualizer.py
```

## 📞 Contact

For questions or suggestions, please submit an Issue or contact the project maintainers.

## 🎯 Future Plans

- [ ] Add 3D visualization mode
- [ ] Support custom time ranges
- [ ] Add satellite orbital parameter display
- [ ] Support additional satellite data sources
- [ ] Add orbital prediction functionality
- [ ] Optimize mobile device display

---

**⭐ If this project helps you, please give it a star!**

---

## 中文版本

# 🛰️ Satellite Constellation Visualizer

一个实时卫星轨道可视化工具，能够创建艺术化的卫星轨道图案和实时追踪卫星位置。

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## ✨ 功能特性

- 🔴 **实时卫星追踪**：动态显示卫星位置和轨道轨迹
- 🎨 **轨道艺术图案**：生成1小时内的卫星轨道艺术图案
- 🗺️ **星座地图**：显示当前所有卫星的静态位置图
- 🌈 **多类别数据**：支持5种不同类型的卫星数据源
- ⚡ **性能优化**：智能数据采样和限制，确保流畅运行

## 🛰️ 支持的卫星类别

| 类别 | 颜色 | 描述 | 数据源 |
|------|------|------|--------|
| ISS & Crew Vehicles | 🔴 红色 | 国际空间站和载人飞行器 | CelesTrak |
| Starlink | 🟢 绿色 | SpaceX星链卫星 | CelesTrak |
| GPS Constellation | 🔵 蓝色 | GPS导航卫星 | CelesTrak |
| Bright Satellites | 🟡 黄色 | 明亮可见卫星 | CelesTrak |
| Weather Satellites | 🟣 紫色 | 气象卫星 | CelesTrak |

## 📋 系统要求

- Python 3.7+
- 网络连接（用于获取卫星轨道数据）
- 支持matplotlib的图形显示环境

## 🔧 安装依赖

```bash
pip install numpy matplotlib requests skyfield
```

或使用requirements.txt：

```bash
pip install -r requirements.txt
```

### 主要依赖包

- **numpy**: 数值计算
- **matplotlib**: 数据可视化和动画
- **requests**: HTTP请求获取卫星数据
- **skyfield**: 天体力学计算和卫星轨道预测

## 🚀 快速开始

### 基本使用

```bash
python satellite_visualizer.py
```

### 交互式菜单

运行程序后，您将看到以下选项：

```
Choose visualization mode:
1. Real-time satellite tracking (animated)    # 实时卫星追踪
2. Create orbital art pattern (1-hour paths)  # 创建轨道艺术图案
3. Current constellation map (static)         # 当前星座地图
4. Exit                                       # 退出
```

### 编程接口使用

```python
from satellite_visualizer import SatelliteVisualizer

# 创建可视化器
viz = SatelliteVisualizer(trail_length=30, update_interval=2000)

# 生成轨道艺术
viz.create_orbital_art()

# 创建星座地图
viz.create_constellation_map()

# 开始实时追踪
viz.start_real_time_visualization()
```

## 📊 数据源和限制

### 数据获取
- 所有卫星数据来自 [CelesTrak](https://celestrak.com/)
- 使用Two-Line Element (TLE) 格式的轨道数据
- 数据实时从互联网获取，确保轨道信息准确

### 性能优化
- 每个类别限制10-50颗卫星
- 轨道艺术模式选择每类别4颗代表性卫星
- 总卫星数量控制在200颗以内
- 1小时时间窗口，每分钟采样一次

## 🎨 输出文件

程序会在当前目录生成以下文件：

- `orbital_art.png`: 1小时轨道艺术图案（300 DPI）
- `constellation_map.png`: 当前卫星位置图（300 DPI）

## 🎯 功能详解

### 1. 实时卫星追踪 (Real-time Tracking)
- **功能**：动画显示卫星实时位置和轨道轨迹
- **特点**：
  - 实时更新卫星位置
  - 显示轨道轨迹（可配置长度）
  - 时间戳和活跃卫星计数
  - 交互式图形界面

### 2. 轨道艺术图案 (Orbital Art Pattern)
- **功能**：生成1小时内的卫星轨道艺术图案
- **特点**：
  - 每个类别选择4颗代表性卫星
  - 1小时时间范围，60个时间点
  - 彩色轨道线条，不同类别用不同颜色
  - 高分辨率PNG输出

### 3. 星座地图 (Constellation Map)
- **功能**：显示当前时刻所有卫星的位置
- **特点**：
  - 静态散点图显示
  - 包含所有加载的卫星
  - 时间戳标注
  - 分类图例

## ⚙️ 配置选项

### SatelliteVisualizer 参数

```python
SatelliteVisualizer(
    trail_length=50,      # 轨道轨迹长度（点数）
    update_interval=1000  # 动画更新间隔（毫秒）
)
```

### 自定义颜色方案

可以修改 `category_colors` 字典来自定义颜色：

```python
self.category_colors = {
    'ISS & Crew Vehicles': '#FF4444',  # 红色
    'Starlink': '#44FF44',             # 绿色
    'GPS Constellation': '#4444FF',    # 蓝色
    'Bright Satellites': '#FFFF44',   # 黄色
    'Weather Satellites': '#FF44FF'   # 紫色
}
```

## 🔍 技术细节

### 坐标系统
- 使用地心直角坐标系 (Earth-Centered Cartesian)
- X-Y平面投影显示
- 单位：公里 (km)

### 时间处理
- 使用UTC时间
- Skyfield库进行精确的天体力学计算
- 支持任意时间范围的轨道预测

### 数据处理流程
1. 从CelesTrak获取TLE数据
2. 解析TLE格式创建卫星对象
3. 使用SGP4模型计算轨道位置
4. 转换为地心坐标系
5. 可视化渲染

## 🐛 故障排除

### 常见问题

**1. 网络连接错误**
```
Failed to load [Category]: HTTPSConnectionPool...
```
- 检查网络连接
- 确认防火墙设置
- 尝试使用代理

**2. 没有卫星数据**
```
No satellites loaded. Please check your internet connection.
```
- 检查网络连接
- 验证CelesTrak网站可访问性

**3. 图形显示问题**
- 确认matplotlib后端配置正确
- 在SSH环境中可能需要X11转发
- Windows用户确认GUI环境可用

### 调试模式

取消注释以下行启用详细日志：
```python
# warnings.filterwarnings('ignore')  # 注释此行
```

## 📈 性能说明

### 资源使用
- **内存**：约50-100MB（取决于卫星数量）
- **CPU**：中等（实时模式下持续计算）
- **网络**：初始化时下载约1-2MB数据

### 优化建议
- 减少 `trail_length` 提升动画性能
- 增加 `update_interval` 降低CPU使用
- 关闭不需要的卫星类别

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issues和Pull Requests！

### 开发环境搭建

```bash
git clone [repository_url]
cd SatelliteConstellationTrails
pip install -r requirements.txt
python satellite_visualizer.py
```

## 📞 联系方式

如有问题或建议，请提交Issue或联系项目维护者。

## 🎯 未来计划

- [ ] 添加3D可视化模式
- [ ] 支持自定义时间范围
- [ ] 添加卫星轨道参数显示
- [ ] 支持更多卫星数据源
- [ ] 添加轨道预测功能
- [ ] 优化移动设备显示

---

**⭐ 如果这个项目对您有帮助，请给它一个星标！**