const bcrypt = require('bcrypt');

const password = 'admin123';
const saltRounds = 10;

const hola =bcrypt.hash(password, saltRounds).then(hash => {
    console.log("Tu nuevo hash es:", hash);
});


console.log("hola es", hola)

