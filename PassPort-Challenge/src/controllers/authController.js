const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

// Simulamos una base de datos en memoria
//Creamos un usuario admin por defecto
const users = [
    {
        id: 999,
        email: 'admin@elamigos.com',
        password: '$2b$10$q5n8Yw43OVeJSQd.0ifKe.s6/omyY.zpKIkKjc3GNeBXKldYQaD4e', // Contraseña admin123 hasheada
        role: 'administrator'
    }
];

const register = async (req, res) => {
    try {
        const { email, password, role } = req.body;

        // 1. Validar si el usuario ya existe
        const userExists = users.find(u => u.email === email);
        if (userExists) {
            return res.status(400).json({ message: "El usuario ya existe" });
        }


        // 2. Hashear la contraseña antes de guardar
        const salt = await bcrypt.genSalt(10); // Generamos un salt con 10 rondas
        const hashedPassword = await bcrypt.hash(password, salt); // Hasheamos la contraseña con el salt generado


        // 3. Guardar el usuario (simulado)
        const newUser = {
            id: users.length + 1,
            email,
            password: hashedPassword, // Guardamos el hash, NUNCA la clave real
            role: 'user' // Seteamos role por defecto como 'user' y admin es asignado manualmente por otro
        };

        // Añadimos el nuevo usuario a nuestra "base de datos"s
        users.push(newUser);

        console.log("Usuarios en la base de datos:", users);

        res.status(201).json({ message: "Usuario registrado con éxito", userId: newUser.id });

    } catch (error) {
        res.status(500).json({ message: "Error en el servidor", error: error.message });
    }
};

// Controlador para login que maneja tanto JWT como sesión basada en cookies
const login = async (req, res) => {
    try {
        const { email, password, stayLoggedIn } = req.body; // stayLoggedIn será un booleano

        const user = users.find(u => u.email === email);
        if (!user || !(await bcrypt.compare(password, user.password))) {
            return res.status(401).json({ message: "Credenciales inválidas" });
        }

        if (stayLoggedIn) {
            // --- OPCIÓN A: SESIÓN PERSISTENTE (COOKIES) ---
            req.session.user = { id: user.id, email: user.email, role: user.role };
            return res.status(200).json({ 
                message: "Login exitoso con Sesión Persistente (Cookie establecida)",
                authType: "session"
            });
        } else {
            // --- OPCIÓN B: SESIÓN SIN ESTADO (JWT) ---
            const token = jwt.sign(
                { id: user.id, email: user.email, role: user.role },
                process.env.JWT_SECRET,
                { expiresIn: '15m' }            // El token expira en 15 minutos
            );
            return res.status(200).json({ 
                message: "Login exitoso con JWT",
                token,
                authType: "jwt"
            });
        }
    } catch (error) {
        res.status(500).json({ message: "Error en el servidor" });
    }
};

// Controlador para logout que maneja tanto sesión como JWT
const logout = (req, res) => {
    // Destruir sesión si existe
    req.session.destroy((err) => {
        if (err) console.log("Error destruyendo sesión");
        
        // Limpiar la cookie del navegador explícitamente
        res.clearCookie('connect.sid'); 
        
        res.status(200).json({ 
            message: "Logout exitoso. Sesión eliminada y Cookie borrada. (Si usabas JWT, recuerda borrarlo en el cliente)" 
        });
    });
};


const updateUserRole = async (req, res) => {
    try {
        const { email, newRole } = req.body;

        // 1. Validar que se enviaron los datos necesarios
        if (!email || !newRole) {
            return res.status(400).json({ message: "Email y el nuevo rol son requeridos" });
        }

        // 2. Buscar al usuario en nuestro "almacén"
        const user = users.find(u => u.email === email);

        if (!user) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }

        // 3. Actualizar el rol
        user.role = newRole;

        console.log(`Sistema: El usuario ${email} ahora es ${newRole}`);
        
        res.status(200).json({ 
            message: `Rol actualizado con éxito. El usuario ${email} ahora es ${newRole}.` 
        });
    } catch (error) {
        res.status(500).json({ message: "Error al actualizar el rol" });
    }
};


module.exports = { register, login, logout, updateUserRole };