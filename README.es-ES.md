

# 🏛️ Sistema RAG para Informes de Trabajo del Gobierno Chino

## 📋 Descripción General del Proyecto

Este proyecto es un sistema inteligente de preguntas y respuestas basado en RAG (Generación Aumentada por Recuperación) diseñado específicamente para informes de trabajo del gobierno chino. Aborda problemas centrales de **recuperación de información incompleta** y **datos insuficientes para comparaciones entre múltiples provincias** mediante una innovadora **arquitectura de recuperación por capas inteligentes** y estrategias de **maximización de la ventana de contexto**, logrando un procesamiento eficiente de documentos a gran escala y preguntas y respuestas inteligentes precisas.

### 🎁 Listo para usar
- **📁 Conjunto de datos completo**: Incluye datos de informes de trabajo gubernamentales de 31 provincias (carpeta docs)
- **🚀 Despliegue con un clic**: Extrae los datos y ejecuta inmediatamente, sin necesidad de preparación adicional de documentos
- **💡 Optimización inteligente**: Sistema de recuperación y preguntas y respuestas profundamente ajustado

### 🎯 Problemas Principales y Soluciones

#### Problemas Originales
1. **Insuficiente integridad de la información**: El sistema no lee informes de trabajo gubernamentales completos antes de responder, omitiendo información disponible
2. **Datos inadecuados para comparaciones entre múltiples provincias**: Datos detallados limitados al comparar varias provincias

#### Soluciones
A través de la **Optimización de Fase 1 Sin Rechunking**, logramos:

1. **🔍 Mejora masiva de la profundidad de recuperación**
   - Consultas de una sola provincia: De 10 a 30 chunks (+200%)
   - Consultas de múltiples provincias: De 6 a 15 chunks (+150%)
   - Consultas de comparación: De 8 a 25 chunks (+213%)
   - Recuperación general: De 20 a 60 chunks (+200%)

2. **📈 Expansión significativa de la ventana de contexto**
   - Contexto total: De 16.000 a 100.000 caracteres (+525%)
   - Mejora promedio de capacidad: 337.8%
   - Aprovecha completamente las capacidades de modelos de contexto largo

3. **🚀 Funcionalidad mejorada del sistema**
   - Agregación de chunks adyacentes agregada para continuidad de contexto
   - Estrategia de truncamiento inteligente optimizada para preservar información de alto valor
   - Ingeniería de prompts mejorada para salidas detalladas y precisas
   - Estructuras de datos mejoradas que admiten más atributos

## ⚡ Optimización de Rendimiento más Reciente v2.1.0

### 🚀 Optimización de Velocidad de Respuesta

El sistema ha completado importantes optimizaciones de rendimiento, con una velocidad de respuesta esperada 3-5 veces mayor:

#### Funcionalidades de Optimización Clave
1. **🔄 Procesamiento Concurrente de API**
   - Nuevo soporte para la API oficial de DeepSeek, respuestas más rápidas y estables
   - Soporta 5-8 solicitudes concurrentes, procesamiento por lotes 4 veces más rápido
   - Cambio inteligente de proveedor de API, permite alternar entre DeepSeek y SiliconFlow

2. **💾 Caché de Consultas Inteligente**
   - Mecanismo de caché TTL de 24 horas, respuestas en milisegundos para consultas idénticas
   - Limpieza y optimización automática de caché, soporta 1000 entradas de caché
   - Monitoreo y estadísticas de tasa de aciertos en caché

3. **⚡ Optimización de Búsqueda Vectorial**
   - Selección inteligente del tipo de índice FAISS óptimo (FlatL2/IVF/IVFPQ)
   - Soporte para búsqueda acelerada por GPU, velocidad de recuperación 2-3 veces mayor
   - Ajuste dinámico de parámetros nprobe, equilibra velocidad y precisión

4. **🎯 Optimización de Estrategia de Procesamiento por Lotes**
   - Ejecución de lotes concurrentes, procesamiento paralelo de consultas de múltiples provincias
   - Optimización de tamaño de lote y parámetros de tiempo de espera
   - Gestión inteligente de hilos de trabajo

#### Mejoras de Rendimiento Esperadas
- **Consulta única**: De 68 segundos a 15-25 segundos ⚡
- **Acierto en caché**: Respuestas en milisegundos 💨
- **Procesamiento concurrente**: Aumento de throughput de 4-5 veces 🚀
- **Aceleración GPU**: Velocidad de recuperación 2-3 veces mayor ⚡

#### Experimenta Rápido la Versión Optimizada

```bash
# 1. Instalar nuevas dependencias
pip install openai>=1.0.0

# 2. Cambio de proveedor de API (opcional)
python API_KIT/switch_api.py deepseek  # Cambiar a API oficial de DeepSeek (recomendado)

# 3. Reiniciar servicio para experimentar el efecto de aceleración
API_KIT/start_all.bat
```

#### Configuración del Proveedor de API

**API Oficial de DeepSeek (Recomendada)**
```python
# Preconfigurado en config/config.py
DEEPSEEK_CONFIG = {
    "api_key": "sk-6617537f09584c38b63477294794c0d0",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat",
    "timeout": 60,  # Configuración de tiempo de espera más rápida
}

API_PROVIDER = "deepseek"  # Cambiar proveedor
```

**Pruebas Comparativas de Rendimiento**
```bash
# Ejemplo de consulta de prueba
"Objetivos de trabajo clave de Henan en 2025"
# v2.0: ~68 segundos
# v2.1: ~20 segundos (DeepSeek) / ~25 segundos (SiliconFlow optimizado)

# Prueba de acierto en caché (consulta repetida)
# v2.1: <100 milisegundos ⚡
```


### Mejora de Métricas Clave
- **Aumento promedio del volumen de información**: 100.0%
- **Aumento promedio del volumen de recuperación**: 100.0% 
- **Aumento de capacidad de contexto**: 337.8%
- **Aumento de capacidad de salida de API**: Adaptado al límite del modelo de 8192 tokens

### Mejoras Detalladas de Configuración

| Configuración | Antes | Después | Mejora |
|---------------|--------|-------|-------------|
| top_k general | 20 | 60 | +200% |
| Contexto máximo | 16.000 caracteres | 100.000 caracteres | +525% |
| Chunks por provincia | 10 | 30 | +200% |
| Chunks multi-provincia | 6 | 15 | +150% |
| Chunks consulta comparación | 8 | 25 | +213% |
| API max_tokens | 20.480 | 8.192 | Adaptado al límite del modelo |
| API timeout | 60s | 180s | +200% |

## 🛠️ Arquitectura Técnica

```
Sistema RAG para Informes de Trabajo del Gobierno Chino (Optimizado)
├── Capa de Procesamiento de Datos
│   ├── Análisis de Documentos Word (python-docx)
│   ├── Segmentación y Preprocesamiento Inteligente de Texto
│   └── Identificación y Clasificación por Provincia
├── Capa de Almacenamiento Vectorial
│   ├── Jina Embeddings v4 (Despliegue local, optimización dual FlashAttention2+SDPA, fuerza modelo local)
│   ├── Base de Datos Vectorial FAISS (Capacidad de búsqueda mejorada)
│   └── Motor de Recuperación Semántica (Soporta recuperación masiva, eficiente en memoria)
├── Capa de Consultas Inteligentes
│   ├── Reconocimiento de Intención de Consulta
│   ├── Estrategia de Recuperación por Capas Inteligente
│   ├── Mecanismo de Agregación de Chunks Adyacentes
│   └── Enrutamiento de Resultados de Recuperación
├── Capa de Agregación de Resultados
│   ├── Algoritmo de Truncamiento Optimizado
│   ├── Puntuación de Densidad de Información
│   └── Salida Formateada Detallada
├── Capa de Interacción con API
│   └── SiliconFlow Tongyi-Zhiwen/QwenLong-L1-32B (Contexto Largo)
└── Capa de Servicio API RESTful (API_KIT)
    ├── Servidor FastAPI (Soporte CORS, verificaciones de salud)
    ├── Interfaz de Consulta Inteligente (POST /api/query)
    ├── Interfaz de Estado del Sistema (GET /api/status)
    ├── Interfaz de Inicialización del Sistema (POST /api/setup)
    └── Soporte de Túnel (integración con ngrok)
```

## ✅ Características Destacadas

### Características Principales

1. **Consultas de Todas las Provincias**: Soporta consultas como "listar los objetivos de trabajo principales de cada provincia"
2. **Consultas Profundas de Una Provincia**: Soporta consultas detalladas como "cuáles son los trabajos clave de Henan para 2025"
3. **Análisis Comparativo Multi-Provincia**: Soporta comparación de datos detallados entre provincias
4. **Análisis de Resumen Estadístico**: Soporta estadísticas y resúmenes de datos provinciales
5. **Consultas Transversales por Tema**: Soporta consultas de temas específicos entre provincias

### Formatos de Salida

- **Formato de Lista por Provincia**: `Provincia: dato específico 1, dato específico 2...` (incluye números detallados)
- **Formato de Informe Detallado**: Contiene todos los indicadores cuantitativos y medidas específicas
- **Formato de Tabla Comparativa**: Comparación detallada de datos interprovinciales
- **Formato de Resumen Estadístico**: Estadísticas y análisis completos de datos

### Características Técnicas

- **Recuperación por Capas Inteligente**: Ajusta dinámicamente las estrategias de recuperación según la complejidad de la consulta
- **Agregación de Chunks Adyacentes**: Obtiene automáticamente información de contexto de chunks relacionados
- **Algoritmo de Truncamiento Optimizado**: Preserva el contenido con mayor densidad de información
- **Ingeniería de Prompts Mejorada**: Garantiza salida de datos detallada y completa
- **Soporte de Contexto Largo**: Aprovecha completamente la ventana de contexto de 100K caracteres
- **Optimización de Modelo Local**: Fuerza el uso de archivos de modelo local, evita descargas por red, mejora la velocidad de inicio
- **Servicio API RESTful**: Soporte completo de interfaz HTTP para facilitar la integración del sistema y llamadas desde frontend

## 📁 Descripción de los Datos

### Conjunto de Datos Integrado
Este proyecto incluye datos completos de informes de trabajo gubernamentales de 31 provincias/regimientos/municipios de China, almacenados en `docs/31省区市政府工作报告.zip`:

| Región | Provincias | Formato de Documento |
|--------|-----------|-----------------|
| **Norte de China** | Pekín, Tianjin, Hebei, Shanxi, Mongolia Interior | .docx |
| **Noreste** | Liaoning, Jilin, Heilongjiang | .docx |
| **Este de China** | Shanghái, Jiangsu, Zhejiang, Anhui, Fujian, Jiangxi, Shandong | .docx |
| **Centro de China** | Henan, Hubei, Hunan | .docx |
| **Sur de China** | Guangdong, Guangxi, Hainan | .docx |
| **Suroeste** | Chongqing, Sichuan, Guizhou, Yunnan, Tíbet | .docx |
| **Noroeste** | Shaanxi, Gansu, Qinghai, Ningxia, Xinjiang | .docx |

### Características de los Datos
- **📊 Integridad de Datos**: Cubre las 31 provincias/regimientos/municipios, sin omisiones
- **📅 Actualidad**: Informes de trabajo gubernamentales anuales más recientes
- **📋 Normalización**: Formato unificado de documento Word para facilitar el procesamiento
- **🔍 Buscabilidad**: Contiene indicadores económicos detallados, objetivos de desarrollo, proyectos clave, etc.

### Uso
```bash
# 1. Extraer archivos de datos
cd docs
unzip "31省区市政府工作报告.zip"

# 2. Los datos se extraerán al directorio docs/31省区市政府工作报告/
# 3. Establecer la ruta a este directorio en el archivo de configuración
```

## ⚡ Inicio Rápido

### Experiencia Rápida en 5 Minutos

```bash
# 1. Clonar proyecto
git clone https://github.com/alexzhu0/government-report-rag.git
cd government-report-rag

# 2. Extraer datos
cd docs && unzip "31省区市政府工作报告.zip" && cd ..

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar archivo de configuración
copy config\config.example.py config\config.py  # Windows
# cp config/config.example.py config/config.py    # Linux/Mac

# 5. Editar archivo de configuración, completar tu clave API
# Editar config/config.py, configurar:
# - api_key: Tu clave API de SiliconFlow
# - raw_documents: "docs/31省区市政府工作报告"

# 6. Ejecutar sistema
python main.py
```

### 🎯 Probar Consultas Inmediatamente
```
🔍 Ingresar consulta: ¿Cuáles son los trabajos clave de Henan para 2025
🔍 Ingresar consulta: Comparar desarrollo industrial entre Guangdong y Jiangsu
🔍 Ingresar consulta: ¿Cuáles son los objetivos de crecimiento del PIB de cada provincia
```

## 🚀 Instalación y Despliegue Detallados

### Requisitos del Entorno

- **Python 3.10+**
- **GPU NVIDIA**: RTX 3060 o superior (recomendado)
- **Memoria**: Al menos 16GB (32GB recomendado)
- **Espacio en Disco**: Al menos 20GB
- **CUDA**: 11.8+ (para aceleración GPU)

## 🌐 Despliegue del Servicio API

### 📋 Visión General de API_KIT

Este proyecto proporciona un módulo completo de servicio API RESTful (`API_KIT/`) que soporta llamadas de interfaz HTTP a las funcionalidades del sistema RAG, facilitando aplicaciones frontend, herramientas de automatización e integración con sistemas de terceros.

#### 🎯 Características Principales
- **Interfaz de Consulta Inteligente**: Soporta consultas en lenguaje natural de informes de trabajo gubernamentales
- **Monitoreo de Estado del Sistema**: Estado y estadísticas de operación del sistema en tiempo real
- **Inicialización del Sistema**: Inicialización remota y reconstrucción de índices vectoriales
- **Túnelización**: Integración con ngrok para acceso externo
- **Soporte CORS**: Configuración CORS completa que soporta llamadas desde frontend

#### 🚀 Inicio Rápido del Servicio API

```bash
# Método 1: Inicio con un clic (recomendado)
cd API_KIT
start_all.bat  # Autoiniciar servicio API y ngrok

# Método 2: Inicio manual
conda activate GovRag
cd API_KIT
start_api.bat
```

#### 📡 Ejemplos de Interfaz API

```bash
# Interfaz de consulta
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Cuáles son los trabajos clave de la provincia de Henan para 2025"}'

# Estado del sistema
curl -X GET "http://localhost:8000/api/status"

# Acceder a documentación API
# http://localhost:8000/docs
```

#### 📚 Documentación Detallada

Para instrucciones completas de configuración, despliegue y uso del servicio API, ver:
**[API_KIT/README.md](API_KIT/README.md)** - Contiene detalladamente:
- Documentación y ejemplos completos de la interfaz API
- Múltiples métodos de inicio y configuraciones de entorno
- Ejemplos de llamada de cliente (Python, JavaScript, cURL)
- Configuración y uso de túnelización
- Configuración de seguridad y optimización de rendimiento
- Solución de problemas y guía de desarrollo

### ⚡ Optimización del Mecanismo de Atención Eficiente

Este proyecto emplea técnicas avanzadas de optimización de mecanismos de atención, mejorando significativamente la eficiencia de cálculo vectorial y el uso de memoria:

#### 🚀 Beneficios y Ventajas de FlashAttention2

**FlashAttention2** es un algoritmo de cálculo de atención eficiente en memoria que proporciona mejoras significativas de rendimiento para el modelo Jina Embeddings v4:

- **🔥 Mejora de Eficiencia de Memoria**: Reducción de uso de memoria del 50-80% en comparación con la atención estándar
- **⚡ Aceleración de Velocidad de Cálculo**: Mejora de velocidad de 2-4 veces en el procesamiento de secuencias largas
- **📊 Soporte de Secuencias más Largas**: Maneja chunks de documentos más largos, mejorando la calidad de recuperación
- **🎯 Mantenimiento de Precisión**: Mantiene la precisión computacional mientras mejora la eficiencia
- **💡 Optimización Dinámica**: Optimiza automáticamente la estrategia de cálculo según las características del hardware

#### 🧠 Significado de la Optimización SDPA (Scaled Dot-Product Attention)

**Optimización SDPA** es la implementación nativa de atención eficiente de PyTorch 2.0+, exitosamente habilitada y completamente aprovechada:

- **🔧 Aceleración de Hardware**: Aprovecha completamente los Tensor Cores y la Jerarquía de Memoria de GPUs modernas
- **📈 Mejora de Throughput**: Mejora significativamente el throughput de procesamiento en escenarios por lotes (probado: 5 textos en 0.56s)
- **🎛️ Optimización Adaptativa**: Selecciona automáticamente la implementación óptima según el tamaño de entrada y hardware
- **🔋 Reducción de Energía**: Rutas de cálculo más eficientes reducen el consumo de energía de la GPU
- **🛡️ Estabilidad Numérica**: Cálculo numérico mejorado que asegura estabilidad en el procesamiento de secuencias largas
- **✅ Verificado Habilitado**: El sistema usa SDPA por defecto, retrocede automáticamente a atención estándar en caso de falla

#### 💻 Opciones Alternativas sin GPU/FlashAttention2

Si tu entorno no soporta GPU o FlashAttention2, el sistema proporciona opciones compatibles:

**Opción 1: Modo CPU**
```python
# Configurar en config/config.py
EMBEDDING_CONFIG = {
    "device": "cpu",  # Cambiar a modo CPU
    "model_name": "jinaai/jina-embeddings-v4",
    # Otras configuraciones permanecen sin cambios
}
```

**Opción 2: Mecanismo de Atención Estándar**
```bash
# El sistema tiene optimización SDPA habilitada, retrocede automáticamente a atención estándar si SDPA falla
# Comparación de rendimiento (datos de prueba reales):
# - Optimizado con SDPA: Línea base de rendimiento 100% (5 textos en 0.56s)
# - Atención Estándar: Rendimiento 70-80%
# - Modo CPU: Rendimiento 30-40%
```

**Opción 3: Configuración Ligera**
```python
# Configuraciones optimizadas para entornos de especificaciones bajas
RETRIEVAL_CONFIG = {
    "top_k": 30,  # Reducir cantidad de chunks de recuperación
    "max_contexts_per_query": 50000,  # Longitud de contexto más baja
    # Adecuado para VRAM de 8GB o operación en CPU
}
```

**Detección de Entorno y Adaptación Automática**
```bash
# El sistema detecta automáticamente y selecciona la configuración óptima al inicio
python -c "from src.embedding_manager import get_embedding_manager; get_embedding_manager().check_optimization_support()"
```

**Tabla Comparativa de Rendimiento**
| Configuración | Requisito GPU | Uso de Memoria | Velocidad de Procesamiento | Rendimiento Real | Escenario Recomendado |
|---------------|-----------------|--------------|------------------|-------------------|---------------------|
| SDPA + GPU | RTX 3060+ | 8GB | Más rápida | 5textos/0.56s | Producción (Habilitado) |
| Atención Estándar + GPU | GTX 1660+ | 6GB | Media | 5textos/0.8s | Prioridad Compatibilidad |
| Modo CPU | Sin GPU | RAM del Sistema | Más lenta | 5textos/2-3s | Entorno Puramente CPU |

### 1. Clonar Proyecto

```bash
git clone https://github.com/alexzhu0/government-report-rag.git
cd government-report-rag
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración del Entorno

Editar `config/config.py`:

```python
# Configuración API SiliconFlow
SILICONFLOW_CONFIG = {
    "api_key": "your-api-key-here",  # Reemplazar con tu clave API
    "base_url": "https://api.siliconflow.cn/v1",
    "model": "Tongyi-Zhiwen/QwenLong-L1-32B",
    "temperature": 0.3,
    "max_tokens": 8192,
    "timeout": 180
}

# Ruta de documentos crudos
DATA_PATHS = {
    "raw_documents": r"Tu ruta de documentos"  # Reemplazar con ruta real
}
```

### 4. Preparar Datos

**Método 1: Usar Datos Proporcionados (Recomendado)**

Hemos preparado datos de informes de trabajo gubernamentales de 31 provincias para ti:

```bash
# Extraer archivos de datos
cd docs
unzip "31省区市政府工作报告.zip"
```

Después de la extracción, obtendrás documentos Word de 31 provincias incluyendo:
- Pekín, Tianjin, Hebei, Shanxi, Mongolia Interior
- Liaoning, Jilin, Heilongjiang, Shanghái, Jiangsu
- Zhejiang, Anhui, Fujian, Jiangxi, Shandong
- Henan, Hubei, Hunan, Guangdong, Guangxi
- Hainan, Chongqing, Sichuan, Guizhou, Yunnan
- Tíbet, Shaanxi, Gansu, Qinghai, Ningxia, Xinjiang

Luego actualiza la ruta en el archivo de configuración:
```python
DATA_PATHS = {
    "raw_documents": r"docs/31省区市政府工作报告",  # Usar datos proporcionados
    # ... otras configuraciones
}
```

**Método 2: Usar Datos Personalizados**

Si tienes otros datos de informes de trabajo gubernamentales, coloca los documentos Word (formato .docx) en el directorio especificado y establece la ruta en el archivo de configuración.

### 5. Ejecutar Sistema

```bash
python main.py
```

La primera ejecución hará automáticamente:
1. 🔍 Detectar y cargar modelo local Jina Embeddings v4 (priorizar modelo local, evitar descarga por red)
2. 📚 Procesar documentos Word y segmentarlos en chunks
3. 🔨 Construir índice vectorial FAISS
4. 🔗 Probar conexión API

**Nota**: El sistema está optimizado para priorizar archivos de modelo local. Si existen archivos de modelo completos en el directorio models, se usará el modelo local directamente sin descarga por red.

## 📝 Ejemplos de Uso

### Iniciar Sistema

```bash
python main.py
```

### Ejemplos de Consulta

#### Consulta Detallada de Una Provincia
```
🔍 Ingresar consulta: ¿Cuáles son los trabajos clave de Henan para 2025

📝 Resultados de Consulta:
Tipo: single_province
Formato: province_list
Conteo de provincias: 1
Tiempo de procesamiento: 23.97s
------------------------------

**Henan:**
1. **Objetivo de Crecimiento Económico**: Crecimiento del PIB alrededor del 5.5%, crecimiento del valor agregado industrial alrededor del 7%...
2. **Impulso al Consumo**: Actualizar 500,000 vehículos, 8 millones de electrodomésticos, implementar 3,000 proyectos de actualización de equipos...
3. **Inversión en Proyectos Principales**: 1,000 proyectos clave provinciales, completar inversión de 1 trillón de yuanes...
...(Contiene 14 categorías detalladas con puntos de datos específicos)

📊 Estadísticas de Procesamiento:
Tasa de éxito: 100.0%
Chunks recuperados: 20 (anteriormente: 10)
Caracteres de contexto: 16,775 caracteres
```

#### Consulta Comparativa Multi-Provincia
```
🔍 Ingresar consulta: Comparar desarrollo industrial entre Guangdong y Jiangsu

📝 Resultados de Consulta:
Tipo: multi_province
Formato: comparison
Conteo de provincias: 2
Tiempo de procesamiento: 18.45s
------------------------------

Análisis comparativo detallado incluyendo:
- Tablas comparativas con datos numéricos específicos
- Análisis de diferencias en medidas de política
- Comparación en profundidad de enfoques de desarrollo
- Comparación precisa de escala de inversión
...(15 chunks por provincia, 30 chunks totales de información rica)
```

## 📁 Estructura del Proyecto

```
government_report_rag/
├── config/
│   └── config.py              # Configuración del sistema (optimizada)
├── src/                       # Módulos centrales (limpios)
│   ├── data_processor.py      # Procesamiento de documentos (estructura de datos mejorada)
│   ├── embedding_manager.py   # Gestión Jina Embeddings v4
│   ├── vector_store.py        # Almacenamiento vectorial FAISS (búsqueda mejorada)
│   ├── retriever.py          # Recuperación RAG inteligente (agregación de chunks adyacentes)
│   ├── query_router.py       # Enrutamiento de consultas (prompt mejorado)
│   ├── result_aggregator.py  # Agregación de resultados
│   └── api_client.py         # Cliente API (timeout optimizado)
├── API_KIT/                  # Módulo de servicio API RESTful
│   ├── api_server.py         # Servidor FastAPI
│   ├── api_models.py         # Modelos de datos API
│   ├── start_all.bat         # Script de inicio con un clic
│   ├── start_api.bat         # Script de inicio API
│   ├── start_ngrok.bat       # Script de inicio ngrok
│   ├── requirements_api.txt  # Dependencias API
│   └── README.md             # Documentación detallada API
├── data/
│   ├── processed/            # Datos de documentos procesados
│   └── vectors/              # Índices vectoriales FAISS
├── models/
│   └── jina-embeddings-v4/   # Modelo de embeddings Jina
├── logs/                     # Registros del sistema
│   └── .gitkeep
├── docs/
│   └── INSTALL_FLASH_ATTENTION.md
├── .gitignore
├── main.py                   # Entrada principal del programa
├── requirements.txt          # Dependencias Python
├── OPTIMIZATION_SUMMARY.md   # Informe resumen de optimización
└── README.md                # Documentación del proyecto
```

## 🔧 Tecnologías de Optimización Clave

### 1. Arquitectura de Recuperación por Capas Inteligente

```python
# Ajustar estrategia de recuperación dinámicamente según complejidad de consulta
def smart_retrieve(self, query: str, max_context_chars: int = None):
    # Consulta de una provincia: 30 chunks, 40000 caracteres
    # Consulta multi-provincia: 15 chunks por provincia, 60000 caracteres
    # Consulta de comparación: 25 chunks por provincia, 100000 caracteres
    # Consulta general: 60 chunks, 100000 caracteres
```

### 2. Mecanismo de Agregación de Chunks Adyacentes

```python
def get_adjacent_chunks(self, chunk: DocumentChunk, window: int = 1):
    # Obtener automáticamente chunks adyacentes antes y después del chunk objetivo
    # Asegurar continuidad y completitud del contexto
    # Mejorar precisión de recuperación de información
```

### 3. Estrategia de Truncamiento Optimizada

```python
def _truncate_results(self, result: RetrievalResult, max_chars: int):
    # Ordenar por puntuación de densidad de información
    # Priorizar información de alto valor
    # Truncar inteligentemente contenido excesivamente largo
```

### 4. Ingeniería de Prompts Mejorada

```python
def _build_prompt(self, query: str, context: str, output_format: str):
    # Posicionamiento profesional de rol
    # Requisitos de formato detallados
    # Mecanismo de verificación de completitud
    # Prioridad de datos cuantitativos
```

## 🙏 Agradecimientos

### Fuente de Datos
Agradecimientos por proporcionar datos de informes de trabajo gubernamentales de 31 provincias, haciendo este proyecto listo para usar y conveniente para investigadores y desarrolladores.

### Contribuciones de Código Abierto
Bienvenido a enviar Issues y Pull Requests para mejorar este proyecto juntos:
- 🐛 Reportar errores
- 💡 Sugerir nuevas funcionalidades  
- 📝 Mejorar documentación
- 🔧 Optimización de código

## 📈 Monitoreo de Rendimiento

### Estadísticas del Sistema

El sistema muestra estadísticas detalladas al inicio:
```
📊 Estadísticas del Sistema: 
- Chunks totales de documentos: 855
- Provincias cubiertas: 31
- Dimensiones vectoriales: 2048
- Estadísticas de distribución de documentos por provincia
```

### Métricas de Rendimiento de Consulta

Cada consulta muestra:
- Cantidad de chunks recuperados
- Cantidad de provincias cubiertas
- Cantidad de caracteres de contexto
- Tiempo de procesamiento
- Tasa de éxito

### Monitoreo de Registros

```bash
# Ver registros del sistema
tail -f logs/government_rag.log

# Buscar información de rendimiento
grep "Retrieval completed\|Processing time" logs/government_rag.log
```

## 🛠️ Solución de Problemas

### Problemas Comunes

1. **Problemas de Timeout de API**
   - Optimizado: Timeout de API aumentado de 60s a 180s
   - Timeout de procesamiento de consulta aumentado de 30s a 120s

2. **Limitación max_tokens**
   - Corregido: Ajustado a 8192 tokens soportados por el modelo
   - Evita errores HTTP 400

3. **Memoria Insuficiente**
   ```bash
   # Verificar memoria disponible
   python -c "import psutil; print(f'Memoria disponible: {psutil.virtual_memory().available / 1024**3:.1f}GB')"
   ```

4. **Falla al Cargar Modelo**
   ```bash
   # Verificar si archivos de modelo local están completos
   ls -la models/jina-embeddings-v4/models--jinaai--jina-embeddings-v4/snapshots/
   
   # Si archivos de modelo local están corruptos o faltantes, puede volver a descargar
   # Eliminar temporalmente parámetro local_files_only para descarga
   python -c "
   from src.embedding_manager import JinaEmbeddingManager
   manager = JinaEmbeddingManager()
   manager.download_and_load_model()
   "
   ```

### Recomendaciones de Optimización de Rendimiento

1. **Habilitar Aceleración GPU**: Asegurar que el entorno CUDA está configurado correctamente
2. **Gestión de Memoria**: Recomendar 32GB de memoria para rendimiento óptimo
3. **Optimización de Red**: Asegurar conexión de red estable para API
4. **Mantenimiento Regular**: Limpiar archivos de registro y caché temporal

## 📋 Dependencias

Paquetes principales de dependencia:

```txt
python-docx==0.8.11      # Análisis de documentos Word
faiss-cpu==1.7.4         # Búsqueda de similitud vectorial
transformers==4.36.2     # Soporte de modelos preentrenados
torch==2.1.2             # Marco de aprendizaje profundo
numpy==1.24.3            # Cálculo numérico
pandas==2.0.3            # Procesamiento de datos
requests==2.31.0         # Solicitudes HTTP
tqdm==4.66.1             # Visualización de barra de progreso
scikit-learn==1.3.2      # Herramientas de aprendizaje automático
jieba==0.42.1            # Segmentación de palabras en chino
```

## 🔄 Registro de Actualizaciones

### v2.1.0 (Última versión - Edición de Optimización de Rendimiento)
- 🚀 **Mejora mayor de rendimiento**: Velocidad de respuesta 3-5 veces mayor, consulta única optimizada de 68s a 15-25s
- ⚡ **Optimización concurrente de API**: Soporte para API oficial de DeepSeek, 5-8 solicitudes concurrentes, procesamiento por lotes 4 veces más rápido
- 💾 **Sistema de caché inteligente**: Caché TTL de 24 horas, respuestas en milisegundos para consultas idénticas, monitoreo de tasa de aciertos en caché
- 🎯 **Aceleración de búsqueda vectorial**: Selección inteligente de índice FAISS, búsqueda acelerada por GPU, ajuste dinámico de parámetros
- 🔄 **Optimización de procesamiento por lotes**: Ejecución de lotes concurrentes, procesamiento paralelo de consultas multi-provincia
- 📊 **Optimización de configuración**: Parámetros de timeout optimizados, tamaño de lote, gestión de hilos de trabajo concurrentes
- 🛠️ **Cambio de proveedor API**: Soporte para cambio inteligente entre API DeepSeek/SiliconFlow, script de cambio con un clic

### v2.0.0 
- ✅ **Optimización Mayor**: Implementada optimización de Fase 1 sin rechunking
- ✅ **Mejora de Capacidad de Recuperación**: Mejora promedio de profundidad de recuperación del 100%
- ✅ **Expansión de Contexto**: Soporte para contexto largo de 100K caracteres
- ✅ **Mejora de Funcionalidades**: Agregación de chunks adyacentes, truncamiento inteligente, prompt mejorado
- ✅ **Estabilidad del Sistema**: Timeout de API optimizado, limitación max_tokens corregida
- ✅ **Limpieza de Código**: Eliminado todo código de prueba, entorno de producción limpio
- ✅ **Mejora de Documentación**: README y informe resumen de optimización actualizados
- ✅ **Optimización de Modelo Local**: Fuerza uso de archivos de modelo local, evita descargas por red, mejora velocidad de inicio del sistema

### v1.0.0
- ✅ Implementación básica del sistema RAG
- ✅ Soporte para informes de trabajo gubernamentales de 31 provincias
- ✅ Funcionalidad básica de consulta y recuperación

## 🎯 Características del Proyecto

El valor central de este proyecto reside en:

1. **Orientado a Problemas**: Aborda específicamente la recuperación de información incompleta y datos insuficientes para comparaciones multi-provincia
2. **Innovación Técnica**: Arquitectura innovadora de recuperación por capas inteligentes y mecanismo de agregación de chunks adyacentes
3. **Optimización de Rendimiento**: Mejora del 100% en volumen de información mediante optimización sistemática
4. **Listo para Producción**: Todo código de prueba limpiado, adecuado para despliegue en entorno de producción
5. **Documentación Completa**: Guías detalladas de instalación, uso y solución de problemas

## 📞 Soporte Técnico

Para preguntas o sugerencias, por favor:
1. Revisar la sección de solución de problemas en este README
2. Revisar archivos de registro `logs/government_rag.log`
3. Consultar el informe de optimización `OPTIMIZATION_SUMMARY.md`
4. Enviar Issues o contactar al equipo de desarrollo

---

**🎉 ¡El sistema ha completado optimizaciones mayores, logrando mejoras significativas en la completitud de recuperación de información y el detalle de datos de comparación multi-provincia!**
