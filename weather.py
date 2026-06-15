import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# https://www.weatherapi.com/api-explorer.aspx comparto el enlace que contiene la información de la API que estamos utilizando para este homework.
# Si la url se construye correctamente deberia verse algo como así: https://api.weatherapi.com/v1/forecast.json?key=448e2268743e45c199884512230108&q=tenerife&days=3&aqi=no&alerts=no&hour=24

class Weather:
  def __init__(self):
    self.base_url = "https://api.weatherapi.com/v1/forecast.json"
    self.api_key = os.getenv("WEATHER_API_KEY")

  def get_weather(self, q= 'Tenerife', days_from_now=3):
    """Retorna el clima actual de Tenerife especifica. Puede recibir otro parametro 'q' para buscar otra ciudad. Por defecto tiene el valor de 'Tenerife' y 3 días de pronostico."""
    
    if not self.api_key:
      return {"error": "WEATHER_API_KEY no está configurada. Revisa tu archivo .env"}

    url = f"{self.base_url}?q={q}&key={self.api_key}&days={days_from_now}&alerts=no&hour=24"

    try:
      response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
      return {"error": f"No se pudo conectar con la API del clima: {e}"}

    try:
      data = response.json()
    except json.JSONDecodeError:
      return {"error": "La API devolvio una respuesta invalida (no es JSON)"}

    if response.status_code != 200:
      mensaje = data.get("error", {}).get("message", "Error desconocido")
      return {"error": f"Error de la API ({response.status_code}): {mensaje}"}


    forecast_days = [{
      'date': day['date'],
      'max_temp': day['day']['maxtemp_c'],
      'min_temp': day['day']['mintemp_c'],
      'condition': day['day']['condition']['text']
    } for day in data['forecast']['forecastday']]

    return forecast_days

  def get_weather_tool_schema(self):
    """Retorna el schema de la funcion get_weather que se utiliza para obtener el clima actual de una ciudad. El schema se utiliza para que el modelo de lenguaje pueda entender la funcion y utilizarla correctamente."""
    
    return {
      "type": "function",
      "name": "get_weather",
      "description": "Retorna el clima actual y de los proximos 3 días de Tenerife. Por defecto tiene el valor de 'Tenerife' y 3 días de pronostico. Puede recibir otro parametro 'q' para buscar otra ciudad.",
      "parameters": {
          "type": "object",
          "properties": {
              "q": {
                "type": "string",
                "description": "Nombre de la ciudad del que se quiere obtener el clima. Por Ejemplo: 'Tenerife', 'Madrid', 'London'"
              },
              "days_from_now": {
                "type": "integer",
                "description": "Número de días desde hoy del que se quiere obtener el clima. Por Ejemplo: 1, 2, 3"
              }
          },
          "required": ["q", "days_from_now"],
          "additionalProperties": False
      }
    }