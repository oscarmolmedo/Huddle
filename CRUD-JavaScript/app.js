// app.js

const express = require('express');

// Importamos el Router que creamos en el Controlador
const startupRouter = require('./controllers/learningController'); 

const app = express();
const PORT = 3000; 

// 1. CONFIGURACIÓN DEL MOTOR DE PLANTILLAS
app.set('view engine', 'ejs'); 

// 2. CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
// Esto le dice a Express que sirva archivos de la carpeta 'public/'
// Si el navegador pide /style.css, Express lo buscará en public/style.css
//Tambien index hace referencia a js/main.js y css/styles.css
//main.js maneja la logica del front-end
//css/styles.css maneja los estilos
app.use(express.static('public'));

// Middleware para entender datos de formularios y JSON
app.use(express.urlencoded({ extended: true })); 
app.use(express.json());

// 3. USAR EL ROUTER PRINCIPAL
// Le decimos a Express: usa todas las rutas definidas en startupRouter
//El controlador dispara index.ejs en la ruta '/'
app.use('/', startupRouter); 


// 4. Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor Express ejecutándose en http://localhost:${PORT}`);
});