const { exec } = require('child_process');

exec('python app.py', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error al ejecutar el script: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Error en el script: ${stderr}`);
        return;
    }
    console.log(`Resultado del cálculo: ${stdout}`);
});
