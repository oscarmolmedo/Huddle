
//imports
const express = require('express');
const router = express.Router();
const learningModel = require('../models/learningModel');


// LEER: Obtener todos los temas
router.get('/', (req, res) => {
  const allTopics = learningModel.getAll();
  res.render('index', { pageTitle: 'CRUD Challenge', topics: allTopics });
});

// CREAR TEMA (POST desde formulario)
router.post('/topics', (req, res) => {
  const { title } = req.body;
  learningModel.addTopic(title);
  res.redirect('/');
});

// MODIFICAR TEMA (PATCH desde fetch)
router.patch('/topics/:id', (req, res) => {
  const { title } = req.body;
  const updated = learningModel.updateTopic(req.params.id, title);
  res.json({ success: true, topic: updated });
});

// ELIMINAR TEMA (DELETE desde fetch)
router.delete('/topics/:id', (req, res) => {
  const deleted = learningModel.deleteTopic(req.params.id);
  if (deleted) {
    res.json({ success: true});
  } else {
    res.status(404).json({ success: false });
  }
});

// CREAR ENLACE (POST)
router.post('/topics/:id/links', (req, res) => {
  const { url, description } = req.body;
  learningModel.addLink(req.params.id, url, description);
  res.redirect('/');
});

// VOTAR (PATCH para tiempo real)
router.patch('/topics/vote/:id', (req, res) => {
  const updated = learningModel.voteTopic(req.params.id);
  // Devolvemos el array completo ordenado para que el front sepa el nuevo orden
  res.json({ success: true, newVotes: updated.votes, allTopics: learningModel.getAll() });
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

module.exports = router;