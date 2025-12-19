//learningController.js hace de intermediario entre las rutas y el modelo

//imports
const express = require('express');
const router = express.Router();
const learningModel = require('../models/learningModel');

// LEER: Obtener todos los temas
//Como siempre estamos en '/' y cada accción actualiza la pagina principal, se dispara getAllOrdered y vemos los elementos ordenados
//req: lo que viene del cliente | res: lo que enviamos al cliente
router.get('/', (req, res) => {                       //RUTA PRINCIPAL. Por mas que no usamos res.send, es necesario tener el res para renderizar
  const allTopics = learningModel.getAllOrdered();   //Devolvemos los temas ordenados
  res.render('index', { pageTitle: 'CRUD Challenge', topics: allTopics });
});

// ELIMINAR TEMA (DELETE desde fetch)
router.delete('/topics/:id', (req, res) => {
  const deleted = learningModel.deleteTopic(req.params.id);           //Llamamos a la funcion del modelo para eliminar el tema
  if (deleted) {                                            
    res.json({ success: true});
  } else {
    res.status(404).json({ success: false });
  }
});

// VOTAR ENLACE (PATCH para tiempo real)
router.patch('/topics/:topicId/links/:linkId/vote', (req, res) => {
  const { topicId, linkId } = req.params;
  const updatedLink = learningModel.voteEnlace(topicId, linkId);

  if (updatedLink) {
    res.json({ success: true, newVotes: updatedLink.votes});
  } else {
    res.status(404).json({ success: false, message: 'No encontrado'});
  }
});


// CREAR TEMA (POST desde formulario)
router.post('/topics', (req, res) => {                //Se define la ruta para crear un tema
  const { title } = req.body;                         //Obtenemos el titulo del cuerpo de la solicitud
  learningModel.addTopic(title);                      //Llamamos a la funcion del modelo para agregar el tema  
  res.redirect('/');                                  //Redirigimos a la pagina principal. Para que el usuario vea el tema creado
});

// MODIFICAR TEMA (PATCH desde fetch)
router.patch('/topics/:id', (req, res) => {
  const { title, links } = req.body;                                          //Obtenemos el nuevo titulo y los links actualizados del cuerpo de la solicitud  
  const updated = learningModel.updateTopic(req.params.id, title, links);    //Llamamos a la funcion del modelo para actualizar el tema
  res.json({ success: true, topic: updated });                               //Devolvemos una respuesta JSON indicando exito y el tema actualizado       
});


// CREAR ENLACE (POST)
router.post('/topics/:id/links', (req, res) => {
  const { url, description } = req.body;
  learningModel.addLink(req.params.id, url, description);
  res.redirect('/');
});

// VOTAR TEMA (PATCH para tiempo real)
router.patch('/topics/vote/:id', (req, res) => {
  const updated = learningModel.voteTopic(req.params.id);
  // Devolvemos el array completo ordenado para que el front sepa el nuevo orden
  res.json({ success: true, newVotes: updated.votes, allTopics: learningModel.getAllOrdered() });
});


// Cuando alguien visite http://localhost:3000/hola
router.get('/hola', (req, res) => {
  // El mensaje está introducido directamente aquí
  res.send('¡Hola! Este es un mensaje directo desde el servidor');
});

module.exports = router;