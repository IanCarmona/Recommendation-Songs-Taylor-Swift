import pandas as pd

# Leer el archivo CSV que contiene los sentimientos
df = pd.read_csv("./todas_las_canciones_sentimientos.csv")

# Crear tres DataFrames para canciones con sentimientos negativos, neutros y positivos
df_negativos = df[(df["lyric_sentimiento"] >= -1) & (df["lyric_sentimiento"] < -0.5)]
df_neutros = df[(df["lyric_sentimiento"] >= -0.5) & (df["lyric_sentimiento"] < 0.5)]
df_positivos = df[(df["lyric_sentimiento"] >= 0.5) & (df["lyric_sentimiento"] <= 1)]

# Guardar cada DataFrame en un archivo CSV separado
df_negativos.to_csv("sentimientos_negativos.csv", index=False)
df_neutros.to_csv("sentimientos_neutros.csv", index=False)
df_positivos.to_csv("sentimientos_positivos.csv", index=False)
