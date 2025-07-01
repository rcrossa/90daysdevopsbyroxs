// Frontend entry point
document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    app.innerHTML = ''; // Limpiar el "Cargando..."

    // Título de bienvenida
    const welcome = document.createElement('h2');
    welcome.textContent = '¡Bienvenido a la aplicación Node-Mongo!';
    app.appendChild(welcome);

    // Información del puerto
    const portInfo = document.createElement('p');
    portInfo.textContent = 'Frontend corriendo en el puerto: 5173';
    portInfo.style.color = '#666';
    app.appendChild(portInfo);

    // Botón para probar la API
    const testButton = document.createElement('button');
    testButton.textContent = 'Probar conexión con API';
    testButton.addEventListener('click', testAPI);
    app.appendChild(testButton);

    // Div para mostrar respuesta de la API
    const apiResponse = document.createElement('div');
    apiResponse.id = 'api-response';
    apiResponse.style.marginTop = '20px';
    app.appendChild(apiResponse);
});

// Función para probar la API
async function testAPI() {
    const responseDiv = document.getElementById('api-response');
    
    try {
        const response = await fetch('http://localhost:3000/');
        const data = await response.text();
        responseDiv.innerHTML = `<p style="color: green;">✅ API Response: ${data}</p>`;
    } catch (error) {
        responseDiv.innerHTML = `<p style="color: red;">❌ Error: ${error.message}</p>`;
    }
}