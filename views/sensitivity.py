import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import FinancialModels

class SensitivityAnalysis:
    def __init__(self, parent, salario_neto, gasto_minimo, tasa_interes, 
                 inflacion, meses, modelo, diff_params):
        self.top = tk.Toplevel(parent)
        self.top.title("Análisis de Sensibilidad")
        self.top.geometry("800x600")
        
        self.salario_neto = salario_neto
        self.gasto_minimo = gasto_minimo
        self.tasa_interes = tasa_interes
        self.inflacion = inflacion
        self.meses = meses
        self.modelo = modelo
        self.diff_params = diff_params
        
        self._create_widgets()

    def _create_widgets(self):
        # Variables
        self.parametro = tk.StringVar(value="tasa_interes")
        self.num_puntos = tk.IntVar(value=10)
        
        # Frame de controles
        frame_controles = ttk.Frame(self.top, padding="10")
        frame_controles.pack(fill="x")
        
        ttk.Label(frame_controles, text="Parámetro a analizar:").grid(
            row=0, column=0, padx=5, pady=5)
        ttk.Combobox(frame_controles, textvariable=self.parametro, 
                    values=["tasa_interes", "inflacion", "salario_neto", "gasto_minimo"]).grid(
                        row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_controles, text="Número de puntos:").grid(
            row=1, column=0, padx=5, pady=5)
        ttk.Spinbox(frame_controles, from_=5, to=20, textvariable=self.num_puntos).grid(
            row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame_controles, text="Generar Análisis", 
                  command=self._generate_analysis).grid(
                      row=2, column=0, columnspan=2, pady=10)
        
        # Frame del gráfico
        self.frame_grafico = ttk.Frame(self.top)
        self.frame_grafico.pack(fill="both", expand=True)

    def _generate_analysis(self):
        parametro = self.parametro.get()
        num_puntos = self.num_puntos.get()
        
        # Configurar rango según parámetro
        if parametro == "tasa_interes":
            valores = np.linspace(0, 0.10, num_puntos)  # De 0% a 10%
            titulo = "Sensibilidad a Tasa de Interés"
            xlabel = "Tasa de Interés Anual"
        elif parametro == "inflacion":
            valores = np.linspace(0, 0.15, num_puntos)  # De 0% a 15%
            titulo = "Sensibilidad a Inflación"
            xlabel = "Tasa de Inflación Anual"
        elif parametro == "salario_neto":
            valores = np.linspace(1500, 3000, num_puntos)  # De 1500 a 3000 Bs.
            titulo = "Sensibilidad a Salario Neto"
            xlabel = "Salario Neto Mensual (Bs.)"
        else:  # gasto_minimo
            valores = np.linspace(1500, 2500, num_puntos)  # De 1500 a 2500 Bs.
            titulo = "Sensibilidad a Gasto Mínimo"
            xlabel = "Gasto Mínimo Mensual (Bs.)"
        
        # Calcular resultados
        resultados = []
        for valor in valores:
            if parametro == "tasa_interes":
                if self.modelo == "discreto":
                    nominal, _ = FinancialModels.discrete_model(
                        self.meses, self.salario_neto - self.gasto_minimo, valor)
                else:
                    nominal = FinancialModels.differential_model(
                        self.meses, valor, self.inflacion/100, self.diff_params)
            elif parametro == "inflacion":
                if self.modelo == "discreto":
                    nominal, _ = FinancialModels.discrete_model(
                        self.meses, self.salario_neto - self.gasto_minimo, 
                        self.tasa_interes/100, valor)
                else:
                    nominal = FinancialModels.differential_model(
                        self.meses, self.tasa_interes/100, valor, self.diff_params)
            elif parametro == "salario_neto":
                ahorro_mensual = valor - self.gasto_minimo
                if self.modelo == "discreto":
                    nominal, _ = FinancialModels.discrete_model(
                        self.meses, ahorro_mensual, self.tasa_interes/100, self.inflacion/100)
                else:
                    self.diff_params['I0'] = valor
                    nominal = FinancialModels.differential_model(
                        self.meses, self.tasa_interes/100, self.inflacion/100, self.diff_params)
            else:  # gasto_minimo
                ahorro_mensual = self.salario_neto - valor
                if self.modelo == "discreto":
                    nominal, _ = FinancialModels.discrete_model(
                        self.meses, ahorro_mensual, self.tasa_interes/100, self.inflacion/100)
                else:
                    nominal = FinancialModels.differential_model(
                        self.meses, self.tasa_interes/100, self.inflacion/100, self.diff_params)
            
            resultados.append((valor, nominal[-1]))
        
        valores_param, valores_ahorro = zip(*resultados)
        
        # Mostrar gráfico
        self._show_chart(valores_param, valores_ahorro, titulo, xlabel)

    def _show_chart(self, x_values, y_values, title, xlabel):
        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        
        # Crear nuevo gráfico
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_values, y_values, 'b-o')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Ahorro Acumulado Final (Bs.)")
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)