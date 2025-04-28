import tkinter as tk
from tkinter import ttk, messagebox

def validate_number_input(value, min_val=None, max_val=None):
    """Valida que un valor sea numérico y esté dentro de un rango"""
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False

def show_error_message(parent, title, message):
    """Muestra un mensaje de error estandarizado"""
    messagebox.showerror(title, message, parent=parent)

def format_currency(value):
    """Formatea un valor numérico como moneda"""
    return f"Bs. {value:,.2f}"

def setup_styles():
    """Configura los estilos globales de la aplicación"""
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10))
    style.configure('TEntry', font=('Arial', 10))
    style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
    style.configure('Result.TLabel', font=('Arial', 10, 'bold'))
    return style