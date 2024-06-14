document.addEventListener('DOMContentLoaded', function() {
    const avatarForm = document.getElementById('avatarForm');
    const loader = document.getElementById('loader');
    const avatarResult = document.getElementById('avatarResult');
    const errorMessage = document.getElementById('errorMessage');

    avatarForm.addEventListener('submit', function(event) {
        event.preventDefault();
        loader.style.display = 'block';
        avatarResult.innerHTML = '';
        errorMessage.innerHTML = '';

        const formData = new FormData(avatarForm);

        fetch('/generate_avatar', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                loader.style.display = 'none';
                if (data.success) {
                    data.avatar_urls.forEach(url => {
                        const img = document.createElement('img');
                        img.className = 'avatar-image';
                        img.src = url;
                        img.alt = 'Generated Avatar';
                        avatarResult.appendChild(img);
                    });
                } else {
                    errorMessage.textContent = 'Error: ' + data.error;
                }
            })
            .catch(error => {
                loader.style.display = 'none';
                errorMessage.textContent = 'Error: ' + error.message;
            });
    });
});
