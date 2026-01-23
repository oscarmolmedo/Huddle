const express = require('express');
const helmet = require('helmet');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const authRoutes = require('./routes/authRoutes');
const app = express();
const session = require('express-session');
const rateLimit = require('express-rate-limit');
require('dotenv').config();




// --- Configuración de Rate Limiting ---
const apiLimiter = rateLimit({
    //windowMs: 15 * 60 * 1000, // 15 minutos
    windowMs: 30 * 1000, // 30 segundos
    max: 5, // Máximo 100 peticiones por ventana por IP
    message: "Demasiadas peticiones desde esta IP, intenta de nuevo en 15 minutos"
});

// Aplicar a todas las rutas o solo a auth
app.use('/api/auth/', apiLimiter);

// --- Middlewares de Seguridad y Utilidad ---
app.use(helmet()); // Protege cabeceras
app.use(cors()); // Control de acceso
app.use(express.json()); // Permite leer JSON en el body
app.use(cookieParser()); // Permite manejar cookies

app.use(session({
    secret: process.env.SESSION_SECRET || 'secreto_temporal',
    resave: false,
    saveUninitialized: false,
    cookie: {
        httpOnly: true, // Evita que JS del cliente lea la cookie (previene XSS)
        secure: false,  // Cambiar a 'true' cuando tengas HTTPS
        maxAge: 3600000 // 1 hora de vida
    }
}));

// --- Rutas ---
app.use('/api/auth', authRoutes);

const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.send('🛡️ Servidor Seguro Operativo');
});

// app.post('/login', (req, res) => {
//     // Este endpoint ahora está manejado en authRoutes
//     res.status(404).json({ message: "Usa /api/auth/login para iniciar sesión" });
// });

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});