// Manejo de eventos para botones de eliminar, editar y votar
document.addEventListener('click', async (e) => {
    
    // ELIMINAR TEMA
    if (e.target.classList.contains('delete-topic-btn')) {
        //Se obtiene el id del tema a eliminar desde el atributo data-id del botón
        const id = e.target.dataset.id;

        if (confirm(`¿Estás seguro de que quieres borrar el tema con ID: ${id}`)) {
            const response = await fetch(`/topics/${id}`, { method: 'DELETE' });        // Llamada a la ruta DELETE del servidor
            console.log("Status del servidor:", response.status);
            if (response.ok) window.location.reload();
        }
    }

    //BOTON VOTAR LINK
    if (e.target.classList.contains('vote-enlace-btn')) {
      //   const topicId = e.target.dataset.topic; // Obtiene el ID del tema
      //   const linkId = e.target.dataset.link;   // Obtiene el ID del enlace
  
      //Desempaquetamos y creamos variables con el mismo nombre
      const {topic, link} = e.target.dataset
        
        // Llamada a la nueva ruta
        const response = await fetch(`/topics/${topic}/links/${link}/vote`, { method: 'PATCH'});
        
        const data = await response.json();
  
        if (data.success) {
            window.location.reload(); 
        }
    }
    // EDITAR TEMA Y LINKS
    if (e.target.classList.contains('edit-topic-btn')) {
        
        const {id, title} = e.target.dataset
        const currentLinks = JSON.parse(e.target.dataset.links); // Recuperamos los links

        // 1. Preguntar por el nuevo título
        const newTitle = prompt("Nuevo nombre del tema:", title);
        if (newTitle === null) return; // Cancelado

        // 2. Iterar por los links actuales para editarlos
        const updatedLinks = [];
        for (let link of currentLinks) {
            const newUrl = prompt(`Editar URL para "${link.description}":`, link.url);
            const newDesc = prompt(`Editar descripción para "${link.url}":`, link.description);
            
            updatedLinks.push({
                id: link.id, // Mantener el ID para no perder votos en el modelo
                url: newUrl || link.url,
                description: newDesc || link.description
            });
        }

        // 3. Enviar todo al servidor
        const response = await fetch(`/topics/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    title: newTitle,
                    links: updatedLinks 
                })
            });

            if (response.ok) window.location.reload();
    }
    //BOTON VOTAR TEMA
    if (e.target.classList.contains('vote-topic-btn')) {
        const id = e.target.dataset.id;
        const response = await fetch(`/topics/vote/${id}`, { method: 'PATCH' });
        const data = await response.json();
        
    if (data.success) {
      //Recargar la página (lo más fácil para asegurar el orden)
      window.location.reload();

    }
  }

})