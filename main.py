import tkinter as tk
import matplotlib.pyplot as plt
import sys
from controllers import FinancialController


def main():
    global root
    root = tk.Tk()
    root.title("Simulador Financiero")
    app = FinancialController(root)

    def on_closing():
        try:
            # Destruir explícitamente el widget del gráfico si existe
            if hasattr(app.view.chart_frame, 'canvas'):
                app.view.chart_frame.canvas.get_tk_widget().destroy()
            
            plt.close('all')  # Cierra cualquier figura abierta de matplotlib
            root.destroy()
            sys.exit()
        except Exception as e:
            print(f"Error al cerrar la aplicación: {e}")
            root.destroy()
            sys.exit(1)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
