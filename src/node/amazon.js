const puppeteer = require('puppeteer');

(async () => {
	const extractProducts = async url => {
		const browser = await puppeteer.launch({headless: false});
		const page = await browser.newPage();
		await page.goto(url);
		const nextUrl = await page.evaluate(() => {
			if(document.querySelector("ul > li.a-last > a"))
				var url = document.querySelector("ul > li.a-last > a").href;
			if(url != null)
				return url
			return null
		});
		const results = await page.evaluate(() => {
			let products = [];
			let product_items = document.getElementsByClassName("s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16");
			for(i = 0; i < product_items.length; i++) {
				if(product_items[i].querySelector("h2 > a") && product_items[i].querySelector(".a-price-whole")) {
					products.push(
						{
							'title': product_items[i].querySelector("h2 > a").textContent.replace(/\t|\n/g,''),
							'url': product_items[i].querySelector("h2 > a").href,
							'price': product_items[i].querySelector(".a-price-whole").textContent
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
	const firstUrl = "https://www.amazon.in/s?k=processsor&ref=nb_sb_noss_2";
	const prds = await extractProducts(firstUrl);
	console.log(prds);
	process.exit();
})();
