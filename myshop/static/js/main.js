document.addEventListener('DOMContentLoaded', function() {
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');

    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.dataset.productId;
            const newQuantity = this.value;
            updateCartQuantity(productId, newQuantity);
        });
    });

    function updateCartQuantity(productId, quantity) {
        fetch(`/cart/update/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: quantity }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Failed to update cart quantity');
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
