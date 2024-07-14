import requests
from opencage.geocoder import OpenCageGeocode

# Claves API
api_key_graphhopper = '64b48f33-ba36-4363-b401-3f7531aa1103'
api_key_opencage = 'fabc278e50cb4a5093c8e9219b99a534'

# Inicializa el geolocalizador de OpenCage
geocoder = OpenCageGeocode(api_key_opencage)

def get_coordinates_and_country(city_name):
    result = geocoder.geocode(city_name)
    if result:
        location = result[0]
        return (location['geometry']['lat'], location['geometry']['lng'], location['components']['country'])
    else:
        return None

def get_route(start, end, vehicle):
    url = f"https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{start[0]},{start[1]}", f"{end[0]},{end[1]}"],
        "vehicle": vehicle,
        "locale": "es",
        "calc_points": True,
        "key": api_key_graphhopper
    }
    response = requests.get(url, params=params)
    return response

def main():
    while True:
        city1 = input("Ingrese la Ciudad de Origen: ")
        city2 = input("Ingrese la Ciudad de Destino: ")

        start_location = get_coordinates_and_country(city1)
        end_location = get_coordinates_and_country(city2)

        if start_location is None or end_location is None:
            print("No se pudieron obtener las coordenadas de una o ambas ciudades. Verifique los nombres e inténtelo de nuevo.")
            continue

        print(f"\nCiudad de Origen: {city1}, País: {start_location[2]}")
        print(f"Ciudad de Destino: {city2}, País: {end_location[2]}")

        modes_of_transport = {
            "1": "car",
            "2": "foot"
        }

        print("\nSeleccione el medio de transporte:")
        print("1. Auto")
        print("2. Caminando")
        transport_choice = input("Ingrese el número correspondiente: ")
        vehicle = modes_of_transport.get(transport_choice)

        if vehicle is None:
            print("Opción no válida. Inténtelo de nuevo.")
            continue

        route_response = get_route(start_location, end_location, vehicle)
        if route_response.ok:
            route_info = route_response.json()
            distance_km = route_info['paths'][0]['distance'] / 1000
            distance_miles = distance_km * 0.621371
            time_hours = route_info['paths'][0]['time'] / 3600000

            print(f"\nDistancia: {distance_km:.2f} km ({distance_miles:.2f} millas)")
            print(f"Duración del viaje: {time_hours:.2f} horas")
            print(f"\nNarrativa del viaje: Desde {city1} a {city2} en {vehicle.capitalize()}.")

        else:
            print(f"\nFallo al obtener la ruta - {route_response.status_code}")
            print(f"Mensaje de error: {route_response.text}")

        salir = input("\n¿Desea salir? (s para salir, cualquier otra tecla para continuar): ")
        if salir.lower() == 's':
            break

if __name__ == "__main__":
    main()

