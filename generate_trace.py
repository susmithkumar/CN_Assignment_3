# Python 2 version
rate_bps = 50 * 1000 * 1000  # 50 Mbps
packet_size_bytes = 1500
interval = float(packet_size_bytes * 8) / rate_bps  # seconds between packets
t = 0.0

with open("50mbps1.trace", "w") as f:
    while t < 60:  # simulate for 60 seconds
        f.write("%.3f %d\n" % (t, packet_size_bytes))
        t += interval
