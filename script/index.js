import { rm } from "fs/promises";
import cron from 'node-cron';
import { exec } from 'child_process';
import path from 'path';
import fs from 'fs';

// 股票名单文件
const STOCK_FILE = path.resolve('stocks.txt');
// 日志目录
const LOG_DIR = path.resolve(process.cwd(), 'test-results');
if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });

async function clearTestResults() {
  const resultsDir = path.resolve("test-results");

  try {
    await rm(resultsDir, { recursive: true, force: true });
    console.log(`🗑️ Cleared: ${resultsDir}`);
  } catch (err) {
    console.error("❌ Failed to clear test-results:", err);
  }
}

clearTestResults();

// Node-cron 定时任务
// 格式："分 时 * * *" 例如每天 03:00 -> "0 3 * * *"
const scheduleTime = '0 3 * * *';


console.log(`🕒 Scheduling Playwright analysis at ${scheduleTime}`);

const schedule = async () => {
  console.log(`🚀 Start running analysis at ${new Date().toISOString()}`);

  const timestamp = new Date().toISOString().replace(/[:T]/g, '-').split('.')[0];
  const logFile = path.join(LOG_DIR, `run-analysis-${timestamp}.log`);

  // 执行 Playwright 测试命令
  // 假设 npm run analysis 可以读取 STOCKS_FILE 环境变量
  const cmd = `STOCKS_FILE=${STOCK_FILE} npm run analysis`;

  console.log(`Running stock, logging to ${logFile}`);
  exec(cmd, (err, stdout, stderr) => {
    fs.appendFileSync(logFile, stdout);
    fs.appendFileSync(logFile, stderr);
    if (err) {
      console.error(`❌ Error running stock:`, err);
    } else {
      console.log(`✅ Finished stock`);
    }
  });
}

cron.schedule(scheduleTime, schedule, {
  scheduled: true,
  timezone: "Asia/Shanghai"
});

// Debug
schedule()