const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  
  const videosDir = path.join(__dirname, 'demo_videos');
  if (!fs.existsSync(videosDir)) {
    fs.mkdirSync(videosDir);
  }

  const context = await browser.newContext({
    recordVideo: { dir: 'demo_videos/', size: { width: 1280, height: 720 } }
  });
  
  const page = await context.newPage();
  
  try {
    console.log("Navigating to localhost...");
    await page.goto('http://localhost:5173');
    
    await page.waitForTimeout(2000);
    
    console.log("Typing query...");
    const input = page.locator('input[placeholder*="discovery query"]');
    await input.click();
    await input.fill('');
    await input.type('Can we cure prion diseases?', { delay: 100 });
    
    console.log("Starting pipeline...");
    const runBtn = page.locator('button#run-pipeline-btn');
    await runBtn.click();
    
    console.log("Waiting for animations...");
    await page.waitForTimeout(8000);
    
    console.log("Generating Academic Paper...");
    const pdfBtn = page.locator('button:has-text("Generate Academic Paper")');
    await pdfBtn.click({ force: true });
    
    await page.waitForTimeout(3500);
    
    await page.locator('button:has-text("×")').click({ force: true });
    await page.waitForTimeout(1000);
    
    console.log("Opening Autonomous PR...");
    const prBtn = page.locator('button:has-text("Open Autonomous PR")');
    await prBtn.click({ force: true });
    
    await page.waitForTimeout(2000);
    
    console.log("Authorizing PR...");
    const authBtn = page.locator('button:has-text("Authorize GitHub PR")');
    await authBtn.click({ force: true });
    
    await page.waitForTimeout(4000);
    
    console.log("Demo successfully recorded!");
  } catch (error) {
    console.error("Error during recording:", error);
  } finally {
    await context.close();
    await browser.close();
  }
})();
