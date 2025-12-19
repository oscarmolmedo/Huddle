
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



 deleteTopic = (id) => {                                                  //Elimina un tema por su id
    const index = topics.find(t => t.id == id);
    //que es index y cual sería su valor
    //index es la posición del elemento en el array topics 
    // que coincide con el id proporcionado. Si no se encuentra, index será -1.
    console.log("Index encontrado:", index.id);
    if (index !== -1) {
      return topics.splice(index, 1); // Elimina el elemento del array
    }
    return null;
};

console.log(deleteTopic(1));
console.log('Array actual',topics);