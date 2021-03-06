const puppeteer = require('puppeteer');

(async () => {
	const extractProducts = async url => {
		const browser = await puppeteer.launch({headless: false});
		const page = await browser.newPage();
		await page.goto(url);
		const nextUrl = await page.evaluate(() => {
			if(document.querySelector("ul.page-numbers li > a.next"))
				var url = document.querySelector("ul.page-numbers li > a.next").href;
			if(url != null)
				return url
			return null
		});
		const results = await page.evaluate(() => {
			let products = []
			let product_items = document.getElementsByClassName("product-item");
			for(i = 0; i < product_items.length; i++) {
				products.push(
					{
						'title': product_items[i].querySelector("div.product-innfo > h3 > a").textContent,
						'url': product_items[i].querySelector("div.product-innfo > h3 > a").href,
						'price': product_items[i].querySelector("div.product-innfo span.price bdi").textContent
					})
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
	const firstUrl = "https://www.primeabgb.com/buy-online-price-india/ram-memory/?filters=_stock_status[instock]";
	const prds = await extractProducts(firstUrl);
	console.log(prds);
	process.exit();
})();