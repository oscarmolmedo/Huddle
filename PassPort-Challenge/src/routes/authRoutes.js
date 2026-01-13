const express = require('express');
const router = express.Router();
const { register, login } = require('../controllers/authController');
const { protect } = require('../middlewares/authMiddleware');
const { authorize } = require('../middlewares/roleMiddleware');

// Rutas públicas
router.post('/register', register);
router.post('/login', login);

// Ruta protegida: Solo si pasas por el middleware 'protect' llegas al handler
router.get('/profile', protect, (req, res) => {
    res.json({
        message: "Bienvenido a tu perfil privado",
        user: req.user // Aquí verás lo que decodificamos en el middleware
    });
});

router.get('/admin', protect, authorize('admin'), (req, res) => {
    res.json({message: ' Bienvenido, Admin. Aqui estan los reportes secretos.'})
});

module.exports = router;