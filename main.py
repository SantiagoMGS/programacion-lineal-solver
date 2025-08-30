import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from itertools import combinations
import sympy as sp

class ProgramacionLinealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolución de Programación Lineal - 2 Variables")
        self.root.geometry("1200x800")
        
        # Variables para almacenar los datos
        self.coef_objetivo = [0, 0]
        self.restricciones = []
        self.tipo_optimizacion = "maximizar"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo para entrada de datos
        input_frame = ttk.LabelFrame(main_frame, text="Datos del Problema", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Frame derecho para gráfico
        graph_frame = ttk.LabelFrame(main_frame, text="Gráfico y Resultados", padding=10)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.setup_input_section(input_frame)
        self.setup_graph_section(graph_frame)
        
    def setup_input_section(self, parent):
        # Función Objetivo
        obj_frame = ttk.LabelFrame(parent, text="Función Objetivo", padding=5)
        obj_frame.pack(fill=tk.X, pady=5)
        
        # Tipo de optimización
        ttk.Label(obj_frame, text="Tipo:").pack(anchor=tk.W)
        self.opt_var = tk.StringVar(value="maximizar")
        opt_combo = ttk.Combobox(obj_frame, textvariable=self.opt_var, 
                                values=["maximizar", "minimizar"], state="readonly", width=15)
        opt_combo.pack(anchor=tk.W, pady=2)
        
        # Coeficientes
        coef_frame = ttk.Frame(obj_frame)
        coef_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(coef_frame, text="Z = ").pack(side=tk.LEFT)
        self.c1_var = tk.StringVar(value="250")
        ttk.Entry(coef_frame, textvariable=self.c1_var, width=8).pack(side=tk.LEFT)
        ttk.Label(coef_frame, text="*X₁ + ").pack(side=tk.LEFT)
        self.c2_var = tk.StringVar(value="300")
        ttk.Entry(coef_frame, textvariable=self.c2_var, width=8).pack(side=tk.LEFT)
        ttk.Label(coef_frame, text="*X₂").pack(side=tk.LEFT)
        
        # Restricciones
        rest_frame = ttk.LabelFrame(parent, text="Restricciones", padding=5)
        rest_frame.pack(fill=tk.X, pady=5)
        
        # Frame para lista de restricciones
        self.rest_list_frame = ttk.Frame(rest_frame)
        self.rest_list_frame.pack(fill=tk.X, pady=5)
        
        # Restricción por defecto
        self.restriccion_entries = []
        self.agregar_restriccion_ui("20", "15", "≤", "600")
        self.agregar_restriccion_ui("10", "15", "≤", "450")
        
        # Botones para restricciones
        btn_frame = ttk.Frame(rest_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Agregar Restricción", 
                  command=self.agregar_restriccion_ui).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Eliminar Última", 
                  command=self.eliminar_restriccion).pack(side=tk.LEFT, padx=2)
        
        # Botón resolver
        ttk.Button(parent, text="RESOLVER PROBLEMA", 
                  command=self.resolver_problema, 
                  style="Accent.TButton").pack(pady=20, fill=tk.X)
        
    def agregar_restriccion_ui(self, a1="0", a2="0", signo="≤", b="0"):
        frame = ttk.Frame(self.rest_list_frame)
        frame.pack(fill=tk.X, pady=2)
        
        entries = {}
        
        # Coeficientes
        entries['a1'] = tk.StringVar(value=a1)
        ttk.Entry(frame, textvariable=entries['a1'], width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(frame, text="*X₁ + ").pack(side=tk.LEFT)
        
        entries['a2'] = tk.StringVar(value=a2)
        ttk.Entry(frame, textvariable=entries['a2'], width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(frame, text="*X₂ ").pack(side=tk.LEFT)
        
        # Signo
        entries['signo'] = tk.StringVar(value=signo)
        signo_combo = ttk.Combobox(frame, textvariable=entries['signo'], 
                                  values=["≤", "≥", "="], state="readonly", width=5)
        signo_combo.pack(side=tk.LEFT, padx=2)
        
        # Término independiente
        entries['b'] = tk.StringVar(value=b)
        ttk.Entry(frame, textvariable=entries['b'], width=8).pack(side=tk.LEFT, padx=2)
        
        self.restriccion_entries.append((frame, entries))
        
    def eliminar_restriccion(self):
        if len(self.restriccion_entries) > 0:
            frame, _ = self.restriccion_entries.pop()
            frame.destroy()
            
    def setup_graph_section(self, parent):
        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Área de resultados
        self.result_frame = ttk.LabelFrame(parent, text="Resultados", padding=10)
        self.result_frame.pack(fill=tk.X, pady=10)
        
        self.result_text = tk.Text(self.result_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def obtener_datos_problema(self):
        try:
            # Función objetivo
            c1 = float(self.c1_var.get())
            c2 = float(self.c2_var.get())
            self.coef_objetivo = [c1, c2]
            self.tipo_optimizacion = self.opt_var.get()
            
            # Restricciones
            self.restricciones = []
            for _, entries in self.restriccion_entries:
                a1 = float(entries['a1'].get())
                a2 = float(entries['a2'].get())
                signo = entries['signo'].get()
                b = float(entries['b'].get())
                
                # Convertir a formato estándar (≤)
                if signo == "≥":
                    a1, a2, b = -a1, -a2, -b
                    signo = "≤"
                
                self.restricciones.append([a1, a2, signo, b])
                
            # Agregar restricciones de no negatividad
            self.restricciones.append([1, 0, "≥", 0])  # X₁ ≥ 0
            self.restricciones.append([0, 1, "≥", 0])  # X₂ ≥ 0
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos ingresados: {str(e)}")
            return False
            
    def calcular_intersecciones(self):
        """Calcula todas las intersecciones entre las restricciones"""
        puntos = []
        
        # Convertir restricciones de ≥ a ≤ para cálculo
        restricciones_calc = []
        for rest in self.restricciones:
            a1, a2, signo, b = rest
            if signo == "≥":
                restricciones_calc.append([-a1, -a2, -b])
            else:  # signo == "≤" o "="
                restricciones_calc.append([a1, a2, b])
        
        # Calcular intersecciones entre cada par de restricciones
        for i, j in combinations(range(len(restricciones_calc)), 2):
            a1_i, a2_i, b_i = restricciones_calc[i]
            a1_j, a2_j, b_j = restricciones_calc[j]
            
            # Resolver sistema de ecuaciones
            det = a1_i * a2_j - a1_j * a2_i
            if abs(det) > 1e-10:  # Evitar división por cero
                x1 = (b_i * a2_j - b_j * a2_i) / det
                x2 = (a1_i * b_j - a1_j * b_i) / det
                puntos.append((x1, x2))
        
        return puntos
        
    def es_punto_factible(self, punto):
        """Verifica si un punto satisface todas las restricciones"""
        x1, x2 = punto
        
        for rest in self.restricciones:
            a1, a2, signo, b = rest
            valor = a1 * x1 + a2 * x2
            
            if signo == "≤":
                if valor > b + 1e-10:
                    return False
            elif signo == "≥":
                if valor < b - 1e-10:
                    return False
            else:  # signo == "="
                if abs(valor - b) > 1e-10:
                    return False
                    
        return True
        
    def encontrar_vertices_factibles(self):
        """Encuentra todos los vértices de la región factible"""
        puntos = self.calcular_intersecciones()
        vertices = []
        
        for punto in puntos:
            if self.es_punto_factible(punto):
                # Redondear para evitar errores numéricos
                x1 = round(punto[0], 6)
                x2 = round(punto[1], 6)
                if (x1, x2) not in vertices:
                    vertices.append((x1, x2))
                    
        return vertices
        
    def evaluar_funcion_objetivo(self, punto):
        """Evalúa la función objetivo en un punto"""
        x1, x2 = punto
        return self.coef_objetivo[0] * x1 + self.coef_objetivo[1] * x2
        
    def encontrar_optimo(self, vertices):
        """Encuentra el punto óptimo entre los vértices"""
        if not vertices:
            return None, None
            
        valores = [(v, self.evaluar_funcion_objetivo(v)) for v in vertices]
        
        if self.tipo_optimizacion == "maximizar":
            mejor = max(valores, key=lambda x: x[1])
        else:
            mejor = min(valores, key=lambda x: x[1])
            
        return mejor[0], mejor[1]
        
    def graficar_solucion(self, vertices, optimo):
        """Genera el gráfico de la solución"""
        self.ax.clear()
        
        # Determinar límites del gráfico
        if vertices:
            x_coords = [v[0] for v in vertices]
            y_coords = [v[1] for v in vertices]
            x_max = max(max(x_coords) * 1.2, 50)
            y_max = max(max(y_coords) * 1.2, 50)
        else:
            x_max, y_max = 50, 50
            
        x_range = np.linspace(0, x_max, 1000)
        
        # Graficar restricciones
        colores = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        for i, rest in enumerate(self.restricciones):
            a1, a2, signo, b = rest
            
            if abs(a2) > 1e-10:  # Si a2 != 0
                y_line = (b - a1 * x_range) / a2
                
                # Solo mostrar restricciones principales (no las de no negatividad)
                if not (a1 == 1 and a2 == 0) and not (a1 == 0 and a2 == 1):
                    color = colores[i % len(colores)]
                    self.ax.plot(x_range, y_line, color=color, 
                               label=f'{a1:.1f}X₁ + {a2:.1f}X₂ {signo} {b:.1f}', linewidth=2)
                    
                    # Sombrear región factible
                    if signo == "≤":
                        self.ax.fill_between(x_range, 0, y_line, alpha=0.1, color=color)
                    elif signo == "≥":
                        self.ax.fill_between(x_range, y_line, y_max, alpha=0.1, color=color)
        
        # Graficar vértices
        if vertices:
            x_coords = [v[0] for v in vertices]
            y_coords = [v[1] for v in vertices]
            self.ax.scatter(x_coords, y_coords, color='black', s=100, zorder=5)
            
            # Etiquetar vértices
            for i, (x, y) in enumerate(vertices):
                self.ax.annotate(f'({x:.2f}, {y:.2f})', (x, y), 
                               xytext=(5, 5), textcoords='offset points')
        
        # Destacar punto óptimo
        if optimo:
            self.ax.scatter(optimo[0], optimo[1], color='red', s=200, 
                          marker='*', zorder=6, label=f'Óptimo: ({optimo[0]:.2f}, {optimo[1]:.2f})')
        
        # Graficar función objetivo
        if optimo:
            # Línea de la función objetivo que pasa por el óptimo
            c1, c2 = self.coef_objetivo
            if abs(c2) > 1e-10:
                valor_optimo = self.evaluar_funcion_objetivo(optimo)
                y_obj = (valor_optimo - c1 * x_range) / c2
                self.ax.plot(x_range, y_obj, 'r--', alpha=0.7, 
                           label=f'Función Objetivo (Z = {valor_optimo:.2f})')
        
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, y_max)
        self.ax.set_xlabel('X₁')
        self.ax.set_ylabel('X₂')
        self.ax.set_title('Región Factible y Solución Óptima')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        self.canvas.draw()
        
    def mostrar_resultados(self, vertices, optimo, valor_optimo):
        """Muestra los resultados en el área de texto"""
        self.result_text.delete(1.0, tk.END)
        
        resultado = "=== RESULTADOS DEL PROBLEMA ===\n\n"
        
        # Problema planteado
        c1, c2 = self.coef_objetivo
        resultado += f"Función Objetivo: {self.tipo_optimizacion.capitalize()} Z = {c1}X₁ + {c2}X₂\n\n"
        
        resultado += "Restricciones:\n"
        for i, rest in enumerate(self.restricciones):
            a1, a2, signo, b = rest
            if not ((a1 == 1 and a2 == 0) or (a1 == 0 and a2 == 1)):  # Excluir no negatividad
                resultado += f"  {a1}X₁ + {a2}X₂ {signo} {b}\n"
        resultado += "  X₁ ≥ 0, X₂ ≥ 0\n\n"
        
        # Puntos de corte
        resultado += "=== PUNTOS DE CORTE (INTERSECCIONES) ===\n"
        intersecciones = self.calcular_intersecciones()
        for i, punto in enumerate(intersecciones):
            x1, x2 = punto
            factible = "✓" if self.es_punto_factible(punto) else "✗"
            resultado += f"Punto {i+1}: ({x1:.3f}, {x2:.3f}) {factible}\n"
        
        # Vértices factibles
        resultado += "\n=== VÉRTICES DE LA REGIÓN FACTIBLE ===\n"
        for i, vertice in enumerate(vertices):
            x1, x2 = vertice
            valor = self.evaluar_funcion_objetivo(vertice)
            resultado += f"Vértice {i+1}: ({x1:.3f}, {x2:.3f}) → Z = {valor:.3f}\n"
        
        # Solución óptima
        resultado += "\n=== SOLUCIÓN ÓPTIMA ===\n"
        if optimo:
            resultado += f"Punto óptimo: X₁ = {optimo[0]:.3f}, X₂ = {optimo[1]:.3f}\n"
            resultado += f"Valor óptimo: Z = {valor_optimo:.3f}\n\n"
            
            # Interpretación para el problema de la startup
            if abs(c1 - 250) < 1e-6 and abs(c2 - 300) < 1e-6:
                resultado += "=== INTERPRETACIÓN PARA LA STARTUP ===\n"
                resultado += f"La empresa debe producir:\n"
                resultado += f"• {optimo[0]:.0f} aplicaciones de productividad (A1)\n"
                resultado += f"• {optimo[1]:.0f} aplicaciones de entretenimiento (A2)\n"
                resultado += f"Para obtener una ganancia máxima de ${valor_optimo:.2f} semanales.\n\n"
                
                # Verificar uso de recursos
                desarrollo_usado = 20 * optimo[0] + 15 * optimo[1]
                pruebas_usado = 10 * optimo[0] + 15 * optimo[1]
                resultado += f"Uso de recursos:\n"
                resultado += f"• Desarrollo: {desarrollo_usado:.1f}/600 horas ({desarrollo_usado/600*100:.1f}%)\n"
                resultado += f"• Pruebas: {pruebas_usado:.1f}/450 horas ({pruebas_usado/450*100:.1f}%)\n"
        else:
            resultado += "No se encontró solución factible.\n"
            
        self.result_text.insert(tk.END, resultado)
        
    def resolver_problema(self):
        """Función principal para resolver el problema"""
        if not self.obtener_datos_problema():
            return
            
        try:
            # Encontrar vértices factibles
            vertices = self.encontrar_vertices_factibles()
            
            if not vertices:
                messagebox.showwarning("Advertencia", "No se encontraron vértices factibles.")
                return
                
            # Encontrar solución óptima
            optimo, valor_optimo = self.encontrar_optimo(vertices)
            
            # Generar gráfico
            self.graficar_solucion(vertices, optimo)
            
            # Mostrar resultados
            self.mostrar_resultados(vertices, optimo, valor_optimo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el problema: {str(e)}")

def main():
    root = tk.Tk()
    app = ProgramacionLinealApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
