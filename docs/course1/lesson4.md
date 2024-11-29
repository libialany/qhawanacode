# Lección 4: Formas graficas

### **Paso 0: repaso de funciones**

```
def nombrefuncion()():
    # codigo 

nombrefuncion()
```

### **Paso 1: ¿Qué es p5.js?**
p5.js es una divertida librería JavaScript que te permite dibujar formas y hacer arte en tu ordenador usando código.


### **Paso 2: Dibuja una Línea**
Una línea es simplemente una conexión entre dos puntos. 
Usamos la función `line()` para dibujarla.

**Código:**

```
def setup():
  createCanvas(windowWidth,windowHeight)

def draw():
  background("white")
  line(50, 50, 350, 350);
```
---

### **Paso 3: Dibujar un Rectángulo**
Un rectángulo es una forma con 4 lados rectos, y usamos la función `rect()` para dibujarlo.


**Código:**
```
def setup():
  createCanvas(windowWidth,windowHeight)

def draw():
  background("white")
  fill(255, 0, 0) 
  rect(100, 200, 200, 100) 
```

fill(255, 0, 0) establece el color de relleno a rojo (usando valores RGB).
rect((100, 100, 200, 100) dibuja un rectángulo en posición (100, 100) con una anchura de 200 y una altura de 100 píxeles.
---

### **Paso 4: Dibujar un Cuadrado**
Un cuadrado es un tipo especial de rectángulo donde todos los lados tienen la misma longitud. Podemos usar la función `rect()` para dibujarlo también, ¡pero esta vez haremos que el ancho y el alto sean iguales!


**Código:**
```
def setup():
  createCanvas(windowWidth,windowHeight)

def draw():
  background("white")
  fill(255, 0, 0) 
  rect(100, 100, 100, 200) 
```

---
Materiales: 

[LABORATORIO](https://colab.research.google.com/github/libialany/qhawanacode/blob/main/docs/course1/lesson4.ipynb)

[Editor](https://code.strivemath.com/)