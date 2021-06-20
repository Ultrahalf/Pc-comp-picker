const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

(async () => {
    const extractProducts = async obj => {
        const browser = await puppeteer.launch({headless: true});
        const page = await browser.newPage();

        //disable css
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
            let page = document.querySelector("ul.pagination > li.active").nextElementSibling;
            if(page != null)
                return page.querySelector("a").href
            return null
        });

        // evaluate the page and return the products
        const results = await page.evaluate((obj) => {
            let vendor = "mdcomputer";
            let products = [];
            let category = obj.component;
            let product_titles = document.getElementsByClassName("right-block right-b");
            let product_prices = document.getElementsByClassName("price-new");
            let titleLen = product_titles.length
            let priceLen = product_prices.length
            if(titleLen == priceLen) {
                for(i = 0; i < titleLen; i++) {
                    products.push(
                        {
                            'category': String(category),
                            'vendor': String(vendor),
                            'title': String(product_titles[i].querySelector("h4 a").textContent.replace(/\t|\n/g,'')),
                            'url': String(product_titles[i].querySelector("h4 a").href),
                            'price': product_prices[i].textContent.replace(/\t|\n/g,'')
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
        url : "https://mdcomputers.in/processor"
    };

    cooler = {
        component: "cooler",
        url : "https://mdcomputers.in/cooling-system"
    };
    motherboard = {
        component: "motherboard",
        url : "https://mdcomputers.in/motherboards"
    };
    memory = {
        component: "memory",
        url : "https://mdcomputers.in/memory"
    };
    storage = {
        component: "storage",
        url : "https://mdcomputers.in/storage"
    };
    pccase = {
        component: "case",
        url : "https://mdcomputers.in/cabinet"
    };
    psu = {
        component: "psu",
        url : "https://mdcomputers.in/smps"
    };
    gpu = {
        component: "gpu",
        url : "https://mdcomputers.in/graphics-card"
    };
    monitor = {
        component: "monitor",
        url : "https://mdcomputers.in/monitors"
    };

    // create a array of object
    const links = [cpu, cooler, motherboard, memory, storage, pccase, psu, gpu, monitor];

    // dummy variable for database
    let mdcomputer = [];

    // loop through the links array
    for(i = 0; i < links.length; i++) {
        prds = await extractProducts(links[i]);

        // log message for debugging
        console.log(links[i].component + " has been scraped");

        // spread operator
        mdcomputer.push(...prds);
    }

    // Database
    let client;
    try {
        client = await MongoClient.connect(dbUrl);
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        await db.collection("products").insertMany(mdcomputer, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
