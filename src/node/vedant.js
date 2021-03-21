const puppeteer = require('puppeteer');

(async () => {
	const extractProducts = async url => {
		const browser = await puppeteer.launch({headless: false});
		const page = await browser.newPage();
		await page.goto(url);
		await autoScroll(page);
		const results = await page.evaluate(() => {
			let products = []
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
						'title': product_items[i].querySelector(".name").textContent,
						'img': product_items[i].querySelector("img").src,
						'url': product_items[i].querySelector(".name > a").href,
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
	const products = await extractProducts(firstUrl);
	console.table(products);
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
