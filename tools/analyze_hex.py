#!/usr/bin/env python3
"""
Analyze an Intel hex file to calculate the total bytes of data that will be written.
"""

try:
    from intelhex import IntelHex
except ImportError:
    print("Error: intelhex module not found. Install with: pip install intelhex")
    exit(1)

def parse_intel_hex(filename):
    """
    Parse an Intel hex file using the intelhex module and return analysis.
    """
    try:
        # Load the Intel HEX file
        ih = IntelHex()
        ih.loadhex(filename)

        # Get memory segments
        segments = ih.segments()
        print(f"Intel HEX file analysis: {filename}")
        print(f"=" * 60)

        total_bytes = 0
        segment_count = 0

        for start_addr, end_addr in segments:
            segment_size = end_addr - start_addr
            total_bytes += segment_size
            segment_count += 1

            print(f"Segment {segment_count}:")
            print(f"  Start address: 0x{start_addr:08X}")
            print(f"  End address:   0x{end_addr:08X}")
            print(f"  Size:          {segment_size} bytes ({segment_size / 1024:.2f} KB)")
            print()

        print(f"Summary:")
        print(f"Total segments: {segment_count}")
        print(f"Total data bytes: {total_bytes}")
        print(f"Total data size: {total_bytes} bytes ({total_bytes / 1024:.2f} KB)")

        # Additional useful information
        min_addr = ih.minaddr()
        max_addr = ih.maxaddr()
        print(f"\nAddress range:")
        print(f"Minimum address: 0x{min_addr:08X}")
        print(f"Maximum address: 0x{max_addr:08X}")
        print(f"Address span: 0x{max_addr - min_addr + 1:08X} bytes")

        return total_bytes

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error parsing Intel HEX file: {e}")
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python analyze_hex.py <hex_file>")
        sys.exit(1)

    filename = sys.argv[1]
    parse_intel_hex(filename)
