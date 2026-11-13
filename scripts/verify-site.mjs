import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.resolve(root, "../verification/site");
await mkdir(output, { recursive: true });
const origin = "http://127.0.0.1:7100";
const server = spawn(process.execPath, [path.join(root, "scripts/dev-server.mjs"), "--host", "127.0.0.1", "--port", "7100"], { stdio: ["ignore", "pipe", "pipe"] });
let serverLog = "";
server.stdout.on("data", (chunk) => { serverLog += chunk; });
server.stderr.on("data", (chunk) => { serverLog += chunk; });

const results = { checks: [], consoleErrors: [], pageErrors: [], failedRequests: [], badResponses: [], screenshots: [], performance: {} };
const check = (condition, name, detail = "") => {
  results.checks.push({ name, pass: Boolean(condition), detail });
  if (!condition) throw new Error(`${name}${detail ? `: ${detail}` : ""}`);
};
const waitForServer = async () => {
  for (let i = 0; i < 80; i += 1) {
    try { const response = await fetch(origin); if (response.ok) return; } catch {}
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`Preview server did not start: ${serverLog}`);
};

let browser;
try {
  await waitForServer();
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: "en-US", permissions: ["clipboard-read", "clipboard-write"] });
  const page = await context.newPage();
  await page.route(/(plausible\.io|static\.cloudflareinsights\.com)/, (route) => route.fulfill({ status: 200, contentType: "application/javascript", body: "" }));
  page.on("console", (message) => { if (message.type() === "error") results.consoleErrors.push(message.text()); });
  page.on("pageerror", (error) => results.pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    const reason = request.failure()?.errorText || "";
    if (reason !== "net::ERR_ABORTED") results.failedRequests.push(`${request.url()} ${reason}`);
  });
  page.on("response", (response) => { if (response.status() >= 400) results.badResponses.push(`${response.status()} ${response.url()}`); });

  const sitemap = await readFile(path.join(root, "sitemap.xml"), "utf8");
  const urls = [...sitemap.matchAll(/<loc>https:\/\/tryfeedflow\.app(.*?)<\/loc>/g)].map((match) => match[1] || "/");
  const shot = async (name, fullPage = true) => {
    if (fullPage) {
      await page.evaluate(async () => {
        const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
        document.documentElement.style.scrollBehavior = "auto";
        const height = document.documentElement.scrollHeight;
        for (let y = 0; y < height; y += Math.max(400, innerHeight * 0.75)) {
          window.scrollTo(0, y);
          await pause(45);
        }
        window.scrollTo(0, 0);
        await pause(100);
      });
      await page.waitForFunction(() => Array.from(document.images).every((image) => image.complete), null, { timeout: 4000 }).catch(() => {});
      const unloaded = await page.evaluate(() => Array.from(document.images).filter((image) => !image.complete || image.naturalWidth === 0).map((image) => image.currentSrc || image.src));
      check(unloaded.length === 0, `Every image loaded for ${name}`, unloaded.join(", "));
    }
    const file = path.join(output, `${name}.jpg`);
    await page.screenshot({ path: file, fullPage, type: "jpeg", quality: 82 });
    results.screenshots.push(file);
  };

  for (const url of urls) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(origin + url, { waitUntil: "networkidle" });
    check(await page.locator("h1").count() === 1, `One h1 on ${url}`);
    const dimensions = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
    check(dimensions.document <= dimensions.viewport + 1 && dimensions.body <= dimensions.viewport + 1, `No desktop overflow on ${url}`, JSON.stringify(dimensions));
    const name = url === "/" ? "home" : url.replace(/^\//, "").replaceAll("/", "-").replace(".html", "");
    await shot(`desktop-${name}`);
  }

  for (const width of [375, 768, 1024]) {
    for (const url of urls) {
      await page.setViewportSize({ width, height: 844 });
      await page.goto(origin + url, { waitUntil: "domcontentloaded" });
      await page.waitForTimeout(100);
      const dimensions = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
      check(dimensions.document <= dimensions.viewport + 1 && dimensions.body <= dimensions.viewport + 1, `No ${width}px overflow on ${url}`, JSON.stringify(dimensions));
      if (url === "/" || url === "/growth-development" || url === "/solids-allergens" || url === "/ambassador") {
        const name = url === "/" ? "home" : url.replace(/^\//, "");
        await shot(`${width}-${name}`);
      }
    }
  }

  // Desktop navigation and theme.
  await page.setViewportSize({ width: 1440, height: 900 });
  for (const item of [{ text: "Feeding", hash: "#feeding" }, { text: "Growth", hash: "#growth" }, { text: "Health", hash: "#health" }]) {
    await page.goto(origin, { waitUntil: "domcontentloaded" });
    await page.locator(".desktop-nav").getByRole("link", { name: item.text, exact: true }).click();
    check(new URL(page.url()).hash === item.hash, `Desktop ${item.text} navigation`);
  }
  await page.goto(origin, { waitUntil: "networkidle" });
  const oldTheme = await page.locator("html").getAttribute("data-theme");
  await page.locator("#themeToggle").click();
  check(await page.locator("html").getAttribute("data-theme") !== oldTheme, "Theme toggle changes theme");
  await shot("desktop-home-dark", false);
  await page.locator("#themeToggle").click();

  // Mobile menu opens, navigates and closes.
  await page.setViewportSize({ width: 375, height: 844 });
  await page.goto(origin, { waitUntil: "domcontentloaded" });
  await page.locator("#menuToggle").click();
  check(await page.locator("#menuToggle").getAttribute("aria-expanded") === "true" && await page.locator("#mobileNav").isVisible(), "Mobile menu opens");
  await page.locator("#mobileNav").getByRole("link", { name: /Growth & development/ }).click();
  check(new URL(page.url()).hash === "#growth" && await page.locator("#mobileNav").isHidden(), "Mobile menu navigates and closes");
  await page.locator("#menuToggle").click();
  await page.keyboard.press("Escape");
  check(await page.locator("#mobileNav").isHidden(), "Escape closes mobile menu");

  // Automatic and manual review localization.
  const locales = [
    { locale: "sv-SE", option: "sv", first: "Mycket användbar app", label: "Svenska" },
    { locale: "no-NO", option: "nb", first: "Veldig nyttig app", label: "Norsk" },
    { locale: "ja-JP", option: "en", first: "Very useful app", label: "English" }
  ];
  for (const item of locales) {
    const localContext = await browser.newContext({ viewport: { width: 1024, height: 800 }, locale: item.locale });
    const localPage = await localContext.newPage();
    await localPage.route(/(plausible\.io|static\.cloudflareinsights\.com)/, (route) => route.fulfill({ status: 200, contentType: "application/javascript", body: "" }));
    await localPage.goto(origin, { waitUntil: "networkidle" });
    const quote = await localPage.locator('[data-review-index="0"] blockquote').textContent();
    check(quote.startsWith(item.first), `Automatic review translation for ${item.locale}`, quote);
    check((await localPage.locator("#reviewLanguage").inputValue()) === "auto", `Automatic option selected for ${item.locale}`);
    check((await localPage.locator("#reviewLanguageStatus").textContent()).includes(item.label), `Review status names ${item.label}`);
    await localContext.close();
  }
  await page.setViewportSize({ width: 1024, height: 800 });
  await page.goto(origin, { waitUntil: "networkidle" });
  await page.locator("#reviewLanguage").selectOption("nb");
  check((await page.locator('[data-review-index="0"] blockquote').textContent()).startsWith("Veldig nyttig app"), "Manual Norwegian review translation");
  await page.reload({ waitUntil: "networkidle" });
  check((await page.locator("#reviewLanguage").inputValue()) === "nb", "Review language persists after reload");
  const originalSwedish = "Super enkel app och har hjälpt mig att få koll på min amning.";
  await page.locator('[data-review-index="2"] .review-toggle').click();
  check((await page.locator('[data-review-index="2"] blockquote').textContent()).startsWith(originalSwedish), "Original Swedish review remains available");
  await page.locator('[data-review-index="2"] .review-toggle').click();
  check((await page.locator('[data-review-index="2"] blockquote').getAttribute("lang")) === "nb", "Translated review can be restored");

  // Ambassador sharing, validation and successful form submission.
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(origin + "/ambassador", { waitUntil: "networkidle" });
  await page.locator("#amb-submit").click();
  check(await page.locator("#formStatus").isVisible(), "Empty ambassador form shows validation feedback");
  await page.getByRole("button", { name: "Share the application link" }).click();
  await page.waitForTimeout(150);
  const clipboard = await page.evaluate(() => navigator.clipboard.readText());
  check(clipboard === "https://tryfeedflow.app/ambassador", "Ambassador application link copies", clipboard);
  await page.locator("#amb-name").fill("Test Applicant");
  await page.locator("#amb-email").fill("test@example.com");
  await page.locator("#amb-country").fill("Norway");
  await page.locator("#amb-role").selectOption({ label: "IBCLC / lactation consultant" });
  await page.locator("#p-pr").check();
  await page.locator("#amb-handle").fill("https://example.com/practice");
  await page.locator("#amb-note").fill("I support families with feeding and want to share a useful record-keeping tool.");
  await page.locator("#amb-consent").check();
  let postedBody = "";
  await page.route(origin + "/", async (route) => {
    if (route.request().method() === "POST") {
      postedBody = route.request().postData() || "";
      await route.fulfill({ status: 200, contentType: "text/html", body: "OK" });
    } else await route.continue();
  });
  await page.locator("#amb-submit").click();
  await page.locator("#formStatus.success").waitFor();
  check((await page.locator("#formStatus").textContent()).includes("received"), "Ambassador form shows successful submission");
  check(postedBody.includes("Test+Applicant") && postedBody.includes("Professional+practice"), "Ambassador form submits expected fields", postedBody);
  await page.locator(".faq-list summary").first().click();
  check(await page.locator(".faq-list details").first().getAttribute("open") !== null, "Ambassador FAQ opens");

  // Homepage performance, excluding intentionally stubbed third-party analytics.
  await page.goto(origin, { waitUntil: "networkidle" });
  results.performance = await page.evaluate(() => {
    const resources = performance.getEntriesByType("resource");
    return {
      requestsIncludingDocument: resources.length + 1,
      encodedBodyBytes: resources.reduce((sum, entry) => sum + (entry.encodedBodySize || 0), 0),
      domContentLoadedMs: Math.round(performance.getEntriesByType("navigation")[0]?.domContentLoadedEventEnd || 0),
      loadMs: Math.round(performance.getEntriesByType("navigation")[0]?.loadEventEnd || 0)
    };
  });
  check(results.consoleErrors.length === 0, "Zero browser console errors", results.consoleErrors.join("\n"));
  check(results.pageErrors.length === 0, "Zero uncaught page errors", results.pageErrors.join("\n"));
  check(results.failedRequests.length === 0, "Zero failed requests", results.failedRequests.join("\n"));
  check(results.badResponses.length === 0, "Zero HTTP 4xx/5xx responses", results.badResponses.join("\n"));
  await writeFile(path.join(output, "results.json"), JSON.stringify(results, null, 2));
  console.log(`Verified ${results.checks.length} checks, ${results.screenshots.length} screenshots, ${results.performance.requestsIncludingDocument} measured home requests.`);
} catch (error) {
  results.failure = error.stack;
  await writeFile(path.join(output, "results.json"), JSON.stringify(results, null, 2));
  console.error(error.stack);
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  server.kill("SIGTERM");
  await new Promise((resolve) => { server.once("exit", resolve); setTimeout(resolve, 1000); });
}
