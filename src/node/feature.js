const puppeteer = require('puppeteer');
const args = process.argv;

(async () => {
    const extractProducts = async url => {
        const browser = await puppeteer.launch({headless: true});
        const page = await browser.newPage();

        await page.goto(url);

        const results = await page.evaluate(() => {
            let temp = {}
            trs = document.querySelectorAll("table tr");
            for(i=0; i < trs.length; i++) {
                tds = trs[i].querySelectorAll("td");
                if(tds.length > 1){
                    feature = tds[0].innerText;
                    value = tds[1].innerText;
                    console.log(feature);
                    console.log(value);
                    features = {};
                    features[feature] = value;
                    temp = {...temp,...features};
                }
            }
            return temp
        });
        await page.close();
        await browser.close();
        return results
    };
    const browser = await puppeteer.launch();
    // let url = args.slice(-1);
    let url = args.pop()
    console.log(url);
    prds = await extractProducts(url);
    console.table(prds);
    process.exit();
})();
