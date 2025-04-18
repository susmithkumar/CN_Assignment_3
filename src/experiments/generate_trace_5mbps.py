# generate_trace_5mbps.py
rate_bps = 5 * 1000 * 1000  # 5 Mbps
packet_size_bytes = 1500
interval = float(packet_size_bytes * 8) / rate_bps  # seconds between packets
t = 0.0

with open("5mbps1.trace", "w") as f:
    while t < 60:  # 60 seconds
        timestamp_ms = int(t * 1000)  # convert to milliseconds
        f.write("%d %d\n" % (timestamp_ms, packet_size_bytes))
        t += interval

