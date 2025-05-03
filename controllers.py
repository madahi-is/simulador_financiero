import tkinter as tk
from tkinter import messagebox
from models import FinancialModels
from views.main_view import MainView
from views.sensitivity import SensitivityAnalysis

from utils import validate_number_input, show_error_message, format_currency
from tkinter import ttk

class FinancialController:
    def __init__(self, root):
        self.root = root
        self.view = MainView(root)
        self._setup_controllers()
        
        # Parámetros del modelo diferencial
        self.diff_params = {
            'c0': 500,    # Consumo autónomo
            'c1': 0.7,    # Propensión marginal a consumir
            'I0': 2061,   # Ingreso inicial (se actualiza)
            'gI': 0.02,   # Tasa de crecimiento del ingreso (2% anual)
            'c2': 0.01    # Efecto del ahorro acumulado en el consumo
        }
        
        # Calcular resultados iniciales
        self.calculate_results()

    def _setup_controllers(self):
        # Conectar botones a métodos
        self.view.controls_frame.calculate_btn.config(command=self.calculate_results)
        #self.view.controls_frame.sensitivity_btn.config(
            #command=self.show_sensitivity_analysis)

    def calculate_results(self):
        try:
            # Obtener valores de la vista
            controls = self.view.controls_frame
            salario = controls.salario_neto.get()
            gasto = controls.gasto_minimo.get()
            tasa = controls.tasa_interes.get() / 100
            inflacion = controls.inflacion.get() / 100
            meses = controls.meses.get()
            modelo = controls.modelo_seleccionado.get()
            
            # Validar entradas
            if not self._validate_inputs(salario, gasto, meses):
                return
            
            # Actualizar parámetros del modelo
            self.diff_params['I0'] = salario
            
            # Calcular ahorro mensual
            ahorro_mensual = salario - gasto
            
            # Calcular según modelo seleccionado
            if modelo == "discreto":
                nominal, real = FinancialModels.discrete_model(
                    meses, ahorro_mensual, tasa, inflacion)
            else:
                nominal = FinancialModels.differential_model(
                    meses, tasa, inflacion, self.diff_params)
                real = [n / ((1 + inflacion/12)**i) for i, n in enumerate(nominal)]
            
            # Mostrar resultados
            self._display_results(ahorro_mensual, nominal, real)
            
            # Calcular escenarios comparativos
            self._calculate_scenarios(ahorro_mensual, meses, inflacion, modelo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def _validate_inputs(self, salario, gasto, meses):
        if gasto >= salario:
            messagebox.showerror("Error", "El gasto no puede ser mayor o igual al salario")
            return False
        
        if meses <= 0:
            messagebox.showerror("Error", "El período debe ser mayor a 0")
            return False
        
        return True

    def _display_results(self, monthly_saving, nominal, real):
        ahorro_nominal = nominal[-1]
        ahorro_real = real[-1]
        perdida = ahorro_nominal - ahorro_real
        
        self.view.results_frame.update_results(
            monthly_saving, ahorro_nominal, ahorro_real, perdida)
        
        self.view.chart_frame.update_chart(len(nominal), nominal, real)

    def _calculate_scenarios(self, monthly_saving, months, inflation, model_type):
        tasas = [0, 3, 5, 7, 10]  # 0%, 3%, 5%, 7%, 10%
        scenarios = []
        
        for tasa in tasas:
            if model_type == "discreto":
                nominal, real = FinancialModels.discrete_model(
                    months, monthly_saving, tasa/100, inflation)
            else:
                nominal = FinancialModels.differential_model(
                    months, tasa/100, inflation, self.diff_params)
                real = [n / ((1 + inflation/12)**i) for i, n in enumerate(nominal)]
            
            scenarios.append((
                f"{tasa}%",
                f"{nominal[-1]:,.2f}",
                f"{real[-1]:,.2f}"
            ))
        
        self.view.results_frame.update_scenarios(scenarios)

    def show_sensitivity_analysis(self):
        controls = self.view.controls_frame
        SensitivityAnalysis(
            self.root,
            salario_neto=controls.salario_neto.get(),
            gasto_minimo=controls.gasto_minimo.get(),
            tasa_interes=controls.tasa_interes.get(),
            inflacion=controls.inflacion.get(),
            meses=controls.meses.get(),
            modelo=controls.modelo_seleccionado.get(),
            diff_params=self.diff_params
        )