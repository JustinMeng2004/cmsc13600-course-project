import hashlib
import pandas as pd
import multiprocessing
from functools import partial
import sys

# KEY: 5262

# TOPIC: The Princess Bride (Buttercup/Westley)


# --- CONFIGURATION ---
PUZZLE_FILE = './PUZZLE-EASY.txt'
DICT_FILE = 'clean_words_expanded.csv'

def load_data():
    """Loads the dictionary and target hashes once."""
    print("Loading dictionary and targets...")
    
    # 1. Load Targets
    with open(PUZZLE_FILE) as f:
        targets = set(line.strip() for line in f.readlines())
        
    # 2. Load Dictionary
    df = pd.read_csv(DICT_FILE)
    words = df['Word'].dropna().astype(str).tolist()
    
    return targets, words

def check_key_range(key_range, words, targets):
    """
    This function will run on a separate CPU core.
    It checks a specific range of keys (e.g., 0-2500) against ALL words.
    """
    found_items = []
    
    for num in key_range:
        key_str = "{:04d}".format(num)
        key_bytes = key_str.encode("utf-8")
        
        # Optimization: Pre-encode words inside the loop only if needed, 
        # but since we are iterating words, we just do it here.
        for word in words:
            word_bytes = word.encode("utf-8")
            
            # CHECK 1: KEY + WORD
            guess = key_bytes + word_bytes
            h = hashlib.sha256(guess).hexdigest()
            
            if h in targets:
                found_items.append((key_str, word, h))
                
            # CHECK 2: WORD + KEY (Just in case)
            # guess_reversed = word_bytes + key_bytes
            # h_rev = hashlib.sha256(guess_reversed).hexdigest()
            # if h_rev in targets:
            #    found_items.append((key_str, word, h_rev))

    return found_items

if __name__ == '__main__':
    # 1. Load Data
    targets, words = load_data()
    print(f"Loaded {len(words)} words. Starting attack on {len(targets)} hashes...")
    
    # 2. Prepare Multiprocessing
    # We split the 10,000 keys into chunks for each CPU core
    num_cores = multiprocessing.cpu_count()
    print(f"Using {num_cores} CPU cores to speed this up!")
    
    # Create ranges (e.g., Core 1 gets keys 0-2499, Core 2 gets 2500-4999...)
    total_keys = 10000
    chunk_size = total_keys // num_cores
    ranges = []
    for i in range(num_cores):
        start = i * chunk_size
        # Ensure the last core gets any remaining keys
        end = total_keys if i == num_cores - 1 else (i + 1) * chunk_size
        ranges.append(range(start, end))

    # 3. Run the Attack
    # 'partial' allows us to pass the constant arguments (words, targets) easily
    worker_func = partial(check_key_range, words=words, targets=targets)
    
    with multiprocessing.Pool(num_cores) as pool:
        # map runs the function across all cores
        results = pool.map(worker_func, ranges)
        
    # 4. Print Results
    print("\n" + "="*40)
    found_any = False
    for result_list in results:
        for (key, word, h) in result_list:
            print(f"SUCCESS! Found: Key={key}, Word={word}")
            print(f"Hash: {h}")
            found_any = True
            
    if not found_any:
        print("No matches found. Try swapping Key+Word order?")
    print("="*40 + "\n")





'''
import hashlib
import time
import sys
import pandas as pd

puzzle_easy_key = 6346
puzzle_easy_misspell = "Fabruart,"

# find the row with mis-spelled word
#key = "{:04d}".format(puzzle_easy_key)

#hashcode = f'{hashlib.sha256(key.encode("utf-8") + puzzle_easy_misspell.encode("utf-8")).hexdigest()}'
#print(f"Hashcode for mis-spelled word with known key {key}: {hashcode}")

df_old = pd.read_csv("clean_words_expanded.csv")


with open('./PUZZLE-EASY.txt') as file:
    lines = [line.strip() for line in file.readlines()]
    # print(lines)

for num in range(1, 10000):
    key = "{:04d}".format(num)
    print(f"Processing key: {key} ...")
    for word in df_old['Word']:
        if not isinstance(word, str):
            continue
        _hashcode = f'{hashlib.sha256(key.encode("utf-8") + word.encode("utf-8")).hexdigest()}'
        if _hashcode in lines[1:3]:
            print(f"Found matching hashcode: {_hashcode} with num: {num} and word: {word}")
            break

'''