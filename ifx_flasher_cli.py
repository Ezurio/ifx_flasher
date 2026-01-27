#!/usr/bin/env python3

"""
Python CLI for Infineon (IFX) Firmware flashing/upgrade
"""

import argparse
import logging
import textwrap
import os
import sys
sys.path.append('./common_lib/libraries')
from ifx_firmware_cfg import ifx_firmware_cfg
from If820Board import IF820_FW_CFG
from HciProgrammer import HciProgrammer
from ifx_board import IfxBoard

LOG_MODULE_HCI_PORT = 'hci_port'
VERSION = '1.0.0'


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


SUPPORTED_BOARDS = {
    'if820': {
        'minidriver': resource_path(f'files{os.sep}if820{os.sep}minidriver-20820A1-uart-patchram.hex'),
        'fw_cfg': IF820_FW_CFG
    },
    'if91x': {
        'minidriver': resource_path(f'files{os.sep}if91x{os.sep}minidriver.hex'),
        'fw_cfg': ifx_firmware_cfg(
            minidriver_load_addr=0x00300400,
            launch_firmware_addr=0x0,
            hci_default_baudrate=115200,
            hci_flash_baudrate=3000000,
            load_addr_delay=0.5,
            chip_erase_delay=5.0)
    },
    'if310': {
        # TODO: Update minidriver for IF310. This is a placeholder and doesn't work yet.
        'minidriver': resource_path(f'files{os.sep}if310{os.sep}minidriver.hex'),
        'fw_cfg': ifx_firmware_cfg(
            minidriver_load_addr=0x00300400,
            launch_firmware_addr=0x0,
            hci_default_baudrate=115200,
            hci_flash_baudrate=3000000,
            load_addr_delay=0.5,
            chip_erase_delay=5.0)
    }
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='ifx_flasher_cli',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
        CLI tool to flash an ifx board (or compatible boards) with new firmware.
        If no COM port is specified, the tool will automatically detect the board and flash it.
        If there is more than one board detected, the user will be prompted to select the board to flash.
        The CLI supports chip erase, firmware update, and flashing firmware with chip erase.
                                        '''))
    parser.add_argument('-b', '--board',
                        type=str, default=str(),
                        help=f"Board type to flash. Supported boards: {', '.join(SUPPORTED_BOARDS)}")
    parser.add_argument('-c', '--connection',
                        type=str, default=str(), help="HCI COM port")
    parser.add_argument('-ce', '--chip_erase', action='store_true',
                        help="perform full chip erase.")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Enable verbose debug messages")
    parser.add_argument('-f', '--file',
                        help="application hex file to flash")
    parser.add_argument('-v', '--version', action='store_true',
                        help="Print the version of the tool and exit.")
    parser.add_argument('-vf', '--verify', action='store_true',
                        help="Verify firmware while flashing with CRC checks. Not all devices support this.")

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
    args, unknown = parser.parse_known_args()
    if args.debug:
        logging.info("Debugging mode enabled")
        logging.getLogger().setLevel(logging.DEBUG)

    if args.version:
        print(f"{VERSION}")
        sys.exit(0)

    print(f"IFX Flasher CLI v{VERSION}")

    board = args.board.casefold()
    if board not in SUPPORTED_BOARDS:
        logging.error(
            f"Unsupported board type '{board}'. Supported boards: {', '.join(SUPPORTED_BOARDS.keys())}")
        sys.exit(1)

    mini_driver = SUPPORTED_BOARDS[board]['minidriver']
    fw_cfg = SUPPORTED_BOARDS[board]['fw_cfg']
    com_port = args.connection
    firmware = args.file
    chip_erase = args.chip_erase
    verify = args.verify

    # TODO: IF310 does not support chip erase. Remove this check when chip erase is supported.
    if board == 'if310' and chip_erase:
        logging.warning(
            "Chip erase is not supported on IF310 and will be ignored.")
        chip_erase = False

    # If the user specifies a COM port, flash firmware in manual mode
    if com_port:
        input("Ensure the board is in HCI download mode and press enter to continue...")
        p = HciProgrammer(mini_driver, com_port,
                          HciProgrammer.HCI_DEFAULT_BAUDRATE, chip_erase, fw_cfg)
        if args.debug:
            logging.getLogger(LOG_MODULE_HCI_PORT).setLevel(logging.DEBUG)
        p.program_firmware(
            baud_rate=fw_cfg.hci_flash_baudrate,
            file_path=firmware,
            chip_erase_enable=chip_erase,
            verify=verify)
    else:
        boards = IfxBoard.get_connected_boards()
        if len(boards) == 0:
            logging.error("No boards found")
            sys.exit(1)

        choice = 0
        if len(boards) > 1:
            print("Which board do you want to flash?")
            for i, board in enumerate(boards):
                print(f"{i}: {board.probe.id}")
            choice = int(input("Enter the number of the board: "))
        board = boards[choice]
        board.flash_firmware(minidriver=mini_driver,
                             firmware=firmware,
                             fw_cfg=fw_cfg,
                             chip_erase=chip_erase,
                             verify=verify)
