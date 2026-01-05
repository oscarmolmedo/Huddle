const express = require('express');
const helmet = require('helmet');
const cookieParser = require('cookie-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();

const authRoutes = require('./routes/authRoutes');

// --- Middlewares de Seguridad y Utilidad ---
app.use(helmet()); // Protege cabeceras
app.use(cors()); // Control de acceso
app.use(express.json()); // Permite leer JSON en el body
app.use(cookieParser()); // Permite manejar cookies

app.use('/api/auth', authRoutes);

const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.send('🛡️ Servidor Seguro Operativo');
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});