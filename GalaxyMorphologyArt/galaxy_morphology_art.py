#!/usr/bin/env python3
"""
Galaxy Morphology Art Visualizer
Creates artistic visualizations from SDSS (Sloan Digital Sky Survey) galaxy data
including morphology-based art and redshift color gradients
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
from matplotlib.collections import PatchCollection
import pandas as pd
import requests
from io import StringIO
import warnings
import colorsys
from scipy.interpolate import griddata
from scipy.stats import gaussian_kde
import seaborn as sns

warnings.filterwarnings('ignore')

class GalaxyArtVisualizer:
    """Main class for creating artistic galaxy visualizations"""
    
    def __init__(self):
        self.galaxy_data = None
        self.fig_size = (16, 10)
        
    def fetch_galaxy_data(self, limit=1000):
        """
        尝试从SDSS数据库获取星系数据
        如果失败则生成合成数据用于演示
        """
        # 简化的SQL查询 - 基于测试结果优化，添加ORDER BY确保结果一致
        query = f"""
        SELECT TOP {limit}
            objid, ra, dec,
            u, g, r, i, z,
            petroR50_r, petroR90_r,
            deVAB_r, expAB_r,
            petroMag_r
        FROM PhotoObj 
        WHERE 
            type = 3 
            AND petroMag_r BETWEEN 15 AND 18
            AND petroR50_r > 0 AND petroR50_r < 10
            AND deVAB_r > 0
            AND dec BETWEEN -1.2 AND -0.8
        ORDER BY objid
        """
        
        # 使用可靠的DR16端点 - 测试证实工作正常
        url = "https://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx"
        params = {
            'cmd': query,
            'format': 'csv'
        }
        
        # 实现渐进式数据获取策略
        if limit > 25:  # 降低阈值
            print(f"Large query ({limit} records) - testing connection first...")
            # 先用小查询测试连接
            test_success = self._test_sdss_connection()
            if not test_success:
                print("Connection test failed, using synthetic data")
                self._generate_synthetic_data(limit)
                return False
        
        try:
            print(f"Requesting {limit} galaxies from SDSS DR16...")
            response = requests.get(url, params=params, timeout=30)  # 减少超时时间
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                response_text = response.text.strip()
                print(f"Response length: {len(response_text)} characters")
                
                # 检查响应是否为HTML错误页面
                if response_text.startswith('<') or 'html' in response_text.lower()[:100]:
                    print("Received HTML error page instead of CSV data")
                    raise ValueError("Server returned HTML instead of CSV data")
                
                # 处理SDSS特有的#Table1头行
                try:
                    lines = response_text.split('\n')
                    if lines[0].startswith('#'):
                        csv_content = '\n'.join(lines[1:])
                    else:
                        csv_content = response_text
                    
                    self.galaxy_data = pd.read_csv(StringIO(csv_content))
                    
                    if len(self.galaxy_data) == 0:
                        raise ValueError("Empty dataset returned")
                    
                    print(f"SUCCESS: Fetched {len(self.galaxy_data)} real galaxies from SDSS!")
                    print(f"Columns: {list(self.galaxy_data.columns)}")
                    
                    # 添加一些基本的形态学参数
                    self._add_basic_morphology()
                    self._calculate_morphology_params()
                    
                    # 保存SDSS数据到CSV文件
                    self._save_sdss_data_to_csv()
                    
                    return True
                    
                except pd.errors.ParserError as parse_error:
                    print(f"CSV parsing error: {parse_error}")
                    print("Raw response preview:")
                    print(response_text[:500])
                    raise parse_error
                    
            else:
                print(f"HTTP error {response.status_code}")
                if response.text:
                    print("Response:", response.text[:300])
                self._generate_synthetic_data(limit)
                return False
                
        except requests.exceptions.Timeout:
            print(f"Network timeout after 30 seconds")
            print("This may be due to:")
            print("- Slow network connection")
            print("- SDSS server load")
            print("- Large query size")
            self._generate_synthetic_data(limit)
            return False
        except Exception as e:
            print(f"Error fetching SDSS data: {e}")
            print("Falling back to synthetic data...")
            self._generate_synthetic_data(limit)
            return False
    
    def _test_sdss_connection(self):
        """测试SDSS连接的小查询"""
        test_query = "SELECT TOP 2 objid, ra, dec FROM PhotoObj WHERE type = 3"
        url = "https://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx"
        
        try:
            response = requests.get(
                url, 
                params={'cmd': test_query, 'format': 'csv'}, 
                timeout=15
            )
            return response.status_code == 200 and len(response.text) > 50
        except:
            return False
    
    def _add_basic_morphology(self):
        """为SDSS数据添加基本形态学分类"""
        if self.galaxy_data is not None:
            # 基于德瓦库仑轮廓拟合分数估算形态学类型
            # deVAB_r 接近1表示椭圆星系，接近0表示螺旋星系
            if 'deVAB_r' in self.galaxy_data.columns:
                self.galaxy_data['fracDeV_r'] = self.galaxy_data['deVAB_r']
            else:
                # 如果没有deVAB_r，使用其他参数估算
                self.galaxy_data['fracDeV_r'] = np.random.beta(2, 2, len(self.galaxy_data))
            
            # 添加形态学分类标志
            self.galaxy_data['elliptical'] = (self.galaxy_data['fracDeV_r'] >= 0.5).astype(int)
            self.galaxy_data['spiral'] = (self.galaxy_data['fracDeV_r'] < 0.5).astype(int)
            
            # 添加基本的颜色指数
            if 'g' in self.galaxy_data.columns and 'r' in self.galaxy_data.columns:
                self.galaxy_data['dered_g'] = self.galaxy_data['g']
                self.galaxy_data['dered_r'] = self.galaxy_data['r']
                if 'i' in self.galaxy_data.columns:
                    self.galaxy_data['dered_i'] = self.galaxy_data['i']
            
            # 添加模拟的红移数据（真实红移需要光谱数据）
            if 'redshift' not in self.galaxy_data.columns:
                # 基于视星等估算红移（亮的星系通常更近）
                mag_normalized = (self.galaxy_data['petroMag_r'] - 15) / 5  # 归一化到0-1
                # 使用beta分布生成合理的红移范围
                self.galaxy_data['redshift'] = np.random.beta(2, 5, len(self.galaxy_data)) * 0.3 * (1 + mag_normalized)
    
    def _save_sdss_data_to_csv(self):
        """将从SDSS获取的数据保存为CSV文件"""
        import os
        from datetime import datetime
        
        # 创建输出目录
        output_dir = 'galaxy_art_output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"sdss_galaxy_data_{timestamp}.csv"
        csv_path = os.path.join(output_dir, csv_filename)
        
        try:
            # 保存数据到CSV
            self.galaxy_data.to_csv(csv_path, index=False)
            print(f"✓ SDSS data saved to: {csv_path}")
            print(f"  Data contains {len(self.galaxy_data)} galaxies with {len(self.galaxy_data.columns)} parameters")
            
            # 显示保存的数据统计
            print(f"  Sample data preview:")
            print(f"    - RA range: {self.galaxy_data['ra'].min():.3f} to {self.galaxy_data['ra'].max():.3f}")
            print(f"    - DEC range: {self.galaxy_data['dec'].min():.3f} to {self.galaxy_data['dec'].max():.3f}")
            print(f"    - Magnitude range: {self.galaxy_data['petroMag_r'].min():.2f} to {self.galaxy_data['petroMag_r'].max():.2f}")
            print(f"    - Redshift range: {self.galaxy_data['redshift'].min():.4f} to {self.galaxy_data['redshift'].max():.4f}")
            
        except Exception as e:
            print(f"⚠️  Warning: Failed to save SDSS data to CSV: {e}")
            print("   Visualization will continue with the data in memory")
    
    def _generate_synthetic_data(self, n_galaxies=200):
        """Generate synthetic galaxy data for demonstration purposes"""
        np.random.seed(42)
        
        # Generate synthetic data that mimics SDSS galaxy properties
        self.galaxy_data = pd.DataFrame({
            'ra': np.random.uniform(148, 152, n_galaxies),
            'dec': np.random.uniform(0.8, 1.2, n_galaxies),  # Adjusted range from 0-4 to 0.8-1.2
            'redshift': np.random.beta(2, 5, n_galaxies) * 0.3,  # Typical range 0-0.3
            'petroR50_r': np.random.lognormal(1.0, 0.5, n_galaxies),  # Half-light radius
            'petroR90_r': np.random.lognormal(1.5, 0.5, n_galaxies),  # 90% light radius
            'fracDeV_r': np.random.beta(2, 2, n_galaxies),  # Elliptical vs Spiral
            'modelMag_r': np.random.normal(17, 1.5, n_galaxies),  # Magnitude
            'expAB_r': np.random.uniform(0.3, 0.9, n_galaxies),  # Axis ratio (ellipticity)
            'dered_g': np.random.normal(18, 1.5, n_galaxies),
            'dered_r': np.random.normal(17, 1.5, n_galaxies),
            'dered_i': np.random.normal(16.5, 1.5, n_galaxies),
        })
        
        # Add morphology classification
        self.galaxy_data['spiral'] = (self.galaxy_data['fracDeV_r'] < 0.5).astype(int)
        self.galaxy_data['elliptical'] = (self.galaxy_data['fracDeV_r'] >= 0.5).astype(int)
        
        self._calculate_morphology_params()
        print(f"Generated {n_galaxies} synthetic galaxies for visualization")
    
    def _calculate_morphology_params(self):
        """Calculate additional morphological parameters"""
        if 'petroR50_r' in self.galaxy_data.columns and 'petroR90_r' in self.galaxy_data.columns:
            # Concentration index (useful for morphology)
            self.galaxy_data['concentration'] = (
                self.galaxy_data['petroR90_r'] / 
                (self.galaxy_data['petroR50_r'] + 0.01)
            )
        
        # Color indices (if magnitude data available)
        if 'dered_g' in self.galaxy_data.columns and 'dered_r' in self.galaxy_data.columns:
            self.galaxy_data['g_r_color'] = (
                self.galaxy_data['dered_g'] - self.galaxy_data['dered_r']
            )
        if 'dered_r' in self.galaxy_data.columns and 'dered_i' in self.galaxy_data.columns:
            self.galaxy_data['r_i_color'] = (
                self.galaxy_data['dered_r'] - self.galaxy_data['dered_i']
            )
    
    def redshift_to_color(self, z, cmap_name='plasma'):
        """
        Convert redshift to color with consistent mapping across all plots
        使用偏红的颜色映射，避免蓝色部分，更符合红移的物理直觉
        
        Parameters:
        -----------
        z : float or array, Redshift values
        cmap_name : str, Color scheme (default: 'plasma' for reddish colors)
        """
        # Use consistent global redshift range for normalization
        # Get actual data range for better normalization
        if hasattr(self, 'galaxy_data') and self.galaxy_data is not None and 'redshift' in self.galaxy_data.columns:
            z_min = self.galaxy_data['redshift'].min()
            z_max = self.galaxy_data['redshift'].max()
        else:
            # Fallback range
            z_min, z_max = 0.0, 0.3
            
        # Normalize redshift to 0-1 range using actual data range
        z_norm = np.clip((np.array(z) - z_min) / (z_max - z_min), 0, 1)
        
        # Use plasma colormap with focus on red/orange/yellow range (避免蓝紫色)
        # Map to the warmer part of plasma colormap (0.3-1.0 range)
        plasma_range = 0.3 + z_norm * 0.7  # 映射到plasma的0.3-1.0范围，避免蓝紫色
        cmap = plt.cm.plasma
        colors = cmap(plasma_range)
        
        return colors
    
    def get_redshift_colormap_info(self):
        """Get consistent colormap and normalization info for colorbars"""
        if hasattr(self, 'galaxy_data') and self.galaxy_data is not None and 'redshift' in self.galaxy_data.columns:
            z_min = self.galaxy_data['redshift'].min()
            z_max = self.galaxy_data['redshift'].max()
        else:
            z_min, z_max = 0.0, 0.3
            
        # 创建一个自定义的颜色映射，对应plasma的0.3-1.0范围
        from matplotlib.colors import LinearSegmentedColormap
        plasma_cmap = plt.cm.plasma
        # 提取plasma colormap的0.3-1.0部分
        colors = plasma_cmap(np.linspace(0.3, 1.0, 256))
        custom_cmap = LinearSegmentedColormap.from_list('plasma_warm', colors)
        
        return custom_cmap, plt.Normalize(vmin=z_min, vmax=z_max)
    
    def create_morphology_art(self):
        """Create artistic visualization based on galaxy morphology"""
        if self.galaxy_data is None:
            print("No galaxy data available. Fetching data first...")
            self.fetch_sdss_galaxies()
        
        fig, axes = plt.subplots(2, 2, figsize=self.fig_size, facecolor='#0a0a0a')
        fig.suptitle('Galaxy Morphology Art Collection', fontsize=20, color='white', y=0.98)
        
        # 1. Morphological Sky Map
        ax1 = axes[0, 0]
        self._plot_morphological_sky(ax1)
        
        # 2. Redshift Gradient Field
        ax2 = axes[0, 1]
        self._plot_redshift_field(ax2)
        
        # 3. Galaxy Size vs Redshift Bubble Art
        ax3 = axes[1, 0]
        self._plot_size_redshift_bubbles(ax3)
        
        # 4. Concentration Index Spiral
        ax4 = axes[1, 1]
        self._plot_concentration_spiral(ax4)
        
        plt.tight_layout()
        return fig
    
    def _plot_morphological_sky(self, ax):
        """Plot galaxies with morphology-dependent shapes and colors"""
        ax.set_facecolor('#000814')
        ax.set_title('Morphological Sky Map', color='white', fontsize=14)
        
        # Create patches for each galaxy
        patches = []
        colors = []
        
        for _, galaxy in self.galaxy_data.iterrows():
            # Determine shape based on morphology
            if 'fracDeV_r' in galaxy:
                is_elliptical = galaxy['fracDeV_r'] > 0.5
            else:
                is_elliptical = galaxy.get('elliptical', 0) > 0.5
            
            # Size based on magnitude (brighter = larger)
            if 'modelMag_r' in galaxy:
                size = (22 - galaxy.get('modelMag_r', 18)) * 0.01
            else:
                size = np.random.uniform(0.02, 0.08)
            
            # Color based on redshift - using consistent mapping
            color = self.redshift_to_color(np.array([galaxy['redshift']]))[0]
            
            if is_elliptical:
                # Elliptical galaxy - use ellipse
                ellipticity = galaxy.get('expAB_r', 0.7)
                patch = Ellipse((galaxy['ra'], galaxy['dec']), 
                               width=size, height=size*ellipticity,
                               angle=np.random.uniform(0, 180))
            else:
                # Spiral galaxy - use spiral arm effect (multiple ellipses)
                for i in range(3):
                    angle = i * 120 + np.random.uniform(-20, 20)
                    spiral_patch = Ellipse((galaxy['ra'], galaxy['dec']), 
                                          width=size*(1+i*0.3), 
                                          height=size*0.3,
                                          angle=angle, alpha=0.6-i*0.2)
                    patches.append(spiral_patch)
                    colors.append(color)
                continue
            
            patches.append(patch)
            colors.append(color)
        
        # Add patches to plot
        p = PatchCollection(patches, facecolors=colors, edgecolors='none', alpha=0.8)
        ax.add_collection(p)
        
        # Add cosmic web effect
        if len(self.galaxy_data) > 10:
            from scipy.spatial import Delaunay
            points = self.galaxy_data[['ra', 'dec']].values
            tri = Delaunay(points)
            ax.triplot(points[:, 0], points[:, 1], tri.simplices, 
                      color='cyan', alpha=0.1, linewidth=0.5)
        
        ax.set_xlim(self.galaxy_data['ra'].min()-0.5, self.galaxy_data['ra'].max()+0.5)
        
        # Adjust y-axis range to focus on the main galaxy distribution
        # For SDSS data (negative dec values), keep the range tight
        dec_range = self.galaxy_data['dec'].max() - self.galaxy_data['dec'].min()
        dec_margin = max(0.05, dec_range * 0.1)  # At least 0.05 degrees margin
        ax.set_ylim(self.galaxy_data['dec'].min() - dec_margin, 
                   self.galaxy_data['dec'].max() + dec_margin)
        
        # Set equal aspect ratio to prevent shape distortion
        ax.set_aspect('equal', adjustable='box')
        
        ax.set_xlabel('Right Ascension (degrees)', color='white')
        ax.set_ylabel('Declination (degrees)', color='white')
        ax.tick_params(colors='white')
        
        # Add redshift colorbar with consistent mapping
        cmap, norm = self.get_redshift_colormap_info()
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Redshift (z)', color='white')
        cbar.ax.tick_params(colors='white')
    
    def _plot_redshift_field(self, ax):
        """Create a continuous redshift gradient field"""
        ax.set_facecolor('#000814')
        ax.set_title('Redshift Gradient Field', color='white', fontsize=14)
        
        # Create grid for interpolation
        ra_range = np.linspace(self.galaxy_data['ra'].min(), 
                               self.galaxy_data['ra'].max(), 100)
        dec_range = np.linspace(self.galaxy_data['dec'].min(), 
                               self.galaxy_data['dec'].max(), 100)
        ra_grid, dec_grid = np.meshgrid(ra_range, dec_range)
        
        # Interpolate redshift values
        points = self.galaxy_data[['ra', 'dec']].values
        values = self.galaxy_data['redshift'].values
        z_grid = griddata(points, values, (ra_grid, dec_grid), method='cubic')
        
        # Create artistic gradient with consistent colormap
        cmap, norm = self.get_redshift_colormap_info()
        im = ax.imshow(z_grid, extent=[ra_range.min(), ra_range.max(),
                                       dec_range.min(), dec_range.max()],
                      cmap=cmap, norm=norm, aspect='auto', alpha=0.8, origin='lower')
        
        # Overlay actual galaxy positions with consistent coloring
        scatter = ax.scatter(self.galaxy_data['ra'], self.galaxy_data['dec'],
                           c=self.galaxy_data['redshift'], s=20,
                           cmap=cmap, norm=norm, edgecolors='white', linewidth=0.5,
                           alpha=0.9, zorder=5)
        
        ax.set_xlabel('Right Ascension (degrees)', color='white')
        ax.set_ylabel('Declination (degrees)', color='white')
        ax.tick_params(colors='white')
        
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Interpolated Redshift', color='white')
        cbar.ax.tick_params(colors='white')
    
    def _plot_size_redshift_bubbles(self, ax):
        """Create bubble art based on galaxy size and redshift"""
        ax.set_facecolor('#0a0a0a')
        ax.set_title('Galaxy Size-Redshift Bubble Art', color='white', fontsize=14)
        
        # Calculate sizes for visualization
        if 'petroR50_r' in self.galaxy_data.columns:
            sizes = np.sqrt(self.galaxy_data['petroR50_r']) * 100
        else:
            sizes = np.random.uniform(50, 500, len(self.galaxy_data))
        
        # Create color array based on redshift with consistent mapping
        colors = []
        for _, galaxy in self.galaxy_data.iterrows():
            z_color = self.redshift_to_color(np.array([galaxy['redshift']]))[0]
            colors.append(z_color)
        
        # Plot bubbles
        scatter = ax.scatter(self.galaxy_data['redshift'],
                           self.galaxy_data.get('concentration', 
                                                np.random.uniform(2, 4, len(self.galaxy_data))),
                           s=sizes, c=colors, alpha=0.6,
                           edgecolors='white', linewidth=1)
        
        # Add glow effect for larger galaxies
        for _, galaxy in self.galaxy_data.iterrows():
            if 'petroR50_r' in galaxy and galaxy['petroR50_r'] > self.galaxy_data['petroR50_r'].median():
                ax.scatter(galaxy['redshift'],
                         galaxy.get('concentration', 3),
                         s=np.sqrt(galaxy['petroR50_r']) * 200,
                         c='yellow', alpha=0.1, edgecolors='none')
        
        ax.set_xlabel('Redshift (z)', color='white')
        ax.set_ylabel('Concentration Index', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_xlim(-0.01, self.galaxy_data['redshift'].max() * 1.1)
    
    def _draw_realistic_galaxy(self, ax, x, y, size, color, galaxy_data, alpha=0.7):
        """Draw realistic galaxy shapes based on morphological parameters"""
        from matplotlib.patches import Ellipse, Circle, Wedge
        
        # Extract morphological parameters
        concentration = galaxy_data.get('concentration', 2.5)
        axis_ratio = galaxy_data.get('expAB_r', 0.7)  # b/a ratio
        is_spiral = galaxy_data.get('spiral', 0) == 1
        
        # Scale size appropriately for visibility - increased for better visibility
        base_size = size / 800  # Increased from 2000 to 800 for larger galaxies
        
        if is_spiral:
            # Spiral galaxy: disk + arms + bulge
            
            # Main disk (more extended)
            disk_width = base_size * 1.5  # Increased from 1.2 to 1.5
            disk_height = disk_width * axis_ratio
            rotation_angle = np.random.uniform(0, 180)
            
            # Disk with gradient effect
            disk = Ellipse((x, y), disk_width, disk_height, 
                          angle=rotation_angle, 
                          facecolor=color, alpha=alpha*0.6,
                          edgecolor='white', linewidth=0.3)
            ax.add_patch(disk)
            
            # Inner disk (brighter core)
            inner_disk = Ellipse((x, y), disk_width*0.6, disk_height*0.6,
                               angle=rotation_angle,
                               facecolor=color, alpha=alpha*0.8,
                               edgecolor='none')
            ax.add_patch(inner_disk)
            
            # Spiral arms (more realistic)
            arm_color = color if isinstance(color, str) else tuple(list(color) + [alpha*0.7])
            arm_length = disk_width * 0.8
            
            # Two spiral arms
            for arm_offset in [0, 180]:
                # Create spiral arm using multiple small ellipses
                for i in range(8):
                    arm_angle = rotation_angle + arm_offset + i * 25
                    arm_radius = arm_length * (0.3 + 0.7 * i / 8)
                    arm_x = x + arm_radius * np.cos(np.radians(arm_angle)) * 0.5
                    arm_y = y + arm_radius * np.sin(np.radians(arm_angle)) * 0.3
                    
                    arm_segment = Ellipse((arm_x, arm_y), 
                                        disk_width*0.2, disk_height*0.12,  # Increased from 0.15, 0.08
                                        angle=arm_angle,
                                        facecolor=color, alpha=alpha*0.4,
                                        edgecolor='none')
                    ax.add_patch(arm_segment)
            
            # Central bulge (based on concentration)
            bulge_size = base_size * 0.4 * (concentration / 3.0)  # Increased from 0.3 to 0.4
            bulge = Circle((x, y), bulge_size,
                         facecolor=color, alpha=alpha*0.9,
                         edgecolor='white', linewidth=0.2)
            ax.add_patch(bulge)
            
        else:
            # Elliptical galaxy: smoother, more concentrated
            
            # Main elliptical body
            ell_width = base_size * 1.1  # Increased from 0.8 to 1.1
            ell_height = ell_width * axis_ratio
            rotation_angle = np.random.uniform(0, 180)
            
            # Outer halo
            outer_ell = Ellipse((x, y), ell_width*1.6, ell_height*1.6,  # Increased from 1.4 to 1.6
                              angle=rotation_angle,
                              facecolor=color, alpha=alpha*0.3,
                              edgecolor='white', linewidth=0.2)
            ax.add_patch(outer_ell)
            
            # Main body
            main_ell = Ellipse((x, y), ell_width, ell_height,
                             angle=rotation_angle,
                             facecolor=color, alpha=alpha*0.7,
                             edgecolor='white', linewidth=0.3)
            ax.add_patch(main_ell)
            
            # Central concentration (brighter core)
            central_size = base_size * 0.5 * (concentration / 3.0)  # Increased from 0.4 to 0.5
            central_ell = Ellipse((x, y), central_size, central_size*axis_ratio,
                                angle=rotation_angle,
                                facecolor=color, alpha=alpha*0.9,
                                edgecolor='none')
            ax.add_patch(central_ell)
    
    def _plot_concentration_spiral(self, ax):
        """Create an artistic spiral based on concentration indices"""
        ax.set_facecolor('#000814')
        ax.set_title('Galactic Concentration Spiral', color='white', fontsize=14)
        
        # Sort galaxies by redshift for spiral ordering
        sorted_data = self.galaxy_data.sort_values('redshift')
        n_galaxies = len(sorted_data)
        
        # Create spiral coordinates
        theta = np.linspace(0, 4*np.pi, n_galaxies)
        r = np.linspace(0.5, 3, n_galaxies)
        
        # Convert to Cartesian
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Colors based on redshift with consistent mapping
        colors = self.redshift_to_color(sorted_data['redshift'].values)
        
        # Sizes based on concentration or magnitude
        if 'concentration' in sorted_data.columns:
            sizes = sorted_data['concentration'].values * 50
        else:
            sizes = np.random.uniform(20, 200, n_galaxies)
        
        # Plot spiral with realistic galaxy shapes
        for i, (xi, yi, color, size) in enumerate(zip(x, y, colors, sizes)):
            # Get galaxy data for this entry
            galaxy_data = sorted_data.iloc[i].to_dict()
            
            # Draw realistic galaxy shape
            self._draw_realistic_galaxy(ax, xi, yi, size, color, galaxy_data, alpha=0.8)
        
        # Connect with lines for spiral effect
        ax.plot(x, y, color='cyan', alpha=0.15, linewidth=0.8)
        
        # Add radial grid
        for i in range(1, 4):
            circle = plt.Circle((0, 0), i, fill=False, 
                              color='white', alpha=0.1)
            ax.add_artist(circle)
        
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add legend
        ax.text(0, -3.8, 'Distance from center: Time (Redshift)', 
               ha='center', color='white', fontsize=10)
        ax.text(0, -4.1, 'Point size: Galaxy concentration', 
               ha='center', color='white', fontsize=10)
    
    def create_interactive_3d_view(self):
        """Create a 3D visualization of galaxy distribution"""
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(14, 10), facecolor='#0a0a0a')
        ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0a')
        
        # Use redshift as z-coordinate (distance proxy)
        x = self.galaxy_data['ra']
        y = self.galaxy_data['dec']
        z = self.galaxy_data['redshift'] * 100  # Scale for visibility
        
        # Use redshift values for color mapping with consistent normalization
        redshift_colors = self.galaxy_data['redshift']
        cmap, norm = self.get_redshift_colormap_info()
        
        # Separate galaxies by morphology for different markers
        spiral_mask = self.galaxy_data.get('spiral', 0) > 0.5
        elliptical_mask = ~spiral_mask
        
        # Plot spiral galaxies with star markers
        if spiral_mask.any():
            spiral_scatter = ax.scatter(x[spiral_mask], y[spiral_mask], z[spiral_mask], 
                                      c=redshift_colors[spiral_mask], s=60, alpha=0.8,
                                      marker='*', edgecolors='white', linewidth=0.5,
                                      cmap=cmap, norm=norm, label='Spiral Galaxies')
        
        # Plot elliptical galaxies with circle markers
        if elliptical_mask.any():
            elliptical_scatter = ax.scatter(x[elliptical_mask], y[elliptical_mask], z[elliptical_mask], 
                                          c=redshift_colors[elliptical_mask], s=50, alpha=0.8,
                                          marker='o', edgecolors='white', linewidth=0.5,
                                          cmap=cmap, norm=norm, label='Elliptical Galaxies')
        
        # Connecting lines removed for cleaner visualization
        # (Previously showed cosmic web effect with lines between nearby galaxies)
        
        ax.set_xlabel('Right Ascension', color='white', labelpad=10)
        ax.set_ylabel('Declination', color='white', labelpad=10)
        ax.set_zlabel('Redshift (×100)', color='white', labelpad=10)
        ax.set_title('3D Galaxy Distribution in Observable Universe', 
                    color='white', fontsize=16, pad=20)
        
        # Customize appearance
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, alpha=0.2, color='white')
        ax.tick_params(colors='white')
        
        # Add colorbar for redshift
        if spiral_mask.any() or elliptical_mask.any():
            # Use the last scatter plot for colorbar reference
            scatter_ref = spiral_scatter if spiral_mask.any() else elliptical_scatter
            cbar = plt.colorbar(scatter_ref, ax=ax, shrink=0.5, aspect=20, pad=0.1)
            cbar.set_label('Redshift (z)', color='white', rotation=270, labelpad=15)
            cbar.ax.tick_params(colors='white')
        
        # Add legend for galaxy morphology (shapes)
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='*', color='w', markerfacecolor='gray', 
                  markersize=12, label='Spiral Galaxies', linestyle=''),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                  markersize=10, label='Elliptical Galaxies', linestyle='')
        ]
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor='#0a0a0a', edgecolor='white',
                 labelcolor='white')
        
        return fig
    
    def save_visualizations(self, output_dir='galaxy_art_output'):
        """Save all visualizations to files"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\nCreating visualizations and saving to '{output_dir}/'...")
        
        # Create and save morphology art
        fig1 = self.create_morphology_art()
        fig1.savefig(f'{output_dir}/galaxy_morphology_art.png', 
                    dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
        print("✓ Saved galaxy_morphology_art.png")
        
        # Create and save 3D view
        fig2 = self.create_interactive_3d_view()
        fig2.savefig(f'{output_dir}/galaxy_3d_distribution.png', 
                    dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
        print("✓ Saved galaxy_3d_distribution.png")
        
        # Save data summary
        if self.galaxy_data is not None:
            summary_file = f'{output_dir}/galaxy_data_summary.txt'
            with open(summary_file, 'w') as f:
                f.write("Galaxy Data Summary\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Total galaxies: {len(self.galaxy_data)}\n")
                f.write(f"Redshift range: {self.galaxy_data['redshift'].min():.4f} - "
                       f"{self.galaxy_data['redshift'].max():.4f}\n")
                if 'spiral' in self.galaxy_data.columns:
                    f.write(f"Spiral galaxies: {self.galaxy_data['spiral'].sum()}\n")
                if 'elliptical' in self.galaxy_data.columns:
                    f.write(f"Elliptical galaxies: {self.galaxy_data['elliptical'].sum()}\n")
                f.write("\n" + "=" * 50 + "\n")
                f.write("Data columns:\n")
                for col in self.galaxy_data.columns:
                    f.write(f"  - {col}\n")
            print(f"✓ Saved galaxy_data_summary.txt")
        
        print(f"\nAll visualizations saved to '{output_dir}/' directory!")


def main():
    """Main execution function"""
    print("=" * 60)
    print(" GALAXY MORPHOLOGY ART VISUALIZER")
    print(" Creating artistic visualizations from astronomical data")
    print("=" * 60)
    
    # Initialize visualizer
    visualizer = GalaxyArtVisualizer()
    
    # Fetch galaxy data (will use synthetic if SDSS unavailable)
    print("\nStep 1: Fetching galaxy data...")
    visualizer.fetch_galaxy_data(limit=50)  # 减少到50个以提高成功率
    
    # Create and save visualizations
    print("\nStep 2: Creating artistic visualizations...")
    visualizer.save_visualizations()
    
    # Display the visualizations
    print("\nStep 3: Displaying visualizations...")
    plt.show()
    
    print("\n" + "=" * 60)
    print(" Visualization complete!")
    print(" Check the 'galaxy_art_output' folder for saved images")
    print("=" * 60)


if __name__ == "__main__":
    main()
