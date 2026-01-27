const validateAuth = (req, res, next) => {
    const { email, password } = req.body;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Validación de existencia
    if (!email || !password) {
        return res.status(400).json({ message: "Email y password son obligatorios" });
    }

    // Validación de formato
    if (!emailRegex.test(email)) {
        return res.status(400).json({ message: "Formato de email inválido" });
    }

    // Validación de seguridad (longitud)
    if (password.length < 6) {
        return res.status(400).json({ message: "La contraseña debe tener al menos 6 caracteres" });
    }

    // Si todo está bien, pasamos al siguiente paso
    next();
};

module.exports = { validateAuth };