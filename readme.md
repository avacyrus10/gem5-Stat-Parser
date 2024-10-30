# gem5 Stat Parser

This project extracts and displays statistics from the `stats.txt` file generated by the gem5 simulator. The user can choose which group of statistics to display, such as CPU stats, Load/Store Queue stats, Functional Unit stats, Cache stats, Branch Prediction stats, and Memory Controller stats.

## Features

- Extracts statistics for the active CPU.
- Displays statistics grouped into different categories.
- Allows the user to choose which group of stats to display via command-line options.

## Usage

### Prerequisites

- Python 3.x installed.
- The `colorama` library for colored terminal output. Install it via:

```bash
pip install colorama
```
## Using the Makefile

The Makefile provides a convenient way to run the script and display specific statistics without manually typing the full command each time.

### Available Tags

- `run_cpu`: Displays CPU statistics.
- `run_lsq`: Displays Load/Store Queue statistics.
- `run_fu`: Displays Functional Unit busy statistics.
- `run_cache`: Displays Cache statistics.
- `run_bp`: Displays Branch Prediction statistics.
- `run_mem_ctrl`: Displays Memory Controller bandwidth and bursts.
- `run_mem_ctrl_balance`: Displays Memory Controller balance statistics.

### Running the Makefile

- To find out how to run, use:

  ```bash
  make help
  ```

