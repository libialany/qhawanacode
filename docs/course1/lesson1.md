# Lección 1: Bases de la programación

## Teoria

### **Clase de Python para Principiantes**

### **1. Variables (Guardando valores)**

En Python, una **variable** es un espacio en memoria que se utiliza para almacenar un valor.

#### Ejemplo de uso:

```python
# Creamos variables para almacenar diferentes tipos de datos
nombre = "Juan"  # Una cadena de texto
edad = 25        # Un número entero
altura = 1.75    # Un número decimal (float)

# Imprimimos los valores de las variables
print("Mi nombre es:", nombre)
print("Tengo", edad, "años.")
print("Mido", altura, "metros.")
```


---

### **2. Importaciones (import)**

En Python, `import` nos permite usar módulos o bibliotecas externas que contienen funciones, clases y herramientas útiles.

#### Ejemplo de uso:

```python
# Importamos el módulo math para poder usar funciones matemáticas
import math

# Usamos la función sqrt (raíz cuadrada) del módulo math
numero = 9
raiz = math.sqrt(numero)
print("La raíz cuadrada de", numero, "es", raiz)
```

### ¿Qué hace `import math`?

- `import math` trae todo el contenido del módulo `math` para que podamos usarlo.

---

### **3. Funciones (Con parámetros)**

Una **función** es un bloque de código que realiza una tarea específica. Las funciones pueden recibir **parámetros**.

#### Ejemplo de uso:

```python
# Definimos una función que toma dos números y devuelve su suma
def sumar(a, b):
    resultado = a + b
    return resultado

# Llamamos a la función con dos números
numero1 = 5
numero2 = 3
suma = sumar(numero1, numero2)  # Pasamos numero1 y numero2 como parámetros

# Imprimimos el resultado
print("La suma de", numero1, "y", numero2, "es", suma)
```

### ¿Qué son las funciones con parámetros?

- **Funciones**: Son bloques de código reutilizables. Pueden recibir **parámetros** (como `a` y `b` en el ejemplo) que les dan información adicional para trabajar.

---

### **Resumen**

- **Variables** son "contenedores" donde guardamos valores como números o cadenas de texto.
- **`import`** nos permite usar módulos externos con funcionalidades útiles.
- **Funciones** son bloques de código que realizan tareas específicas y pueden tomar parámetros para hacerlo.

---

### **Ejemplo Final: Usando todo junto**

Aquí tienes un ejemplo completo que usa importaciones, variables y funciones:

```python
import math  # Importamos el módulo math

# Definimos una función que usa math para calcular el área de un círculo
def area_circulo(radio):
    area = math.pi * (radio ** 2)  # Usamos math.pi para obtener el valor de pi
    return area

# Usamos variables para almacenar el radio y el resultado
mi_radio = 5
mi_area = area_circulo(mi_radio)

# Mostramos el resultado
print(f"El área de un círculo con radio {mi_radio} es {mi_area:.2f}")
```

En este ejemplo:

1. **Importamos `math`** para usar el valor de pi.
2. **Creamos una función `area_circulo`** que recibe un parámetro (`radio`) y devuelve el área del círculo.
3. Usamos **una variable (`mi_radio`)** para guardar el valor del radio y luego pasamos esa variable como parámetro a la función.

---

## Laboratorio

[LABORATORIO](https://colab.research.google.com/github/libialany/qhawanacode/blob/main/docs/course1/lesson1.ipynb)


---

## Pytamaro

[Ejercicio](https://pytamaro.si.usi.ch/activities/luce-hoc/plain-wall/en/v1?curriculum=luce-hoc%2Fcastle)
