"""
Ventana principal de la aplicación de programación lineal.
Actúa como orquestador entre los diferentes paneles.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import Optional

from core.models import LinearProgrammingProblem
from core.solver import LinearProgrammingSolver
from gui.input_panel import InputPanel
from gui.graph_panel import GraphPanel


class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.solver = LinearProgrammingSolver()
        self.current_problem: Optional[LinearProgrammingProblem] = None
        
        self._setup_window()
        self._setup_menu()
        self._setup_panels()
        self._setup_styles()
    
    def _setup_window(self):
        """Configura las propiedades básicas de la ventana"""
        self.root.title("Programación Lineal - Solver Gráfico de 2 Variables")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Configurar icono si existe
        try:
            # Intentar cargar icono (opcional)
            pass
        except:
            pass
    
    def _setup_styles(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        
        # Intentar usar tema moderno
        try:
            style.theme_use('clam')  # Tema más moderno que default
        except:
            pass
        
        # Configurar estilo para botón principal
        style.configure('Accent.TButton', 
                       font=('Arial', 12, 'bold'),
                       padding=(10, 10))
    
    def _setup_menu(self):
        """Configura la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo Problema", command=self._new_problem, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Guardar Problema...", command=self._save_problem, accelerator="Ctrl+S")
        file_menu.add_command(label="Cargar Problema...", command=self._load_problem, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exportar Resultados...", command=self._export_results, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self._exit_application, accelerator="Ctrl+Q")
        
        # Menú Ejemplos
        examples_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ejemplos", menu=examples_menu)
        examples_menu.add_command(label="Startup de Software", command=self._load_startup_example)
        examples_menu.add_command(label="Problema de Producción", command=self._load_production_example)
        examples_menu.add_command(label="Mezcla de Productos", command=self._load_mix_example)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Cómo usar", command=self._show_help)
        help_menu.add_command(label="Sobre el método gráfico", command=self._show_method_info)
        help_menu.add_separator()
        help_menu.add_command(label="Acerca de", command=self._show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self._new_problem())
        self.root.bind('<Control-s>', lambda e: self._save_problem())
        self.root.bind('<Control-o>', lambda e: self._load_problem())
        self.root.bind('<Control-e>', lambda e: self._export_results())
        self.root.bind('<Control-q>', lambda e: self._exit_application())
    
    def _setup_panels(self):
        """Configura los paneles principales de la aplicación"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel de entrada de datos (izquierda)
        self.input_panel = InputPanel(main_frame, self._on_solve_problem)
        
        # Panel de gráfico (derecha)
        self.graph_panel = GraphPanel(main_frame)
        
        # Barra de estado
        self._setup_status_bar()
    
    def _setup_status_bar(self):
        """Configura la barra de estado"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Etiqueta de estado
        self.status_label = ttk.Label(self.status_bar, text="Listo - Configure los datos y presione RESOLVER PROBLEMA")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Indicador de progreso (opcional)
        self.progress_var = tk.StringVar(value="")
        self.progress_label = ttk.Label(self.status_bar, textvariable=self.progress_var)
        self.progress_label.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def _on_solve_problem(self, problem: LinearProgrammingProblem):
        """
        Callback ejecutado cuando se solicita resolver un problema.
        
        Args:
            problem: Problema de programación lineal a resolver
        """
        try:
            # Actualizar estado
            self.status_label.config(text="Resolviendo problema...")
            self.progress_var.set("Calculando...")
            self.root.update()
            
            # Resolver problema
            solution = self.solver.solve(problem)
            self.current_problem = problem
            
            # Mostrar solución
            self.graph_panel.display_solution(solution)
            
            # Actualizar estado
            if solution.is_feasible and solution.optimal_point:
                status_text = f"Problema resuelto - Óptimo: {solution.optimal_point} = {solution.optimal_value:.3f}"
            else:
                status_text = "Problema resuelto - Sin solución factible"
            
            self.status_label.config(text=status_text)
            self.progress_var.set("")
            
        except Exception as e:
            self.status_label.config(text="Error al resolver problema")
            self.progress_var.set("")
            messagebox.showerror("Error", f"Error al resolver el problema:\\n{str(e)}")
    
    def _new_problem(self):
        """Inicia un nuevo problema limpiando todos los datos"""
        response = messagebox.askyesno("Nuevo Problema", 
                                     "¿Desea limpiar todos los datos y comenzar un nuevo problema?")
        if response:
            self.input_panel.clear_all_constraints()
            self.input_panel.c1_var.set("0")
            self.input_panel.c2_var.set("0")
            self.input_panel.optimization_var.set("maximizar")
            self.graph_panel.clear_display()
            self.current_problem = None
            self.status_label.config(text="Nuevo problema iniciado")
    
    def _save_problem(self):
        """Guarda el problema actual en un archivo JSON"""
        try:
            problem = self.input_panel.get_problem()
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
                title="Guardar Problema"
            )
            
            if filename:
                problem_data = self._problem_to_dict(problem)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(problem_data, f, indent=2, ensure_ascii=False)
                
                self.status_label.config(text=f"Problema guardado: {filename}")
                messagebox.showinfo("Guardado", "Problema guardado exitosamente")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el problema:\\n{str(e)}")
    
    def _load_problem(self):
        """Carga un problema desde un archivo JSON"""
        filename = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Cargar Problema"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    problem_data = json.load(f)
                
                self._load_problem_from_dict(problem_data)
                self.status_label.config(text=f"Problema cargado: {filename}")
                messagebox.showinfo("Cargado", "Problema cargado exitosamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el problema:\\n{str(e)}")
    
    def _export_results(self):
        """Exporta los resultados actuales a un archivo de texto"""
        if not hasattr(self.graph_panel, 'current_solution') or not self.graph_panel.current_solution:
            messagebox.showwarning("Sin resultados", "No hay resultados para exportar. Resuelva un problema primero.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Exportar Resultados"
        )
        
        if filename:
            try:
                results_text = self.graph_panel.result_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(results_text)
                
                self.status_label.config(text=f"Resultados exportados: {filename}")
                messagebox.showinfo("Exportado", "Resultados exportados exitosamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar resultados:\\n{str(e)}")
    
    def _load_startup_example(self):
        """Carga el ejemplo de la startup de software"""
        self.input_panel.load_startup_example()
        self.status_label.config(text="Ejemplo de startup cargado")
        messagebox.showinfo("Ejemplo", "Ejemplo de la startup de software cargado. Presione RESOLVER PROBLEMA.")
    
    def _load_production_example(self):
        """Carga un ejemplo de problema de producción"""
        self.input_panel.clear_all_constraints()
        self.input_panel.optimization_var.set("maximizar")
        self.input_panel.c1_var.set("400")
        self.input_panel.c2_var.set("300")
        self.input_panel.add_constraint("2", "1", "≤", "100")  # Materia prima
        self.input_panel.add_constraint("1", "2", "≤", "80")   # Mano de obra
        self.status_label.config(text="Ejemplo de producción cargado")
        messagebox.showinfo("Ejemplo", "Ejemplo de problema de producción cargado.")
    
    def _load_mix_example(self):
        """Carga un ejemplo de problema de mezcla farmacéutica"""
        self.input_panel.clear_all_constraints()
        self.input_panel.optimization_var.set("minimizar")
        self.input_panel.c1_var.set("20")   # Costo Compuesto A
        self.input_panel.c2_var.set("30")   # Costo Compuesto B
        self.input_panel.add_constraint("1", "1", "≥", "40")   # Volumen mínimo 40 litros
        self.input_panel.add_constraint("2", "1", "≤", "80")   # Concentración máxima regulada
        self.status_label.config(text="Ejemplo de mezcla farmacéutica cargado")
        messagebox.showinfo("Ejemplo", "Ejemplo de mezcla farmacéutica cargado.\n\nProblema: Minimizar costo de producción de jarabe medicinal\nCompuestos: A ($20/L) y B ($30/L)\nRestricciones: Volumen mínimo y concentración regulada.")
    
    def _show_help(self):
        """Muestra la ayuda de la aplicación"""
        help_text = """
CÓMO USAR LA APLICACIÓN:

1. FUNCIÓN OBJETIVO:
   • Seleccione el tipo (maximizar/minimizar)
   • Ingrese los coeficientes de X₁ y X₂

2. RESTRICCIONES:
   • Ingrese los coeficientes de cada restricción
   • Seleccione el tipo de desigualdad (≤, ≥, =)
   • Agregue o elimine restricciones según necesite

3. RESOLVER:
   • Presione "RESOLVER PROBLEMA"
   • El gráfico mostrará la región factible
   • Los resultados aparecerán en el panel derecho

4. CARACTERÍSTICAS:
   • Cálculo automático de intersecciones
   • Identificación de vértices factibles
   • Determinación de la solución óptima
   • Interpretación detallada de resultados

5. MENÚS:
   • Archivo: Guardar/cargar problemas
   • Ejemplos: Problemas predefinidos
   • Ayuda: Información adicional
        """
        
        self._show_info_dialog("Ayuda", help_text)
    
    def _show_method_info(self):
        """Muestra información sobre el método gráfico"""
        method_text = """
MÉTODO GRÁFICO PARA PROGRAMACIÓN LINEAL:

El método gráfico es una técnica para resolver problemas de 
programación lineal con 2 variables. Sigue estos pasos:

1. FORMULACIÓN:
   • Definir función objetivo y restricciones
   • Convertir a forma estándar

2. GRAFICACIÓN:
   • Graficar cada restricción como una línea
   • Identificar la región factible (área sombreada)

3. VÉRTICES:
   • Encontrar intersecciones entre restricciones
   • Identificar cuáles están en la región factible

4. EVALUACIÓN:
   • Evaluar la función objetivo en cada vértice
   • El óptimo está siempre en un vértice (teoría simplex)

5. SOLUCIÓN:
   • Para maximizar: elegir el vértice con mayor valor
   • Para minimizar: elegir el vértice con menor valor

Este método es visual e intuitivo, ideal para problemas 
educativos y de pequeña escala.
        """
        
        self._show_info_dialog("Método Gráfico", method_text)
    
    def _show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """
PROGRAMACIÓN LINEAL - SOLVER GRÁFICO

Versión 2.0 - Arquitectura Modular

Aplicación desarrollada en Python para resolver problemas
de programación lineal de 2 variables usando el método gráfico.

CARACTERÍSTICAS:
• Interfaz gráfica intuitiva con tkinter
• Cálculo matemático preciso con numpy
• Graficación profesional con matplotlib
• Arquitectura modular y extensible
• Ejemplos predefinidos incluidos

DESARROLLADO PARA:
• Estudiantes de investigación operativa
• Profesores de matemáticas aplicadas
• Profesionales que necesitan soluciones rápidas

TECNOLOGÍAS:
• Python 3.8+
• tkinter (interfaz)
• matplotlib (gráficos)
• numpy (cálculos)

© 2024 - Herramienta Educativa Open Source
        """
        
        self._show_info_dialog("Acerca de", about_text)
    
    def _show_info_dialog(self, title: str, message: str):
        """Muestra un diálogo de información personalizado"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 50))
        
        # Texto con scroll
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=('Arial', 10))
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)
        
        # Botón cerrar
        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)
    
    def _problem_to_dict(self, problem: LinearProgrammingProblem) -> dict:
        """Convierte un problema a diccionario para serialización"""
        return {
            "objective_function": {
                "c1": problem.objective_function.c1,
                "c2": problem.objective_function.c2,
                "optimization_type": problem.objective_function.optimization_type.value
            },
            "constraints": [
                {
                    "a1": constraint.a1,
                    "a2": constraint.a2,
                    "inequality_type": constraint.inequality_type.value,
                    "b": constraint.b
                }
                for constraint in problem.constraints
                if not ((constraint.a1 == 1 and constraint.a2 == 0) or 
                       (constraint.a1 == 0 and constraint.a2 == 1))  # Excluir no negatividad
            ]
        }
    
    def _load_problem_from_dict(self, problem_data: dict):
        """Carga un problema desde un diccionario"""
        # Limpiar datos actuales
        self.input_panel.clear_all_constraints()
        
        # Cargar función objetivo
        obj_func = problem_data["objective_function"]
        self.input_panel.c1_var.set(str(obj_func["c1"]))
        self.input_panel.c2_var.set(str(obj_func["c2"]))
        self.input_panel.optimization_var.set(obj_func["optimization_type"])
        
        # Cargar restricciones
        for constraint_data in problem_data["constraints"]:
            self.input_panel.add_constraint(
                str(constraint_data["a1"]),
                str(constraint_data["a2"]),
                constraint_data["inequality_type"],
                str(constraint_data["b"])
            )
    
    def _exit_application(self):
        """Maneja la salida de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Inicia la aplicación"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._exit_application()
        except Exception as e:
            messagebox.showerror("Error Fatal", f"Error inesperado:\\n{str(e)}")
            self.root.quit()
