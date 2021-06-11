const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

(async () => {
    const extractProducts = async obj => {
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
        await page.goto(obj.url);
        const results = await page.evaluate((obj) => {
            let products = [];
            let vendor = "itdepot";
            let category = obj.component;
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
                            'category': category,
                            'vendor': vendor,
                            'title': product_items[i].querySelector("div.product-details.text-md-left.flex-grow-1 > div.card-text.px-2.py-1.font-size85.product_title > a").textContent,
                            'img': product_items[i].querySelector("img").src,
                            'url': product_items[i].querySelector("div.product-details.text-md-left.flex-grow-1 > div.card-text.px-2.py-1.font-size85.product_title > a").href,
                            'price': product_items[i].querySelector("strong").textContent
                        })
                }
                if(document.querySelector("ul.pagination > li:last-child > a"))
                    document.querySelector("ul.pagination > li:last-child > a").click();
                j++;
            }
            return products
        },obj);
        await page.close();
        await browser.close();
        return results
    };

    const browser = await puppeteer.launch();
    let prds = 0;

    // defines all the links as object
    let cpu  =  {
        component: "cpu",
        url : "https://www.theitdepot.com/products-Processors_C30.html"
    };

    cooler = {
        component: "cooler",
        url : "https://www.theitdepot.com/products-Cooling+Devices_C10.html"
    };
    motherboard = {
        component: "motherboard",
        url : "https://www.theitdepot.com/products-Motherboards_C13.html"
    };
    memory = {
        component: "memory",
        url : "https://www.theitdepot.com/products-RAM+(Memory)_C6.html"
    };
    storage = {
        component: "storage",
        url : "https://www.theitdepot.com/products-Hard+Drives+HDD_C12.html"
    };
    pccase = {
        component: "case",
        url : "https://www.theitdepot.com/products-Computer+Cabinets_C5.html"
    };
    psu = {
        component: "psu",
        url : "https://www.theitdepot.com/products-PSU+(+Power+Supply+Units)_C14.html"
    };
    gpu = {
        component: "gpu",
        url : "https://www.theitdepot.com/products-Graphic+Cards_C45.html"
    };
    monitor = {
        component: "monitor",
        url : "https://www.theitdepot.com/products-Monitor_C7.html"
    };

    // create a array of object
    const links = [cpu, cooler, motherboard, memory, storage, pccase, psu, gpu, monitor];
    let itdepot = []
    // loop through the links array
    for(i = 0; i < links.length; i++) {
        prds = await extractProducts(links[i]);
        // spread operator
        itdepot.push(...prds);
    }

    let client;
    try {
        client = await MongoClient.connect(dbUrl);
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        await db.collection("products").insertMany(itdepot, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
