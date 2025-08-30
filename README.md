# Aplicación de Programación Lineal - 2 Variables

## Descripción

Esta aplicación en Python permite resolver problemas de programación lineal de 2 variables de forma gráfica e interactiva. Calcula automáticamente los puntos de corte, identifica los vértices de la región factible y determina la solución óptima.

## Características Principales

### 🎯 Funcionalidades Core

- ✅ Interfaz gráfica intuitiva con tkinter
- ✅ Entrada de datos flexible para función objetivo y restricciones
- ✅ Soporte para maximización y minimización
- ✅ Diferentes tipos de inecuaciones (≤, ≥, =)
- ✅ Cálculo automático de puntos de corte e intersecciones
- ✅ Identificación de vértices de la región factible
- ✅ Graficación automática de la solución con matplotlib
- ✅ Evaluación de la función objetivo en todos los vértices
- ✅ Determinación del punto y valor óptimo
- ✅ Interpretación detallada de los resultados

## Instalación

### Prerequisitos

- Python 3.8 o superior (se recomienda Python 3.10 o 3.11)

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

**Nota:** tkinter viene incluido por defecto en la mayoría de las instalaciones de Python.

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Interfaz de Usuario

#### Panel Izquierdo - Entrada de Datos

1. **Función Objetivo:**

   - Selecciona el tipo de optimización (maximizar/minimizar)
   - Ingresa los coeficientes de X₁ y X₂

2. **Restricciones:**

   - Ingresa los coeficientes de cada restricción
   - Selecciona el tipo de inecuación (≤, ≥, =)
   - Especifica el término independiente
   - Usa "Agregar Restricción" para más restricciones
   - Usa "Eliminar Última" para quitar restricciones

3. **Resolver:**
   - Haz clic en "RESOLVER PROBLEMA" para obtener la solución

#### Panel Derecho - Resultados

1. **Gráfico:**

   - Visualización de todas las restricciones
   - Región factible sombreada
   - Vértices marcados con coordenadas
   - Punto óptimo destacado con estrella roja
   - Línea de la función objetivo

2. **Resultados Textuales:**
   - Formulación del problema
   - Todos los puntos de corte calculados
   - Vértices de la región factible
   - Evaluación de la función objetivo en cada vértice
   - Solución óptima con interpretación

## Ejemplos Incluidos

La aplicación incluye tres ejemplos predefinidos accesibles desde el menú **Ejemplos**:

### 1. Startup de Software 🚀

**Enunciado:** Una startup de desarrollo de software está lanzando su producto al mercado. Ha decidido producir dos tipos de aplicaciones móviles: una de productividad (A1) y una de entretenimiento (A2). La empresa busca maximizar su beneficio total.

**Datos del problema:**

- **Variables:** A1 (apps de productividad), A2 (apps de entretenimiento)
- **Función Objetivo:** Maximizar Z = 250·A1 + 300·A2
- **Restricciones:**
  - Desarrollo: 20·A1 + 15·A2 ≤ 600 horas (La ganancia por A1 es $250, por A2 es $300)
  - Pruebas: 10·A1 + 15·A2 ≤ 450 horas (A1 necesita 20h desarrollo + 10h pruebas, A2 necesita 15h desarrollo + 15h pruebas)
  - A1 ≥ 0, A2 ≥ 0

**Solución Esperada:**

- Punto óptimo: A1 = 15, A2 = 20
- Ganancia máxima: Z = $9,750 semanales

### 2. Problema de Producción 🏭

**Enunciado:** Una fábrica produce dos tipos de productos (P1 y P2) y quiere maximizar sus ganancias. El producto P1 genera $400 de utilidad por unidad y P2 genera $300 por unidad. La producción está limitada por la disponibilidad de materia prima y mano de obra.

**Datos del problema:**

- **Variables:** P1 (producto tipo 1), P2 (producto tipo 2)
- **Función Objetivo:** Maximizar Z = 400·P1 + 300·P2
- **Restricciones:**
  - Materia prima: 2·P1 + 1·P2 ≤ 100 unidades
  - Mano de obra: 1·P1 + 2·P2 ≤ 80 horas
  - P1 ≥ 0, P2 ≥ 0

**Interpretación:** P1 requiere 2 unidades de materia prima y 1 hora de mano de obra, mientras que P2 requiere 1 unidad de materia prima y 2 horas de mano de obra.

### 3. Problema de Mezcla 🧪

**Enunciado:** Una empresa debe preparar una mezcla de dos componentes químicos (C1 y C2) para cumplir con ciertos requisitos de calidad, minimizando el costo total. El componente C1 cuesta $20 por unidad y C2 cuesta $30 por unidad.

**Datos del problema:**

- **Variables:** C1 (componente 1), C2 (componente 2)
- **Función Objetivo:** Minimizar Z = 20·C1 + 30·C2
- **Restricciones:**
  - Requisito mínimo: 1·C1 + 1·C2 ≥ 40 (cantidad mínima total)
  - Límite superior: 2·C1 + 1·C2 ≤ 80 (restricción de capacidad)
  - C1 ≥ 0, C2 ≥ 0

**Interpretación:** Se debe producir al menos 40 unidades totales de la mezcla, pero la capacidad está limitada por la segunda restricción.

### Cómo Acceder a los Ejemplos

1. **Desde el Menú**: Ve a `Ejemplos` → Selecciona el ejemplo deseado
2. **Carga Automática**: Los datos se cargan automáticamente en los campos
3. **Resolver**: Presiona `RESOLVER PROBLEMA` para ver la solución
4. **Experimentar**: Modifica los valores para explorar diferentes escenarios

## Funcionalidades del Menú

### 📁 Menú Archivo

- **Nuevo Problema** (`Ctrl+N`) - Limpiar todos los datos para comenzar desde cero
- **Guardar Problema** (`Ctrl+S`) - Guardar el problema actual en formato JSON
- **Cargar Problema** (`Ctrl+O`) - Cargar un problema guardado previamente
- **Exportar Resultados** (`Ctrl+E`) - Exportar la solución a archivo de texto
- **Salir** (`Ctrl+Q`) - Cerrar la aplicación

### 📋 Menú Ejemplos

- **Startup de Software** - Problema de maximización de ganancias
- **Problema de Producción** - Restricciones de recursos industriales
- **Mezcla de Productos** - Problema de minimización de costos

### ❓ Menú Ayuda

- **Cómo usar** - Guía paso a paso de la aplicación
- **Sobre el método gráfico** - Explicación teórica del algoritmo
- **Acerca de** - Información sobre la aplicación

## Funcionalidades Técnicas

### Algoritmos Implementados

1. **Cálculo de Intersecciones:** Resuelve sistemas de ecuaciones 2x2 para encontrar todos los puntos de corte
2. **Verificación de Factibilidad:** Evalúa cada punto contra todas las restricciones
3. **Método Gráfico:** Implementa el método simplex gráfico para 2 variables
4. **Evaluación Sistemática:** Evalúa la función objetivo en todos los vértices factibles
