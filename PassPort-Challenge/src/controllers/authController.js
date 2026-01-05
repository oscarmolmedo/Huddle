const bcrypt = require('bcrypt');

// Simulamos una base de datos en memoria (solo para el Día 1)
const users = [];

const register = async (req, res) => {
    try {
        const { email, password } = req.body;

        // 1. Validar si el usuario ya existe
        const userExists = users.find(u => u.email === email);
        if (userExists) {
            return res.status(400).json({ message: "El usuario ya existe" });
        }

        // --- TU MISIÓN AQUÍ ---
        // 2. Generar el 'salt' (sal)
        // 3. Hashear la contraseña usando el salt
        const salt = await bcrypt.genSalt(10); // Generamos un salt con 10 rondas
        const hashedPassword = await bcrypt.hash(password, salt); // Hasheamos la contraseña con el salt generado

        // 4. Guardar el usuario (simulado)
        const newUser = {
            id: users.length + 1,
            email,
            password: hashedPassword // Guardamos el hash, NUNCA la clave real
        };
        users.push(newUser);

        console.log("Usuarios en la base de datos:", users);

        res.status(201).json({ message: "Usuario registrado con éxito", userId: newUser.id });
    } catch (error) {
        res.status(500).json({ message: "Error en el servidor", error: error.message });
    }
};

module.exports = { register };