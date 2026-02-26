const express               = require('express');
const helmet                = require('helmet');
const cookieParser          = require('cookie-parser');
const cors                  = require('cors');
const app                   = express();
const session               = require('express-session');
const rateLimit             = require('express-rate-limit');

// Se exporta archivos y configuraciones de entorno
require('dotenv').config();                         
const PORT                  = process.env.PORT;     
const authRoutes = require('./routes/authRoutes');  

// --- Configuración de Rate Limiting ---
const apiLimiter = rateLimit({
    //windowMs: 15 * 60 * 1000,     
    windowMs: 30 * 1000,            // 30 segundos
    max: 5,                         
    message: "Demasiadas peticiones desde esta IP, intenta de nuevo en 30 segundos"
});


//No bloquea ip de proxy sino la del cliente
app.set('trust proxy', 1);          // Si estás detrás de un proxy (como Heroku, Nginx, etc.)


// --- Middlewares de Seguridad y Utilidad ---
app.use(helmet());                  // Protege cabeceras
app.use(cors());                    // Control de acceso
app.use(express.json());            // Permite leer JSON en el body
app.use(cookieParser());            // Permite manejar cookies
app.use(express.urlencoded({ extended: true })); // Permite leer datos de formularios | Para pruebas con Postman

// Configuración de sesiones (Cookies)
app.use(session({
    secret: process.env.SESSION_SECRET || 'secreto_temporal',
    resave: false,
    saveUninitialized: false,
    cookie: {
        httpOnly: true,             // Evita que JS del cliente lea la cookie (previene XSS)
        secure: false,              // Cambiar a 'true' para usar HTTPS
        maxAge: 3600000             // 1 hora de vida
    }
}));



// --- Rutas ---
app.use('/api/auth', apiLimiter);   // Aplicar rate limiting a todas las rutas de autenticación
app.use('/api/auth', authRoutes);   // Rutas de autenticación

// Ruta de prueba para verificar que el servidor está corriendo
app.get('/', (req, res) => {
    res.send('🛡️ Servidor Seguro Operativo');
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});