const express = require('express');
const router = express.Router();

// Importamos los controladores y middlewares necesarios
const { register, login, updateUserRole } = require('../controllers/authController');
const { protect } = require('../middlewares/authMiddleware');
const { authorize } = require('../middlewares/roleMiddleware');
const { validateAuth } = require('../middlewares/validatorMiddleware');


// Rutas públicas (raíz /api/auth)
router.post('/register', validateAuth, register);
router.post('/login', validateAuth, login);


// ---Ruta protegida: Solo si pasas por el middleware 'protect' llegas al handler---
//Ruta que devuelve el perfil del usuario autenticado
router.get('/profile', protect, (req, res) => {
    res.json({
        message: "Bienvenido a tu perfil privado",
        user: req.user // Aquí verás lo que decodificamos en el middleware
    });
});

// Ruta protegida y autorizada solo para usuarios con role 'admin'
router.get('/admin', protect, authorize('admin'), (req, res) => {
    res.json({
        message: ' Bienvenido, Admin. Aqui estan los reportes secretos.'
    })
});

// Solo los que tengan un token válido Y sean admins pueden tocar este endpoint
router.patch('/update-role', protect, authorize('administrator'), (req, res, next) => {
    next();
}, updateUserRole);

module.exports = router;