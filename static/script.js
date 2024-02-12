const button = document.getElementById('submitBtn');
const modal = document.getElementById('modal');
const top10Div = document.getElementById('top10');
const viewGraphBtn = document.getElementById('viewGraph');
const graphDiv = document.getElementById('graph');
const closeBtn = document.getElementsByClassName('close')[0];

button.addEventListener('click', async () => {
    const text = document.getElementById('entry').value;

    try {
        const response = await fetch('http://localhost:5000/ruta_para_enviar_texto_a_python', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        if (response.ok) {
            console.log('Texto enviado correctamente a Python');
            const data = await response.json();
            const top10 = data.top_10_songs.map(song => `${song.album_name} - ${song.track_title}`).join('<br>');

            top10Div.innerHTML = `<h3>Top 5 Canciones:</h3><div>${top10}</div>`;
            modal.style.display = 'block';

            viewGraphBtn.addEventListener('click', () => {
                graphDiv.innerHTML = `<img src="data:image/png;base64,${data.graph}" alt="Gráfico 3D">`;
                graphDiv.style.display = 'block';
            });
        } else {
            console.error('Error al enviar el texto a Python');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    graphDiv.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
        graphDiv.style.display = 'none';
    }
});
