// WISHLIST 

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
        tab = document.getElementsByClassName("tab");
        for (i = 0; i < tab.length; i++) {
            tab[i].className = tab[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(id).style.display = "block";
        event.currentTarget.className += " active";

    })

}

// END OF WISHLIST

