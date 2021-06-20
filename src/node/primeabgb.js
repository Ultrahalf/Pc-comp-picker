const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

(async () => {
    const extractProducts = async obj => {
        const browser = await puppeteer.launch({headless: true});
        const page = await browser.newPage();

        // disable css
        await page.setRequestInterception(true);
        page.on('request', (req) => {
            if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
                req.abort();
            }
            else {
                req.continue();
            }
        });

        // Configure the navigation timeout
        await page.setDefaultNavigationTimeout(0);

        await page.goto(obj.url);

        // check if there's a next page button
        const nextUrl = await page.evaluate(() => {
            if(document.querySelector("ul.page-numbers li > a.next"))
                var url = document.querySelector("ul.page-numbers li > a.next").href;
            if(url != null)
                return url
            return null
        });

        // evaluate the page and return the products
        const results = await page.evaluate((obj) => {
            let vendor = "primeabgb";
            let products = [];
            let category = obj.component;
            let product_items = document.getElementsByClassName("product-item");
            for(i = 0; i < product_items.length; i++) {
                if(product_items[i].querySelector("div.flashs > span.out-of-stock")){
                } else {
                    if(product_items[i].querySelector("div.product-innfo span.price bdi"))
                        price = product_items[i].querySelector("div.product-innfo span.price ins bdi").textContent
                    else
                        price = "call for price"
                    products.push(
                        {
                            'category': String(category),
                            'vendor': String(vendor),
                            'title': String(product_items[i].querySelector("div.product-innfo > h3 > a").textContent),
                            'url': String(product_items[i].querySelector("div.product-innfo > h3 > a").href),
                            'img': String(product_items[i].querySelector("div.product-thumb > div.thumb-inner > a > img").src),
                            'price': price
                        })
                }
            }
            return products
        },obj);
        await page.close();
        await browser.close();
        if(results.length < 1 || nextUrl == null){
            return results
        } else {
            var link = {
                component: obj.component,
                url : nextUrl
            };
            return results.concat(await extractProducts(link))
        }
    };

    const browser = await puppeteer.launch();

    // defines all the links as object
    let cpu  =  {
        component: "cpu",
        url : "https://www.primeabgb.com/buy-online-price-india/cpu-processor/"
    };

    cooler = {
        component: "cooler",
        url : "https://www.primeabgb.com/buy-online-price-india/cpu-cooler/"
    };
    motherboard = {
        component: "motherboard",
        url : "https://www.primeabgb.com/buy-online-price-india/motherboards/"
    };
    memory = {
        component: "memory",
        url : "https://www.primeabgb.com/buy-online-price-india/ram-memory/"
    };
    storage = {
        component: "storage",
        url : "https://www.primeabgb.com/buy-online-price-india/internal-hard-drive/"
    };
    pccase = {
        component: "case",
        url : "https://www.primeabgb.com/buy-online-price-india/pc-cases-cabinet/"
    };
    psu = {
        component: "psu",
        url : "https://www.primeabgb.com/buy-online-price-india/power-supplies-smps/"
    };
    gpu = {
        component: "gpu",
        url : "https://www.primeabgb.com/buy-online-price-india/graphic-cards-gpu/"
    };
    monitor = {
        component: "monitor",
        url : "https://www.primeabgb.com/buy-online-price-india/led-monitors/"
    };

    // create a array of object
    // const links = [cpu, cooler, motherboard, memory, storage, pccase, psu, gpu, monitor];
    const links = [cpu];

    // create a dummy variable for database
    let primeabgb = [];

    // loop through the links array
    for(i = 0; i < links.length; i++) {
        prds = await extractProducts(links[i]);

        // log message for debugging
        console.log(links[i].component + " has been scraped");

        // spread operator
        primeabgb.push(...prds);
    }

    // database
    let client;
    try {
        client = await MongoClient.connect(dbUrl);
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        await db.collection("products").insertMany(primeabgb, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
