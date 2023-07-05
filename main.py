#!/usr/bin/python3

import argparse
import requests


# Pagina a la que se le hará la petición
URL_PAGINA = "https://api.openweathermap.org/data/2.5/weather"
# API KEY obtenida en https://openweathermap.org/api
API_KEY = "649195894c39b3432ef154a14429a944"


def obtener_region() -> str:
    """
    Esta función hace una petición a la API de OpenWeatherMap y 
    devuelve la region/región en la que se encuentra el usuario.
    """

    # Obtener la región del usuario a través de la petición HTTP
    res = requests.get("https://ipapi.co/region", headers={"User-agent": "Mozilla/5.0"})

    # Si la respuesta del servidor a la petición es 200, entonces todo está bien
    if res.status_code == 200:
        # Retorna el contenido que se obtuvo de la petición
        return res.content.decode("utf-8")
    # Se devuelve un valor por defecto en caso de no entrar en el if
    return "Atlixco"


def unidad_medida(unidad: str) -> str:
    """
    Esta función devuelve la unidad de medida en la que se encuentra el usuario.
    """
    #  Diccionario que almacena las unidades de medida con su respectiva clave
    val = {
        "metric": "ºC",
        "imperial": "ºF",
        None: " K"
    }
    # Devuelve el valor de la key que ingrese, en caso de no haber una coincidencia
    # devolverá un valor por defecto
    return val.get(unidad, " K")


def icono_correspondiente(icono: str) -> str:
    """
    Retorna un icono según el código que se le pase como parámetro.
    """
    # d -> dia; n -> noche
    ico = {
        "01d": "  Cielo limpio ",  # Cielo limpio
        "01n": " ",  # 
        "02d": "  Pocas nubes ",  # Pocas nubes
        "02n": " ",  # 
        "03d": "  Nubes dispersas ",  # Nubes dispersas
        "03n": " ",  # 
        "04d": "摒  Nubes rotas ",  # Nubes rotas
        "04n": " ",  # 
        "09d": "  Aguacero ",  # Aguacero
        "09n": " ",  # 
        "10d": "  LLuvia ",  # LLuvia
        "10n": " ",  # 
        "11d": "朗  Tormenta ",  # Tormenta
        "11n": "朗 ",  # 
        "13d": "  Nieve ",  # Nieve
        "13n": " ",  # 
        "50d": "  Niebla ",  # Niebla
        "50n": " ",  # 
        None: "  "
    }

    # En caso de no encontrar key que coincida se retronará un valor por defecto
    return ico.get(icono, " ")


def obtener_temp(region: str, medida: str) -> dict[str, str] | None:
    try:
        # Hace la petición a la API pasando los parámetros de la región, idioma, media y API_KEY y
        # trae los datos en formato JSON
        datos = requests.get(f"{URL_PAGINA}?q={region}&units={medida}&appid={API_KEY}").json()

        # Trae la temperatura
        temperatura = datos["main"]["temp"]

        # Trae la unidad de medida a usar
        unidad = unidad_medida(medida)

        # Trae el icono correspondiente del clima
        icono = icono_correspondiente(datos["weather"][0]["icon"])

        # Retorna el icono correspondiente junto a la temperatura con su unidad de medida
        return {
            "icono": icono,
            "temperatura": f"{temperatura}{unidad}"
        }
    except Exception:
        return None


def main():
    # Argumentos de la linea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument( "-r", "--region", dest="region", type=str, help="indica la region a usar")
    parser.add_argument( "-u", "--unidad", dest="unidad", type=str, help="indica la region a usar")
    args = parser.parse_args()

    # Si no se ingresan parámetros, se obtienen los parámetros por defecto
    region = args.region if args.region else obtener_region()
    unidad = args.unidad if args.unidad else "metric"

    # Se obtienen los datos retornados, puede ser un diccionario o None
    temp = obtener_temp(region, unidad)
    if temp:  # En caso de no ser None...
        icono, temperatura = temp.values()  # ... Se obtienen los valores del diccionario
        print(f"{icono}{temperatura}")  # Se muestra el icono con su respectiva temperatura


if __name__ == "__main__":
    main()
