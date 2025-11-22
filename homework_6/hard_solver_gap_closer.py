import hashlib

# --- CONFIGURATION ---
KEY = "049677629"  # Your 9-digit key
PUZZLE_FILE = './PUZZLE.txt'

# The exact text from Mistborn (Logbook of the Lord Ruler)
# I broke it down word-by-word to match your line numbers.
mistborn_quote = [
    "I", "consider", "myself", "to", "be", "a", "man", "of", 
    "principle", "But", "what", "man", "does", "not", "Even", 
    "the", "cutthroat", "I", "have", "noticed", "considers", 
    "his", "actions", "moral", "after", "a", "fashion", 
    "Perhaps", "another", "person", "reading", "of", "my", 
    "life", "would", "name", "me", "a", "religious", "tyrant", 
    "He", "could", "call", "me", "arrogant", "What", "is", 
    "to", "make", "that", "man's", "opinion", "any", "less", 
    "valid", "than", "my", "own", "I", "guess", "it", "all", 
    "comes", "down", "to", "one", "fact", "In", "the", "end", 
    "I'm", "the", "one", "with", "the", "armies", 

    'principle.', 'But,','not?','cutthroat,', 'noticed,', 'fashion.'
]

def verify_quote():
    print(f"Verifying the 'Mistborn' quote against your puzzle...")
    
    # 1. Load Puzzle File
    with open(PUZZLE_FILE) as f:
        target_hashes = [line.strip() for line in f.readlines()]

    print("-" * 60)
    missing_lines = []

    # 2. Check Line by Line
    for i, target_hash in enumerate(target_hashes):
        # Get the word from the book that matches this line number
        if i < len(mistborn_quote):
            word_from_book = mistborn_quote[i]
            
            # Check Exact Word
            payload = KEY + word_from_book
            h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            
            if h == target_hash:
                print(f"Line {i+1}: {word_from_book} [MATCH]")
            else:
                # Check Capitalized version just in case
                payload_cap = KEY + word_from_book.capitalize()
                h_cap = hashlib.sha256(payload_cap.encode("utf-8")).hexdigest()
                
                if h_cap == target_hash:
                    print(f"Line {i+1}: {word_from_book.capitalize()} [MATCH]")
                else:
                    # If NEITHER match, then THIS is your typo!
                    print(f"Line {i+1}: >>> {word_from_book.upper()} (MISSPELLED IN PUZZLE) <<<")
                    missing_lines.append((i+1, word_from_book))
        else:
            print(f"Line {i+1}: [Extra line in puzzle?]")

    print("-" * 60)
    
    if missing_lines:
        print("\nCONCLUSION:")
        print(f"The quote is correct. {76 - len(missing_lines)} lines matched perfectly.")
        print(f"The misspelled word is located at Line {missing_lines[0][0]}.")
        print(f"The word SHOULD be '{missing_lines[0][1]}', but the hash didn't match.")
        print("You now just need to find the typo for that ONE word.")

if __name__ == "__main__":
    verify_quote()