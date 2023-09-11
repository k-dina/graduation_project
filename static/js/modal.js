document.addEventListener("DOMContentLoaded", function() {

    const modal = new bootstrap.Modal(document.getElementById('modal'));

    stopButton.addEventListener('click', () => {
        modal.show();
    });
});
