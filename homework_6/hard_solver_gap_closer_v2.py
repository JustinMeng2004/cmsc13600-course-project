import hashlib

# --- CONFIGURATION ---
KEY = "049677629"
PUZZLE_FILE = './PUZZLE.txt'

# Map of Line Number -> The Correct Word (from the book)
missing_map = {
    9: "principle",
    10: "But",       # Might be attached to previous word if spacing was bad?
    14: "not",       # Likely "not?"
    17: "cutthroat", # Likely "cutthroat,"
    20: "noticed",   # Likely "noticed,"
    24: "moral",
    27: "fashion",   # Likely "fashion."
    30: "person",
    34: "life",
    40: "tyrant",    # Likely "tyrant."
    45: "arrogant",  # Likely "arrogant."
    51: "man's",     # Check smart quotes
    58: "own",       # Likely "own?"
    67: "fact",      # Likely "fact:"
    70: "end",       # Likely "end,"
    71: "I'm",       # Check smart quotes
    76: "armies"     # Likely "armies."
}

def solve_punctuation():
    print(f"Checking for hidden punctuation with Key: {KEY}...\n")
    
    with open(PUZZLE_FILE) as f:
        lines = [line.strip() for line in f.readlines()]

    unsolved = []

    for line_num, word in missing_map.items():
        target_hash = lines[line_num - 1]
        solved_this_line = False

        # 1. Generate Punctuation Variations
        variations = []
        
        # Base variations (Lower, Capitalized)
        bases = [word, word.lower(), word.capitalize()]
        
        # Add Punctuation (. , ? : ;)
        suffixes = ["", ".", ",", "?", "!", ":", ";"]
        
        for b in bases:
            for s in suffixes:
                variations.append(b + s)
                
                # Handle Smart Quotes (man's vs man’s)
                if "'" in b:
                    variations.append((b + s).replace("'", "’")) # Curly quote

        # 2. Test Variations
        for v in variations:
            h = hashlib.sha256((KEY + v).encode("utf-8")).hexdigest()
            if h == target_hash:
                print(f"Line {line_num}: Solved as '{v}'")
                solved_this_line = True
                break
        
        if not solved_this_line:
            print(f"Line {line_num}: >>> STILL FAILING ({word}) <<<")
            unsolved.append((line_num, word))

    # 3. Final Report
    print("\n" + "="*50)
    if len(unsolved) == 1:
        line, word = unsolved[0]
        print(f"FOUND IT! The REAL typo is on Line {line} ('{word}').")
        print("Everything else was just punctuation.")
        print(f"Now you just need to brute-force typos for '{word}'")
        print(f"Remember to check '{word}.' or '{word},' in your brute force!")
    elif len(unsolved) == 0:
        print("Everything solved! There were no typos, just punctuation mismatches.")
    else:
        print(f"Still have {len(unsolved)} failing lines.")

if __name__ == "__main__":
    solve_punctuation()