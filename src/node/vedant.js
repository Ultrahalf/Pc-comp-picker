const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

(async () => {
    const extractProducts = async obj => {
        const browser = await puppeteer.launch({headless: false});
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

        // evaluate the page and return the products
        const results = await page.evaluate((obj) => {
            let products = [];
            let vendor = "vedant";
            let category = obj.component;
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
                        'category': category,
                        'vendor': vendor,
                        'title': product_items[i].querySelector(".name").textContent,
                        'img': product_items[i].querySelector("img").src,
                        'url': product_items[i].querySelector(".name > a").href,
                        'price': price.replace(/\t|\n/g,''),
                    })
            }
            return products
        }, obj);
        await page.close();
        await browser.close();
        if (results.length < 1) {
            return results
        } else {
            const nextPageNumber = parseInt(obj.url.match(/page=(\d+)$/)[1], 10) + 1;
            let nextUrl = obj.url.replace(/page=(\d+)$/, 'page=' + nextPageNumber)
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
        url : "https://www.vedantcomputers.com/pc-components/processor?page=1"
    };

    cooler = {
        component: "cooler",
        url : "https://www.vedantcomputers.com/pc-components/fans-and-cooling?page=1"
    };
    motherboard = {
        component: "motherboard",
        url : "https://www.vedantcomputers.com/pc-components/motherboard?page=1"
    };
    memory = {
        component: "memory",
        url : "https://www.vedantcomputers.com/pc-components/memory?page=1"
    };
    storage = {
        component: "storage",
        url : "https://www.vedantcomputers.com/pc-components/storage?page=1"
    };
    pccase = {
        component: "case",
        url : "https://www.vedantcomputers.com/pc-components/cabinet?page=1"
    };
    psu = {
        component: "psu",
        url : "https://www.vedantcomputers.com/pc-components/power-supply?page=1"
    };
    gpu = {
        component: "gpu",
        url : "https://www.vedantcomputers.com/pc-components/graphics-card?page=1"
    };
    monitor = {
        component: "monitor",
        url : "https://www.vedantcomputers.com/pc-components/monitor?page=1"
    };

    // create a array of object
    const links = [cpu, cooler, motherboard, memory, storage, pccase, psu, gpu, monitor];

    // create a dummy variable for database
    let vedant = [];

    // loop through the links array
    for(i = 0; i < links.length; i++) {
        prds = await extractProducts(links[i]);

        // log message for debugging
        console.log(links[i].component + " has been scraped");

        // spread operator
        vedant.push(...prds);
    }

    // database
    let client;
    try {
        client = await MongoClient.connect(dbUrl);
        console.log("Connected correctly to server");
        const db = client.db(dbName, { useUnifiedTopology: true });
        await db.collection("products").insertMany(vedant, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
