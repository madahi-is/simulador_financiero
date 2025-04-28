"""
Paquete que contiene todas las vistas de la aplicación financiera
"""

from .main_view import MainView
from .controls_frame import ControlsFrame
from .chart_frame import ChartFrame
from .results_frame import ResultsFrame
from .sensitivity import SensitivityAnalysis

__all__ = [
    'MainView',
    'ControlsFrame',
    'ChartFrame',
    'ResultsFrame',
    'SensitivityAnalysis'
]