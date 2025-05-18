import tkinter as tk
from tkinter import ttk, messagebox
import db_operations
import plot_operations
import weather_processor
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Scrapy @ Raghav Sharma")
        self.root.geometry("700x700")
        
        # Initialize database connection
        self.db = db_operations.DBOperations()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create welcome section
        self.create_welcome_section()
        
        # Create data section
        self.create_data_section()
        
        # Create plots section
        self.create_plots_section()
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="Ready")
        self.status_label.grid(row=3, column=0, pady=10)
        
    def create_welcome_section(self):
        welcome_frame = ttk.LabelFrame(self.main_frame, text="Welcome", padding="10")
        welcome_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        welcome_label = ttk.Label(welcome_frame, 
                                text="Weather Scrapy - Raghav sharma",
                                font=("Arial", 16, "bold"))
        welcome_label.pack(pady=5)
        
        description = ttk.Label(welcome_frame,
                              text="View weather data and generate visualizations ")
        description.pack(pady=5)
        
        # Add scrape button
        # ttk.Button(welcome_frame, 
        #           text="Scrape New Weather Data",
        #           command=self.scrape_weather).pack(pady=5)
        
    def create_data_section(self):
        data_frame = ttk.LabelFrame(self.main_frame, text="Weather Data", padding="10")
        data_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Date range selection
        date_frame = ttk.Frame(data_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(date_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        self.start_date_entry = ttk.Entry(date_frame)
        self.start_date_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(date_frame, text="End Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self.end_date_entry = ttk.Entry(date_frame)
        self.end_date_entry.grid(row=0, column=3, padx=5)
        
        ttk.Button(date_frame, text="Load Data", command=self.load_data).grid(row=0, column=4, padx=5)
        
        # Create Treeview
        columns = ("Date", "Location", "Min Temp", "Max Temp", "Avg Temp")
        self.tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def create_plots_section(self):
        plots_frame = ttk.LabelFrame(self.main_frame, text="Visualizations", padding="10")
        plots_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Plot type selection
        plot_type_frame = ttk.Frame(plots_frame)
        plot_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(plot_type_frame, text="Plot Type:").grid(row=0, column=0, padx=5)
        self.plot_type = tk.StringVar(value="boxplot")
        ttk.Radiobutton(plot_type_frame, text="Year-to-Year Boxplot", variable=self.plot_type, 
                       value="boxplot", command=self.update_plot_inputs).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(plot_type_frame, text="Monthly Line Plot", variable=self.plot_type, 
                       value="lineplot", command=self.update_plot_inputs).grid(row=0, column=2, padx=5)
        
        # Input frame for plot parameters
        self.input_frame = ttk.Frame(plots_frame)
        self.input_frame.pack(fill=tk.X, pady=5)
        
        # Boxplot inputs
        self.boxplot_frame = ttk.Frame(self.input_frame)
        ttk.Label(self.boxplot_frame, text="Start Year:").grid(row=0, column=0, padx=5)
        self.start_year_entry = ttk.Entry(self.boxplot_frame, width=10)
        self.start_year_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(self.boxplot_frame, text="End Year:").grid(row=0, column=2, padx=5)
        self.end_year_entry = ttk.Entry(self.boxplot_frame, width=10)
        self.end_year_entry.grid(row=0, column=3, padx=5)
        
        # Line plot inputs
        self.lineplot_frame = ttk.Frame(self.input_frame)
        ttk.Label(self.lineplot_frame, text="Year:").grid(row=0, column=0, padx=5)
        self.year_entry = ttk.Entry(self.lineplot_frame, width=10)
        self.year_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(self.lineplot_frame, text="Month:").grid(row=0, column=2, padx=5)
        self.month_entry = ttk.Entry(self.lineplot_frame, width=10)
        self.month_entry.grid(row=0, column=3, padx=5)
        
        # Generate button
        ttk.Button(plots_frame, text="Generate Plot", command=self.generate_plot).pack(pady=5)
        
        # Plot display area
        self.plot_frame = ttk.Frame(plots_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Show initial input frame
        self.update_plot_inputs()
        
    def update_plot_inputs(self):
        # Hide all input frames
        self.boxplot_frame.pack_forget()
        self.lineplot_frame.pack_forget()
        
        # Show the appropriate input frame
        if self.plot_type.get() == "boxplot":
            self.boxplot_frame.pack(fill=tk.X, pady=5)
        else:
            self.lineplot_frame.pack(fill=tk.X, pady=5)
    
    def load_data(self):
        try:
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Fetch data
            data = self.db.fetch_data(start_date, end_date)
            
            # Insert data into treeview
            for record in data:
                self.tree.insert("", tk.END, values=(
                    record[1],  # date
                    record[2],  # location
                    f"{record[3]:.1f}" if record[3] is not None else "N/A",  # min temp
                    f"{record[4]:.1f}" if record[4] is not None else "N/A",  # max temp
                    f"{record[5]:.1f}" if record[5] is not None else "N/A"   # avg temp
                ))
            
            self.status_label.config(text=f"Loaded {len(data)} records")
        except Exception as e:
            self.status_label.config(text="Error loading data")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def generate_plot(self):
        try:
            # Clear previous plot
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            
            plot_type = self.plot_type.get()
            data = self.db.fetch_data()
            
            if not data:
                messagebox.showwarning("Warning", "No data available to plot")
                return
            
            plot_ops = plot_operations.PlotOperations(data)
            
            if plot_type == "boxplot":
                start_year = int(self.start_year_entry.get())
                end_year = int(self.end_year_entry.get())
                plot_ops.generate_year_to_year_boxplot(start_year, end_year)
            else:  # lineplot
                year = int(self.year_entry.get())
                month = int(self.month_entry.get())
                plot_ops.generate_lineplot(year, month)
            
            # Embed the plot in the UI
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_label.config(text="Plot generated successfully")
        except Exception as e:
            self.status_label.config(text="Error generating plot")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def scrape_weather(self):
        try:
            self.status_label.config(text="Scraping weather data...")
            from scrape_weather import main as scrape_main
            scrape_main()
            self.status_label.config(text="Weather data scraped successfully!")
            messagebox.showinfo("Success", "Weather data has been scraped successfully!")
        except Exception as e:
            self.status_label.config(text="Error during scraping")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop() 