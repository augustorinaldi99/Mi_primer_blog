document.addEventListener("DOMContentLoaded", function () {
    const casilla = document.getElementById("id_modificar_tags");
    const campo = document.getElementById("id_tags_texto");

    if (!casilla || !campo) return;

    function actualizarCampo() {
        campo.disabled = !casilla.checked;
    }

    casilla.addEventListener("change", actualizarCampo);
    actualizarCampo();
});