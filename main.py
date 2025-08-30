#!/usr/bin/env python3
"""
Aplicación de Programación Lineal - Solver Gráfico de 2 Variables

Punto de entrada principal de la aplicación modular.
"""

import sys
import os

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal de la aplicación"""
    try:
        # Importar y ejecutar la aplicación principal
        from gui.main_window import MainWindow
        
        # Crear y ejecutar la ventana principal
        app = MainWindow()
        app.run()
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas:")
        print("pip install matplotlib numpy sympy")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
