document.addEventListener('DOMContentLoaded', function() {
    const messageItems = document.querySelectorAll('.message');
    messageItems.forEach(item => {
        item.addEventListener('contextmenu', function(e) {
            e.preventDefault(); // Empêche le menu contextuel par défaut de s'ouvrir
            const messageId = this.dataset.messageId;
            const confirmDelete = confirm("Voulez-vous vraiment supprimer ce message ?");
            if (confirmDelete) {
                // Supprimer le message de l'interface utilisateur
                this.remove();

                // Envoyer une requête AJAX pour supprimer le message du serveur
                fetch(`/delete_message/${messageId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erreur lors de la suppression du message');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Message supprimé avec succès du serveur :', data);
                })
                .catch(error => {
                    console.error('Erreur lors de la suppression du message :', error);
                });
            }
        });
    });
});

// Fonction pour obtenir le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
