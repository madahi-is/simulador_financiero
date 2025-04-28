import numpy as np
from scipy.integrate import odeint

class FinancialModels:
    @staticmethod
    def discrete_model(months, monthly_saving, annual_interest, annual_inflation=0):
        """Modelo de ahorro discreto con interés compuesto"""
        monthly_interest = annual_interest / 12
        monthly_inflation = annual_inflation / 12
        accumulated = 0
        nominal_history = []
        real_history = []
        
        for month in range(1, months + 1):
            accumulated = accumulated * (1 + monthly_interest) + monthly_saving
            nominal_history.append(accumulated)
            real_value = accumulated / ((1 + monthly_inflation) ** month)
            real_history.append(real_value)
            
        return nominal_history, real_history

    @staticmethod
    def differential_model(months, annual_interest, annual_inflation, params):
        """Modelo diferencial de ahorro-consumo"""
        t = np.linspace(0, months, months)
        r = annual_interest / 12
        inflation_monthly = annual_inflation / 12
        
        sol = odeint(FinancialModels._diff_equation, 0, t, 
                    args=(r, params['c0'], params['c1'], params['I0'], 
                          params['gI']/12, params['c2'], inflation_monthly))
        return sol.flatten()

    @staticmethod
    def _diff_equation(A, t, r, c0, c1, I0, gI, c2, inflation):
        """Ecuación diferencial para el modelo continuo"""
        I = I0 * np.exp(gI * t)
        dAdt = (1 - c1) * I - c0 + (c2 + r - inflation) * A
        return dAdt