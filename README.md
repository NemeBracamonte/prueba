# 🐧 Clasificador de especies de pingüinos (Streamlit)

App de testing que predice la especie de un pingüino (Adelie, Chinstrap o Gentoo) a partir de cuatro medidas morfológicas, usando un modelo de regresión logística entrenado con scikit-learn.

## Contenido del proyecto

```
pinguinos/
├── app.py                      # Aplicación Streamlit
├── modelo_especie_rl.joblib    # Modelo entrenado (exportado desde Colab)
├── requirements.txt            # Dependencias
└── README.md
```

## Requisitos previos

- Python 3.10 o superior
- Los archivos `app.py`, `modelo_especie_rl.joblib` y `requirements.txt` en la misma carpeta

## Paso a paso

### 1. Exportar el modelo desde Colab

El modelo se guarda en `/content/` de Colab. Para descargarlo:

```python
from google.colab import files
files.download("modelo_especie_rl.joblib")
```

Copiá el archivo descargado a la carpeta del proyecto.

### 2. Anotar la versión de scikit-learn usada en Colab

```python
import sklearn
print(sklearn.__version__)
```

Abrí `requirements.txt` y reemplazá la línea `scikit-learn` por la versión exacta, por ejemplo:

```
scikit-learn==1.6.1
```

> ⚠️ Si la versión local no coincide con la de Colab, el modelo puede fallar al predecir (por ejemplo: `AttributeError: 'SimpleImputer' object has no attribute '_fill_dtype'`).

### 3. Crear y activar un entorno virtual

Desde una terminal, dentro de la carpeta del proyecto:

**Windows (PowerShell o CMD)**
```
python -m venv env
env\Scripts\activate
```

**macOS / Linux**
```
python3 -m venv env
source env/bin/activate
```

### 4. Instalar las dependencias

```
pip install -r requirements.txt
```

### 5. Ejecutar la app

```
streamlit run app.py
```

Se abre automáticamente en el navegador. Si no, ingresá a http://localhost:8501.

Para detenerla, presioná `Ctrl + C` en la terminal.

## Uso

Ingresá las cuatro medidas y presioná **Predecir especie**:

| Campo | Unidad |
|---|---|
| Longitud del pico | mm |
| Profundidad del pico | mm |
| Longitud de la aleta | mm |
| Masa corporal | g |

La app muestra la especie predicha, su probabilidad y un gráfico con la probabilidad de cada especie.

## Validaciones

| Situación | Comportamiento |
|---|---|
| Campo vacío | Error: campo obligatorio. No predice. |
| Texto no numérico (ej. `abc`) | Error: valor inválido. No predice. |
| Valor negativo o cero | Error: debe ser mayor que 0. No predice. |
| Valor numérico fuera del rango habitual | Advertencia amarilla. Sí predice. |

Se acepta coma o punto como separador decimal. Los rangos de advertencia se pueden ajustar en la lista `CAMPOS` de `app.py`.

## Casos de prueba

| ID | Caso | Datos | Resultado esperado |
|---|---|---|---|
| CF-01 | Ingreso válido | 39.1 / 18.7 / 181 / 3750 | Acepta y predice |
| CF-02 | Campo obligatorio | Masa corporal vacía | Error, no predice |
| CF-03 | Tipo y rango inválido | pico = `abc`, masa = -500 | Errores, no predice |
| CF-04 | Predicción de especie | 50.0 / 15.2 / 218 / 5700 | Devuelve una especie válida |
| CF-05 | Visualización | 46.5 / 14.5 / 213 / 4400 | Muestra la especie de forma clara |

Orden de los datos: longitud del pico, profundidad del pico, longitud de la aleta, masa corporal.

## Problemas frecuentes

- **`FileNotFoundError` / "No se encontró modelo_especie_rl.joblib"**: el modelo no está en la misma carpeta que `app.py`, o ejecutaste el comando desde otra carpeta.
- **`AttributeError` al predecir**: desfase de versiones de scikit-learn. Instalá la misma versión que en Colab, o reentrená y guardá el modelo en tu entorno local.
- **`streamlit` no se reconoce como comando**: el entorno virtual no está activado. Repetí el paso 3.
