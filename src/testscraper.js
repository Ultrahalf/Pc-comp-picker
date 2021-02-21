const puppeteer = require('puppeteer');

let scrape = async () => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.goto('https://mdcomputers.in/memory');
  const nextbtn = await page.evaluate(() => {
   return document.querySelector("li.active").nextElementSibling
});
  const result = await page.evaluate(() => {
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
	  return {
		products
	  }
   });
  await browser.close();
  return result;
};

scrape().then((value) => {
    console.log(value);
});
