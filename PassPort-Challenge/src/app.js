const express               = require('express');
const helmet                = require('helmet');
const cookieParser          = require('cookie-parser');
const cors                  = require('cors');
const app                   = express();
const session               = require('express-session');
const rateLimit             = require('express-rate-limit');
const { doubleCsrf } = require('csrf-csrf'); 


require('dotenv').config();                         

const PORT                  = process.env.PORT;
const SECRETRO              = process.env.JWT_SECRET;    
const authRoutes = require('./routes/authRoutes');  



//No bloquea ip de proxy sino la del cliente
app.set('trust proxy', 1);          // Si estás detrás de un proxy (como Heroku, Nginx, etc.)

// --- Middlewares de Seguridad y Utilidad ---
app.use(helmet());                  // Protege cabeceras
app.use(cors({origin: `http://localhost:${PORT}`, credentials: true}));                    // Control de acceso
app.use(express.json());            // Permite leer JSON en el body
app.use(cookieParser(SECRETRO));            // Permite manejar cookies
app.use(express.urlencoded({ extended: true })); // Permite leer datos de formularios | Para pruebas con Postman

// --- Configuración de Rate Limiting ---
const apiLimiter = rateLimit({
    //windowMs: 15 * 60 * 1000,     
    windowMs: 30 * 1000,            // 30 segundos
    max: 5,                         
    message: "Demasiadas peticiones desde esta IP, intenta de nuevo en 30 segundos"
});

// // Configuración de sesiones (Cookies)
app.use(session({
    secret: SECRETRO,
    resave: false,
    saveUninitialized: true,
    cookie: {
        httpOnly: true,                                 // Evita que JS del cliente lea la cookie (previene XSS)
        secure: process.env.NODE_ENV === 'production',              
        sameSite: 'lax',
        maxAge: 3600000                                 // 1 hora de vida
    }
}));


// --- 1. Configuración de Double CSRF ---
const doubleCsrfOptions = {
    getSecret: () => SECRETRO,
    cookieName: "csrfToken", 
    getSessionIdentifier: (req) => req.sessionID,
    cookieOptions: {
        httpOnly: true,
        sameSite: "Lax",
        secure: process.env.NODE_ENV === 'production',
    },
    size: 64,
    ignoredMethods: ["GET"],
    getTokenFromRequest: (req) => req.headers["x-csrf-token"], 
};

// Desestructuramos DESPUÉS de tener las opciones claras
const {
    invalidCsrfTokenErrorMiddleware,
    generateCsrfToken,
    doubleCsrfProtection,
} = doubleCsrf(doubleCsrfOptions);



// --- Rutas ---
// ---Para obtener el Token---
app.get('/api/get-csrf-token', (req, res) => {
    console.log("ID de sesión al generar:", req.sessionID);
    const token = generateCsrfToken(req, res);
    res.json({ csrfToken: token });
});

app.use('/api/auth', apiLimiter);                        // Aplicar rate limiting a todas las rutas de autenticación
app.use('/api/auth', doubleCsrfProtection,authRoutes);   // Rutas de autenticación

// ---Manejo de Errores de CSRF---
// app.use((err, req, res, next) => {
//     if (err.code === "EBADCSRFTOKEN") {
//         console.log("--- DEBUG CSRF ---");
//         console.log("Token en Header:", req.headers["x-csrf-token"]);
//         console.log("Cookies recibidas:", req.cookies);
//         console.log("Session ID actual:", req.sessionID);
//         return res.status(403).json({ error: "Token CSRF inválido", detalle: err.message });
//     }
//     next(err);
// });

// Ruta de prueba para verificar que el servidor está corriendo
app.get('/', (req, res) => {
    res.send('🛡️ Servidor Seguro Operativo');
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});