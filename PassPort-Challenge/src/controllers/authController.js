const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

// Simulamos una base de datos en memoria (solo para el Día 1)
const users = [];

const register = async (req, res) => {
    try {
        const { email, password, role } = req.body;

        // 1. Validar si el usuario ya existe
        const userExists = users.find(u => u.email === email);
        if (userExists) {
            return res.status(400).json({ message: "El usuario ya existe" });
        }

        const salt = await bcrypt.genSalt(10); // Generamos un salt con 10 rondas
        const hashedPassword = await bcrypt.hash(password, salt); // Hasheamos la contraseña con el salt generado

        // 4. Guardar el usuario (simulado)
        const newUser = {
            id: users.length + 1,
            email,
            password: hashedPassword, // Guardamos el hash, NUNCA la clave real
            role: role || 'user' // Rol por defecto 'user'
        };
        users.push(newUser);

        console.log("Usuarios en la base de datos:", users);

        res.status(201).json({ message: "Usuario registrado con éxito", userId: newUser.id });
    } catch (error) {
        res.status(500).json({ message: "Error en el servidor", error: error.message });
    }
};

const login = async (req, res) => {
    try {
        const { email, password } = req.body;

        // 1. Buscar al usuario por email
        const user = users.find(u => u.email === email);
        if (!user) {
            return res.status(400).json({ message: "Credenciales inválidas" });
        }

        // 2. Comparar la contraseña ingresada con el hash almacenado
        const isPasswordValid = await bcrypt.compare(password, user.password);
        if (!isPasswordValid) {
            return res.status(400).json({ message: "Credenciales inválidas" });
        }

// --- GENERACIÓN DEL JWT ---
        // Firmamos un token que contiene el ID del usuario
        const token = jwt.sign(
            { id: user.id, email: user.email, role: user.role }, 
            process.env.JWT_SECRET, 
            { expiresIn: '1h' }
        );

        // Enviamos el token al cliente. El cliente deberá guardarlo (ej. LocalStorage)
        res.status(200).json({ message: "Login exitoso", token: token});
    } catch (error) {
        res.status(500).json({ message: "Error en el servidor", error: error.message });
    }
};

module.exports = { register, login };