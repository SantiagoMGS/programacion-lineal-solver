"""
Solver para problemas de programación lineal de 2 variables.
Implementa el método gráfico para encontrar la solución óptima.
"""
from typing import List, Optional, Tuple
from itertools import combinations
import numpy as np

from .models import (
    LinearProgrammingProblem, Point, Solution, VertexEvaluation,
    Constraint, InequalityType, OptimizationType
)


class LinearProgrammingSolver:
    """Resuelve problemas de programación lineal de 2 variables usando método gráfico"""
    
    def __init__(self, tolerance: float = 1e-10):
        self.tolerance = tolerance
    
    def solve(self, problem: LinearProgrammingProblem) -> Solution:
        """
        Resuelve el problema de programación lineal completo.
        
        Args:
            problem: Problema de programación lineal a resolver
            
        Returns:
            Solution: Solución completa del problema
        """
        # Agregar restricciones de no negatividad
        problem.add_non_negativity_constraints()
        
        # Calcular todas las intersecciones
        intersection_points = self._calculate_intersections(problem.constraints)
        
        # Encontrar vértices factibles
        feasible_vertices = self._find_feasible_vertices(intersection_points, problem.constraints)
        
        # Evaluar función objetivo en cada vértice
        vertex_evaluations = self._evaluate_vertices(feasible_vertices, problem.objective_function)
        
        # Encontrar solución óptima
        optimal_point, optimal_value = self._find_optimal_solution(vertex_evaluations, problem.objective_function)
        
        return Solution(
            problem=problem,
            intersection_points=intersection_points,
            feasible_vertices=feasible_vertices,
            vertex_evaluations=vertex_evaluations,
            optimal_point=optimal_point,
            optimal_value=optimal_value,
            is_feasible=len(feasible_vertices) > 0
        )
    
    def _calculate_intersections(self, constraints: List[Constraint]) -> List[Point]:
        """
        Calcula todas las intersecciones entre pares de restricciones.
        
        Args:
            constraints: Lista de restricciones
            
        Returns:
            List[Point]: Lista de puntos de intersección
        """
        intersection_points = []
        
        # Convertir restricciones a formato matricial para cálculo
        matrix_constraints = self._convert_constraints_to_matrix_form(constraints)
        
        # Calcular intersecciones entre cada par de restricciones
        for i, j in combinations(range(len(matrix_constraints)), 2):
            intersection = self._solve_2x2_system(matrix_constraints[i], matrix_constraints[j])
            if intersection is not None:
                intersection_points.append(intersection)
        
        return intersection_points
    
    def _convert_constraints_to_matrix_form(self, constraints: List[Constraint]) -> List[Tuple[float, float, float]]:
        """
        Convierte restricciones a forma matricial [a1, a2, b] donde a1*x1 + a2*x2 = b
        
        Args:
            constraints: Lista de restricciones originales
            
        Returns:
            List[Tuple]: Lista de coeficientes [a1, a2, b]
        """
        matrix_form = []
        
        for constraint in constraints:
            # Para intersecciones, tratamos todas como igualdades
            # Si es ≥, convertimos multiplicando por -1
            if constraint.inequality_type == InequalityType.MAYOR_IGUAL:
                matrix_form.append((-constraint.a1, -constraint.a2, -constraint.b))
            else:  # ≤ o =
                matrix_form.append((constraint.a1, constraint.a2, constraint.b))
        
        return matrix_form
    
    def _solve_2x2_system(self, eq1: Tuple[float, float, float], 
                         eq2: Tuple[float, float, float]) -> Optional[Point]:
        """
        Resuelve un sistema 2x2 de ecuaciones lineales.
        
        Args:
            eq1: Primera ecuación [a1, a2, b] -> a1*x1 + a2*x2 = b
            eq2: Segunda ecuación [c1, c2, d] -> c1*x1 + c2*x2 = d
            
        Returns:
            Point: Punto de intersección o None si no existe
        """
        a1, a2, b = eq1
        c1, c2, d = eq2
        
        # Calcular determinante
        det = a1 * c2 - c1 * a2
        
        if abs(det) < self.tolerance:
            # Las líneas son paralelas o coincidentes
            return None
        
        # Resolver usando regla de Cramer
        x1 = (b * c2 - d * a2) / det
        x2 = (a1 * d - c1 * b) / det
        
        return Point(x1, x2)
    
    def _find_feasible_vertices(self, intersection_points: List[Point], 
                               constraints: List[Constraint]) -> List[Point]:
        """
        Filtra los puntos de intersección para encontrar solo los vértices factibles.
        
        Args:
            intersection_points: Todos los puntos de intersección
            constraints: Restricciones del problema
            
        Returns:
            List[Point]: Vértices que satisfacen todas las restricciones
        """
        feasible_vertices = []
        
        for point in intersection_points:
            if self._is_point_feasible(point, constraints):
                # Evitar duplicados con tolerancia
                if not any(point == existing for existing in feasible_vertices):
                    feasible_vertices.append(point)
        
        return feasible_vertices
    
    def _is_point_feasible(self, point: Point, constraints: List[Constraint]) -> bool:
        """
        Verifica si un punto satisface todas las restricciones.
        
        Args:
            point: Punto a verificar
            constraints: Lista de restricciones
            
        Returns:
            bool: True si el punto es factible
        """
        for constraint in constraints:
            if not constraint.is_satisfied(point.x1, point.x2, self.tolerance):
                return False
        return True
    
    def _evaluate_vertices(self, vertices: List[Point], 
                          objective_function) -> List[VertexEvaluation]:
        """
        Evalúa la función objetivo en cada vértice factible.
        
        Args:
            vertices: Lista de vértices factibles
            objective_function: Función objetivo
            
        Returns:
            List[VertexEvaluation]: Evaluaciones de cada vértice
        """
        evaluations = []
        
        for vertex in vertices:
            objective_value = objective_function.evaluate(vertex.x1, vertex.x2)
            evaluations.append(VertexEvaluation(
                point=vertex,
                objective_value=objective_value,
                is_feasible=True
            ))
        
        return evaluations
    
    def _find_optimal_solution(self, vertex_evaluations: List[VertexEvaluation], 
                              objective_function) -> Tuple[Optional[Point], Optional[float]]:
        """
        Encuentra la solución óptima entre las evaluaciones de vértices.
        
        Args:
            vertex_evaluations: Evaluaciones de vértices
            objective_function: Función objetivo
            
        Returns:
            Tuple[Point, float]: Punto óptimo y valor óptimo
        """
        if not vertex_evaluations:
            return None, None
        
        # Encontrar el mejor según el tipo de optimización
        if objective_function.optimization_type == OptimizationType.MAXIMIZAR:
            best_evaluation = max(vertex_evaluations, key=lambda x: x.objective_value)
        else:  # MINIMIZAR
            best_evaluation = min(vertex_evaluations, key=lambda x: x.objective_value)
        
        return best_evaluation.point, best_evaluation.objective_value
    
    def get_constraint_line_points(self, constraint: Constraint, 
                                 x_range: Tuple[float, float] = (0, 50),
                                 num_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtiene puntos para graficar una línea de restricción.
        
        Args:
            constraint: Restricción a graficar
            x_range: Rango de valores X
            num_points: Número de puntos a generar
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Arrays de coordenadas X e Y
        """
        x_values = np.linspace(x_range[0], x_range[1], num_points)
        
        if abs(constraint.a2) < self.tolerance:
            # Línea vertical
            if abs(constraint.a1) > self.tolerance:
                x_line = constraint.b / constraint.a1
                return np.full_like(x_values, x_line), x_values
            else:
                # Restricción degenerada
                return x_values, np.zeros_like(x_values)
        else:
            # Línea normal: y = (b - a1*x) / a2
            y_values = (constraint.b - constraint.a1 * x_values) / constraint.a2
            return x_values, y_values
