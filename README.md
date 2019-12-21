# Miner monitor pi


* L3+ miner monitor
* Configured by config file
* Multiple miners supported
* Checks miner status
* Check hashrate on pool
* Logs history to xml
* Display status on simple web page
* Automatically restart miners

Uses python 3. Made to run on Raspberry pi.
Uses GPIO to restart miner in case of reporting faulty chip.
In case of failure temporarily raises the conresponding GPIO high to swith off miner's power supply. Also checks hashrate reported by litecoinpool.org.
Tested with raspberry pi 2B.

See and edit included miner_monitor.conf file for configuration.

## Run the monitor

With default miner_monitor.conf:

`python monitor.py`

or other config file:

`python monitor.py path/to/config/file.conf`
