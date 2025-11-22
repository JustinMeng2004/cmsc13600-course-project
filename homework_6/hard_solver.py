import hashlib
import multiprocessing
from functools import partial
import sys
import time  # <--- Added this library

# --- CONFIGURATION ---
PUZZLE_FILE = './PUZZLE.txt' 
TARGET_WORD = "the" # If this fails, try "and", "a", "to"

def check_key_range_for_specific_word(key_range, target_hashes, target_word_bytes):
    """
    Checks a range of keys against ONE specific word.
    """
    for num in key_range:
        key_str = "{:09d}".format(num)
        key_bytes = key_str.encode("utf-8")
        
        # Calculate Hash: KEY + WORD
        guess = key_bytes + target_word_bytes
        h = hashlib.sha256(guess).hexdigest()
        
        if h in target_hashes:
            return (key_str, h)
            
    return None

if __name__ == '__main__':
    # 1. Start the Timer
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Starting attack...")
    print(f"Target Word: '{TARGET_WORD}'")
    print("Scanning 1,000,000,000 keys...")

    # 2. Load Data
    try:
        with open(PUZZLE_FILE) as f:
            target_hashes = set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        print(f"ERROR: Could not find {PUZZLE_FILE}")
        sys.exit()

    target_word_bytes = TARGET_WORD.encode("utf-8")
    
    # 3. Setup Multiprocessing
    num_cores = multiprocessing.cpu_count() - 2
    print(f"Engaging {num_cores} CPU cores...")
    
    total_keys = 1000000000
    chunk_size = total_keys // num_cores
    ranges = []
    for i in range(num_cores):
        start = i * chunk_size
        end = total_keys if i == num_cores - 1 else (i + 1) * chunk_size
        ranges.append(range(start, end))

    # 4. Run the Attack
    worker_func = partial(check_key_range_for_specific_word, 
                          target_hashes=target_hashes, 
                          target_word_bytes=target_word_bytes)
    
    with multiprocessing.Pool(num_cores) as pool:
        # The script will "freeze" here while working
        results = pool.map(worker_func, ranges)
        
    # 5. Stop Timer & Calculate Duration
    end_time = time.time()
    elapsed_seconds = end_time - start_time
    minutes = int(elapsed_seconds // 60)
    seconds = int(elapsed_seconds % 60)

    # 6. Check Results
    print("\n" + "="*40)
    found = False
    for res in results:
        if res:
            found_key, found_hash = res
            print(f"SUCCESS! KEY FOUND: {found_key}")
            print(f"Matched Word: '{TARGET_WORD}'")
            print(f"Hash: {found_hash}")
            found = True
            break
            
    if not found:
        print(f"Failed to find Key using word '{TARGET_WORD}'.")
        print("Try changing TARGET_WORD to 'and', 'a', or 'of'.")
    
    print("-" * 40)
    print(f"Total Time Taken: {minutes} min {seconds} sec")
    print("="*40 + "\n")