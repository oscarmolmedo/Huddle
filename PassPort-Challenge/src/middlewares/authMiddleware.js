// --- Middleware de autenticación que maneja tanto JWT como sesión basada en cookies ---
// Este middleware sirve para proteger rutas y verificar si el usuario está autenticado

const jwt = require('jsonwebtoken');

const protect = (req, res, next) => {
    // 1. Intentar validar por JWT (Header Authorization)
    let token = req.headers.authorization?.startsWith('Bearer') 
                ? req.headers.authorization.split(' ')[1] 
                : null;

    console.log("Token recibido en middleware:", req.headers.authorization);

    if (token) {
        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET);      //jwt.verify devuelve un objeto decodificado
            req.user = decoded;                                             // Inyectamos el usuario del token
            return next();
        } catch (error) {
            return res.status(401).json({ message: "JWT inválido o expirado" });
        }
    }

    // 2. Si no hay JWT, intentar validar por Sesión (Cookie)
    if (req.session && req.session.user) {
        req.user = req.session.user;                                        // Inyectamos el usuario de la sesión
        console.log("Usuario autenticado vía sesión:", req.session);
        return next();
    }

    // 3. Si no hay ninguno, denegar acceso
    res.status(401).json({ message: "No autorizado. Debes iniciar sesión." });
};


module.exports = { protect };