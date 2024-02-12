import pandas as pd

# Lista de nombres de archivos CSV a procesar.
archivos_csv = ["01-taylor_swift.csv", "02-fearless_taylors_version.csv", "03-speak_now_deluxe_package.csv", "04-red_deluxe_edition.csv", "05-1989_deluxe.csv", "06-reputation.csv", "07-lover.csv", "08-folklore_deluxe_version.csv", "09-evermore_deluxe_version.csv"]

# Crear un DataFrame vacío para almacenar los datos combinados.
datos_combinados = pd.DataFrame()

# Leer y combinar los datos de todos los archivos CSV.
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    datos_combinados = pd.concat([datos_combinados, df])

# Crear un diccionario para almacenar las letras de las canciones juntas
letras_canciones = {}

# Combinar las letras de las canciones para cada álbum, título y número de canción
for album, titulo, numero, letra in zip(datos_combinados["album_name"], datos_combinados["track_title"], datos_combinados["track_n"], datos_combinados["lyric"]):
    clave = (album, titulo, numero)
    if clave in letras_canciones:
        letras_canciones[clave] += " " + letra
    else:
        letras_canciones[clave] = letra

# Crear listas separadas para álbum, título, número de canción y letras
albumes = []
titulos = []
numeros = []
letras = []

for clave, letra in letras_canciones.items():
    album, titulo, numero = clave
    albumes.append(album)
    titulos.append(titulo)
    numeros.append(numero)
    letras.append(letra)

# Crear un DataFrame con las letras de las canciones juntas
letras_df = pd.DataFrame({"album_name": albumes, "track_title": titulos, "track_n": numeros, "lyrics": letras})

# Guardar el resultado de las letras en un archivo CSV
archivo_salida_letras = "canciones_letras_juntas.csv"
letras_df.to_csv(archivo_salida_letras, index=False)
