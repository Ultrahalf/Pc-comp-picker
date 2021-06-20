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
            if(document.querySelector("ul > li.a-last > a")) {
                var url = document.querySelector("ul > li.a-last > a").href;
            }
            if(url != null) {
                return url
            } else {
                return null
            }
        });

        // evaluate the page and return the products
        const results = await page.evaluate((obj) => {
            let products = [];
            let vendor = "amazon";
            let category = obj.component;
            let product_items = document.getElementsByClassName("s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16");
            for(i = 0; i < product_items.length; i++) {
                if(product_items[i].querySelector("h2 > a") && product_items[i].querySelector(".a-price-whole")) {
                    products.push(
                        {
                            'category': String(category),
                            'vendor': String(vendor),
                            'title': String(product_items[i].querySelector("h2 > a").textContent.replace(/\t|\n/g,'')),
                            'img': String(product_items[i].querySelector("img").src),
                            'url': String(product_items[i].querySelector("h2 > a").href),
                            'price': product_items[i].querySelector(".a-price-whole").textContent,
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
            if (count < 3) {
                count += 1;
                var link = {
                    component: obj.component,
                    url : nextUrl
                };
                return results.concat(await extractProducts(link))
            } else {
                return results
            }
        }
    };

    const browser = await puppeteer.launch();

    // defines all the links as object
    let cpu  =  {
        component: "cpu",
        url : "https://www.amazon.in/s?k=processor&i=computers&rh=n%3A1375391031%2Cp_89%3AAMD%7CIntel&dc&qid=1623516011&rnid=3837712031&ref=sr_nr_p_89_2"
    };

    cooler = {
        component: "cooler",
        url : "https://www.amazon.in/s?k=cpu+cooler&i=computers&ref=nb_sb_noss_1"
    };
    motherboard = {
        component: "motherboard",
        url : "https://www.amazon.in/s?k=motherboard&i=computers&ref=nb_sb_noss_2"
    };
    memory = {
        component: "memory",
        url : "https://www.amazon.in/s?k=ram&i=computers&ref=nb_sb_noss_1"
    };
    storage = {
        component: "storage",
        url : "https://www.amazon.in/s?k=internal+storage&i=computers&ref=nb_sb_noss_1"
    };
    pccase = {
        component: "case",
        url : "https://www.amazon.in/s?k=computer+cabinet&i=computers&crid=232R6EQYRLEGJ&sprefix=computer+cabin%2Ccomputers%2C356&ref=nb_sb_ss_ts-doa-p_1_14"
    };
    psu = {
        component: "psu",
        url : "https://www.amazon.in/s?k=power+supply+unit&i=computers&ref=nb_sb_noss"
    };
    gpu = {
        component: "gpu",
        url : "https://www.amazon.in/s?k=graphic+cards&i=computers&rh=n%3A976392031%2Cp_89%3AAORUS%7CASUS%7CDEEPCOOL%7CDell%7CEVGA%7CGIGABYTE%7CGalax%7CInno3D%7CMSI%7CPNY%7CREO%7CSapphire%7CZotac%7CnVidia&dc&crid=15QXD8DOCE57G&qid=1623516408&rnid=3837712031&sprefix=graphic%2Caps%2C341&ref=sr_nr_p_89_17"
    };
    monitor = {
        component: "monitor",
        url : "https://www.amazon.in/s?k=monitor&ref=nb_sb_noss_1"
    };

    // create a array of object
    const links = [cpu, cooler, motherboard, memory, storage, pccase, psu, gpu, monitor];

    // create a dummy variable for database
    let amazon = [];

    // loop through the links array
    for(i = 0; i < links.length; i++) {
        // count to set the number of pages to vist per category
        count = 1;
        prds = await extractProducts(links[i]);

        // log message for debugging
        console.log(links[i].component + " has been scraped");

        // spread operator
        amazon.push(...prds);
    }

    // Database
    let client;
    try {
        client = await MongoClient.connect(dbUrl);
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        await db.collection("products").insertMany(amazon, function(err, res) {
            if (err) throw err;
            db.close();
        });
    } catch (err) {
        console.log(err.stack);
    }
    client.close();
    process.exit();
})();
