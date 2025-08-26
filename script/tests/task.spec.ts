import fs from "fs";
import { test} from "@playwright/test";

const stockCodes = fs.readFileSync("stocks.txt", "utf-8")
.split("\n")
.map(line => line.trim())
.filter(Boolean); // 去掉空行

test.describe.parallel("run agent", async () => {
  for (const stockCode of stockCodes) {
    test(`run analysis for ${stockCode}`, async ({ page }) => {
      test.setTimeout(45 * 60 * 1000)
      
      try {
        // Try internal network if it not reachable.
        await page.goto("http://localhost:8501");
        await page.getByTestId('stBaseButton-primary').waitFor()
        
        await page.getByRole('textbox', { name: 'Ticker Symbol' }).fill(stockCode)
        await page.getByRole("button", { name: "Run Analysis" }).click();
        
        await page.getByText("Analysis completed successfully!").waitFor({timeout:40 * 60 * 1000})

        console.log(`✅ ${stockCode} 分析完成`);
      } catch (err) {
        console.error(`❌ ${stockCode} 超时未完成，保存截图`);
  
        const now = new Date();
        const timestamp = now.toISOString().replace(/[:T]/g, "-").split(".")[0];
        const filename = `./test-results/${timestamp}_${stockCode}.png`;
  
        await page.screenshot({ path: filename, fullPage: true });
        throw err;
      }
    });
  }
})