// BUTTON CATEGORY 
document.querySelector(".btn_category").addEventListener("click", function() {
    this.classList.toggle("active");
    var category = this.nextElementSibling;
    if (category.style.display === "grid") {
        category.style.display = "none";
    } else {
        category.style.display = "grid";
    }
});

// ACTIVE CATEGORY INDICATOR

productPageBtns = document.querySelectorAll(".btn-product-page");
for( i = 0; i < productPageBtns.length; i++) {
    productPageBtns[i].addEventListener("click", (event) => {
        categoryBtn = document.querySelectorAll(".btn-product-page")
        for (i = 0; i < categoryBtn.length; i++) {
            categoryBtn[i].className = categoryBtn[i].className.replace(" active", "");
        }
        event.currentTarget.className += " active";
    })
}

// END OF ACTIVE CATEGORY INDICATOR
// END OF BUTTON CATEGORY

