"""
Panel de entrada de datos para la aplicación de programación lineal.
Contiene los controles para ingresar función objetivo y restricciones.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Optional

from core.models import (
    LinearProgrammingProblem, ObjectiveFunction, Constraint,
    OptimizationType, InequalityType
)


class ConstraintEntry:
    """Representa una entrada de restricción en la interfaz"""
    
    def __init__(self, parent_frame: ttk.Frame, 
                 on_delete_callback: Callable, 
                 a1: str = "0", a2: str = "0", 
                 inequality: str = "≤", b: str = "0"):
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill=tk.X, pady=2)
        self.on_delete_callback = on_delete_callback
        
        # Variables para los campos
        self.a1_var = tk.StringVar(value=a1)
        self.a2_var = tk.StringVar(value=a2)
        self.inequality_var = tk.StringVar(value=inequality)
        self.b_var = tk.StringVar(value=b)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario para esta restricción"""
        # Coeficiente de X1
        ttk.Entry(self.frame, textvariable=self.a1_var, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(self.frame, text="*X₁ + ").pack(side=tk.LEFT)
        
        # Coeficiente de X2
        ttk.Entry(self.frame, textvariable=self.a2_var, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(self.frame, text="*X₂ ").pack(side=tk.LEFT)
        
        # Tipo de desigualdad
        inequality_combo = ttk.Combobox(self.frame, textvariable=self.inequality_var,
                                       values=["≤", "≥", "="], state="readonly", width=5)
        inequality_combo.pack(side=tk.LEFT, padx=2)
        
        # Término independiente
        ttk.Entry(self.frame, textvariable=self.b_var, width=8).pack(side=tk.LEFT, padx=2)
        
        # Botón eliminar
        delete_btn = ttk.Button(self.frame, text="✕", width=3,
                               command=lambda: self.on_delete_callback(self))
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def get_constraint(self) -> Constraint:
        """
        Obtiene el objeto Constraint a partir de los valores ingresados.
        
        Returns:
            Constraint: Restricción creada
            
        Raises:
            ValueError: Si los valores no son válidos
        """
        try:
            a1 = float(self.a1_var.get())
            a2 = float(self.a2_var.get())
            b = float(self.b_var.get())
            
            # Mapear símbolo a enum
            inequality_map = {
                "≤": InequalityType.MENOR_IGUAL,
                "≥": InequalityType.MAYOR_IGUAL,
                "=": InequalityType.IGUAL
            }
            
            inequality_type = inequality_map[self.inequality_var.get()]
            
            return Constraint(a1, a2, inequality_type, b)
            
        except ValueError as e:
            raise ValueError(f"Error en restricción: {str(e)}")
    
    def destroy(self):
        """Elimina esta entrada de restricción"""
        self.frame.destroy()


class InputPanel:
    """Panel principal de entrada de datos"""
    
    def __init__(self, parent: tk.Widget, on_solve_callback: Callable):
        self.parent = parent
        self.on_solve_callback = on_solve_callback
        self.constraint_entries: List[ConstraintEntry] = []
        
        # Variables para la función objetivo
        self.optimization_var = tk.StringVar(value="maximizar")
        self.c1_var = tk.StringVar(value="250")
        self.c2_var = tk.StringVar(value="300")
        
        self._setup_ui()
        self._add_default_constraints()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario del panel"""
        # Frame principal del panel
        self.frame = ttk.LabelFrame(self.parent, text="Datos del Problema", padding=10)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Sección de función objetivo
        self._setup_objective_function_section()
        
        # Sección de restricciones  
        self._setup_constraints_section()
        
        # Botón resolver
        self._setup_solve_button()
    
    def _setup_objective_function_section(self):
        """Configura la sección de función objetivo"""
        obj_frame = ttk.LabelFrame(self.frame, text="Función Objetivo", padding=5)
        obj_frame.pack(fill=tk.X, pady=5)
        
        # Tipo de optimización
        ttk.Label(obj_frame, text="Tipo:").pack(anchor=tk.W)
        opt_combo = ttk.Combobox(obj_frame, textvariable=self.optimization_var,
                                values=["maximizar", "minimizar"], state="readonly", width=15)
        opt_combo.pack(anchor=tk.W, pady=2)
        
        # Coeficientes de la función objetivo
        coef_frame = ttk.Frame(obj_frame)
        coef_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(coef_frame, text="Z = ").pack(side=tk.LEFT)
        ttk.Entry(coef_frame, textvariable=self.c1_var, width=8).pack(side=tk.LEFT)
        ttk.Label(coef_frame, text="*X₁ + ").pack(side=tk.LEFT)
        ttk.Entry(coef_frame, textvariable=self.c2_var, width=8).pack(side=tk.LEFT)
        ttk.Label(coef_frame, text="*X₂").pack(side=tk.LEFT)
    
    def _setup_constraints_section(self):
        """Configura la sección de restricciones"""
        rest_frame = ttk.LabelFrame(self.frame, text="Restricciones", padding=5)
        rest_frame.pack(fill=tk.X, pady=5)
        
        # Frame para lista de restricciones
        self.constraints_list_frame = ttk.Frame(rest_frame)
        self.constraints_list_frame.pack(fill=tk.X, pady=5)
        
        # Botones para manejo de restricciones
        btn_frame = ttk.Frame(rest_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Agregar Restricción",
                  command=self.add_constraint).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Limpiar Todo",
                  command=self.clear_all_constraints).pack(side=tk.LEFT, padx=2)
    
    def _setup_solve_button(self):
        """Configura el botón de resolver"""
        solve_btn = ttk.Button(self.frame, text="RESOLVER PROBLEMA",
                              command=self._on_solve_clicked,
                              style="Accent.TButton")
        solve_btn.pack(pady=20, fill=tk.X)
    
    def _add_default_constraints(self):
        """Agrega las restricciones por defecto del ejemplo"""
        # Restricción de desarrollo: 20*X1 + 15*X2 <= 600
        self.add_constraint("20", "15", "≤", "600")
        # Restricción de pruebas: 10*X1 + 15*X2 <= 450
        self.add_constraint("10", "15", "≤", "450")
    
    def add_constraint(self, a1: str = "0", a2: str = "0", 
                      inequality: str = "≤", b: str = "0"):
        """
        Agrega una nueva restricción al panel.
        
        Args:
            a1: Coeficiente de X1
            a2: Coeficiente de X2 
            inequality: Tipo de desigualdad
            b: Término independiente
        """
        constraint_entry = ConstraintEntry(
            self.constraints_list_frame,
            self._delete_constraint_callback,
            a1, a2, inequality, b
        )
        self.constraint_entries.append(constraint_entry)
    
    def _delete_constraint_callback(self, constraint_entry: ConstraintEntry):
        """
        Callback para eliminar una restricción.
        
        Args:
            constraint_entry: Entrada de restricción a eliminar
        """
        if constraint_entry in self.constraint_entries:
            self.constraint_entries.remove(constraint_entry)
            constraint_entry.destroy()
    
    def clear_all_constraints(self):
        """Elimina todas las restricciones"""
        for entry in self.constraint_entries[:]:  # Crear copia para iterar
            self._delete_constraint_callback(entry)
    
    def get_problem(self) -> LinearProgrammingProblem:
        """
        Construye y retorna el problema de programación lineal a partir de los datos ingresados.
        
        Returns:
            LinearProgrammingProblem: Problema construido
            
        Raises:
            ValueError: Si hay errores en los datos ingresados
        """
        try:
            # Crear función objetivo
            c1 = float(self.c1_var.get())
            c2 = float(self.c2_var.get())
            
            opt_type = (OptimizationType.MAXIMIZAR 
                       if self.optimization_var.get() == "maximizar" 
                       else OptimizationType.MINIMIZAR)
            
            objective_function = ObjectiveFunction(c1, c2, opt_type)
            
            # Crear restricciones
            constraints = []
            for i, entry in enumerate(self.constraint_entries):
                try:
                    constraint = entry.get_constraint()
                    constraints.append(constraint)
                except ValueError as e:
                    raise ValueError(f"Error en restricción {i+1}: {str(e)}")
            
            if not constraints:
                raise ValueError("Debe ingresar al menos una restricción")
            
            return LinearProgrammingProblem(objective_function, constraints)
            
        except ValueError as e:
            raise ValueError(f"Error en los datos: {str(e)}")
    
    def _on_solve_clicked(self):
        """Maneja el evento de clic en el botón resolver"""
        try:
            problem = self.get_problem()
            self.on_solve_callback(problem)
        except ValueError as e:
            messagebox.showerror("Error en los datos", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def load_startup_example(self):
        """Carga el ejemplo de la startup de software"""
        # Limpiar restricciones existentes
        self.clear_all_constraints()
        
        # Configurar función objetivo
        self.optimization_var.set("maximizar")
        self.c1_var.set("250")
        self.c2_var.set("300")
        
        # Agregar restricciones del ejemplo
        self.add_constraint("20", "15", "≤", "600")  # Desarrollo
        self.add_constraint("10", "15", "≤", "450")  # Pruebas
    
    def validate_numeric_input(self, value: str) -> bool:
        """
        Valida que una entrada sea un número válido.
        
        Args:
            value: Valor a validar
            
        Returns:
            bool: True si es válido
        """
        if value == "" or value == "-":
            return True  # Permitir campos vacíos y signo negativo
        try:
            float(value)
            return True
        except ValueError:
            return False
