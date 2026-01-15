# ifx_flasher

Host tool for flashing Infineon firmware over HCI UART

## Prerequisites

- Install Python 3.11. Python 3.12 is not supported.
- A board with IF820, IF310, or IFX91x module and access to the device's HCI UART.

## Setup

### Clone the Repository

```
git clone --recurse-submodules https://github.com/rfpros/ifx_flasher.git
```

### Install Dependencies

Before running any samples or tests, be sure to install the Python dependencies:

```
pip3 install -r requirements.txt
```

### Flash the Firmware

```
# Auto detect board and flash firmware
python3 ifx_flasher_cli.py -b if310 -f firmware.hcd

# Specify serial port (for boards other than Ezurio DVKs)
python3 ifx_flasher_cli.py -b if310 -c /dev/ttyUSB0 -f firmware.hcd
```

### Tool Help and Documentation

```
python3 ifx_flasher_cli.py -h
```
