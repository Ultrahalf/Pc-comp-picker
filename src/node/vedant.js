const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

(async () => {
    const extractProducts = async url => {
        const browser = await puppeteer.launch({headless: false});
        const page = await browser.newPage();
        await page.goto(url);
        const results = await page.evaluate(() => {
            let vendor = "vendant";
            let products = [];
            let product_items = document.querySelectorAll(".product-thumb");
            let len = product_items.length
            for(i = 0; i <= len - 1; i++) {
                if(product_items[i].querySelector(".price")) {
                    if(product_items[i].querySelector(".price-new")){
                        price = product_items[i].querySelector(".price-new").textContent
                    }
                    else  {
                        price = product_items[i].querySelector(".price").textContent
                    }
                }
                products.push(
                    {
                        'vendor': vendor,
                        'title': product_items[i].querySelector(".name").textContent,
                        'img': product_items[i].querySelector("img").src,
                        'url': product_items[i].querySelector(".name > a").href,
                        'price': price.replace(/\t|\n/g,''),
                    })
            }
            return products
        });
        await page.close();
        await browser.close();
        if (results.length < 1) {
            return results
        } else {
            const nextPageNumber = parseInt(url.match(/page=(\d+)$/)[1], 10) + 1;
            const nextUrl = `https://www.vedantcomputers.com/pc-components/graphics-card?fq=1&page=${nextPageNumber}`;
            return results.concat(await extractProducts(nextUrl))
        }
    };

    const browser = await puppeteer.launch();
    const firstUrl = "https://www.vedantcomputers.com/pc-components/graphics-card?fq=1&page=1";
    const prds = await extractProducts(firstUrl);
    let client;
    try {
        client = await MongoClient.connect(dbUrl);
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        await db.collection("products").insertMany(prds, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
