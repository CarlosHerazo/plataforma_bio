document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("confirmarAgregarContenedor").addEventListener("click", function(event) {
        
        event.preventDefault();  

        Swal.fire({
            title: '¿Estás seguro?',
            text: "¿Deseas agregar este nuevo contenedor?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, agregarlo!',
            cancelButtonText: 'Cancelar',
            customClass: {
                confirmButton: 'btn btn-dark', // Clase de Bootstrap para el botón de confirmación
                cancelButton: 'btn btn-danger' // Clase de Bootstrap para el botón de cancelación
            }
        }).then((result) => {
            if (result.isConfirmed) {
                // Enviar el formulario directamente
                document.getElementById("AgregarContenedorForm").submit();
            }
        });
    });
});
