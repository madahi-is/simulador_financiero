import tkinter as tk
import matplotlib.pyplot as plt
import sys
from controllers import FinancialController
from views.expense_form import ExpenseForm

def main():
    global root
    root = tk.Tk()
    
    def start_simulation(salary, total_expenses, monthly_saving):
        # Configurar los valores iniciales en el simulador
        app = FinancialController(root)
        app.view.controls_frame.salario_neto.set(salary)
        app.view.controls_frame.gasto_minimo.set(total_expenses)
        app.calculate_results()
        
        def on_closing():
            try:
                if hasattr(app.view.chart_frame, 'canvas'):
                    app.view.chart_frame.canvas.get_tk_widget().destroy()
                plt.close('all')
                root.destroy()
                sys.exit()
            except Exception as e:
                print(f"Error al cerrar la aplicación: {e}")
                root.destroy()
                sys.exit(1)

        root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Mostrar primero el formulario de gastos
    ExpenseForm(root, start_simulation)

    root.mainloop()

if __name__ == "__main__":
    main()