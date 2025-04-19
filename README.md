# Pantheon of Congestion Control

The Pantheon enables benchmarking and comparison of many congestion control algorithms using a common interface. It supports testing schemes locally using Mahimahi or remotely over the Internet.

**Project Repository**: https://pantheon.stanford.edu  
**USENIX Paper**: https://www.usenix.org/conference/atc18/presentation/yan-francis  
**Google Group**: https://groups.google.com/forum/#!forum/pantheon-stanford

---

## My Setup and Execution Journey
'''
used ubuntu-20.04.6-desktop-amd24 on VMware Workstation 17 player(used 4 cores and 6gb ram ,35gb space which will allow less crash and run faster)
'''
### Repository Cloning and Initialization
```bash
git clone https://github.com/StanfordSNR/pantheon.git
cd pantheon
git submodule update --init --recursive
```

### Dependencies
- Mahimahi setup:
```bash
git clone https://github.com/ravinet/mahimahi.git
cd mahimahi
./autogen.sh
./configure
make
sudo make install
```

- System-wide dependencies:
```bash
sudo apt update
sudo apt install libboost-dev libprotobuf-dev protobuf-c-compiler protobuf-compiler \
    libjemalloc-dev libboost-python-dev libpython2.7-dev iperf python2.7
```

- Pantheon dependencies:
```bash
src/experiments/setup.py --install-deps --all
```
Initial Setup

```bash
PYTHONPATH=src /usr/local/python2/bin/python src/experiments/setup.py --setup --all
```
Run on Every Reboot
```bash
PYTHONPATH=src /usr/local/python2/bin/python src/experiments/setup.py --all
---

## ⚙️ Python 2.7 Manual Setup (if required)
```bash
wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
tar -xzf Python-2.7.18.tgz
cd Python-2.7.18
./configure --prefix=/usr/local/python2
make -j4
sudo make install
```

### pip and modules
```bash
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
/usr/local/python2/bin/python2.7 get-pip.py
/usr/local/python2/bin/pip install pyyaml==3.13
```

### Shared Library Fixes
```bash
sudo ln -s /usr/local/python2/lib/libpython2.7.so.1.0 /usr/lib/libpython2.7.so.1.0
export LD_LIBRARY_PATH=/usr/local/python2/lib:$LD_LIBRARY_PATH
```

---

## 🏗️ Building Mahimahi from Source
- C++20 flag was replaced with `-std=c++17`
- Fixed string truncation warning in `netdevice.cc`

```bash
cd ~/Desktop/networks/mahimahi
./autogen.sh
./configure
make -j4
sudo make install
```

---

## 🛠️ Building and Setting Up Pantheon
```bash
cd ~/Desktop/networks/pantheon
PYTHONPATH=src /usr/local/python2/bin/python src/experiments/setup.py --setup --all
```

If needed:
```bash
sudo apt install libpython2.7-dev libboost-python1.71-dev libjemalloc-dev
```

---

## 🧪 Running Tests
```bash
src/experiments/test.py local --schemes "bbr cubic copa"
```

If `IndexError` occurs:
- Ensure all wrapper scripts define `arg_parser.receiver_first()`
- Ensure `run_first` is implemented correctly

To test manually:
```bash
src/wrappers/<scheme>.py setup
src/wrappers/<scheme>.py setup_after_reboot
src/wrappers/<scheme>.py run_first
# Then based on order:
src/wrappers/<scheme>.py receiver <port>
src/wrappers/<scheme>.py sender <IP> <port>
```

Mahimahi shell example:
```bash
iperf -s  # Receiver
mm-delay 5 mm-link 50mbps.trace 50mbps.trace -- iperf -c 100.64.0.1 -t 60 -i 1
```

---

## 📊 Analysis
```bash
src/analysis/analyze.py --data-dir src/experiments/data
```
Generates:
- Throughput & RTT graphs
- Packet loss
- Full PDF report `pantheon_report.pdf`

View or convert:
```bash
evince pantheon_report.pdf &
convert -density 150 pantheon_report.pdf output.png
```

---

## 🔧 Common Issues & Fixes
- Built Mahimahi with C++17 manually
- Installed Python 2.7 with pip, SSL, zlib support
- Symlinked missing `.so` libraries
- Fixed wrapper script bugs in `bbr.py`, `cubic.py`
- Solved `IndexError` by correcting malformed `cmd_to_run_tc` entries

---

## 🎯 Summary
Pantheon is now fully operational with custom setup on Ubuntu VM. Performance of BBR, CUBIC, and COPA is measurable, analysis is automated, and custom schemes can be added easily.

---

