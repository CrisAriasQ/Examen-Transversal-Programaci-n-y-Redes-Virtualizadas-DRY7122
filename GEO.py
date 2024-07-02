from geopy.geocoders import Nominatim
from geopy.distance import distance

def obtener_coordenadas(ciudad, pais):
    geolocator = Nominatim(user_agent="mi_app_geopy")
    location = geolocator.geocode(f"{ciudad}, {pais}")
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

def calcular_distancia(ciudad_origen, pais_origen, ciudad_destino, pais_destino):
    coords_origen = obtener_coordenadas(ciudad_origen, pais_origen)
    coords_destino = obtener_coordenadas(ciudad_destino, pais_destino)
    
    if coords_origen and coords_destino:
        dist_millas = distance(coords_origen, coords_destino).miles
        return dist_millas
    else:
        return None

def millas_a_kilometros(millas):
    return millas * 1.60934

def calcular_duracion_viaje(distancia, velocidad_promedio_coche):
    tiempo_horas = distancia / velocidad_promedio_coche
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)
    return horas, minutos

def obtener_narrativa(ciudad_origen, ciudad_destino, distancia, duracion_horas, duracion_minutos, medio_transporte):
    if medio_transporte.lower() == 'coche':
        medio = "coche"
    elif medio_transporte.lower() == 'avion':
        medio = "avión"
    else:
        medio = "medio de transporte"
        
    narrativa = f"Viajando desde {ciudad_origen} a {ciudad_destino}, que están a aproximadamente {distancia:.2f} millas de distancia en {medio}.\n"
    narrativa += f"El viaje tomaría aproximadamente {duracion_horas} horas y {duracion_minutos} minutos."
    return narrativa

def main():
    while True:
        ciudad_origen = input("Ingrese la ciudad de origen (en español): ")
        if ciudad_origen.lower() == 's':
            break
        
        pais_origen = input("Ingrese el país de origen (en español): ")
        
        ciudad_destino = input("Ingrese la ciudad de destino (en español): ")
        if ciudad_destino.lower() == 's':
            break
        
        pais_destino = input("Ingrese el país de destino (en español): ")
        
        medio_transporte = input("Ingrese el tipo de medio de transporte (coche/avion): ")
        
        distancia_millas = calcular_distancia(ciudad_origen, pais_origen, ciudad_destino, pais_destino)
        
        if distancia_millas is None:
            print("No se pudo calcular la distancia. Verifique las ciudades ingresadas.")
            continue
        
        distancia_km = millas_a_kilometros(distancia_millas)
        
        if medio_transporte.lower() == 'coche':
            velocidad_promedio_coche = 60  # millas por hora
            duracion_horas, duracion_minutos = calcular_duracion_viaje(distancia_millas, velocidad_promedio_coche)
        
        elif medio_transporte.lower() == 'avion':
            velocidad_promedio_avion = 800  # kilómetros por hora (ejemplo)
            duracion_horas, duracion_minutos = calcular_duracion_viaje(distancia_km, velocidad_promedio_avion)
        
        else:
            print("Tipo de medio de transporte no válido.")
            continue
        
        print(f"\nDistancia entre {ciudad_origen}, {pais_origen} y {ciudad_destino}, {pais_destino}:")
        print(f"- Millas: {distancia_millas:.2f} mi")
        print(f"- Kilómetros: {distancia_km:.2f} km")
        print(f"Duración del viaje en {medio_transporte}: {duracion_horas} horas y {duracion_minutos} minutos.")
        
        narrativa = obtener_narrativa(ciudad_origen, ciudad_destino, distancia_millas, duracion_horas, duracion_minutos, medio_transporte)
        print("\nNarrativa del viaje:")
        print(narrativa)
        
        opcion_salir = input("\n¿Desea salir? (s/n): ")
        if opcion_salir.lower() == 's':
            break

if __name__ == "__main__":
    main()
