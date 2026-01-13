const jwt = require('jsonwebtoken');

const protect = (req, res, next) => {
    let token;

    // Los tokens se envían comúnmente en el header 'Authorization' como 'Bearer <token>'
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
        try {
            // 1. Extraer el token del string "Bearer XXXXXX"
            token = req.headers.authorization.split(' ')[1];

            // 2. Verificar el token usando nuestra clave secreta
            const decoded = jwt.verify(token, process.env.JWT_SECRET);

            // 3. Añadir los datos del usuario decodificados al objeto 'req' 
            // para que las siguientes funciones tengan acceso a ellos
            req.user = decoded;

            // 4. Continuar al siguiente paso (el controlador de la ruta)
            next();
        } catch (error) {
            return res.status(401).json({ message: "No autorizado, token fallido" });
        }
    }

    if (!token) {
        return res.status(401).json({ message: "No autorizado, no hay token" });
    }
};



module.exports = { protect };