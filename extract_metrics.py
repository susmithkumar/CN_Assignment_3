#!/usr/bin/env python2.7
import os
import sys
import glob
import json
import numpy as np

def process_logs(data_dir="src/experiments/data", schemes=None):
    """Extract metrics from log files and save to JSON"""
    # Auto-detect available schemes if none specified
    if schemes is None:
        all_logs = glob.glob(os.path.join(data_dir, "*_datalink_run*.log"))
        schemes = list(set([os.path.basename(log).split('_')[0] for log in all_logs]))

    print("Processing data for schemes:", schemes)

    results = {}

    for scheme in schemes:
        datalink_files = sorted(glob.glob(os.path.join(data_dir, f"{scheme}_datalink_run*.log")))
        acklink_files = sorted(glob.glob(os.path.join(data_dir, f"{scheme}_acklink_run*.log")))

        if not datalink_files or not acklink_files:
            print(f"No log files found for {scheme}, skipping")
            continue

        scheme_data = {"runs": []}

        for run_idx, (datalink, acklink) in enumerate(zip(datalink_files, acklink_files)):
            print(f"Processing {scheme} run {run_idx+1}")
            run_data = {"run": run_idx+1}

            # Get throughput data
            throughput = extract_throughput(datalink)
            if throughput:
                run_data.update({
                    "throughput_avg_mbps": np.mean(throughput),
                    "throughput_max_mbps": np.max(throughput),
                    "throughput_min_mbps": np.min(throughput),
                    "throughput_samples": len(throughput)
                })

            # Get delay data
            delay = extract_delay(acklink)
            if delay:
                run_data.update({
                    "delay_avg_ms": np.mean(delay),
                    "delay_max_ms": np.max(delay),
                    "delay_min_ms": np.min(delay),
                    "delay_samples": len(delay)
                })

            scheme_data["runs"].append(run_data)

        results[scheme] = scheme_data

    # Save results
    json_file = os.path.join(data_dir, "cc_metrics.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {json_file}")

    # Print summary
    print("\nPerformance Summary:")
    print("Scheme\tAvg Throughput (Mbps)\tAvg Delay (ms)")
    print("------\t--------------------\t-------------")
    for scheme, data in results.items():
        avg_throughput = np.mean([run.get("throughput_avg_mbps", 0) for run in data["runs"]])
        avg_delay = np.mean([run.get("delay_avg_ms", 0) for run in data["runs"]])
        print(f"{scheme}\t{avg_throughput:.2f}\t\t\t{avg_delay:.2f}")

    return results

def extract_throughput(datalink_file):
    """Extract throughput measurements from datalink log file"""
    throughput = []
    try:
        with open(datalink_file, 'r') as f:
            for line in f:
                if 'Mbits/sec' in line:
                    parts = line.strip().split()
                    for i, part in enumerate(parts):
                        if part == 'Mbits/sec':
                            try:
                                throughput.append(float(parts[i-1]))
                            except:
                                pass
    except Exception as e:
        print(f"Error processing {datalink_file}: {e}")

    return throughput

def extract_delay(acklink_file):
    """Extract delay measurements from acklink log file"""
    delay = []
    try:
        with open(acklink_file, 'r') as f:
            for line in f:
                if 'ms' in line and 'delay' in line.lower():
                    parts = line.strip().split()
                    for i, part in enumerate(parts):
                        if part == 'ms':
                            try:
                                delay.append(float(parts[i-1]))
                            except:
                                pass
    except Exception as e:
        print(f"Error processing {acklink_file}: {e}")

    return delay

if __name__ == "__main__":
    data_dir = "src/experiments/data"
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]

    schemes = None  # Auto-detect available schemes
    if len(sys.argv) > 2:
        schemes = sys.argv[2].split(',')

    process_logs(data_dir, schemes)
