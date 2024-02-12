from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
import base64
from googletrans import Translator

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ruta_para_enviar_texto_a_python", methods=["POST"])
def procesar_texto():
    data = request.get_json()
    text = data["text"]
    
    # Traducir el texto de español a inglés
    translator = Translator()
    translated_text = translator.translate(text, src='es', dest='en').text
    # Cargar el archivo CSV con las canciones
    songs_df = pd.read_csv("./canciones_letras_juntas.csv")
    
    # El texto ingresado
    input_text = translated_text
    
    # Procesar el texto y las letras de las canciones para calcular la similitud
    stop_words = set(stopwords.words("english"))

    # Tokenizar y preprocesar el texto de entrada sin stopwords
    input_words = [
        word
        for word in word_tokenize(input_text.lower())
        if word.isalnum() and word not in stop_words
    ]

    # Tokenizar y preprocesar las letras de las canciones sin stopwords
    songs_df["lyrics_cleaned"] = songs_df["lyrics"].apply(
        lambda x: " ".join(
            [
                word
                for word in word_tokenize(x.lower())
                if word.isalnum() and word not in stop_words
            ]
        )
    )

    # Crear un vectorizador para contar las palabras en las letras de las canciones
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(songs_df["lyrics_cleaned"])

    # Transformar el texto de entrada usando el mismo vectorizador
    input_vector = vectorizer.transform([" ".join(input_words)])

    # Calcular la similitud de coseno entre el texto de entrada y las letras de todas las canciones
    similarities = cosine_similarity(input_vector, X)

    # Agregar la columna 'similarity' al DataFrame de canciones
    songs_df["similarity"] = similarities[0]

    # Ordenar las canciones por similitud en orden descendente
    songs_df = songs_df.sort_values(by="similarity", ascending=False)

    # Tomar las 10 canciones más similares
    top_10_songs = songs_df.head(5)

    # Aplicar PCA para reducir la dimensionalidad a 3 componentes
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X.toarray())

    # Agregar el texto de entrada a los datos PCA
    input_pca = pca.transform(input_vector.toarray())

    # Visualizar los datos en un gráfico 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Dibujar los puntos de las canciones en el Top 10
    for i, row in top_10_songs.iterrows():
        ax.scatter(X_pca[i, 0], X_pca[i, 1], X_pca[i, 2], label=row["track_title"], s=50)

    # Dibujar el punto del texto de entrada en rojo
    ax.scatter(
        input_pca[:, 0],
        input_pca[:, 1],
        input_pca[:, 2],
        label="Texto de Entrada",
        color="black",
        s=100,
    )

    # Etiquetar los puntos con el nombre de la canción
    for i, row in top_10_songs.iterrows():
        ax.text(X_pca[i, 0], X_pca[i, 1], X_pca[i, 2], row["track_title"], fontsize=12)

    ax.set_xlabel("Componente Principal 1")
    ax.set_ylabel("Componente Principal 2")
    ax.set_zlabel("Componente Principal 3")
    ax.set_title("Vectorización de Canciones y Texto de Entrada (Top 5 Canciones) en 3D")

    # Mostrar el Top 10 en la consola
    
    # Convertir la figura a una representación base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Mostrar el Top 10 en la consola
    print(top_10_songs[["album_name", "track_title"]])
    
    plt.close(fig)

    # Devolver los resultados al frontend
    return jsonify({
        "top_10_songs": top_10_songs.to_dict(orient='records'),
        "graph": img_str
    })

if __name__ == "__main__":
    app.run(debug=True)
    

    

    
