import hashlib
import string

# --- CONFIGURATION ---
KEY = "049677629"
PUZZLE_FILE = './PUZZLE.txt'

# The final two bosses
targets = {
    24: "moral",
    40: "tyrant"
}

def get_edits1(word):
    """Generates all strings 1 edit away."""
    letters = string.ascii_lowercase
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def get_edits2(word):
    """Generates all strings 2 edits away (recursive)."""
    edits1 = get_edits1(word)
    edits2 = set()
    for e1 in edits1:
        edits2.update(get_edits1(e1))
    return edits1.union(edits2)

def deep_solve():
    print(f"Generating 2-Edit Deep Search (approx 100k variations)...")
    
    with open(PUZZLE_FILE) as f:
        lines = [line.strip() for line in f.readlines()]

    for line_num, base_word in targets.items():
        target_hash = lines[line_num - 1]
        print(f"--- ATTACKING LINE {line_num} ({base_word}) ---")
        
        # 1. Generate massive list of typos (0, 1, and 2 edits)
        # This covers things like "tyrrannt" (double error)
        typo_list = get_edits2(base_word)
        typo_list.add(base_word) # Add original just in case
        
        # 2. Add some manual "Word Swaps" just in case it's not a typo but a change
        if base_word == "moral":
            typo_list.update(["immoral", "amoral", "morale", "morals"])
        if base_word == "tyrant":
            typo_list.update(["leader", "ruler", "king", "zealot", "god"])

        found = False
        
        # 3. Test every typo with Punctuation
        punctuation_marks = ["", ".", ",", "?", "!", ":", ";"]
        
        for i, typo in enumerate(typo_list):
            if i % 10000 == 0: print(f"   Checked {i} variations...")

            for p in punctuation_marks:
                # Try: "tyrrannt.", "Tyrrannt."
                guesses = [typo + p, typo.capitalize() + p]
                
                for guess in guesses:
                    h = hashlib.sha256((KEY + guess).encode("utf-8")).hexdigest()
                    
                    if h == target_hash:
                        print("\n" + "!"*50)
                        print(f"BINGO! FOUND IT!")
                        print(f"Line {line_num}: {guess}")
                        print(f"Based on: {base_word}")
                        print("!"*50 + "\n")
                        found = True
                        break
                if found: break
            if found: break
            
        if not found:
            print(f"Line {line_num}: STILL FAILED. (Checked {len(typo_list)*len(punctuation_marks)*2} hashes)")
            print("Is it possible the word is completely different? (e.g. synonym?)")

if __name__ == "__main__":
    deep_solve()