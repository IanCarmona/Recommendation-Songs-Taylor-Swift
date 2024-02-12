import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from mpl_toolkits.mplot3d import Axes3D

# Cargar el archivo CSV con las canciones
songs_df = pd.read_csv("./canciones_letras_juntas.csv")

# El texto ingresado
input_text = "Heartbreak is like a cold winter in the heart. Words turn hurtful, and happy memories fade into a sigh of melancholy. Every sad song becomes an echo of what once was, and tears are the only companions on lonely nights. Places that used to be special turn gloomy and empty, and the love that once felt so strong dissipates into the distance. Heartbreak is a silent pain carried in the chest, an invisible wound that only time can heal."

#input_text = "Sunshine fills the sky, and a gentle breeze dances through the trees. Laughter and joy are the soundtrack of the day, and every moment is a new reason to smile. Friends gather, sharing stories and dreams, and the world feels full of endless possibilities. With a heart full of gratitude and a spirit brimming with happiness, life is a beautiful adventure, and every day is a treasure to be cherished."

# Procesar el texto y las letras de las canciones para calcular la similitud
stop_words = set(stopwords.words('english'))

# Tokenizar y preprocesar el texto de entrada sin stopwords
input_words = [word for word in word_tokenize(input_text.lower()) if word.isalnum() and word not in stop_words]

# Tokenizar y preprocesar las letras de las canciones sin stopwords
songs_df['lyrics_cleaned'] = songs_df['lyrics'].apply(lambda x: ' '.join([word for word in word_tokenize(x.lower()) if word.isalnum() and word not in stop_words]))

# Crear un vectorizador para contar las palabras en las letras de las canciones
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(songs_df['lyrics_cleaned'])

# Transformar el texto de entrada usando el mismo vectorizador
input_vector = vectorizer.transform([" ".join(input_words)])

# Calcular la similitud de coseno entre el texto de entrada y las letras de todas las canciones
similarities = cosine_similarity(input_vector, X)

# Agregar la columna 'similarity' al DataFrame de canciones
songs_df['similarity'] = similarities[0]

# Ordenar las canciones por similitud en orden descendente
songs_df = songs_df.sort_values(by='similarity', ascending=False)

# Tomar las 10 canciones más similares
top_10_songs = songs_df.head(5)

# Aplicar PCA para reducir la dimensionalidad a 3 componentes
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X.toarray())

# Agregar el texto de entrada a los datos PCA
input_pca = pca.transform(input_vector.toarray())

# Visualizar los datos en un gráfico 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Dibujar los puntos de las canciones en el Top 10
for i, row in top_10_songs.iterrows():
    ax.scatter(X_pca[i, 0], X_pca[i, 1], X_pca[i, 2], label=row['track_title'])

# Dibujar el punto del texto de entrada en rojo
ax.scatter(input_pca[:, 0], input_pca[:, 1], input_pca[:, 2], label="Texto de Entrada", color='black')

# Etiquetar los puntos con el nombre de la canción
for i, row in top_10_songs.iterrows():
    ax.text(X_pca[i, 0], X_pca[i, 1], X_pca[i, 2], row['track_title'], fontsize=8)

ax.set_xlabel("Componente Principal 1")
ax.set_ylabel("Componente Principal 2")
ax.set_zlabel("Componente Principal 3")
ax.set_title("Vectorización de Canciones y Texto de Entrada (Top 5 Canciones) en 3D")

plt.legend()
plt.show()

# Mostrar el Top 10 en la consola
print(top_10_songs[['album_name', 'track_title']])
