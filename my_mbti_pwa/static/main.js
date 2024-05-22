document.addEventListener('DOMContentLoaded', () => {
    const mbtiSelect = document.getElementById('mbti-select');
    const mbtiDescription = document.getElementById('mbti-description');

    mbtiSelect.addEventListener('change', async () => {
        const selectedType = mbtiSelect.value;
        if (selectedType) {
            const response = await fetch('/mbti_data.json');
            const data = await response.json();
            mbtiDescription.textContent = data[selectedType];
        } else {
            mbtiDescription.textContent = 'MBTI 유형을 선택해주세요.';
        }
    });

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    }
});
