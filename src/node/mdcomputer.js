const puppeteer = require('puppeteer');
var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";
var dbName = "pccomppicker";

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
		const nextUrl = await page.evaluate(() => {
			let page = document.querySelector("ul.pagination > li.active").nextElementSibling;
			if(page != null)
				return page.querySelector("a").href
			return null
		});
		const results = await page.evaluate(() => {
            let vendor = "mdcomputer";
			let products = [];
			let product_titles = document.getElementsByClassName("right-block right-b");
			let product_prices = document.getElementsByClassName("price-new");
			let titleLen = product_titles.length
			let priceLen = product_prices.length
			if(titleLen == priceLen) {
				for(i = 0; i < titleLen; i++) {
					products.push(
						{
                            'vendor': vendor,
							'title': product_titles[i].querySelector("h4 a").textContent.replace(/\t|\n/g,''),
							'url': product_titles[i].querySelector("h4 a").href,
							'price': product_prices[i].textContent.replace(/\t|\n/g,'')
						})
				}
			}
			return products
		});
		await page.close();
		await browser.close();
		if(results.length < 1 || nextUrl == null){
			return results
		} else {
			return results.concat(await extractProducts(nextUrl))
		}
	};

	const browser = await puppeteer.launch();
	const firstUrl = "https://mdcomputers.in/memory?page=1";
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
