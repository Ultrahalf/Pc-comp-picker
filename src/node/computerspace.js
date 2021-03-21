const puppeteer = require('puppeteer');

(async () => {
    const extractProducts = async url => {
        const browser = await puppeteer.launch({headless: false});
        const page = await browser.newPage();
        await page.goto(url);
        await page.setRequestInterception(true);
        page.on('request', (req) => {
            if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
                req.abort();
            }
            else {
                req.continue();
            }
        });
        const nextUrl = await page.evaluate(() => {
            if(document.querySelector("ul.pagination-custom > li:last-child a"))
                var url = document.querySelector("ul.pagination-custom> li:last-child a").href;
            if(url != null)
                return url
            return null
        });
        const results = await page.evaluate(() => {
            let products = []
            var product_items = document.querySelectorAll("#shopify-section-collection-template > div.grid > div:nth-child(2) > div .grid__item");
            var len = product_items.length;
            for(i = 0;i <= len -1; i++){
                products.push(
                    {
                        "title": product_items[i].querySelector("p.product-title").textContent,
                        "img": product_items[i].querySelector("img").src,
                        "url": product_items[i].querySelector("div.grid div > a").href,
                        "price": product_items[i].querySelector(".price-dis-sec span.visually-hidden + span.money").textContent
                    })
            }
            return products
        });
        await page.close();
        await browser.close();
        if(results.length < 1 || nextUrl == null) {
            return results
        } else {
            return results.concat(await extractProducts(nextUrl))
        }
    };

    const browser = await puppeteer.launch();
    const firstUrl = "https://computerspace.in/collections/cabinets?page=1";
    const prds = await extractProducts(firstUrl);
    console.table(prds);
    process.exit();
})();
