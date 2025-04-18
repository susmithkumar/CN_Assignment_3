# clean_trace.py (drop the first column)
with open("50mbps1.trace", "r") as infile, \
     open("50mbps1_raw.trace", "w") as outfile:
    for line in infile:
        parts = line.strip().split()
        if len(parts) >= 3:
            outfile.write("%s %s\n" % (parts[1], parts[2]))  # only keep timestamp and size

