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

**Enunciado:** Una startup de desarrollo de software está lanzando su producto al mercado. Ha decidido producir dos tipos de aplicaciones móviles: una de productividad (A1) y una de entretenimiento (A2). La empresa busca maximizar su beneficio total. Para producir cada aplicación, se requiere tiempo de desarrollo y de pruebas.

**Detalles del problema:**

- **Ganancias:** La ganancia por cada aplicación de productividad (A1) es de $250, y por cada aplicación de entretenimiento (A2) es de $300
- **Recursos requeridos por app:**
  - Para producir A1: se necesitan 20 horas de desarrollo y 10 horas de pruebas
  - Para producir A2: se necesitan 15 horas de desarrollo y 15 horas de pruebas
- **Recursos disponibles:** La empresa dispone de un total de 600 horas para desarrollo y 450 horas para pruebas a la semana

**Formulación matemática:**

- **Variables:** A1 = número de apps de productividad, A2 = número de apps de entretenimiento
- **Función Objetivo:** Maximizar Z = 250·A1 + 300·A2 (ganancia total semanal)
- **Restricciones:**
  - Desarrollo: 20·A1 + 15·A2 ≤ 600 (horas de desarrollo consumidas)
  - Pruebas: 10·A1 + 15·A2 ≤ 450 (horas de pruebas consumidas)
  - A1 ≥ 0, A2 ≥ 0 (no se pueden producir cantidades negativas)

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

### 3. Problema de Mezcla Farmacéutica 🧪

**Enunciado:** Un laboratorio farmacéutico debe producir un jarabe medicinal mezclando dos ingredientes activos: Compuesto A y Compuesto B. El objetivo es minimizar los costos de producción mientras se cumplen los estándares de calidad y regulaciones sanitarias.

**Contexto del problema:**

- **Compuesto A:** Ingrediente activo básico, costo $20 por litro
- **Compuesto B:** Ingrediente activo premium, costo $30 por litro
- **Producto final:** Jarabe medicinal de alta calidad para exportación

**Datos del problema:**

- **Variables:** A = litros de Compuesto A, B = litros de Compuesto B
- **Función Objetivo:** Minimizar Z = 20·A + 30·B (costo total en dólares)

- **Restricciones:**
  - **Volumen mínimo:** A + B ≥ 40 (se necesitan al menos 40 litros de producto final)
  - **Concentración máxima:** 2·A + B ≤ 80 (límite de concentración activa por regulaciones)
  - **Disponibilidad:** A ≥ 0, B ≥ 0 (no se pueden usar cantidades negativas)

**Interpretación detallada:**

- La **primera restricción** garantiza que se produzca el volumen mínimo requerido para el pedido
- La **segunda restricción** evita que el medicamento sea demasiado concentrado (el Compuesto A tiene el doble de potencia)
- El **objetivo de minimización** busca la mezcla más económica que cumpla con las regulaciones

**Solución esperada:** Encontrar la combinación óptima de compuestos que produzca el jarabe al menor costo posible.

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

- **Startup de Software** - Maximización de ganancias con recursos limitados
- **Problema de Producción** - Optimización de recursos industriales (materia prima y mano de obra)
- **Mezcla Farmacéutica** - Minimización de costos en producción de jarabe medicinal

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
