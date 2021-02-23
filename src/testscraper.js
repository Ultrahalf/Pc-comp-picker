const puppeteer = require('puppeteer');

(async () => {
	const extractProducts = async url => {
		const browser = await puppeteer.launch({headless: false});
		const page = await browser.newPage();
		await page.goto(url);
		const results = await page.evaluate(() => {
			let products = []
			let prd_titles = document.getElementsByClassName("right-block right-b");
			let prd_prices = document.getElementsByClassName("price-new");
			if(prd_titles.length == prd_prices.length) {
				for(i = 0; i < prd_titles.length; i++) {
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
		if(results.length < 1){
			return results
		} else {
			const nextPageNumber = parseInt(url.match(/page=(\d+)$/)[1], 10) + 1;
			const nextUrl = `https://mdcomputers.in/memory?page=${nextPageNumber}`;
			return results.concat(await extractProducts(nextUrl))
		}
	};

	const browser = await puppeteer.launch();
	const firstUrl =
		"https://mdcomputers.in/memory?page=1";
	const prds = await extractProducts(firstUrl);
	console.log(prds);
})();
