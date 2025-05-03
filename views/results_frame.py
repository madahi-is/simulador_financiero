import tkinter as tk
from tkinter import ttk

class ResultsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="5")
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self, text="RESULTADOS", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=2)
        
        # Resultados principales
        self._create_result_label("Ahorro Mensual:", 1)
        self._create_result_label("Ahorro Total Nominal:", 2)
        self._create_result_label("Ahorro Total Real:", 3)
        self._create_result_label("Pérdida por Inflación:", 4)
        
        # Tabla de escenarios
        ttk.Label(self, text="Escenarios Comparativos", style="Title.TLabel").grid(
            row=5, column=0, columnspan=2, pady=10)
        
        self.scenarios_table = ttk.Treeview(
            self, columns=('Tasa', 'Nominal', 'Real'), show='headings', height=4)
        self.scenarios_table.heading('Tasa', text='Tasa %')
        self.scenarios_table.heading('Nominal', text='Nominal (Bs.)')
        self.scenarios_table.heading('Real', text='Real (Bs.)')
        self.scenarios_table.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Configurar expansión
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _create_result_label(self, text, row):
        ttk.Label(self, text=text).grid(row=row, column=0, sticky="w", pady=2)
        label = ttk.Label(self, text="", style="Result.TLabel")
        label.grid(row=row, column=1, sticky="w", pady=2)
        setattr(self, f"result_label_{row}", label)

    def update_results(self, monthly_saving, nominal, real, inflation_loss):
        self.result_label_1.config(text=f"Bs. {monthly_saving:,.2f}")
        self.result_label_2.config(text=f"Bs. {nominal:,.2f}")
        self.result_label_3.config(text=f"Bs. {real:,.2f}")
        self.result_label_4.config(
            text=f"Bs. {inflation_loss:,.2f} ({inflation_loss/nominal*100:.1f}%)")

    def update_scenarios(self, scenarios):
        self.scenarios_table.delete(*self.scenarios_table.get_children())
        for scenario in scenarios:
            self.scenarios_table.insert('', 'end', values=scenario)