import tkinter as tk
from tkinter import messagebox

class GastoForm:
    def __init__(self, master, on_ahorro_positivo):
        self.top = tk.Toplevel(master)
        self.top.title("Formulario de Gasto")

        self.on_ahorro_positivo = on_ahorro_positivo

        tk.Label(self.top, text="Salario neto mensual:").grid(row=0, column=0)
        self.salario_entry = tk.Entry(self.top)
        self.salario_entry.grid(row=0, column=1)

        tk.Label(self.top, text="Gasto mensual mínimo:").grid(row=1, column=0)
        self.gasto_entry = tk.Entry(self.top)
        self.gasto_entry.grid(row=1, column=1)

        tk.Button(self.top, text="Iniciar Simulación", command=self.procesar_datos).grid(row=2, columnspan=2, pady=10)

    def procesar_datos(self):
        try:
            salario = float(self.salario_entry.get())
            gasto = float(self.gasto_entry.get())

            if gasto >= salario:
                messagebox.showerror("Error", "El gasto no puede ser mayor o igual al salario")
            else:
                self.top.destroy()
                self.on_ahorro_positivo()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos")
            print("Datos inválidos.")
