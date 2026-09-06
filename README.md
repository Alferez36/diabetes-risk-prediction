# Predicción riesgo de diabetes
Proyecto **end-to-end de Machine Learning** orientado a la predicción del riesgo de diabetes a través de variables demográficas, clínicas, cardiovasculares y del estilo de vida.

Se aborda tanto la **clasificación binaria** de diabetes como la **clasificación multiclase del tipo de diabetes**, además de desarrollar un modelo orientado a la **estimación temprana del riesgo** utilizando variables que pueden estar disponibles antes de realizar determinadas pruebas clínicas.

## Puntos a destacar
- Dataset con **100.000 resgistros de pacientes**.
- Análisis exploratorio de los datos (EDA) y análisis de características.
- Procesamiento categórico con pipelines de codificación.
- División train/test con una proporción 80/20.
- Comparación de modelos entre regresión logística, árbol de decisión y random forest.
- Ajuste de hiperparámetros con RandomizedSearchCV. 
- Análisis de diferentes umbrales de decisión para estudiar el equilibrio entre precisión y exhaustividad. 
- Validación cruzada de 5 pliegues. 
- Análisis de feature importance. 
- Pipelines de preprocesamiento y modelos entrenados persistidos con joblib. 
- Interfaz interactiva con Streamlit.

## Dataset
El dataset contiene **100.000 registros de pacientes** e incluye variables pertennecientes a diferentes categorías: 
- Demográficas: edad, género, etnia
- Socioeconómicas: nivel educativo, ingresos, ocupación/empleo
- Estilo de vida: tabaquismo, consumo de alcohol, actividad física, dieta, horas de sueño, tiempo frente a pantallas
- Antropometría: IMC (índice de masa corporal) y relación cintura-cadera
- Variables cardiovasculares: presión arterial, frecuencia cardíaca, colesterol, HDL, LDL, triglicéridos
- Biomarcadores clínicos: glucosa en ayunas, glucosa posprandial, insulina, HbA1c
- Puntuación de riesgo de diabetes (diabetes risk score)
- Etapa/tipo de diabetes
- Diagnóstico binario de diabetes (sí o no)

La variable objetivo binaria consiste en un 60% de pacientes diagnosticados y 40% de no diagnosticados con diabetes. 

La variable multiclase presenta un desequilibrio muy elevado en el que la diabetes tipo 1 y gestacional representan menos del 0.5% de los registros. Es una limitación importante dentro del modelo B multiclase. 


## Modelos desarrollados
Se han desarrollado tres enfoques diferentes: 

- **Modelo A  (Clasificación binaria)**: Clasificación binaria de presencia o binaria de diabetes con todas la variables clínicas. 
- **Modelo B  (Clasificación multiclase)**: Predicción del tipo específico de diabetes con todas las variables clínicas. 
- **Modelo C  (Clasificación binaria basada en el estilo de vida)**: Estimación temprana del riesgo de diabetes utilizando exclusivamente variables de hábitos, características demográficas y perfil cardiovascular.

En las iteraciones iniciales del modelo A, la inclusión de las variables directamente relacionadas con el diagnóstico deriva en una precisión cercana al 100%. Este comportamiento evidencia un problema de data leakage. Por lo tanto, en el modelo C se han eliminado: 

```text
hba1c
glucose_postprandial
glucose_fasting
insulin_level
diagnosed_diabetes
diabetes_stage
diabetes_risk_score
```

El modelo A y C se desarrollaron en el Jupyter notebook `ModelTraningAC`, mientras que el modelo B en el `ModelTraniningB`.


## Manual del desarrollador

Instrucciones para desplegar el proyecto de manera local. 

### Estructura del proyecto
Para un correcto funcionamiento de la aplicación, el directorio del proyecto debe mantener la siguiente estructura: 

```bash
/
├── app.py   
├── model_A_forest.joblib
├── preprocessor_A.joblib
├── model_C_forest.joblib
├── preprocessor_C.joblib
└── requirements.txt
```

Incluye los preprocesadores de ambos modelos, los propios modelos entrenados, el código fuente para la aplicación (app.py) y las dependencias del sistema (requirements.txt). 

### Requisitos
- Python 3.9 o superior. 
- Gestor de paquetes pip.
- scikit-learn==1.6.1.   

El entrenamiento de los modelos se hizo sobre la versión scikit-learn 1.6.1. Se ha declarado para que no haya problemas en el deployment, ya que algunos sistemas utilizan versiones más actualizadas. 

### Instalación
1. Clonar el repositorio en local. 
2. Instalar dependencias:
`pip install -r requirements.txt`

### Ejecución local 
Se lanza la aplicación en el navegador en una URL local con el siguiente comando: 
`python -m streamlit run app.py`

## Manual de usuario 

Instrucciones de uso del prototipo. 

Este prototipo permite evaluar la presencia de diabetes en un paciente a través de modelo de aprendizaje automático supervisado. 

### 1. Selección del modelo 
En la barra lateral izquierda, puede seleccionar el modelo: 

- Modelo A (Clasificación binaria): Utiliza variables clínicas y demográficas para estimar la presencia de diabetes.
- Modelo B (Índice de riesgo): Evalúa el índice de riesgo basado en el estilo de vida y los antecendentes del paciente, sin las variables clínicas cómo la glucosa. 

### 2. Introducción de datos
La interfaz está organizada en varias pestañas en la que se debe de ingresar la información de cada paciente. 
1. Perfil: Datos demográficos y situación socioeconómica. 
2. Biomarcadores (Solo Modelo A): Glucosa e insulina. 
3. Vitales y lípidos: Valores cardiovasculares y perfil lipídico.  
4. Antecendetes y Estilo de vida: Posibles antecedentes y registro de actividad física, sueño, dieta y otros hábitos. 

### 3. Obtención del resultado
Tras haber completado todos los campos haga clic en el botón "EJECUTAR DIAGNÓSTICO". La aplicación le mostrará la métrica de probabilidad (0-100%) de padecer la enfermedad junto a un mensaje visual (Rojo para Positivo, Verde para negativo). 

>[!WARNING] 
>Esta herramienta es un prototipo con fines educativos e informativos y no sustituye el juicio del profesional santitario. Si cree que padece síntomas consistentes con diabetes, consulte a un profesional.