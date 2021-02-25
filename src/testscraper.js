/*vedantcomputer*/
let product_items = document.getElementsByClassName("product-thumb");
for(i = 0; i <= product_items.length; i++) {
	if(product_items[i].querySelector(".price-new")){
		price = product_items[i].querySelector(".price-new").textContent
	}
	else  {
		price = product_items[i].querySelector(".price").textContent
	}
	console.log(product_items[i].querySelector(".name").textContent)
	console.log(product_items[i].querySelector(".name > a").href)
	console.log(price);
}
/************************************************************/
/*theitdepot*/
let product_items = document.getElementsByClassName("product-item");
for(i = 0; i < product_items.length; i++) {
	console.log(product_items[i].querySelector("div.product-details.text-md-left.flex-grow-1 > div.card-text.px-2.py-1.font-size85.product_title > a").textContent);
	console.log(product_items[i].querySelector("div.product-details.text-md-left.flex-grow-1 > div.card-text.px-2.py-1.font-size85.product_title > a").href);
	console.log(product_items[i].querySelector("strong").textContent);
}
/******************************************************************************/
/*primeadgb*/
let product_items = document.getElementsByClassName("product-item");
for(i = 0; i < product_items.length; i++) {
	console.log(product_items[i].querySelector("div.product-innfo > h3 > a").textContent);
	console.log(product_items[i].querySelector("div.product-innfo > h3 > a").href);
	console.log(product_items[i].querySelector("div.product-innfo > span > ins > span > bdi").textContent);
}

/******************************************************************************/
/*amazon*/
	let product_items = document.getElementsByClassName("sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20");
for(i = 0; i < product_items.length; i++) {
console.log(product_items[i].querySelector("h2 > a").textContent.replace(/\t|\n/g,''))
console.log(product_items[i].querySelector("h2 > a").href)
console.log(product_items[i].querySelector(".a-price-whole").textContent)
}
/******************************************************************************/
