# Python 2 version: Mahimahi expects timestamps as integers (ms)
rate_bps = 50 * 1000 * 1000  # 50 Mbps
packet_size_bytes = 1500
interval_sec = float(packet_size_bytes * 8) / rate_bps  # seconds between packets
t = 0.0

with open("50mbps1.trace", "w") as f:
    while t < 60:  # simulate for 60 seconds
        timestamp_ms = int(t * 1000)  # convert to integer milliseconds
        f.write("%d %d\n" % (timestamp_ms, packet_size_bytes))
        t += interval_sec

