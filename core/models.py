"""
Modelos de datos para la aplicación de programación lineal.
"""
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class OptimizationType(Enum):
    """Tipo de optimización"""
    MAXIMIZAR = "maximizar"
    MINIMIZAR = "minimizar"


class InequalityType(Enum):
    """Tipo de desigualdad"""
    MENOR_IGUAL = "≤"
    MAYOR_IGUAL = "≥" 
    IGUAL = "="


@dataclass
class Constraint:
    """Representa una restricción del problema de programación lineal"""
    a1: float  # Coeficiente de X1
    a2: float  # Coeficiente de X2
    inequality_type: InequalityType
    b: float   # Término independiente
    
    def __str__(self):
        return f"{self.a1}·X₁ + {self.a2}·X₂ {self.inequality_type.value} {self.b}"
    
    def evaluate(self, x1: float, x2: float) -> float:
        """Evalúa la restricción en un punto dado"""
        return self.a1 * x1 + self.a2 * x2
    
    def is_satisfied(self, x1: float, x2: float, tolerance: float = 1e-10) -> bool:
        """Verifica si un punto satisface la restricción"""
        value = self.evaluate(x1, x2)
        
        if self.inequality_type == InequalityType.MENOR_IGUAL:
            return value <= self.b + tolerance
        elif self.inequality_type == InequalityType.MAYOR_IGUAL:
            return value >= self.b - tolerance
        else:  # IGUAL
            return abs(value - self.b) <= tolerance


@dataclass
class ObjectiveFunction:
    """Función objetivo del problema"""
    c1: float  # Coeficiente de X1
    c2: float  # Coeficiente de X2
    optimization_type: OptimizationType
    
    def __str__(self):
        return f"{self.optimization_type.value.capitalize()} Z = {self.c1}·X₁ + {self.c2}·X₂"
    
    def evaluate(self, x1: float, x2: float) -> float:
        """Evalúa la función objetivo en un punto"""
        return self.c1 * x1 + self.c2 * x2


@dataclass
class LinearProgrammingProblem:
    """Problema completo de programación lineal"""
    objective_function: ObjectiveFunction
    constraints: List[Constraint]
    
    def __str__(self):
        lines = [str(self.objective_function)]
        lines.append("Sujeto a:")
        for constraint in self.constraints:
            lines.append(f"  {constraint}")
        return "\n".join(lines)
    
    def add_non_negativity_constraints(self):
        """Agrega restricciones de no negatividad si no existen"""
        # Verificar si ya existen restricciones X1 >= 0 y X2 >= 0
        has_x1_non_neg = any(c.a1 == 1 and c.a2 == 0 and c.inequality_type == InequalityType.MAYOR_IGUAL and c.b == 0 
                            for c in self.constraints)
        has_x2_non_neg = any(c.a1 == 0 and c.a2 == 1 and c.inequality_type == InequalityType.MAYOR_IGUAL and c.b == 0 
                            for c in self.constraints)
        
        if not has_x1_non_neg:
            self.constraints.append(Constraint(1, 0, InequalityType.MAYOR_IGUAL, 0))
        if not has_x2_non_neg:
            self.constraints.append(Constraint(0, 1, InequalityType.MAYOR_IGUAL, 0))


@dataclass 
class Point:
    """Punto en el plano cartesiano"""
    x1: float
    x2: float
    
    def __str__(self):
        return f"({self.x1:.3f}, {self.x2:.3f})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        tolerance = 1e-6
        return (abs(self.x1 - other.x1) < tolerance and 
                abs(self.x2 - other.x2) < tolerance)
    
    def __hash__(self):
        # Redondear para hacer hasheable con tolerancia
        return hash((round(self.x1, 6), round(self.x2, 6)))


@dataclass
class VertexEvaluation:
    """Evaluación de un vértice"""
    point: Point
    objective_value: float
    is_feasible: bool = True
    
    def __str__(self):
        status = "✓" if self.is_feasible else "✗"
        return f"{self.point} → Z = {self.objective_value:.3f} {status}"


@dataclass
class Solution:
    """Solución completa del problema"""
    problem: LinearProgrammingProblem
    intersection_points: List[Point]
    feasible_vertices: List[Point]
    vertex_evaluations: List[VertexEvaluation]
    optimal_point: Optional[Point]
    optimal_value: Optional[float]
    is_feasible: bool = True
    
    def __str__(self):
        if not self.is_feasible:
            return "Problema sin solución factible"
        
        if self.optimal_point is None:
            return "No se encontró solución óptima"
        
        return (f"Solución óptima: {self.optimal_point}\n"
                f"Valor óptimo: Z = {self.optimal_value:.3f}")
