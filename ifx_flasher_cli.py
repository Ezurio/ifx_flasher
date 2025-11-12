#!/usr/bin/env python3

"""
Python CLI for Infineon (IFX) Firmware flashing/upgrade

pyinstaller command to produce a single executable file:

pyinstaller --clean --console --noconfirm  --onefile --add-data "files/if820/:files/if820/minidriver-20820A1-uart-patchram.hex" --collect-all pyocd  --collect-all cmsis_pack_manager -p common_lib/libraries ifx_flasher_cli.py

"""

import argparse
import logging
import textwrap
import os
import sys
sys.path.append('./common_lib/libraries')
from ifx_board import IfxBoard
from HciProgrammer import HciProgrammer
from If820Board import IF820_FW_CFG

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
                        type=str, default=str(), required=True,
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

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
    args, unknown = parser.parse_known_args()
    if args.debug:
        logging.info("Debugging mode enabled")
        logging.getLogger().setLevel(logging.DEBUG)

    if args.version:
        print(f"{VERSION}")
        exit(0)

    print(f"IFX Flasher CLI v{VERSION}")

    board = args.board.casefold()
    if board not in SUPPORTED_BOARDS:
        logging.error(
            f"Unsupported board type '{board}'. Supported boards: {', '.join(SUPPORTED_BOARDS.keys())}")
        exit(1)

    mini_driver = SUPPORTED_BOARDS[board]['minidriver']
    fw_cfg = SUPPORTED_BOARDS[board]['fw_cfg']
    com_port = args.connection
    firmware = args.file
    chip_erase = args.chip_erase

    # If the user specifies a COM port, flash firmware in manual mode
    if com_port:
        input("Ensure the board is in HCI download mode and press enter to continue...")
        p = HciProgrammer(mini_driver, com_port,
                          HciProgrammer.HCI_DEFAULT_BAUDRATE, chip_erase, fw_cfg)
        if args.debug:
            logging.getLogger(LOG_MODULE_HCI_PORT).setLevel(logging.DEBUG)
        p.program_firmware(
            fw_cfg.hci_flash_baudrate, firmware, chip_erase)
    else:
        boards = IfxBoard.get_connected_boards()
        if len(boards) == 0:
            logging.error("No boards found")
            exit(1)

        choice = 0
        if len(boards) > 1:
            print("Which board do you want to flash?")
            for i, board in enumerate(boards):
                print(f"{i}: {board.probe.id}")
            choice = int(input("Enter the number of the board: "))
        board = boards[choice]
        board.flash_firmware(minidriver=mini_driver,
                             firmware=firmware, fw_cfg=fw_cfg, chip_erase=chip_erase)
