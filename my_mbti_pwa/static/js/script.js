function showImage() {
    const mbti = document.getElementById("mbti").value;
    const img = document.getElementById("mbtiImage");
    if (mbti) {
        img.src = `/static/images/${mbti}.png`;
        img.style.display = "block";
    } else {
        img.style.display = "none";
    }
}
