import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self._create_widgets()
        self._setup_chart()

    def _create_widgets(self):
        ttk.Label(self, text="GRÁFICO DE AHORRO", style="Title.TLabel").grid(
            row=0, column=0, pady=5)

    def _setup_chart(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.ax.set_title("Evolución del Ahorro")
        self.ax.set_xlabel("Meses")
        self.ax.set_ylabel("Ahorro Acumulado (Bs.)")
        self.ax.grid(True)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_chart(self, months, nominal, real):
        self.ax.clear()
        
        months_range = range(1, months + 1)
        self.ax.plot(months_range, nominal, 'b-', label='Nominal')
        self.ax.plot(months_range, real, 'r--', label='Real (ajustado por inflación)')
        
        self.ax.set_title("Evolución del Ahorro")
        self.ax.set_xlabel("Meses")
        self.ax.set_ylabel("Ahorro Acumulado (Bs.)")
        self.ax.legend()
        self.ax.grid(True)
        
        self.canvas.draw()