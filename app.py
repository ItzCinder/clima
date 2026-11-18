import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Cliente con caché de 1 hora y reintentos
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Diccionario para traducir los códigos meteorológicos (WMO) de Open-Meteo
ESTADOS_CLIMA = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna densa",
    61: "Lluvia leve",
    63: "Lluvia moderada",
    65: "Lluvia fuerte",
    71: "Nieve leve",
    73: "Nieve moderada",
    75: "Nieve fuerte",
    80: "Chubascos leves",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    95: "Tormenta eléctrica",
    96: "Tormenta con granizo leve",
    99: "Tormenta con granizo fuerte",
}

def search_location(search: str, limit: int = 10) -> list[dict]:
    """resultados = search_location("Montevideo")

# for i, lugar in enumerate(resultados, start=1):
#     print(f"{i}. {lugar['etiqueta']} ({lugar['lat']}, {lugar['lon']})")
    Recibe un texto de búsqueda y devuelve una lista de diccionarios
    con las localizaciones coincidentes.
    """
    if not search or not search.strip():
        return []

    res = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": search.strip(), "count": 10, "language": "es"},
        timeout=5
    ).json()

    resultsRaws = res.get("results", [])

    # Filtrado para descartar calles, estaciones, hoteles, etc
    # resultsFiltered = [
    #    site for site in resultsRaws
    #    if site.get("feature_code", "").startswith(("PPL", "PCLI"))
    # ]

    # Ordenar de mayor a menor la población
    resultsOrdered = sorted(
        resultsRaws,
        key=lambda site: site.get("population", 0),
        reverse=True
    )

    coincidences = []
    locations_seen = set()
    for site in resultsOrdered[:limit]:
        name = site.get("name", "")
        region = site.get("admin1", "")
        country = site.get("country", "")
        label = ", ".join(filter(None, [name, region, country]))

        location_key = (
            name.lower(),
            region.lower(),
            country.lower(),
            round(site["latitude"], 4),
            round(site["longitude"], 4),
        )
        if location_key in locations_seen:
            continue

        locations_seen.add(location_key)
        coincidences.append({
            "etiqueta": label,
            "nombre": name,
            "region": region,
            "pais": country,
            "lat": site["latitude"],
            "lon": site["longitude"],
        })

    return coincidences


# resultados = search_location("Montevideo")

# for i, lugar in enumerate(resultados, start=1):
#     print(f"{i}. {lugar['etiqueta']} ({lugar['lat']}, {lugar['lon']})")