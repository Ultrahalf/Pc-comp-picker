const puppeteer = require('puppeteer');

(async () => {
	const extractProducts = async url => {
		const browser = await puppeteer.launch({headless: false});
		const page = await browser.newPage();
		await page.goto(url);
		await autoScroll(page);
		const results = await page.evaluate(() => {
			let products = []
			let prd = document.querySelectorAll(".product-thumb");
			let len = prd.length
			for(i = 0; i <= len - 1; i++) {
				if(prd[i].querySelector(".price")) {
					if(prd[i].querySelector(".price-new")){
						price = prd[i].querySelector(".price-new").textContent
					}
					else  {
						price = prd[i].querySelector(".price").textContent
					}
				}
				products.push(
					{
						'title': prd[i].querySelector(".name").textContent,
						'url': prd[i].querySelector(".name > a").href,
						'price': price.replace(/\t|\n/g,''),
					})
			}
			return products
			// return len
		});
		await page.close();
		await browser.close();
		return results
	};

	const browser = await puppeteer.launch();
	const firstUrl = "https://www.vedantcomputers.com/pc-components/graphics-card"
	const prds = await extractProducts(firstUrl);
	console.log(prds);
	process.exit();
})();

async function autoScroll(page){
	await page.evaluate(async () => {
		await new Promise((resolve, reject) => {
			var totalHeight = 0;
			var distance = 20;
			var timer = setInterval(() => {
				var scrollHeight = document.body.scrollHeight;
				window.scrollBy(0, distance);
				totalHeight += distance;

				if(totalHeight >= scrollHeight){
					clearInterval(timer);
					resolve();
				}
				if(document.querySelector(".ias-trigger-next a"))
					document.querySelector(".ias-trigger-next > a.btn").click();
			}, 100);
		});
	});
}
