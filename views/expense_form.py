import tkinter as tk
from tkinter import ttk, messagebox

class ExpenseForm(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Registro de Gastos Mensuales")
        self.geometry("800x600")
        self.callback = callback
        
        self.categories = {
            "Vivienda": ["Vivienda compartida", "Servicios (agua, luz, gas, internet básico)", "Mantenimiento"],
            "Alimentación": ["Comida en casa (supermercado, mercado)", "Comida fuera (almuerzo ocasional, salidas)"],
            "Transporte": ["Transporte público: micros, buses", "Taxi/Uber ocasional"],
            "Educación/Desarrollo": ["Cursos, libros, materiales de estudio"],
            "Salud": ["Seguro de salud", "Gastos médicos ocasionales"],
            "Entretenimiento/Ocio": ["Salidas (cine, eventos)", "Suscripciones (streaming)"],
            "Vestimenta/Cuidado Personal": ["Ropa, calzado", "Productos de higiene"],
            "Comunicación": ["Recarga de celular", "Plan de datos"],
            "Deudas/Préstamos": ["Cuotas de préstamos"],
            "Otros Gastos": ["Imprevistos", "Regalos"]
        }
        
        self._create_widgets()
        
    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para ingresar salario
        salary_frame = ttk.LabelFrame(main_frame, text="Ingresos", padding="10")
        salary_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(salary_frame, text="Salario Neto Mensual (Bs.):").pack(side=tk.LEFT)
        self.salary_entry = ttk.Entry(salary_frame)
        self.salary_entry.pack(side=tk.LEFT, padx=10)
        
        # Frame para gastos
        expenses_frame = ttk.LabelFrame(main_frame, text="Gastos Mensuales", padding="10")
        expenses_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(expenses_frame)
        scrollbar = ttk.Scrollbar(expenses_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear campos para cada categoría
        self.expense_entries = {}
        row = 0
        for category, subcategories in self.categories.items():
            ttk.Label(scrollable_frame, text=category, style="Title.TLabel").grid(
                row=row, column=0, sticky="w", pady=(10, 2))
            row += 1
            
            for subcat in subcategories:
                ttk.Label(scrollable_frame, text=subcat).grid(
                    row=row, column=0, sticky="w", padx=20)
                entry = ttk.Entry(scrollable_frame)
                entry.grid(row=row, column=1, pady=2)
                self.expense_entries[subcat] = entry
                row += 1
        
        # Botón de calcular
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Calcular Ahorro", command=self._calculate_saving).pack()
    
    def _calculate_saving(self):
        try:
            # Obtener salario
            salary = float(self.salary_entry.get())
            
            # Calcular total de gastos
            total_expenses = 0
            for subcat, entry in self.expense_entries.items():
                value = entry.get()
                if value:
                    total_expenses += float(value)
            
            # Calcular ahorro
            monthly_saving = salary - total_expenses
            
            if monthly_saving > 0:
                self.callback(salary, total_expenses, monthly_saving)
                self.destroy()
            else:
                advice = """Para lograr un ahorro inicial, el joven necesitaría:
1. Reducir sus gastos: Analizar cada categoría de gasto y buscar formas de disminuir
los costos, acercándose más a los valores mínimos o encontrando alternativas más
económicas.
2. Aumentar sus ingresos: Explorar oportunidades para obtener ingresos adicionales
como trabajos a tiempo parcial, freelancing e incluso explorara otras oportunidades.
¿Qué otras oportunidades considera viables?"""
                
                messagebox.showwarning(
                    "Ahorro Negativo", 
                    f"Su gasto mensual excede su salario en Bs. {-monthly_saving:.2f}\n\n{advice}"
                )
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos en todos los campos")