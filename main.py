import re
import argparse
from tabulate import tabulate
from colorama import Fore, Style, init

init()


def find_active_cpu(file_path):
    """
    Find the active core by the number of clocks and instructions.
    """
    cpu_data = {}
    pattern_cycles = re.compile(r'system\.clusters\.(cpu\d+)\.numCycles\s+(\d+)')
    pattern_insts_committed = re.compile(r'system\.clusters\.(cpu\d+)\.committedInsts\s+(\d+)')

    with open(file_path, 'r') as file:
        for line in file:
            if match := pattern_cycles.search(line):
                cpu = match.group(1)
                cycles = int(match.group(2))
                if cpu not in cpu_data:
                    cpu_data[cpu] = {'cycles': cycles, 'committedInsts': 0}
                else:
                    cpu_data[cpu]['cycles'] = cycles
            if match := pattern_insts_committed.search(line):
                cpu = match.group(1)
                committed_insts = int(match.group(2))
                if cpu not in cpu_data:
                    cpu_data[cpu] = {'cycles': 0, 'committedInsts': committed_insts}
                else:
                    cpu_data[cpu]['committedInsts'] = committed_insts

    active_cpu = max(cpu_data, key=lambda x: (cpu_data[x]['cycles'], cpu_data[x]['committedInsts']))
    print(
        f"Active CPU is {active_cpu} with {cpu_data[active_cpu]['cycles']} cycles and {cpu_data[active_cpu]['committedInsts']} committed instructions")
    return active_cpu


def extract_cpu_statistics(file_path, active_cpu):
    stats = {}

    # CPU statistics
    pattern_cycles = re.compile(rf'system\.clusters\.{active_cpu}\.numCycles\s+(\d+)')
    pattern_insts_issued = re.compile(rf'system\.clusters\.{active_cpu}\.instsIssued\s+(\d+)')
    pattern_insts_committed = re.compile(rf'system\.clusters\.{active_cpu}\.committedInsts\s+(\d+)')
    pattern_cpi = re.compile(rf'system\.clusters\.{active_cpu}\.cpi\s+([\d\.]+)')
    pattern_ipc = re.compile(rf'system\.clusters\.{active_cpu}\.ipc\s+([\d\.]+)')

    # Load/Store Queue statistics
    pattern_lsq_forw_loads = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.forwLoads\s+(\d+)')
    pattern_lsq_squashed_loads = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.squashedLoads\s+(\d+)')
    pattern_lsq_squashed_stores = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.squashedStores\s+(\d+)')
    pattern_lsq_ignored_responses = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.ignoredResponses\s+(\d+)')
    pattern_lsq_mem_order_violations = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.memOrderViolation\s+(\d+)')
    pattern_lsq_rescheduled_loads = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.rescheduledLoads\s+(\d+)')
    pattern_lsq_blocked_by_cache = re.compile(rf'system\.clusters\.{active_cpu}\.lsq\d+\.blockedByCache\s+(\d+)')

    # Functional Unit usage patterns
    pattern_fu_busy = re.compile(rf'system\.clusters\.{active_cpu}\.statFuBusy::(\w+)\s+(\d+)\s+([\d\.]+)%')

    # Cache patterns
    pattern_cache_hits = re.compile(rf'system\.clusters\.{active_cpu}\.dcache\.overallHits::total\s+(\d+)')
    pattern_cache_misses = re.compile(rf'system\.clusters\.{active_cpu}\.dcache\.overallMisses::total\s+(\d+)')
    pattern_cache_miss_rate = re.compile(rf'system\.clusters\.{active_cpu}\.dcache\.overallMissRate::total\s+([\d\.]+)')
    pattern_cache_latency = re.compile(
        rf'system\.clusters\.{active_cpu}\.dcache\.overallAvgMissLatency::total\s+([\d\.]+)')

    # Memory Dependency Unit patterns
    pattern_mem_dep_unit = re.compile(rf'system\.clusters\.{active_cpu}\.MemDepUnit__(\d+)\.(\w+)\s+(\d+)')

    # Branch prediction patterns
    pattern_bp_btb_lookups = re.compile(rf'system\.clusters\.{active_cpu}\.branchPred\.BTBLookups\s+(\d+)')
    pattern_bp_btb_hits = re.compile(rf'system\.clusters\.{active_cpu}\.branchPred\.BTBHits\s+(\d+)')
    pattern_bp_btb_hit_ratio = re.compile(rf'system\.clusters\.{active_cpu}\.branchPred\.BTBHitRatio\s+([\d\.]+)')

    # Memory Controller patterns
    pattern_mem_bw_read = re.compile(r'system\.mem_ctrls(\d+)\.dram\.bwRead::total\s+(\d+)')
    pattern_mem_bw_write = re.compile(r'system\.mem_ctrls(\d+)\.dram\.bwWrite::total\s+(\d+)')
    pattern_mem_read_bursts = re.compile(r'system\.mem_ctrls(\d+)\.dram\.readBursts\s+(\d+)')
    pattern_mem_write_bursts = re.compile(r'system\.mem_ctrls(\d+)\.dram\.writeBursts\s+(\d+)')
    pattern_mem_queue_latency = re.compile(r'system\.mem_ctrls(\d+)\.dram\.avgQueueLatency\s+([\d\.]+)')
    pattern_mem_accesses = re.compile(r'system\.mem_ctrls(\d+)\.dram\.accesses::total\s+(\d+)')

    mem_ctrl_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            # CPU statistics
            if match := pattern_cycles.search(line):
                stats['numCycles'] = int(match.group(1))
            if match := pattern_insts_issued.search(line):
                stats['instsIssued'] = int(match.group(1))
            if match := pattern_insts_committed.search(line):
                stats['committedInsts'] = int(match.group(1))
            if match := pattern_cpi.search(line):
                stats['cpi'] = float(match.group(1))
            if match := pattern_ipc.search(line):
                stats['ipc'] = float(match.group(1))

            # Load/Store Queue statistics
            if match := pattern_lsq_forw_loads.search(line):
                stats['lsq_forw_loads'] = int(match.group(1))
            if match := pattern_lsq_squashed_loads.search(line):
                stats['lsq_squashed_loads'] = int(match.group(1))
            if match := pattern_lsq_squashed_stores.search(line):
                stats['lsq_squashed_stores'] = int(match.group(1))
            if match := pattern_lsq_ignored_responses.search(line):
                stats['lsq_ignored_responses'] = int(match.group(1))
            if match := pattern_lsq_mem_order_violations.search(line):
                stats['lsq_mem_order_violations'] = int(match.group(1))
            if match := pattern_lsq_rescheduled_loads.search(line):
                stats['lsq_rescheduled_loads'] = int(match.group(1))
            if match := pattern_lsq_blocked_by_cache.search(line):
                stats['lsq_blocked_by_cache'] = int(match.group(1))

            # Functional Unit statistics
            if match := pattern_fu_busy.search(line):
                fu_type = match.group(1)
                fu_busy_count = int(match.group(2))
                fu_busy_rate = float(match.group(3))
                if 'FU_Busy' not in stats:
                    stats['FU_Busy'] = {}
                stats['FU_Busy'][fu_type] = {'count': fu_busy_count, 'rate': fu_busy_rate}

            # Cache statistics
            if match := pattern_cache_hits.search(line):
                stats['cache_hits'] = int(match.group(1))
            if match := pattern_cache_misses.search(line):
                stats['cache_misses'] = int(match.group(1))
            if match := pattern_cache_miss_rate.search(line):
                stats['cache_miss_rate'] = float(match.group(1))
            if match := pattern_cache_latency.search(line):
                stats['cache_miss_latency'] = float(match.group(1))

            # Memory Dependency Unit statistics
            if match := pattern_mem_dep_unit.search(line):
                unit_id = match.group(1)
                event_type = match.group(2)
                value = int(match.group(3))
                if 'MemDepUnit' not in stats:
                    stats['MemDepUnit'] = {}
                if unit_id not in stats['MemDepUnit']:
                    stats['MemDepUnit'][unit_id] = {}
                stats['MemDepUnit'][unit_id][event_type] = value

            # Branch prediction statistics
            if match := pattern_bp_btb_lookups.search(line):
                stats['btb_lookups'] = int(match.group(1))
            if match := pattern_bp_btb_hits.search(line):
                stats['btb_hits'] = int(match.group(1))
            if match := pattern_bp_btb_hit_ratio.search(line):
                stats['btb_hit_ratio'] = float(match.group(1))

            # Memory Controller statistics
            if match := pattern_mem_bw_read.search(line):
                mem_ctrl_id = match.group(1)
                bw_read = int(match.group(2))
                if mem_ctrl_id not in mem_ctrl_data:
                    mem_ctrl_data[mem_ctrl_id] = {}
                mem_ctrl_data[mem_ctrl_id]['bw_read'] = bw_read
            if match := pattern_mem_bw_write.search(line):
                mem_ctrl_id = match.group(1)
                bw_write = int(match.group(2))
                mem_ctrl_data[mem_ctrl_id]['bw_write'] = bw_write
            if match := pattern_mem_read_bursts.search(line):
                mem_ctrl_id = match.group(1)
                read_bursts = int(match.group(2))
                mem_ctrl_data[mem_ctrl_id]['read_bursts'] = read_bursts
            if match := pattern_mem_write_bursts.search(line):
                mem_ctrl_id = match.group(1)
                write_bursts = int(match.group(2))
                mem_ctrl_data[mem_ctrl_id]['write_bursts'] = write_bursts
            if match := pattern_mem_queue_latency.search(line):
                mem_ctrl_id = match.group(1)
                queue_latency = float(match.group(2))
                mem_ctrl_data[mem_ctrl_id]['queue_latency'] = queue_latency
            if match := pattern_mem_accesses.search(line):
                mem_ctrl_id = match.group(1)
                accesses = int(match.group(2))
                mem_ctrl_data[mem_ctrl_id]['accesses'] = accesses

    # Calculate total bandwidth and balance
    total_read_bw = sum(mem_ctrl['bw_read'] for mem_ctrl in mem_ctrl_data.values())
    total_write_bw = sum(mem_ctrl['bw_write'] for mem_ctrl in mem_ctrl_data.values())
    for mem_ctrl_id, mem_ctrl in mem_ctrl_data.items():
        read_share = (mem_ctrl['bw_read'] / total_read_bw * 100) if total_read_bw else 0
        write_share = (mem_ctrl['bw_write'] / total_write_bw * 100) if total_write_bw else 0
        mem_ctrl['read_share'] = read_share
        mem_ctrl['write_share'] = write_share

    stats['mem_ctrl_data'] = mem_ctrl_data
    return stats


def display_statistics(stats, category):
    if category == "cpu":
        print("\nCPU Statistics:")
        cpu_stats = [
            ["Cycles", stats.get('numCycles', 'N/A')],
            ["Instructions Issued", stats.get('instsIssued', 'N/A')],
            ["Instructions Committed", stats.get('committedInsts', 'N/A')],
            ["CPI", stats.get('cpi', 'N/A')],
            ["IPC", stats.get('ipc', 'N/A')]
        ]
        print(tabulate(cpu_stats, headers=["Metric", "Value"], tablefmt="grid"))

    elif category == "lsq":
        print("\nLoad/Store Queue Statistics:")
        lsq_stats = [
            ["Forwarded Loads", stats.get('lsq_forw_loads', 'N/A')],
            ["Squashed Loads", stats.get('lsq_squashed_loads', 'N/A')],
            ["Squashed Stores", stats.get('lsq_squashed_stores', 'N/A')],
            ["Ignored Responses", stats.get('lsq_ignored_responses', 'N/A')],
            ["Memory Order Violations", stats.get('lsq_mem_order_violations', 'N/A')],
            ["Rescheduled Loads", stats.get('lsq_rescheduled_loads', 'N/A')],
            ["Blocked By Cache", stats.get('lsq_blocked_by_cache', 'N/A')]
        ]
        print(tabulate(lsq_stats, headers=["Metric", "Value"], tablefmt="grid"))

    elif category == "fu":
        print("\nFunctional Unit Busy Stats:")
        fu_stats = [[fu_type, f"{Fore.GREEN}{fu_data['count']}{Style.RESET_ALL}" if fu_data[
                                                                                        'count'] != 0 else f"{Fore.RED}{fu_data['count']}{Style.RESET_ALL}",
                     f"{fu_data['rate']}%"] for fu_type, fu_data in stats.get('FU_Busy', {}).items()]
        print(tabulate(fu_stats, headers=["Functional Unit", "Busy Count", "Busy Rate"], tablefmt="grid"))

    elif category == "cache":
        print("\nCache Stats:")
        cache_stats = [
            ["Cache Hits", stats.get('cache_hits', 'N/A')],
            ["Cache Misses", stats.get('cache_misses', 'N/A')],
            ["Cache Miss Rate", stats.get('cache_miss_rate', 'N/A')],
            ["Cache Miss Latency", stats.get('cache_miss_latency', 'N/A')]
        ]
        print(tabulate(cache_stats, headers=["Metric", "Value"], tablefmt="grid"))

    elif category == "bp":
        print("\nBranch Prediction Stats:")
        branch_pred_stats = [
            ["BTB Lookups", stats.get('btb_lookups', 'N/A')],
            ["BTB Hits", stats.get('btb_hits', 'N/A')],
            ["BTB Hit Ratio", stats.get('btb_hit_ratio', 'N/A')]
        ]
        print(tabulate(branch_pred_stats, headers=["Metric", "Value"], tablefmt="grid"))

    elif category == "mem_ctrl":
        print("\nMemory Controller Stats:")
        mem_ctrl_stats_1 = [
            ["Read Bandwidth (Bytes/s)", stats['mem_ctrl_data'].get('0', {}).get('bw_read', 'N/A')],
            ["Write Bandwidth (Bytes/s)", stats['mem_ctrl_data'].get('0', {}).get('bw_write', 'N/A')],
            ["Read Bursts", stats['mem_ctrl_data'].get('0', {}).get('read_bursts', 'N/A')],
            ["Write Bursts", stats['mem_ctrl_data'].get('0', {}).get('write_bursts', 'N/A')]
        ]
        print(tabulate(mem_ctrl_stats_1, headers=["Metric", "Value"], tablefmt="grid"))

    elif category == "mem_ctrl_balance":
        print("\nMemory Controller Balance Stats:")
        mem_ctrl_headers = ["Memory Controller", "Read Bandwidth (Bytes/s)", "Write Bandwidth (Bytes/s)", "Read Bursts",
                            "Write Bursts", "Queue Latency", "Total Accesses", "Read % Share", "Write % Share"]
        mem_ctrl_table = []
        for mem_ctrl_id, mem_ctrl in stats['mem_ctrl_data'].items():
            mem_ctrl_table.append([
                f"Memory Controller {mem_ctrl_id}",
                mem_ctrl.get('bw_read', 'N/A'),
                mem_ctrl.get('bw_write', 'N/A'),
                mem_ctrl.get('read_bursts', 'N/A'),
                mem_ctrl.get('write_bursts', 'N/A'),
                mem_ctrl.get('queue_latency', 'N/A'),
                mem_ctrl.get('accesses', 'N/A'),
                f"{mem_ctrl.get('read_share', 0):.2f}%",
                f"{mem_ctrl.get('write_share', 0):.2f}%"
            ])
        print(tabulate(mem_ctrl_table, headers=mem_ctrl_headers, tablefmt="grid"))


def main():
    parser = argparse.ArgumentParser(description="Extract and display specific statistics from the gem5 stat file.")
    parser.add_argument("file_path", help="Path to the stat file")
    parser.add_argument("--category", choices=["cpu", "lsq", "fu", "cache", "bp", "mem_ctrl", "mem_ctrl_balance"],
                        required=True, help="Category of statistics to display")

    args = parser.parse_args()

    active_cpu = find_active_cpu(args.file_path)
    stats = extract_cpu_statistics(args.file_path, active_cpu)

    display_statistics(stats, args.category)


if __name__ == "__main__":
    main()
