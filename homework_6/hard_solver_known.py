import hashlib
import pandas as pd

# --- CONFIGURATION ---
# Use the key you just found
KEY = "049677629" 
PUZZLE_FILE = './PUZZLE.txt'
DICT_FILE = 'clean_words_expanded.csv'

import string

def get_edits1(word):
    """Generates all typos 1 edit away."""
    letters = string.ascii_lowercase
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    # 1. Deletes (e.g. "tyrnt")
    deletes = [L + R[1:] for L, R in splits if R]
    # 2. Transposes (e.g. "tryant")
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # 3. Replaces (e.g. "syrant")
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    # 4. Inserts (e.g. "tyrannt")
    inserts = [L + c + R for L, R in splits for c in letters]
    
    return list(set(deletes + transposes + replaces + inserts))

def get_edits2(word):
    """
    Returns a LIST of all words exactly 2 edits away.
    """
    # 1. Get words 1 step away
    edits1 = get_edits1(word)
    
    # 2. Get words 1 step away from THOSE (1+1 = 2)
    edits2_set = set()
    for e1 in edits1:
        # We use .update() to add the new batch to our collection
        edits2_set.update(get_edits1(e1))
    
    # 3. CONVERT TO LIST
    # We convert the set to a list here. 
    # sorted() is optional, but makes the list easier to read.
    return sorted(list(edits2_set))


#############################

tyrant_list = get_edits1('tyrant')
tyrant_list += get_edits2('tyrant')
tyrant_list += [word+'.' for word in tyrant_list]

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
    for word in df['Word'].dropna().astype(str).tolist() + ['"moral"'] + tyrant_list:
        # Hash = sha256( KEY + WORD )
        # Make sure this order matches what worked in your previous script!
        # payload = KEY + word
        # h = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        payload = KEY.encode('utf-8') + word.encode('utf-8')
        h = hashlib.sha256(payload).hexdigest()
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