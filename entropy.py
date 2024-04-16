import sys
import pathlib as pt
from math import log2
import numpy as np
import argparse

def _cl_co():
    def co(i):
        o = 0
        for _ in range(8):
            o += i & 1
            i >>= 1
        return o

    LUT = [co(i) for i in range(256)]

    return LUT.__getitem__  # fastest way to count bits in a byte

bitcount = _cl_co()

def calculate_entropy(probs):
    """Calculate the entropy given the probabilities."""
    ent = -1 * (probs * np.log2(np.where(probs == 0, np.ones(1), probs))).sum()
    return ent

def calculate_bit_level_entropy(counts, tot):
    """Calculate the bit-level informational entropy."""
    bit_counts = np.zeros(9, dtype=np.uint32)  # 0 to 8 bits
    for byte_value, count in enumerate(counts):
        bit_sum = bitcount(byte_value)
        bit_counts[bit_sum] += count
    
    # Calculate bit-level probabilities
    bit_probs = bit_counts / tot
    
    # Calculate entropy using bit-level probabilities
    bit_level_ent = calculate_entropy(bit_probs)
    return bit_level_ent

def main(argv=sys.argv):
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Calculate byte-level or bit-level entropy of files.")
    parser.add_argument("files", metavar="F", nargs="+", help="File paths to calculate entropy for")
    parser.add_argument("-b", "--bit", action="store_true", help="Calculate bit-level informational entropy")

    args = parser.parse_args(argv[1:])
    
    for filename in args.files:  # Loop through all arguments except program name
        f = pt.Path(filename)
        
        tot = 0
        counts = np.zeros(256, dtype=np.uint32)
        
        with f.open("rb") as fp:
            while (b := fp.read(256)):
                for byte in b:
                    tot += 1
                    counts[byte] += 1
        
        probs = counts / tot
        
        # Calculate byte-level entropy
        byte_level_ent = calculate_entropy(probs)
        
        print(f"--- File: {filename} ---")
        print(f"Entropy per byte: {byte_level_ent:.6f} bits or {byte_level_ent / 8:.6f} bytes")
        print(f"Entropy of file: {byte_level_ent * tot:.6f} bits or {byte_level_ent * tot / 8:.6f} bytes")
        print(f"Size of file: {tot} bytes")
        print(f"Delta: {tot - (byte_level_ent * tot) / 8:.6f} bytes compressible theoretically")
        print(f"Best Theoretical Coding ratio: {8 / byte_level_ent:.6f}")
        
        if args.bit:
            # Calculate bit-level informational entropy if `-b/--bit` flag is used
            bit_level_ent = calculate_bit_level_entropy(counts, tot)
            print(f"Informational entropy per bit: {bit_level_ent:.6f} bits")
            
        print("")  # Add a newline between file results
        

    # p1 = h / tot
    # p0 = (tot - h) / tot
    # print("Probability to be high: ", p1, h, tot)

    # # Realised late, I could have calculated byte entropy and wouldn't need
    # # bit counting
    # ent = p1 * (log2(tot) - log2(h)) + p0 * (log2(tot) - log2(tot - h))
    # print("Informational entropy per bit: ", ent, "bits")
    # print("Entropy per byte: ", ent * 8, "bits")
    # print("Entropy of entire file: ", ent * tot, "bits")

if __name__ == "__main__":
    main()