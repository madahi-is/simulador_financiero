import tkinter as tk
from tkinter import ttk
from views.controls_frame import ControlsFrame
from views.chart_frame import ChartFrame
from views.results_frame import ResultsFrame

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Salud Financiera Juvenil")
        self.root.geometry("1000x700")
        self._setup_style()
        self._create_widgets()

    def _setup_style(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Result.TLabel', font=('Arial', 10, 'bold'))

    def _create_widgets(self):
        # Crear frames principales
        self.controls_frame = ControlsFrame(self.root)
        self.controls_frame.grid(row=0, column=0, sticky="nsew",padx=80 , pady=(0, 5))
        
        self.chart_frame = ChartFrame(self.root)
        self.chart_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        
        self.results_frame = ResultsFrame(self.root)
        self.results_frame.grid(row=1, column=0, sticky="nsew" ,pady=0)
        
        # Configurar pesos de grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)