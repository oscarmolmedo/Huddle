const express = require('express');
const helmet = require('helmet');
const cookieParser = require('cookie-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();
const session = require('express-session');

const authRoutes = require('./routes/authRoutes');

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
        httpOnly: true, // 🛡️ Evita que JS del cliente lea la cookie (previene XSS)
        secure: false,  // 🛡️ Cambiar a 'true' cuando tengas HTTPS
        maxAge: 3600000 // 1 hora de vida
    }
}));

app.use('/api/auth', authRoutes);

const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.send('🛡️ Servidor Seguro Operativo');
});

app.post('/login', (req, res) => {
    // Este endpoint ahora está manejado en authRoutes
    res.status(404).json({ message: "Usa /api/auth/login para iniciar sesión" });
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});