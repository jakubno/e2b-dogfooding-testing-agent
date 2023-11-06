const playwright = require('playwright');

async function setupBrowser() {
    const browser = await playwright['chromium'].launch();
    const context = await browser.newContext();
    const page = await context.newPage();
    return { browser, page };
}

module.exports = setupBrowser;