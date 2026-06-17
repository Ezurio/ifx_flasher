# ifx_flasher

Host tool for flashing Infineon firmware over HCI UART

## Prerequisites

- Install Python 3.9 or greater.
- A board with IF820, IF310, or IFX91x module and access to the device's HCI UART.

## Setup

### Clone the Repository

```
git clone --recurse-submodules [THIS_REPO_URL]
```

### Install Dependencies

Before running any samples or tests, be sure to install the Python dependencies:

```
pip3 install -r requirements.txt
```

### Linux Permissions

On Linux, you may need to set up udev rules to allow access to the serial ports without root privileges. Create a file at `/etc/udev/rules.d/99-ezurio.rules` with the following content:

```
# Ezurio
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0001", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0002", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0003", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0004", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0005", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0006", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0007", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0008", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="0009", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="000a", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="000b", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="000c", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="000d", MODE="0666", GROUP="plugdev", TAG+="uaccess"
ATTRS{idVendor}=="3016", ATTRS{idProduct}=="000e", MODE="0666", GROUP="plugdev", TAG+="uaccess"
```

Then reload the udev rules:

```
sudo udevadm control --reload-rules
```

Add user to plugdev group:

```
sudo usermod -aG plugdev $USER
```

You may need to log out and back in for group changes to take effect.

### Firmware

#### IF310 HCI Firmware

There are two versions of the IF310 HCI firmware available:

- The HCD file is loaded to RAM and must be reloaded on each boot: [CYW55500A1_001.002.032.0211.0125.hcd](files/if310/firmware/CYW55500A1_001.002.032.0211.0125.hcd)
- The HEX file is loaded into external flash and persists across reboots: [CYW55500A1_001.002.032.0211.0125.hex](files/if310/firmware/CYW55500A1_001.002.032.0211.0125.hex). An external flash must be connected to the IF310 module for this to work. The IF310 DVK includes an external flash to store the firmware.

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
