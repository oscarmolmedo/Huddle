document.addEventListener('click', async (e) => {
  // ELIMINAR TEMA
    if (e.target.classList.contains('delete-topic-btn')) {
        if (confirm('¿Estás seguro de que quieres borrar este tema?')) {
            const id = e.target.dataset.id;
            const response = await fetch(`/topics/${id}`, { method: 'DELETE' });
            console.log("Status del servidor:", response.status);
            if (response.ok) window.location.reload();
        }
    }

    // EDITAR TEMA
    if (e.target.classList.contains('edit-topic-btn')) {
        const id = e.target.dataset.id;
        const oldTitle = e.target.dataset.title;
        const newTitle = prompt("Nuevo nombre del tema:", oldTitle);

        if (newTitle && newTitle !== oldTitle) {
            const response = await fetch(`/topics/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTitle })
            });
            if (response.ok) window.location.reload();
        }
    }

  if (e.target.classList.contains('vote-topic-btn')) {
    const id = e.target.dataset.id;
    const response = await fetch(`/topics/vote/${id}`, { method: 'PATCH' });
    const data = await response.json();

    if (data.success) {
      // OPCIÓN A: Recargar la página (lo más fácil para asegurar el orden)
      window.location.reload(); 


    }
  }
  if (e.target.classList.contains('vote-enlace-btn')) {
      const topicId = e.target.dataset.topic; // Obtiene el ID del tema
      const linkId = e.target.dataset.link;   // Obtiene el ID del enlace
      
      // Llamada a la nueva ruta
      const response = await fetch(`/topics/${topicId}/links/${linkId}/vote`, { 
          method: 'PATCH'
      });
      
      const data = await response.json();

      if (data.success) {
          window.location.reload(); 
      }
  }

});
document.querySelectorAll('.vote-topic-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const id = e.target.dataset.id;
        const response = await fetch(`/topics/vote/${id}`, { method: 'PATCH' });
        const data = await response.json();
        if (data.success) {
            // Actualizar el numerito en el HTML sin recargar
            location.reload(); // O actualizar el DOM manualmente
        }
    });
});