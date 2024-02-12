from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from nltk.corpus import stopwords

# Descargar la lista de stopwords si aún no lo has hecho
import nltk
nltk.download("stopwords")

sid = SentimentIntensityAnalyzer()

# Lista de nombres de archivos CSV a procesar.
archivos_csv = ["01-taylor_swift.csv", "02-fearless_taylors_version.csv", "03-speak_now_deluxe_package.csv", "04-red_deluxe_edition.csv", "05-1989_deluxe.csv", "06-reputation.csv", "07-lover.csv", "08-folklore_deluxe_version.csv", "09-evermore_deluxe_version.csv"]

# Crear un DataFrame vacío para almacenar los datos combinados.
datos_combinados = pd.DataFrame()

# Leer y combinar los datos de todos los archivos CSV.
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    datos_combinados = pd.concat([datos_combinados, df])

# Cargar la lista de stopwords de NLTK
stop_words = set(stopwords.words("english"))

# Función para eliminar las stopwords y unir toda la letra de la canción
def preprocess_lyric(text):
    words = text.split()
    words = [word for word in words if word.lower() not in stop_words]
    return " ".join(words)

# Aplicar la eliminación de stopwords y unión de la letra de la canción a la columna "lyric"
datos_combinados["lyric"] = datos_combinados["lyric"].apply(preprocess_lyric)

print(datos_combinados["lyric"])

# Calcular el sentimiento de toda la letra de la canción y almacenar los resultados en una nueva columna.
datos_combinados["lyric_sentimiento"] = datos_combinados.groupby(["album_name", "track_title", "track_n"])["lyric"].transform(lambda x: sid.polarity_scores(" ".join(x))['compound'])

# Eliminar las filas duplicadas y mantener una fila por canción.
result = datos_combinados.drop_duplicates(subset=["album_name", "track_title", "track_n"])[["album_name", "track_title", "track_n", "lyric_sentimiento"]]

# Guardar el resultado en un nuevo archivo CSV.
result.to_csv("todas_las_canciones_sentimientos.csv", index=False)
