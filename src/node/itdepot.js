const puppeteer = require('puppeteer');

(async () => {
    const extractProducts = async url => {
        const browser = await puppeteer.launch({headless: false});
        const page = await browser.newPage();
        await page.setRequestInterception(true);
        page.on('request', (req) => {
            if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
                req.abort();
            }
            else {
                req.continue();
            }
        });
        await page.goto(url);
        const results = await page.evaluate(() => {
            let products = [];
            let product_items = document.getElementsByClassName("product-item");
            let len = product_items.length;
            if(document.querySelector("ul.pagination")) {
                var next = document.querySelector("ul.pagination");
                var totalLi = next.querySelectorAll("li").length;
            } else {
                totalLi = 5
            }
            var j = 1
            while (j <= totalLi - 4){
                for(i = 0; i < len; i++) {
                    products.push(
                        {
                            "title": product_items[i].querySelector("div.product-details.text-md-left.flex-grow-1 > div.card-text.px-2.py-1.font-size85.product_title > a").textContent,
                            "img": product_items[i].querySelector("img").src,
                            "url": product_items[i].querySelector("div.product-details.text-md-left.flex-grow-1 > div.card-text.px-2.py-1.font-size85.product_title > a").href,
                            "price": product_items[i].querySelector("strong").textContent
                        })
                }
                if(document.querySelector("ul.pagination > li:last-child > a"))
                    document.querySelector("ul.pagination > li:last-child > a").click();
                j++;
            }
            return products
        });
        await page.close();
        await browser.close();
        return results
    };

    const browser = await puppeteer.launch();
    let prds = 0;
    const firstUrl = "https://www.theitdepot.com/products-RAM+(Memory)_C6.html";
    prds = await extractProducts(firstUrl);
    console.table(prds);
    process.exit();
})();
