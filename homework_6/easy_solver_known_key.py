import hashlib
import pandas as pd

# --- CONFIGURATION ---
# Use the key you just found
KEY = "5262" 
PUZZLE_FILE = './PUZZLE-EASY.txt'
DICT_FILE = 'clean_words_expanded.csv'

def solve_puzzle():
    print(f"Decoding puzzle using known key: {KEY}...")

    # 1. Load the puzzle hashes (keep order to read the sentence)
    with open(PUZZLE_FILE) as f:
        puzzle_hashes = [line.strip() for line in f.readlines()]

    # 2. Load the dictionary
    df = pd.read_csv(DICT_FILE)
    # Create a fast lookup table: { hash : word }
    # We pre-calculate the hash for every word in the dictionary using Key 5262
    lookup_table = {}
    
    print("Building lookup table (this is fast)...")
    for word in df['Word'].dropna().astype(str):
        # Hash = sha256( KEY + WORD )
        # Make sure this order matches what worked in your previous script!
        payload = KEY + word
        h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        lookup_table[h] = word

    # 3. Reconstruct the sentence
    print("\n" + "="*40)
    print("THE DECODED MESSAGE:")
    print("="*40)
    
    missing_hashes = []
    
    for i, h in enumerate(puzzle_hashes):
        if h in lookup_table:
            word = lookup_table[h]
            print(f"Line {i+1}: {word}")
        else:
            print(f"Line {i+1}: >>> [MISSING/MISSPELLED] <<<")
            missing_hashes.append((i+1, h))

    # 4. Help you solve the missing word
    if missing_hashes:
        print("\n" + "="*40)
        print(f"Found {len(missing_hashes)} missing word(s).")
        print("Look at the sentence above. What word logically fits in the blank?")
        print("Target Hash:", missing_hashes[0][1])
        print("="*40)

if __name__ == "__main__":
    solve_puzzle()