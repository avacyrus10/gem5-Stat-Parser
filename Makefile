
all: help

help:
	@echo "Usage:"
	@echo "  make run FILES='<file_paths>' CATEGORY='<category>'"
	@echo ""
	@echo "Available Commands:"
	@echo "  make run_cpu FILES='<file_paths>'     Run CPU statistics for specified files"
	@echo "  make run_lsq FILES='<file_paths>'     Run Load/Store Queue statistics"
	@echo "  make run_fu FILES='<file_paths>'      Run Functional Unit statistics"
	@echo "  make run_cache FILES='<file_paths>'   Run Cache statistics"
	@echo "  make run_bp FILES='<file_paths>'      Run Branch Predictor statistics"
	@echo "  make run_mem_ctrl FILES='<file_paths>'    Run Memory Controller statistics"
	@echo "  make run_mem_ctrl_balance FILES='<file_paths>' Run Memory Controller Balance statistics"
	@echo ""
	@echo "Arguments:"
	@echo "  FILES='<file_paths>'     Paths to the input stat files, separated by spaces (e.g., 'stats1.txt stats2.txt')"
	@echo "  CATEGORY='<category>'    Specify the category of statistics (cpu, lsq, fu, cache, bp, mem_ctrl, mem_ctrl_balance)"
	@echo ""
	@echo "Example:"
	@echo "  make run FILES='stats1.txt stats2.txt' CATEGORY=cpu"


run:
	@if [ -z "$(FILES)" ] || [ -z "$(CATEGORY)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run FILES='<file_paths>' CATEGORY='<category>'"; \
	else \
		python3 main.py $(FILES) --category $(CATEGORY); \
	fi

run_cpu:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_cpu FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category cpu; \
	fi

run_lsq:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_lsq FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category lsq; \
	fi

run_fu:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_fu FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category fu; \
	fi

run_cache:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_cache FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category cache; \
	fi

run_bp:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_bp FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category bp; \
	fi

run_mem_ctrl:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_mem_ctrl FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category mem_ctrl; \
	fi

run_mem_ctrl_balance:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required arguments."; \
		echo "Usage: make run_mem_ctrl_balance FILES='<file_paths>'"; \
	else \
		python3 main.py $(FILES) --category mem_ctrl_balance; \
	fi
	
run_all:
	@if [ -z "$(FILES)" ]; then \
		echo "Error: Missing required argument FILES."; \
		echo "Usage: make run_all FILES='<file_paths>'"; \
	else \
		$(MAKE) run_cpu FILES="$(FILES)"; \
		$(MAKE) run_lsq FILES="$(FILES)"; \
		$(MAKE) run_fu FILES="$(FILES)"; \
		$(MAKE) run_cache FILES="$(FILES)"; \
		$(MAKE) run_bp FILES="$(FILES)"; \
		$(MAKE) run_mem_ctrl FILES="$(FILES)"; \
		$(MAKE) run_mem_ctrl_balance FILES="$(FILES)"; \
	fi
	
	

