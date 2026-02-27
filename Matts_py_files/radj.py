#!/usr/bin/env python3
"""
XENITH GSQ Polygon Data Downloader - GUI Version
===========================================================

Graphical user interface version with icon support for both window and .exe compilation.

Features:
- User-friendly GUI with dropdowns and buttons
- Custom window icon support
- Folder browser for output directory
- Progress bar for downloads
- Real-time status updates
- Coordinate input with lat,lon order
- Can be compiled to standalone .exe with custom icon

Requirements:
- tkinter (built into Python)
- gsq_polygon_client_final_fixed.py
- Optional: icon.ico file for window icon

To create .exe with icon:
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico gsq_gui_downloader_with_icon.py

Author: Manus AI
Date: August 27, 2025
Version: 4.1 (GUI with Icon Support)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from typing import List, Dict, Optional
import json

# Import our GSQ client
try:
    from gsq_polygon_client_final_fixed import GSQPolygonClient
except ImportError:
    print("Error: gsq_polygon_client_final_fixed.py not found!")
    print("Please ensure the GSQ client file is in the same directory.")
    sys.exit(1)


class GSQDownloaderGUI:
    """
    GUI application for GSQ polygon data downloading with icon support.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Xenith Custom GSQ Polygon Data Downloader v4.1")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        self.set_window_icon()
        
        # Initialize client
        self.client = GSQPolygonClient()
        self.download_thread = None
        
        # Predefined regions (stored as lat,lon for display, converted to lon,lat for API)
        self.predefined_regions = {
            'Mount Isa Mineral Province': {
                'description': 'Major copper, lead, zinc mining region',
                'coords': [[-21.0, 139.0], [-21.0, 141.0], [-20.0, 141.0], [-20.0, 139.0], [-21.0, 139.0]]
            },
            'Bowen Basin Coal Region': {
                'description': 'Major coal mining and sedimentary basin',
                'coords': [[-23.0, 147.0], [-23.0, 150.5], [-20.0, 150.5], [-20.0, 147.0], [-23.0, 147.0]]
            },
            'Brisbane Metropolitan Region': {
                'description': 'Urban geology and environmental data',
                'coords': [[-27.8, 152.5], [-27.8, 153.5], [-27.0, 153.5], [-27.0, 152.5], [-27.8, 152.5]]
            },
            'Cairns Region': {
                'description': 'Tropical geology and mineral exploration',
                'coords': [[-17.2, 145.0], [-17.2, 146.0], [-16.5, 146.0], [-16.5, 145.0], [-17.2, 145.0]]
            },
            'Great Barrier Reef Catchment': {
                'description': 'Environmental and marine geological data',
                'coords': [[-25.0, 145.0], [-25.0, 154.0], [-10.0, 154.0], [-10.0, 145.0], [-25.0, 145.0]]
            },
            'Custom Polygon': {
                'description': 'Enter your own coordinates',
                'coords': None
            }
        }
        
        # Data types
        self.data_types = {
            'All Data Types (Recommended)': {
                'filter': None,
                'terms': ['geology', 'mining', 'exploration', 'geochemistry', 'geophysics']
            },
            'Geochemistry Data': {
                'filter': 'earth_science_data_category:geochemistry',
                'terms': ['geochemistry', 'chemical analysis', 'assay', 'elements']
            },
            'Geophysics Data': {
                'filter': 'earth_science_data_category:geophysics',
                'terms': ['geophysics', 'magnetic', 'gravity', 'seismic']
            },
            'Geological Data': {
                'filter': 'earth_science_data_category:geology',
                'terms': ['geology', 'geological', 'structure', 'stratigraphy']
            },
            'Mining Data': {
                'filter': 'earth_science_data_category:mining',
                'terms': ['mining', 'exploration', 'resource', 'reserve']
            },
            'Hydrogeology Data': {
                'filter': 'earth_science_data_category:hydrogeology',
                'terms': ['hydrogeology', 'groundwater', 'aquifer', 'water']
            }
        }
        
        # File formats
        self.file_formats = {
            'All Formats (Recommended)': None,
            'PDF Reports': ['PDF'],
            'CSV Data Files': ['CSV'],
            'Excel Spreadsheets': ['XLSX'],
            'ZIP Archives': ['ZIP'],
            'Shapefiles': ['SHP'],
            'GeoTIFF Images': ['TIF'],
            'Text Files': ['TXT']
        }
        
        self.setup_ui()
    
    def set_window_icon(self):
        """Set the window icon if available."""
        # List of possible icon file names to look for
        icon_files = [
            'app_icon.ico',
            'icon.ico', 
            'gsq_icon.ico',
            'geological_icon.ico',
            'earth_icon.ico'
        ]
        
        for icon_file in icon_files:
            if os.path.exists(icon_file):
                try:
                    self.root.iconbitmap(icon_file)
                    print(f"✅ Window icon loaded: {icon_file}")
                    return
                except Exception as e:
                    print(f"⚠️ Could not load icon {icon_file}: {e}")
        
        # If no .ico file found, try to create a simple text-based icon
        try:
            # This creates a simple colored window icon using tkinter's built-in method
            self.root.iconname("GSQ Downloader")
            print("ℹ️ Using default system icon")
        except:
            print("ℹ️ No custom icon available, using system default")
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title with icon emoji
        title_label = ttk.Label(main_frame, text="🌏 GSQ Polygon Data Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for organized sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Area Selection
        area_frame = ttk.Frame(notebook)
        notebook.add(area_frame, text="📍 Search Area")
        self.setup_area_tab(area_frame)
        
        # Tab 2: Data Selection
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="🔬 Data Type")
        self.setup_data_tab(data_frame)
        
        # Tab 3: Settings
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Settings")
        self.setup_settings_tab(settings_frame)
        
        # Tab 4: Download
        download_frame = ttk.Frame(notebook)
        notebook.add(download_frame, text="🚀 Download")
        self.setup_download_tab(download_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to download geological data")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def setup_area_tab(self, parent):
        """Setup area selection tab."""
        # Region selection
        ttk.Label(parent, text="Select Search Region:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        self.region_var = tk.StringVar(value="Mount Isa Mineral Province")
        region_combo = ttk.Combobox(parent, textvariable=self.region_var, 
                                   values=list(self.predefined_regions.keys()),
                                   state="readonly", width=50)
        region_combo.pack(fill=tk.X, pady=(0, 10))
        region_combo.bind('<<ComboboxSelected>>', self.on_region_change)
        
        # Region description
        self.region_desc_var = tk.StringVar()
        desc_label = ttk.Label(parent, textvariable=self.region_desc_var, 
                              foreground='blue', font=('Arial', 10))
        desc_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Custom coordinates frame
        self.coords_frame = ttk.LabelFrame(parent, text="Custom Coordinates (Latitude, Longitude)")
        self.coords_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Instructions
        instructions = ttk.Label(self.coords_frame, 
                                text="Enter coordinates as: latitude,longitude (e.g., -21.0,139.0)\n" +
                                     "Queensland range: Latitude -29 to -10, Longitude 138 to 154\n" +
                                     "Minimum 3 points required. One coordinate per line.")
        instructions.pack(anchor=tk.W, padx=10, pady=5)
        
        # Coordinates text area
        self.coords_text = scrolledtext.ScrolledText(self.coords_frame, height=8, width=60)
        self.coords_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons frame
        coords_buttons = ttk.Frame(self.coords_frame)
        coords_buttons.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(coords_buttons, text="Load Example", 
                  command=self.load_example_coords).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(coords_buttons, text="Clear", 
                  command=self.clear_coords).pack(side=tk.LEFT, padx=5)
        ttk.Button(coords_buttons, text="Validate", 
                  command=self.validate_coords).pack(side=tk.LEFT, padx=5)
        
        # Initialize region description
        self.on_region_change()
    
    def setup_data_tab(self, parent):
        """Setup data type selection tab."""
        # Data type selection
        ttk.Label(parent, text="Data Type:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        self.data_type_var = tk.StringVar(value="All Data Types (Recommended)")
        data_combo = ttk.Combobox(parent, textvariable=self.data_type_var,
                                 values=list(self.data_types.keys()),
                                 state="readonly", width=50)
        data_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Search terms
        ttk.Label(parent, text="Search Terms:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.search_mode_var = tk.StringVar(value="suggested")
        ttk.Radiobutton(search_frame, text="Use suggested terms", 
                       variable=self.search_mode_var, value="suggested").pack(anchor=tk.W)
        ttk.Radiobutton(search_frame, text="Custom terms:", 
                       variable=self.search_mode_var, value="custom").pack(anchor=tk.W)
        ttk.Radiobutton(search_frame, text="Search everything", 
                       variable=self.search_mode_var, value="all").pack(anchor=tk.W)
        
        self.custom_terms_var = tk.StringVar(value="copper gold mining")
        custom_entry = ttk.Entry(search_frame, textvariable=self.custom_terms_var, width=50)
        custom_entry.pack(fill=tk.X, pady=(5, 0))
        
        # File formats
        ttk.Label(parent, text="File Formats:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        
        self.format_var = tk.StringVar(value="All Formats (Recommended)")
        format_combo = ttk.Combobox(parent, textvariable=self.format_var,
                                   values=list(self.file_formats.keys()),
                                   state="readonly", width=50)
        format_combo.pack(fill=tk.X, pady=(0, 10))
    
    def setup_settings_tab(self, parent):
        """Setup settings tab."""
        # Max datasets
        ttk.Label(parent, text="Maximum Datasets:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        datasets_frame = ttk.Frame(parent)
        datasets_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.max_datasets_var = tk.StringVar(value="20")
        datasets_spinbox = ttk.Spinbox(datasets_frame, from_=1, to=1000, 
                                      textvariable=self.max_datasets_var, width=10)
        datasets_spinbox.pack(side=tk.LEFT)
        
        ttk.Label(datasets_frame, text="(Recommended: 20-50 for testing, up to 1000 for bulk downloads)").pack(side=tk.LEFT, padx=(10, 0))
        
        # Output directory
        ttk.Label(parent, text="Output Directory:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.output_dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "gsq_polygon_data"))
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, width=60)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output_dir).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Precise filtering
        ttk.Label(parent, text="Filtering Options:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        
        self.precise_filtering_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="Use precise polygon filtering (slower but more accurate)",
                       variable=self.precise_filtering_var).pack(anchor=tk.W, pady=(0, 10))
        
        # Preview mode
        self.preview_mode_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(parent, text="Preview mode (search only, don't download files)",
                       variable=self.preview_mode_var).pack(anchor=tk.W, pady=(0, 10))
    
    def setup_download_tab(self, parent):
        """Setup download tab."""
        # Summary frame
        summary_frame = ttk.LabelFrame(parent, text="Download Summary")
        summary_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=8, width=70)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(parent, text="Progress")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.StringVar(value="Ready to start download")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(anchor=tk.W, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.download_button = ttk.Button(buttons_frame, text="🚀 Start Download", 
                                         command=self.start_download, style='Accent.TButton')
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(buttons_frame, text="❌ Cancel", 
                                       command=self.cancel_download, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="📁 Open Output Folder", 
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="📋 Update Summary", 
                  command=self.update_summary).pack(side=tk.LEFT)
        
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Download Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, width=70)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize summary
        self.update_summary()
    
    def on_region_change(self, event=None):
        """Handle region selection change."""
        region_name = self.region_var.get()
        region_info = self.predefined_regions[region_name]
        self.region_desc_var.set(region_info['description'])
        
        # Update coordinates text if not custom
        if region_name != 'Custom Polygon' and region_info['coords']:
            coords_text = '\n'.join([f"{coord[0]},{coord[1]}" for coord in region_info['coords']])
            self.coords_text.delete(1.0, tk.END)
            self.coords_text.insert(1.0, coords_text)
    
    def load_example_coords(self):
        """Load example coordinates."""
        example_coords = [
            [-21.0, 139.0],
            [-21.0, 141.0], 
            [-20.0, 141.0],
            [-20.0, 139.0],
            [-21.0, 139.0]
        ]
        coords_text = '\n'.join([f"{coord[0]},{coord[1]}" for coord in example_coords])
        self.coords_text.delete(1.0, tk.END)
        self.coords_text.insert(1.0, coords_text)
    
    def clear_coords(self):
        """Clear coordinates text."""
        self.coords_text.delete(1.0, tk.END)
    
    def validate_coords(self):
        """Validate entered coordinates."""
        try:
            coords = self.parse_coordinates()
            if len(coords) >= 3:
                messagebox.showinfo("Validation", f"✅ Valid polygon with {len(coords)} vertices")
            else:
                messagebox.showwarning("Validation", "❌ Need at least 3 coordinates for a polygon")
        except Exception as e:
            messagebox.showerror("Validation Error", f"❌ Invalid coordinates: {e}")
    
    def parse_coordinates(self) -> List[List[float]]:
        """Parse coordinates from text area."""
        coords_text = self.coords_text.get(1.0, tk.END).strip()
        if not coords_text:
            raise ValueError("No coordinates entered")
        
        coordinates = []
        for line in coords_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if ',' not in line:
                raise ValueError(f"Invalid format: {line}. Use latitude,longitude")
            
            try:
                lat_str, lon_str = line.split(',')
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())
                
                # Validate Queensland bounds
                if not (-29 <= lat <= -10):
                    raise ValueError(f"Latitude {lat} outside Queensland range (-29 to -10)")
                if not (138 <= lon <= 154):
                    raise ValueError(f"Longitude {lon} outside Queensland range (138 to 154)")
                
                coordinates.append([lat, lon])
            except ValueError as e:
                raise ValueError(f"Error parsing line '{line}': {e}")
        
        if len(coordinates) < 3:
            raise ValueError("Need at least 3 coordinates")
        
        # Close polygon if needed
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
        
        return coordinates
    
    def convert_latlon_to_lonlat(self, latlon_coords: List[List[float]]) -> List[List[float]]:
        """Convert (lat,lon) coordinates to (lon,lat) for API."""
        return [[coord[1], coord[0]] for coord in latlon_coords]
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def update_summary(self):
        """Update download summary."""
        try:
            # Get current settings
            region = self.region_var.get()
            data_type = self.data_type_var.get()
            search_mode = self.search_mode_var.get()
            file_format = self.format_var.get()
            max_datasets = self.max_datasets_var.get()
            output_dir = self.output_dir_var.get()
            precise = self.precise_filtering_var.get()
            preview = self.preview_mode_var.get()
            
            # Build search terms
            if search_mode == "suggested":
                terms = ' OR '.join(self.data_types[data_type]['terms'][:3])
            elif search_mode == "custom":
                custom_terms = self.custom_terms_var.get().strip()
                terms = ' OR '.join(custom_terms.split()) if custom_terms else "No terms"
            else:
                terms = "*:* (everything)"
            
            # Get coordinates info
            try:
                coords = self.parse_coordinates()
                coords_info = f"Valid polygon with {len(coords)-1} vertices"
            except:
                coords_info = "Invalid or missing coordinates"
            
            summary = f"""📋 DOWNLOAD CONFIGURATION
{'='*50}

📍 Search Area: {region}
   Coordinates: {coords_info}

🔬 Data Type: {data_type}
   Search Terms: {terms}
   File Formats: {file_format}

⚙️ Settings:
   Max Datasets: {max_datasets}
   Output Directory: {output_dir}
   Precise Filtering: {'Yes' if precise else 'No'}
   Preview Mode: {'Yes' if preview else 'No'}

Status: {'Ready for preview' if preview else 'Ready for download'}
"""
            
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(1.0, summary)
            
        except Exception as e:
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(1.0, f"Error updating summary: {e}")
    
    def start_download(self):
        """Start the download process."""
        try:
            # Validate inputs
            coords_latlon = self.parse_coordinates()
            coords_lonlat = self.convert_latlon_to_lonlat(coords_latlon)
            
            max_datasets = int(self.max_datasets_var.get())
            output_dir = self.output_dir_var.get()
            
            if not output_dir:
                messagebox.showerror("Error", "Please select an output directory")
                return
            
            # Disable download button, enable cancel
            self.download_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.progress_bar.start()
            
            # Start download in separate thread
            self.download_thread = threading.Thread(
                target=self.download_worker,
                args=(coords_lonlat, max_datasets, output_dir),
                daemon=True
            )
            self.download_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start download: {e}")
            self.reset_download_state()
    
    def download_worker(self, polygon_coords, max_datasets, output_dir):
        """Worker function for download (runs in separate thread)."""
        try:
            # Update status
            self.root.after(0, lambda: self.progress_var.set("Preparing download..."))
            
            # Build search parameters
            data_type_info = self.data_types[self.data_type_var.get()]
            
            # Search terms
            search_mode = self.search_mode_var.get()
            if search_mode == "suggested":
                search_query = ' OR '.join(data_type_info['terms'][:3])
            elif search_mode == "custom":
                custom_terms = self.custom_terms_var.get().strip()
                search_query = ' OR '.join(custom_terms.split()) if custom_terms else '*:*'
            else:
                search_query = '*:*'
            
            # Filters
            filters = []
            if data_type_info['filter']:
                filters.append(data_type_info['filter'])
            filters.append('type:report')
            
            # File formats
            file_formats = self.file_formats[self.format_var.get()]
            
            # Update status
            self.root.after(0, lambda: self.progress_var.set("Searching for datasets..."))
            
            # Preview mode or full download
            if self.preview_mode_var.get():
                # Preview only - search without downloading
                results = self.client.search_datasets_polygon(
                    polygon_coords=polygon_coords,
                    query=search_query,
                    filters=filters,
                    max_results=max_datasets,
                    precise_filtering=self.precise_filtering_var.get()
                )
                
                if results:
                    preview_results = {
                        'success': True,
                        'search_results': results,
                        'total_datasets': len(results['results']),
                        'preview_mode': True
                    }
                    self.root.after(0, lambda: self.download_complete(preview_results))
                else:
                    self.root.after(0, lambda: self.download_error("Search failed"))
            else:
                # Full download
                results = self.client.search_and_download_polygon(
                    polygon_coords=polygon_coords,
                    query=search_query,
                    filters=filters,
                    max_datasets=max_datasets,
                    base_dir=output_dir,
                    resource_formats=file_formats,
                    precise_filtering=self.precise_filtering_var.get()
                )
                
                self.root.after(0, lambda: self.download_complete(results))
                
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))
    
    def download_complete(self, results):
        """Handle download completion."""
        self.reset_download_state()
        
        if not results.get('success'):
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, f"❌ Download failed: {results.get('error', 'Unknown error')}")
            return
        
        # Display results
        if results.get('preview_mode'):
            # Preview results
            datasets = results['search_results']['results']
            result_text = f"🔍 PREVIEW RESULTS\n{'='*50}\n\n"
            result_text += f"Found {len(datasets)} datasets matching your criteria:\n\n"
            
            for i, dataset in enumerate(datasets[:10], 1):  # Show first 10
                title = dataset['title'][:80] + "..." if len(dataset['title']) > 80 else dataset['title']
                result_text += f"{i}. {title}\n"
                result_text += f"   Resources: {len(dataset.get('resources', []))}\n"
                result_text += f"   Type: {dataset.get('type', 'unknown')}\n\n"
            
            if len(datasets) > 10:
                result_text += f"... and {len(datasets) - 10} more datasets\n\n"
            
            result_text += "To download these datasets, disable Preview Mode and run again."
        else:
            # Download results
            result_text = f"✅ DOWNLOAD COMPLETE!\n{'='*50}\n\n"
            result_text += f"📊 Summary:\n"
            result_text += f"   Datasets found: {results['total_datasets']}\n"
            result_text += f"   Resources downloaded: {results['successful_downloads']}/{results['total_resources']}\n"
            result_text += f"   Output directory: {results['download_directory']}\n\n"
            
            # Show sample datasets
            if results['total_datasets'] > 0:
                datasets = results['search_results']['results'][:5]
                result_text += f"📋 Sample datasets downloaded:\n"
                for i, dataset in enumerate(datasets, 1):
                    title = dataset['title'][:60] + "..." if len(dataset['title']) > 60 else dataset['title']
                    result_text += f"   {i}. {title}\n"
                    result_text += f"      Resources: {len(dataset.get('resources', []))}\n"
                
                result_text += f"\n📁 Files saved to: {os.path.abspath(results['download_directory'])}"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, result_text)
        
        self.progress_var.set("Download completed successfully!")
        messagebox.showinfo("Success", "Download completed! Check the Results tab for details.")
    
    def download_error(self, error_msg):
        """Handle download error."""
        self.reset_download_state()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, f"❌ Error: {error_msg}")
        self.progress_var.set(f"Error: {error_msg}")
        messagebox.showerror("Download Error", f"Download failed: {error_msg}")
    
    def cancel_download(self):
        """Cancel the download."""
        if self.download_thread and self.download_thread.is_alive():
            # Note: Python threading doesn't support clean cancellation
            # This is a limitation - the download will continue in background
            messagebox.showwarning("Cancel", "Download cancellation requested. The process may continue in the background.")
        
        self.reset_download_state()
        self.progress_var.set("Download cancelled")
    
    def reset_download_state(self):
        """Reset download UI state."""
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
    
    def open_output_folder(self):
        """Open the output folder in file explorer."""
        output_dir = self.output_dir_var.get()
        if os.path.exists(output_dir):
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                os.system(f"open '{output_dir}'")
            else:
                os.system(f"xdg-open '{output_dir}'")
        else:
            messagebox.showwarning("Folder Not Found", f"Output directory does not exist: {output_dir}")


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    
    # Set up styling
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Create and run the application
    app = GSQDownloaderGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()

