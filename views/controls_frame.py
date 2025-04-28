import tkinter as tk
from tkinter import ttk

class ControlsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self, text="CONTROLES", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=5)
        
        # Variables de control
        self.salario_neto = tk.DoubleVar(value=2061)
        self.gasto_minimo = tk.DoubleVar(value=1900)
        self.tasa_interes = tk.DoubleVar(value=3)
        self.inflacion = tk.DoubleVar(value=5)
        self.meses = tk.IntVar(value=120)
        self.modelo_seleccionado = tk.StringVar(value="discreto")
        
        # Controles de entrada
        self._create_input_field("Salario Neto Mensual (Bs.):", self.salario_neto, 1)
        self._create_input_field("Gasto Mínimo Mensual (Bs.):", self.gasto_minimo, 2)
        self._create_input_field("Tasa de Interés Anual (%):", self.tasa_interes, 3)
        self._create_input_field("Inflación Anual (%):", self.inflacion, 4)
        self._create_input_field("Período (meses):", self.meses, 5)
        
        # Selector de modelo
        ttk.Label(self, text="Modelo:").grid(row=6, column=0, sticky="w", pady=2)
        ttk.Radiobutton(self, text="Discreto", variable=self.modelo_seleccionado, 
                       value="discreto").grid(row=6, column=1, sticky="w", pady=2)
        ttk.Radiobutton(self, text="Diferencial", variable=self.modelo_seleccionado, 
                       value="diferencial").grid(row=7, column=1, sticky="w", pady=2)
        
        # Botones
        self.calculate_btn = ttk.Button(self, text="Calcular")
        self.calculate_btn.grid(row=8, column=0, columnspan=2, pady=10)
        
        self.sensitivity_btn = ttk.Button(self, text="Análisis de Sensibilidad")
        self.sensitivity_btn.grid(row=9, column=0, columnspan=2, pady=5)

    def _create_input_field(self, label_text, variable, row):
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(self, textvariable=variable).grid(row=row, column=1, pady=2)