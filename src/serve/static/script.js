
// WISHLIST 

if(document.querySelectorAll(".wishlist-nav .tab")) {
    tab = document.querySelectorAll(".wishlist-nav .tab");
    for (var i = 0; i < tab.length; i++) { 
        (function() { tab[0].click() })()
        tab[i].addEventListener('click', event => {
            // set id
            var id = event.currentTarget.innerText.toLowerCase();
            if(id == "price graph") {
                id = "price-graph";
            }

            // hide content
            let tabContent = document.querySelectorAll("#tab-content-area > .tab-content");
            for (var i = 0; i < tabContent.length; i++) { 
                tabContent[i].style.display = 'none';
            }

            // toggle off active tabs
            tab = document.querySelectorAll(".tab");
            for (i = 0; i < tab.length; i++) {
                tab[i].className = tab[i].className.replace(" active", "");
            }

            // Show the current tab, and add an "active" class to the button that opened the tab
            document.getElementById(id).style.display = "block";
            event.currentTarget.className += " active";

        })

    }
}

// END OF WISHLIST

// PRICE GRAPH

if(document.querySelectorAll(".btn-graph-group")) {
    btn = document.querySelectorAll(".btn-graph-group .btn");
    for (var i = 0; i < btn.length; i++) { 
        (function() { btn[0].click() })()
        btn[i].addEventListener('click', event => {
            // set id
            var id = event.currentTarget.id
            if(id == "btn-graph-total") { 
                id = "graph-total";
            } else { 
                id = "graph-hist";
            }

            // hide content
            let graphs = document.querySelectorAll("#price-graph.tab-content > .graph");
            for (var i = 0; i < graphs.length; i++) { 
                graphs[i].style.display = 'none';
            }

            // toggle off active tabs
            btn = document.querySelectorAll(".btn-graph-group .btn");
            for (i = 0; i < btn.length; i++) {
                btn[i].className = btn[i].className.replace(" active", "");
            }

            // Show the current tab, and add an "active" class to the button that opened the tab
            document.getElementById(id).style.display = "block";
            event.currentTarget.className += " active";

        })

    }
}

// END OF PRICE GRAPH

// BUTTON CATEGORY 

if(document.querySelector(".btn_category")) {
    document.querySelector(".btn_category").addEventListener("click", function() {
        this.classList.toggle("active");
        var category = this.nextElementSibling;
        if (category.style.display === "grid") {
            category.style.display = "none";
        } else {
            category.style.display = "grid";
        }
    });
}

// END OF BUTTON CATEGORY

//  FILTER PAGE

if(document.querySelector("#openfilter")) {
    document.querySelector("#openfilter").addEventListener("click", () => {
        document.querySelector("#features-page").style.width = "100%";
    });
}

if(document.querySelector("#features-page > .closebtn")) {
    document.querySelector("#features-page > .closebtn").addEventListener("click", () => {
        document.querySelector("#features-page").style.width = "0%";
    });
}

//  END OF FILTER PAGE
