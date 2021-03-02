const puppeteer = require('puppeteer');

(async () => {
	const extractProducts = async url => {
		const browser = await puppeteer.launch({headless: false});
		const page = await browser.newPage();
		await page.goto(url);
		const nextUrl = await page.evaluate(() => {
			let page = document.querySelector("ul.pagination > li.active").nextElementSibling;
			if(page != null)
				return page.querySelector("a").href
			return null
		});
		const results = await page.evaluate(() => {
			let products = []
			let prd_titles = document.getElementsByClassName("right-block right-b");
			let prd_prices = document.getElementsByClassName("price-new");
			let tottitle = prd_titles.length
			let totprice = prd_prices.length
			if(tottitle == totprice) {
				for(i = 0; i < tottitle; i++) {
					products.push(
						{
							'title': prd_titles[i].querySelector("h4 a").textContent.replace(/\t|\n/g,''),
							'url': prd_titles[i].querySelector("h4 a").href,
							'price': prd_prices[i].textContent.replace(/\t|\n/g,'')
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
	console.log(prds);
	process.exit();
})();
