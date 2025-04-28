import tkinter as tk
from controllers import FinancialController

def main():
    root = tk.Tk()
    app = FinancialController(root)

    # Esta línea asegura que cuando cierres la ventana, también cierres el proceso
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()

if __name__ == "__main__":
    main()