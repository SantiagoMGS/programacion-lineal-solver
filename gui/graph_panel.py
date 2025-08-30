"""
Panel de graficación para la aplicación de programación lineal.
Contiene el gráfico de la región factible y los resultados.
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Optional

from core.models import Solution, InequalityType
from core.solver import LinearProgrammingSolver


class GraphPanel:
    """Panel para mostrar el gráfico y resultados de la solución"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.current_solution: Optional[Solution] = None
        self.solver = LinearProgrammingSolver()
        
        # Configuración de colores para las restricciones
        self.constraint_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario del panel"""
        # Frame principal del panel
        self.frame = ttk.LabelFrame(self.parent, text="Gráfico y Resultados", padding=10)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Configurar gráfico
        self._setup_matplotlib()
        
        # Configurar área de resultados
        self._setup_results_area()
    
    def _setup_matplotlib(self):
        """Configura el widget de matplotlib"""
        # Crear figura
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.patch.set_facecolor('white')
        
        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar gráfico inicial
        self._setup_initial_plot()
    
    def _setup_initial_plot(self):
        """Configura el gráfico inicial vacío"""
        self.ax.clear()
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 50)
        self.ax.set_xlabel('X₁', fontsize=12)
        self.ax.set_ylabel('X₂', fontsize=12)
        self.ax.set_title('Región Factible - Programación Lineal', fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        
        # Mensaje inicial
        self.ax.text(25, 25, 'Ingrese los datos y presione\n"RESOLVER PROBLEMA"', 
                    ha='center', va='center', fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        self.canvas.draw()
    
    def _setup_results_area(self):
        """Configura el área de resultados textuales"""
        self.result_frame = ttk.LabelFrame(self.frame, text="Resultados Detallados", padding=10)
        self.result_frame.pack(fill=tk.X, pady=10)
        
        # Crear frame con scrollbar para el texto
        text_frame = ttk.Frame(self.result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=8, width=50, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Texto inicial
        initial_text = ("Bienvenido al Solucionador de Programación Lineal\n\n"
                       "Esta aplicación resuelve problemas de programación lineal "
                       "de 2 variables usando el método gráfico.\n\n"
                       "Funcionalidades:\n"
                       "• Cálculo automático de intersecciones\n"
                       "• Identificación de la región factible\n"
                       "• Evaluación de la función objetivo\n"
                       "• Determinación de la solución óptima\n\n"
                       "Configure los datos y presione 'RESOLVER PROBLEMA'.")
        self.result_text.insert(tk.END, initial_text)
        self.result_text.config(state=tk.DISABLED)
    
    def display_solution(self, solution: Solution):
        """
        Muestra la solución completa en el panel.
        
        Args:
            solution: Solución a mostrar
        """
        self.current_solution = solution
        
        # Generar gráfico
        self._plot_solution()
        
        # Mostrar resultados textuales
        self._display_text_results()
    
    def _plot_solution(self):
        """Genera el gráfico de la solución"""
        if not self.current_solution:
            return
        
        solution = self.current_solution
        self.ax.clear()
        
        # Determinar límites del gráfico
        x_max, y_max = self._calculate_plot_limits()
        x_range = np.linspace(0, x_max, 1000)
        
        # Graficar restricciones
        self._plot_constraints(x_range, x_max, y_max)
        
        # Graficar puntos de intersección
        self._plot_intersection_points()
        
        # Graficar vértices factibles
        self._plot_feasible_vertices()
        
        # Graficar punto óptimo
        self._plot_optimal_point()
        
        # Graficar función objetivo
        self._plot_objective_function(x_range)
        
        # Configurar ejes y título
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, y_max)
        self.ax.set_xlabel('X₁ (Variable 1)', fontsize=12)
        self.ax.set_ylabel('X₂ (Variable 2)', fontsize=12)
        self.ax.set_title('Región Factible y Solución Óptima', fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Ajustar layout y dibujar
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _calculate_plot_limits(self) -> tuple:
        """Calcula los límites apropiados para el gráfico"""
        solution = self.current_solution
        
        if solution.feasible_vertices:
            x_coords = [v.x1 for v in solution.feasible_vertices]
            y_coords = [v.x2 for v in solution.feasible_vertices]
            x_max = max(max(x_coords) * 1.3, 10)
            y_max = max(max(y_coords) * 1.3, 10)
        else:
            x_max, y_max = 50, 50
        
        # Considerar también las intersecciones para el límite
        if solution.intersection_points:
            x_coords_all = [p.x1 for p in solution.intersection_points if p.x1 >= 0 and p.x2 >= 0]
            y_coords_all = [p.x2 for p in solution.intersection_points if p.x1 >= 0 and p.x2 >= 0]
            if x_coords_all and y_coords_all:
                x_max = max(x_max, max(x_coords_all) * 1.2)
                y_max = max(y_max, max(y_coords_all) * 1.2)
        
        return min(x_max, 200), min(y_max, 200)  # Límite máximo razonable
    
    def _plot_constraints(self, x_range: np.ndarray, x_max: float, y_max: float):
        """Grafica las restricciones del problema"""
        solution = self.current_solution
        
        for i, constraint in enumerate(solution.problem.constraints):
            # Saltar restricciones de no negatividad (se asumen implícitas)
            if self._is_non_negativity_constraint(constraint):
                continue
            
            color = self.constraint_colors[i % len(self.constraint_colors)]
            
            try:
                # Obtener puntos de la línea
                x_line, y_line = self.solver.get_constraint_line_points(
                    constraint, (0, x_max), len(x_range)
                )
                
                # Filtrar puntos dentro de los límites del gráfico
                valid_indices = (y_line >= 0) & (y_line <= y_max)
                x_line_valid = x_line[valid_indices]
                y_line_valid = y_line[valid_indices]
                
                if len(x_line_valid) > 1:
                    # Graficar línea de restricción
                    label = self._get_constraint_label(constraint)
                    self.ax.plot(x_line_valid, y_line_valid, color=color, 
                               label=label, linewidth=2)
                    
                    # Sombrear región factible para la restricción
                    self._shade_feasible_region(constraint, x_line_valid, y_line_valid, color, y_max)
                    
            except Exception as e:
                print(f"Error graficando restricción {i}: {e}")
    
    def _is_non_negativity_constraint(self, constraint) -> bool:
        """Verifica si es una restricción de no negatividad"""
        return ((constraint.a1 == 1 and constraint.a2 == 0) or 
                (constraint.a1 == 0 and constraint.a2 == 1)) and constraint.b == 0
    
    def _get_constraint_label(self, constraint) -> str:
        """Genera etiqueta para una restricción"""
        return f'{constraint.a1:.0f}X₁ + {constraint.a2:.0f}X₂ {constraint.inequality_type.value} {constraint.b:.0f}'
    
    def _shade_feasible_region(self, constraint, x_line: np.ndarray, y_line: np.ndarray, 
                              color: str, y_max: float):
        """Sombrea la región factible de una restricción"""
        if constraint.inequality_type == InequalityType.MENOR_IGUAL:
            self.ax.fill_between(x_line, 0, y_line, alpha=0.1, color=color)
        elif constraint.inequality_type == InequalityType.MAYOR_IGUAL:
            self.ax.fill_between(x_line, y_line, y_max, alpha=0.1, color=color)
    
    def _plot_intersection_points(self):
        """Grafica todos los puntos de intersección"""
        solution = self.current_solution
        
        if solution.intersection_points:
            x_coords = [p.x1 for p in solution.intersection_points if p.x1 >= 0 and p.x2 >= 0]
            y_coords = [p.x2 for p in solution.intersection_points if p.x1 >= 0 and p.x2 >= 0]
            
            if x_coords and y_coords:
                self.ax.scatter(x_coords, y_coords, color='gray', s=30, alpha=0.6, 
                              label='Intersecciones', marker='o')
    
    def _plot_feasible_vertices(self):
        """Grafica los vértices factibles"""
        solution = self.current_solution
        
        if solution.feasible_vertices:
            x_coords = [v.x1 for v in solution.feasible_vertices]
            y_coords = [v.x2 for v in solution.feasible_vertices]
            
            self.ax.scatter(x_coords, y_coords, color='black', s=100, zorder=5,
                           label='Vértices Factibles', marker='o')
            
            # Etiquetar vértices
            for vertex in solution.feasible_vertices:
                self.ax.annotate(f'({vertex.x1:.1f}, {vertex.x2:.1f})', 
                               (vertex.x1, vertex.x2),
                               xytext=(8, 8), textcoords='offset points',
                               fontsize=9, fontweight='bold')
    
    def _plot_optimal_point(self):
        """Grafica el punto óptimo"""
        solution = self.current_solution
        
        if solution.optimal_point:
            self.ax.scatter(solution.optimal_point.x1, solution.optimal_point.x2, 
                          color='red', s=250, marker='*', zorder=6,
                          label=f'Óptimo: ({solution.optimal_point.x1:.1f}, {solution.optimal_point.x2:.1f})')
            
            # Anotar valor óptimo
            self.ax.annotate(f'Z* = {solution.optimal_value:.1f}',
                           (solution.optimal_point.x1, solution.optimal_point.x2),
                           xytext=(15, 15), textcoords='offset points',
                           fontsize=10, fontweight='bold', color='red',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    def _plot_objective_function(self, x_range: np.ndarray):
        """Grafica la línea de la función objetivo"""
        solution = self.current_solution
        
        if solution.optimal_point and solution.optimal_value is not None:
            obj_func = solution.problem.objective_function
            
            # Línea de función objetivo que pasa por el óptimo
            if abs(obj_func.c2) > 1e-10:
                y_obj = (solution.optimal_value - obj_func.c1 * x_range) / obj_func.c2
                valid_indices = (y_obj >= 0) & (y_obj <= self.ax.get_ylim()[1])
                if np.any(valid_indices):
                    self.ax.plot(x_range[valid_indices], y_obj[valid_indices], 
                               'r--', alpha=0.7, linewidth=2,
                               label=f'Función Objetivo (Z = {solution.optimal_value:.1f})')
    
    def _display_text_results(self):
        """Muestra los resultados textuales"""
        if not self.current_solution:
            return
        
        solution = self.current_solution
        
        # Limpiar texto anterior
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Construir texto de resultados
        result_text = self._build_results_text(solution)
        
        # Mostrar texto
        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state=tk.DISABLED)
        
        # Hacer scroll al inicio
        self.result_text.see(tk.INSERT)
    
    def _build_results_text(self, solution: Solution) -> str:
        """Construye el texto de resultados completo"""
        lines = []
        
        lines.append("=== RESULTADOS DEL PROBLEMA ===\n")
        
        # Problema planteado
        lines.append("PROBLEMA PLANTEADO:")
        lines.append(f"• {solution.problem.objective_function}")
        lines.append("• Restricciones:")
        for i, constraint in enumerate(solution.problem.constraints):
            if not self._is_non_negativity_constraint(constraint):
                lines.append(f"  - {constraint}")
        lines.append("  - X₁ ≥ 0, X₂ ≥ 0\n")
        
        # Puntos de intersección
        lines.append("=== ANÁLISIS MATEMÁTICO ===")
        lines.append(f"Puntos de intersección encontrados: {len(solution.intersection_points)}")
        for i, point in enumerate(solution.intersection_points[:10], 1):  # Mostrar máximo 10
            feasible_mark = "✓" if point in solution.feasible_vertices else "✗"
            lines.append(f"  {i}. {point} {feasible_mark}")
        
        if len(solution.intersection_points) > 10:
            lines.append(f"  ... y {len(solution.intersection_points) - 10} puntos más\n")
        else:
            lines.append("")
        
        # Vértices factibles y evaluaciones
        lines.append("=== VÉRTICES DE LA REGIÓN FACTIBLE ===")
        if solution.vertex_evaluations:
            for i, evaluation in enumerate(solution.vertex_evaluations, 1):
                lines.append(f"{i}. {evaluation}")
        else:
            lines.append("No se encontraron vértices factibles.\n")
        
        lines.append("")
        
        # Solución óptima
        lines.append("=== SOLUCIÓN ÓPTIMA ===")
        if solution.optimal_point and solution.optimal_value is not None:
            lines.append(f"Punto óptimo: X₁* = {solution.optimal_point.x1:.3f}, X₂* = {solution.optimal_point.x2:.3f}")
            lines.append(f"Valor óptimo: Z* = {solution.optimal_value:.3f}\n")
            
            # Interpretación específica para el ejemplo de startup
            lines.extend(self._get_startup_interpretation(solution))
        else:
            lines.append("No se encontró solución factible.")
        
        return "\n".join(lines)
    
    def _get_startup_interpretation(self, solution: Solution) -> list:
        """Genera interpretación específica para el problema de la startup"""
        obj_func = solution.problem.objective_function
        
        # Verificar si es el problema de la startup (coeficientes 250 y 300)
        if abs(obj_func.c1 - 250) < 1e-6 and abs(obj_func.c2 - 300) < 1e-6:
            lines = []
            lines.append("=== INTERPRETACIÓN PARA LA STARTUP ===")
            lines.append("La empresa de desarrollo de software debe producir:")
            lines.append(f"• {solution.optimal_point.x1:.0f} aplicaciones de productividad (A1)")
            lines.append(f"• {solution.optimal_point.x2:.0f} aplicaciones de entretenimiento (A2)")
            lines.append(f"Para obtener una ganancia máxima de ${solution.optimal_value:.2f} semanales.\n")
            
            # Análisis de recursos
            desarrollo_usado = 20 * solution.optimal_point.x1 + 15 * solution.optimal_point.x2
            pruebas_usado = 10 * solution.optimal_point.x1 + 15 * solution.optimal_point.x2
            
            lines.append("ANÁLISIS DE RECURSOS:")
            lines.append(f"• Desarrollo: {desarrollo_usado:.1f}/600 horas ({desarrollo_usado/600*100:.1f}% utilizado)")
            lines.append(f"• Pruebas: {pruebas_usado:.1f}/450 horas ({pruebas_usado/450*100:.1f}% utilizado)\n")
            
            # Recomendaciones
            lines.append("RECOMENDACIONES:")
            if desarrollo_usado >= 599:
                lines.append("• El recurso de desarrollo está al límite.")
            if pruebas_usado >= 449:
                lines.append("• El recurso de pruebas está al límite.")
            
            return lines
        
        return []
    
    def clear_display(self):
        """Limpia el panel y vuelve al estado inicial"""
        self.current_solution = None
        self._setup_initial_plot()
        
        # Limpiar resultados
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        initial_text = ("Panel limpio.\n\n"
                       "Configure nuevos datos y presione 'RESOLVER PROBLEMA' "
                       "para generar una nueva solución.")
        self.result_text.insert(tk.END, initial_text)
        self.result_text.config(state=tk.DISABLED)
