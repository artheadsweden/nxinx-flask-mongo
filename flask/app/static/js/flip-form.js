let rotate = () => {
    let form_div = document.getElementById("flipper");
    let slide1 = document.getElementById("slide1");
    let slide2 = document.getElementById("slide2");
    if (slide1.checked) {
        form_div.style.transform = "rotateY(180deg)";
        form_div.style.height = "350px";
        slide1.checked = true;
        slide2.checked = true;
    } else {
        form_div.style.transform = "rotateY(0deg)";
        form_div.style.height = "300px";
        slide1.checked = false;
        slide2.checked = false;
    }

}