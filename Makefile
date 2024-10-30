all: run

run_cpu:
	python3 main.py stats.txt --category cpu

run_lsq:
	python3 main.py stats.txt --category lsq

run_fu:
	python3 main.py stats.txt --category fu

run_cache:
	python3 main.py stats.txt --category cache

run_bp:
	python3 main.py stats.txt --category bp

run_mem_ctrl:
	python3 main.py stats.txt --category mem_ctrl

run_mem_ctrl_balance:
	python3 main.py stats.txt --category mem_ctrl_balance

