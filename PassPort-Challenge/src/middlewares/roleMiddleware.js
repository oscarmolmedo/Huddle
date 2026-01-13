const authorize = (...rolesPermitidos) => {
    return (req, res, next) => {

        // req.user viene del middleware 'protect' que ejecutamos antes
        if (!req.user || !rolesPermitidos.includes(req.user.role)) {
            return res.status(403).json({ 
                message: "Acceso denegado: No tienes los permisos suficientes" 
            });
        }
        next();
    };
};

module.exports = { authorize };