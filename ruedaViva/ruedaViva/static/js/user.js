document.getElementById("confirmarAgregarUsuario").addEventListener("click", function(event) {
    
    event.preventDefault();  // Evitar el envío predeterminado

    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Deseas agregar este nuevo usuario?",
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
            document.getElementById("agregarUsuarioForm").submit();  // Enviar el formulario
        }
    });
});
