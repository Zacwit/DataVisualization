#!/usr/bin/env python3
"""
Real-time Satellite Constellation Visualizer
Creates artistic visualizations of satellite positions and orbital trails
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import requests
from skyfield.api import load, EarthSatellite, utc
from skyfield.sgp4lib import EarthSatellite as SGP4Satellite
from datetime import datetime, timedelta
import time
from collections import defaultdict, deque
import warnings
warnings.filterwarnings('ignore')

class SatelliteVisualizer:
    def __init__(self, trail_length=50, update_interval=1000):
        """
        Initialize the satellite visualizer
        
        Args:
            trail_length (int): Number of points in orbital trail
            update_interval (int): Animation update interval in milliseconds
        """
        self.trail_length = trail_length
        self.update_interval = update_interval
        self.satellites = {}
        self.satellite_trails = defaultdict(lambda: deque(maxlen=trail_length))
        
        # Define consistent category colors with high contrast
        self.category_colors = {
            'ISS & Crew Vehicles': '#FF4444',      # Bright Red
            'Starlink': '#44FF44',                 # Bright Green  
            'GPS Constellation': '#4444FF',        # Bright Blue
            'Bright Satellites': '#FFFF44',       # Bright Yellow
            'Weather Satellites': '#FF44FF'       # Bright Magenta
        }
        
        # Load timescale
        self.ts = load.timescale()
        
        # 不在初始化时设置图形，只在需要实时追踪时才创建
        self.fig = None
        self.ax = None
        
        # Load satellite data
        self.load_satellites()
    
    def setup_plot(self):
        """Setup the matplotlib figure and axis"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(15, 12), facecolor='black')
        
        # Create Earth representation
        earth = Circle((0, 0), 6371, color='#1f4e79', alpha=0.7, zorder=1)
        self.ax.add_patch(earth)
        
        # Add continents outline (simplified)
        self.add_earth_features()
        
        # Set equal aspect ratio and limits
        self.ax.set_xlim(-15000, 15000)
        self.ax.set_ylim(-15000, 15000)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('black')
        
        # Add grid and labels
        self.ax.grid(True, alpha=0.3, color='gray')
        self.ax.set_xlabel('X (km)', color='white', fontsize=12)
        self.ax.set_ylabel('Y (km)', color='white', fontsize=12)
        self.ax.set_title('Real-time Satellite Constellation Tracker\n', 
                         color='white', fontsize=16, fontweight='bold')
        
        # Add timestamp text
        self.time_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                     color='cyan', fontsize=10, verticalalignment='top')
        
        # Add satellite count text
        self.count_text = self.ax.text(0.02, 0.94, '', transform=self.ax.transAxes, 
                                      color='yellow', fontsize=10, verticalalignment='top')
        
        # Initialize plot elements for real-time tracking
        self.satellite_points = {}
        self.trail_lines = {}
        
        # Create legend using consistent category colors
        legend_handles = []
        for category, color in self.category_colors.items():
            # Check if we have satellites in this category
            category_has_satellites = any(
                sat_info['category'] == category 
                for sat_info in self.satellites.values()
            )
            
            if category_has_satellites:
                # Create a dummy plot for legend
                legend_handles.append(self.ax.plot([], [], 'o', color=color, 
                                                  markersize=6, alpha=0.8, 
                                                  label=category)[0])
        
        # Create plot elements for each satellite
        for name, sat_info in self.satellites.items():
            color = sat_info['color']
            
            # Create point for satellite
            self.satellite_points[name] = self.ax.plot([], [], 'o', 
                                                      color=color, 
                                                      markersize=4, 
                                                      alpha=0.8,
                                                      zorder=3)[0]
            
            # Create trail line
            self.trail_lines[name] = self.ax.plot([], [], '-', 
                                                 color=color, 
                                                 alpha=0.3, 
                                                 linewidth=1,
                                                 zorder=2)[0]
        
        # Add legend for data sources
        if legend_handles:
            legend = self.ax.legend(handles=legend_handles, loc='upper right', 
                                   facecolor='black', edgecolor='white', 
                                   labelcolor='white', fontsize=9, 
                                   title='Data Sources', title_fontsize=10,
                                   framealpha=0.8)
            # Make legend title white
            legend.get_title().set_color('white')
        
    def add_earth_features(self):
        """Add basic Earth features for visual reference"""
        # Equator line
        equator_x = np.linspace(-6371, 6371, 100)
        equator_y = np.zeros_like(equator_x)
        self.ax.plot(equator_x, equator_y, '--', color='lightblue', alpha=0.5, linewidth=1)
        
        # Prime meridian
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
        meridian_x = 6371 * np.cos(theta)
        meridian_y = 6371 * np.sin(theta)
        self.ax.plot(meridian_x, meridian_y, '--', color='lightblue', alpha=0.5, linewidth=1)
    
    def load_satellites(self):
        """Load satellite TLE data from various sources"""
        satellite_sources = {
            'ISS & Crew Vehicles': 'https://celestrak.com/NORAD/elements/stations.txt',
            'Starlink': 'https://celestrak.com/NORAD/elements/starlink.txt',
            'GPS Constellation': 'https://celestrak.com/NORAD/elements/gps-ops.txt',
            'Bright Satellites': 'https://celestrak.com/NORAD/elements/visual.txt',
            'Weather Satellites': 'https://celestrak.com/NORAD/elements/weather.txt'
        }
        
        print("Loading satellite data...")
        
        for category, url in satellite_sources.items():
            try:
                print(f"Fetching {category}...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                lines = response.text.strip().split('\n')
                
                # Parse TLE data (3 lines per satellite)
                for i in range(0, len(lines) - 2, 3):
                    if i + 2 < len(lines):
                        name = lines[i].strip()
                        line1 = lines[i + 1].strip()
                        line2 = lines[i + 2].strip()
                        
                        try:
                            satellite = EarthSatellite(line1, line2, name, self.ts)
                            self.satellites[name] = {
                                'satellite': satellite,
                                'category': category,
                                'color': self.category_colors.get(category, '#FFFFFF')  # Use category color
                            }
                            
                            # Limit total satellites for performance
                            if len(self.satellites) >= 100:
                                break
                        except Exception as e:
                            continue
                
                if len(self.satellites) >= 100:
                    break
                    
            except Exception as e:
                print(f"Failed to load {category}: {e}")
                continue
        
        print(f"Loaded {len(self.satellites)} satellites")
        
        # 图形元素将在需要时创建（在setup_plot中）
    
    def calculate_satellite_position(self, satellite, current_time):
        """Calculate satellite position in Earth-centered coordinates"""
        try:
            # Get satellite position
            geocentric = satellite.at(current_time)
            
            # Convert to Earth-centered Cartesian coordinates (km)
            x, y, z = geocentric.position.km
            
            return x, y, z
        except Exception:
            return None, None, None
    
    def update_animation(self, frame):
        """Update animation frame"""
        current_time = self.ts.now()
        
        active_satellites = 0
        
        for name, sat_info in self.satellites.items():
            satellite = sat_info['satellite']
            
            # Calculate position
            x, y, z = self.calculate_satellite_position(satellite, current_time)
            
            if x is not None and y is not None:
                active_satellites += 1
                
                # Update satellite position (using X-Y projection)
                self.satellite_points[name].set_data([x], [y])
                
                # Add to trail
                self.satellite_trails[name].append((x, y))
                
                # Update trail
                if len(self.satellite_trails[name]) > 1:
                    trail_x, trail_y = zip(*self.satellite_trails[name])
                    self.trail_lines[name].set_data(trail_x, trail_y)
                    
                    # Fade trail alpha based on age
                    alphas = np.linspace(0.1, 0.6, len(trail_x))
                    self.trail_lines[name].set_alpha(0.4)
        
        # Update text displays
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.time_text.set_text(f'Time: {time_str}')
        self.count_text.set_text(f'Active Satellites: {active_satellites}')
        
        return list(self.satellite_points.values()) + list(self.trail_lines.values()) + [self.time_text, self.count_text]
    
    def create_orbital_art(self):
        """Create artistic orbital pattern visualization"""
        print("Generating orbital art patterns...")
        
        fig, ax = plt.subplots(figsize=(15, 15), facecolor='black')
        ax.set_facecolor('black')
        
        # Time range for orbital art (24 hours)
        start_datetime = datetime.now()
        times_datetime = [start_datetime + timedelta(minutes=i*10) for i in range(144)]  # Every 10 minutes for 24 hours
        times = self.ts.utc([t.replace(tzinfo=utc) for t in times_datetime])
        
        # Earth
        earth = Circle((0, 0), 6371, color='#1f4e79', alpha=0.5, zorder=1)
        ax.add_patch(earth)
        
        # Track which categories are actually plotted for legend
        plotted_categories = set()
        
        # Plot orbital paths
        for name, sat_info in list(self.satellites.items())[:20]:  # Limit for performance
            satellite = sat_info['satellite']
            category = sat_info['category']
            color = sat_info['color']
            positions = []
            
            for t in times:
                x, y, z = self.calculate_satellite_position(satellite, t)
                if x is not None:
                    positions.append((x, y))
            
            if positions:
                x_coords, y_coords = zip(*positions)
                # Only add label for the first satellite of each category
                label = category if category not in plotted_categories else ""
                if category not in plotted_categories:
                    plotted_categories.add(category)
                
                ax.plot(x_coords, y_coords, '-', color=color, 
                       alpha=0.7, linewidth=1.5, zorder=2, label=label)
        
        ax.set_xlim(-20000, 20000)
        ax.set_ylim(-20000, 20000)
        ax.set_aspect('equal')
        ax.set_title('24-Hour Orbital Art Pattern', color='white', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.2, color='gray')
        
        # Add legend for data sources
        if plotted_categories:
            legend = ax.legend(loc='upper right', facecolor='black', edgecolor='white', 
                              labelcolor='white', fontsize=10, title='Data Sources', 
                              title_fontsize=12, framealpha=0.8)
            # Make legend title white
            legend.get_title().set_color('white')
        
        plt.tight_layout()
        plt.savefig('orbital_art.png', dpi=300, facecolor='black')
        print("Orbital art saved as 'orbital_art.png'")
        plt.show()  # 显示选择的图形窗口
    
    def start_real_time_visualization(self):
        """Start the real-time animation"""
        print("Starting real-time satellite visualization...")
        print("Close the plot window to stop the animation")
        
        # 只在需要实时追踪时才创建图形
        if self.fig is None:
            self.setup_plot()
        
        # Create animation
        anim = animation.FuncAnimation(
            self.fig, 
            self.update_animation,
            interval=self.update_interval,
            blit=False,
            cache_frame_data=False
        )
        
        plt.tight_layout()
        plt.show()
        
        return anim
    
    def create_constellation_map(self):
        """Create a static constellation map showing current positions"""
        print("Creating constellation map...")
        
        fig, ax = plt.subplots(figsize=(15, 12), facecolor='black')
        ax.set_facecolor('black')
        
        current_time = self.ts.now()
        
        # Earth
        earth = Circle((0, 0), 6371, color='#1f4e79', alpha=0.6, zorder=1)
        ax.add_patch(earth)
        
        # Plot current positions and collect unique categories
        plotted_categories = set()  # Track which categories we've already labeled
        
        for name, sat_info in self.satellites.items():
            satellite = sat_info['satellite']
            category = sat_info['category']
            color = sat_info['color']
            
            x, y, z = self.calculate_satellite_position(satellite, current_time)
            
            if x is not None and y is not None:
                # Only add label for the first satellite of each category
                label = category if category not in plotted_categories else ""
                if category not in plotted_categories:
                    plotted_categories.add(category)
                
                ax.scatter(x, y, c=[color], s=30, alpha=0.8, zorder=3, label=label)
        
        ax.set_xlim(-25000, 25000)
        ax.set_ylim(-25000, 25000)
        ax.set_aspect('equal')
        ax.set_title(f'Current Satellite Constellation Map\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}', 
                    color='white', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, color='gray')
        
        # Create a clean legend with only data source categories
        if plotted_categories:
            legend = ax.legend(loc='upper right', facecolor='black', edgecolor='white', 
                              labelcolor='white', fontsize=10, title='Data Sources', 
                              title_fontsize=12, framealpha=0.8)
            # Make legend title white
            legend.get_title().set_color('white')
        
        plt.tight_layout()
        plt.savefig('constellation_map.png', dpi=300, facecolor='black')
        print("Constellation map saved as 'constellation_map.png'")
        plt.show()  # 显示选择的图形窗口

def main():
    """Main function to run the satellite visualizer"""
    print("=== Real-time Satellite Constellation Visualizer ===")
    print()
    
    # Create visualizer
    viz = SatelliteVisualizer(trail_length=30, update_interval=2000)
    
    if not viz.satellites:
        print("No satellites loaded. Please check your internet connection.")
        return
    
    while True:
        print("\nChoose visualization mode:")
        print("1. Real-time satellite tracking (animated)")
        print("2. Create orbital art pattern (24-hour paths)")
        print("3. Current constellation map (static)")
        print("4. Exit")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                viz.start_real_time_visualization()
            elif choice == '2':
                viz.create_orbital_art()
                print("Close the plot window to continue or choose another option...")
            elif choice == '3':
                viz.create_constellation_map()
                print("Close the plot window to continue or choose another option...")
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\nProgram interrupted. Goodbye!")
            break
        except EOFError:
            print("\nInput ended. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing...")
            continue

if __name__ == "__main__":
    main()