const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

(async () => {
    const extractProducts = async obj => {
        const browser = await puppeteer.launch({headless: false});
        const page = await browser.newPage();

        await page.goto(obj.url);

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

        // check if there's next page button
        const nextUrl = await page.evaluate(() => {
            if(document.querySelector("ul.pagination-custom > li:last-child a"))
                var url = document.querySelector("ul.pagination-custom> li:last-child a").href;
            if(url != null)
                return url
            return null
        });

        // evaluate the page and return products
        const results = await page.evaluate((obj) => {
            let products = [];
            let vendor = "computerspace";
            let category = obj.component;
            var product_items = document.querySelectorAll("#shopify-section-collection-template > div.grid > div:nth-child(2) > div .grid__item");
            var len = product_items.length;
            for(i = 0;i <= len -1; i++){
                products.push(
                    {
                        'category': category,
                        'vendor': vendor,
                        'title': product_items[i].querySelector("p.product-title").textContent,
                        'img': product_items[i].querySelector("img").src,
                        'url': product_items[i].querySelector("div.grid div > a").href,
                        'price': product_items[i].querySelector(".price-dis-sec span.money").textContent
                    })
            }
            return products
        },obj);
        await page.close();
        await browser.close();
        if(results.length < 1 || nextUrl == null) {
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
        url : "https://computerspace.in/collections/processor"
    };

    cooler = {
        component: "cooler",
        url : "https://computerspace.in/collections/liquid-coolers"
    };
    motherboard = {
        component: "motherboard",
        url : "https://computerspace.in/collections/motherboard"
    };
    memory = {
        component: "memory",
        url : "https://computerspace.in/collections/ram"
    };
    storage = {
        component: "storage",
        url : "https://computerspace.in/collections/storage"
    };
    pccase = {
        component: "case",
        url : "https://computerspace.in/collections/cabinets"
    };
    psu = {
        component: "psu",
        url : "https://computerspace.in/collections/power-supply-unit"
    };
    gpu = {
        component: "gpu",
        url : "https://computerspace.in/collections/graphics-card"
    };
    monitor = {
        component: "monitor",
        url : "https://computerspace.in/collections/monitor"
    };

    // create a array of object
    const links = [cpu, cooler, motherboard, memory, storage, pccase, psu, gpu, monitor];

    // dummy variable for database
    let computerspace = [];

    // loop through the links array
    for(i = 0; i < links.length; i++) {
        prds = await extractProducts(links[i]);

        //log message for debugging
        console.log(links[i].component + " has been scraped");

        // spread operator
        computerspace.push(...prds);
    }

    // Database
    let client;
    try {
        client = await MongoClient.connect(dbUrl, { useNewUrlParser: true, useUnifiedTopology: true });
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        await db.collection("products").insertMany(computerspace, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
