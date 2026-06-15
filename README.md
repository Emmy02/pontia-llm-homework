# pontia-llm-homework

## Configuración del entorno (.env)

El proyecto usa [python-dotenv](https://pypi.org/project/python-dotenv/) para cargar variables de entorno desde un archivo `.env` en la raíz del proyecto.

1. Copia `.env.example` a `.env`:

   ```bash
   cp .env.example .env
   ```

2. Completa las siguientes variables en tu `.env`:

   | Variable          | Descripción                                                                 |
   |-------------------|------------------------------------------------------------------------------|
   | `WEATHER_API_KEY` | API key de [WeatherAPI](https://www.weatherapi.com/) usada por `weather.py`. |
   | `GEMINI_API_KEY`  | API key de Google Gemini, si el proyecto la utiliza como proveedor de LLM.   |
   | `OPENAI_API_KEY`  | API key de OpenAI, si el proyecto la utiliza como proveedor de LLM.          |

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Weather.py

`weather.py` define la clase `Weather`, que encapsula el acceso a la API de pronóstico del clima de [WeatherAPI](https://www.weatherapi.com/v1/forecast.json).

### `Weather.__init__()`

Lee `WEATHER_API_KEY` desde las variables de entorno (cargadas vía `.env`) y configura la URL base de la API (`https://api.weatherapi.com/v1/forecast.json`).

### `Weather.get_weather(q='Tenerife', days_from_now=1)`

Obtiene el clima actual y el pronóstico para una ciudad.

- **`q`** (`str`, por defecto `'Tenerife'`): nombre de la ciudad a consultar (por ejemplo, `'Madrid'`, `'London'`).
- **`days_from_now`** (`int`, por defecto `1`): número de días de pronóstico a solicitar.

Devuelve el JSON de la respuesta de WeatherAPI. En caso de error devuelve un diccionario `{"error": "..."}` cuando:
- No está configurada `WEATHER_API_KEY`.
- Falla la conexión con la API (timeout, red, etc.).
- La respuesta no es un JSON válido.
- La API responde con un código de estado distinto de 200.

### `Weather.get_weather_tool_schema()`

Devuelve el *schema* de la función `get_weather` en el formato esperado por modelos de lenguaje con *function calling* (tipo OpenAI/Gemini tools). Describe el nombre, la descripción y los parámetros (`q`, `days_from_now`) que el modelo debe usar para invocar `get_weather` correctamente.

### Ejemplo de uso

```python
from weather import Weather

weather = Weather()
print(weather.get_weather("Tenerife"))
```
