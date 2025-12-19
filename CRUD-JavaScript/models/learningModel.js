let topics = [
  { 
    id: 1, 
    title: "Node.js Basico", 
    votes: 10,
    links: [
      { id: 101, url: "https://nodejs.org", description: "Doc Oficial", votes: 5 }
    ]
  },
  { 
    id: 2, 
    title: "Python", 
    votes: 10,
    links: [
      { id: 102, url: "https://nodejs.org", description: "Doc Oficial", votes: 5 }
    ]
  }
];

module.exports = {
  getAllOrdered: () => {                                                //Retorna los temas ordenados por votos
    topics.sort((a, b) => b.votes - a.votes);
    topics.forEach(t => t.links.sort((a, b) => b.votes - a.votes));
    return topics;
  },
  
  // ELIMINAR TEMA
  deleteTopic: (id) => {                                                  //Elimina un tema por su id
    const index = topics.find(t => t.id == id);
    //que es index y cual sería su valor
    //index es la posición del elemento en el array topics 
    // que coincide con el id proporcionado. Si no se encuentra, index será -1.
    if (index !== -1) {
      return topics.splice(index, 1); // Elimina el elemento del array
    }
    return null;
  },
  
  // VOTAR Enlace 
  voteEnlace: (topicId, linkId) => {                                    //Pasamos id y enlace por que un tema puede tener varios enlaces
  const topic = topics.find(t => t.id == topicId);
  if (topic) {
    const link = topic.links.find(l => l.id == linkId)
    if (link) {
      link.votes++;
      return link;
    }
  }
  return null;
  },

  // CREAR TEMA
  addTopic: (title) => {                                              //Agrega un nuevo tema y retorna el tema creado(diccionario)
    const newTopic = {
      id: Date.now(),                                                 // Generamos un ID único basado en el tiempo. Ejemplo de id: 1625247600000
      title: title,
      votes: 0,
      links: []
    };
    topics.push(newTopic);
    return newTopic;
  },

  // MODIFICAR TEMA Y LINKS
  updateTopic: (id, newTitle, updatedLinks) => {                          //Actualiza el titulo y los links de un tema
    const topic = topics.find(t => t.id == id);
    if (topic) {
      if (newTitle) topic.title = newTitle;
      
      // Si enviamos links para actualizar
      if (updatedLinks && Array.isArray(updatedLinks)) {                  // Verificamos que updatedLinks sea un array
        topic.links = updatedLinks.map(link => {
          // Buscamos si el link ya existía para mantener sus votos
          const existingLink = topic.links.find(l => l.id == link.id);
          return {
            id: link.id || Date.now(),
            url: link.url,
            description: link.description,
            votes: existingLink ? existingLink.votes : 0
          };
        });
      }
    }
    return topic;
  },

  // CREAR ENLACE DENTRO DE TEMA
  addLink: (topicId, url, description) => {
    const topic = topics.find(t => t.id == topicId);
    if (topic) {
      topic.links.push({ id: Date.now(), url, description, votes: 0 });
    }
  },

  // VOTAR TEMA 
  voteTopic: (id) => {
    const topic = topics.find(t => t.id == id);
    if (topic) topic.votes++;
    return topic;
  },

};