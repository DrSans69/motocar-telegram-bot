// const link = process.argv[2];
// console.log(process.argv);
const link =
    "https://auto.ria.com/uk/auto_volkswagen_transporter_35726292.html";
const puppeteer = require("puppeteer");

const scrapeData = async (url) => {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: "domcontentloaded" });

    const price = await page.evaluate(() => {
        const priceParent = document
            .querySelector(".price_value")
            .querySelector("strong");
        return priceParent ? priceParent.innerHTML : null;
    });

    await browser.close();

    return price;
};

if (!link) {
    console.error("Please provide a valid link as a command-line argument.");
    process.exit(1);
}

scrapeData(link)
    .then((result) => {
        if (result) {
            console.log("Contaier:", result);
        } else {
            console.log("Could not find");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
    });
