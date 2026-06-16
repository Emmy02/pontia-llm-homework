# pontia-llm-homework

## Configuración del entorno (.env)

El proyecto usa [python-dotenv](https://pypi.org/project/python-dotenv/) para cargar variables de entorno desde un archivo `.env` en la raíz del proyecto.

1. Copia `.env.example` a `.env`:

   ```bash
   cp .env.example .env
   ```

> **Nota:** Tuve un inconveniente con el OPENIA_API_KEY que usted me creó, por eso he tenido que utilizar mi propia KEY. Compartire la keys por discord.


2. Completa las siguientes variables en tu `.env`:

   | Variable          | Descripción                                                                 |
   |-------------------|------------------------------------------------------------------------------|
   | `WEATHER_API_KEY` | API key de [WeatherAPI](https://www.weatherapi.com/) usada por `weather.py`. |
   | `OPENAI_API_KEY`  | API key de OpenAI, si el proyecto la utiliza como proveedor de LLM.          |


## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Weather.py
Obtiene el clima actual y el pronóstico para una ciudad.

- **`q`** (`str`, por defecto `'Tenerife'`): nombre de la ciudad a consultar (por ejemplo, `'Madrid'`).
- **`days_from_now`** (`int`, por defecto `3`): número de días de pronóstico a solicitar.

Devuelve el JSON de la respuesta de WeatherAPI. En caso de error devuelve un diccionario `{"error": "..."}` cuando:
- No está configurada `WEATHER_API_KEY`.
- Falla la conexión con la API (timeout, red, etc.).
- La respuesta no es un JSON válido.
- La API responde con un código de estado distinto de 200.

### `Weather.get_weather_tool_schema()`

Devuelve el *schema* de la función `get_weather` en el formato esperado por modelos de lenguaje con *function calling* (tipo OpenAI/Gemini tools). Describe el nombre, la descripción y los parámetros (`q`, `days_from_now`) que el modelo debe usar para invocar `get_weather` correctamente.



## tenerife-rag.ipynb
Este archivo tiene toda la lógica del proyecto. Hace lo siguiente:

1. Importa la clase `Weather` de `weather.py`.
  1.1. Usa la función `get_weather` para obtener el pronóstico del tiempo para Tenerife.
  1.2. Usa la función `get_weather_tool_schema` para obtener el schema de la función `get_weather` que el LLM usará para obtener información del clima de Tenerife.

2. Importar todas los modulos necesarios para llevar a cabo el proyecto.
3. Utiliza una funcion llamada `search_tenerife_docs` y `search_tenerife_guide` para compartir datos del PDF con el LLM según sea necesario.
4. Definimos instrucciones `TENERIFE_ASSISTANT_INSTRUCTIONS` y comenzamos a hacer pruebas cada vez mas complejas.


