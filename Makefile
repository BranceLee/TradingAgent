# 默认股票代码文件
STOCKS_FILE ?= script/stocks.txt
# 默认执行时间（可通过参数覆盖）
TIME ?= "16:54"

run-cli:
	python -m cli.main

# 运行定时调度任务
run-task:
	@echo "Running Playwright analysis for stocks in $(STOCKS_FILE)..."
	@(cd $(PWD)/script && npm run task)

run-analysis:
	@(cd $(PWD)/script && npm run analysis)

start:
	@set -a; \
	. .env; \
	set +a; \
	streamlit run app.py
