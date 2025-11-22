import pandas as pd
import hashlib
import random

# read all the words from a dictionary
#df_old = pd.read_csv("dictionary.csv", sep=',', quotechar='"')

import pandas as pd

def create_expanded_csv(input_file, output_file):
    print("Reading dictionary...")
    df = pd.read_csv(input_file, on_bad_lines='skip')
    
    # 1. Extract the words and convert to string
    # We specificially ensure they are strings to avoid errors
    words = df['Word'].dropna().astype(str).str.strip()
    
    # 2. Create the 'lowercase' version
    # This takes every word and makes it lowercase (e.g., "APPLE" -> "apple")
    lower_words = words.str.lower()
    
    # 3. Combine both lists (Original + Lowercase)
    # This ensures you have "Apple" AND "apple" in your file
    combined_words = pd.concat([words, lower_words])
    
    # 4. Remove duplicates
    # (If "apple" was already there, we don't want it twice)
    combined_words = combined_words.drop_duplicates()
    
    # 5. Save to CSV
    # We name the header 'Word' so your other script knows what column to look for
    combined_words.to_csv(output_file, index=False, header=['Word'])
    
    print(f"Success! Saved to {output_file}")
    print(f"Total words: {len(combined_words)}")

# Run it
create_expanded_csv('dictionary.csv', 'clean_words_expanded.csv')



#print(len(df_old['word']))
'''
# read all 76 hashcodes being generated before
legit_outputs = set()
with open("PUZZLE.txt", "r") as puzzle:
    for line in puzzle:
        if line.strip():
            legit_outputs.add(line.strip())
# print(legit_outputs)

# key = "{:09d}".format(int(random.random() * 1000000000))
# words = open("TEXT", "r").read()

for digest in legit_outputs:
    has_found = False
    for i in range(1, 1_000_000_000):
        key = f"{i:09d}"
        print(f"processing key: {key} ...")
        for word in df['word']:
            if not isinstance(word, str):
                continue
            _digest = str(hashlib.sha256(key.encode("utf-8")+ word.encode("utf-8")).hexdigest())
            if _digest == digest:
                print(f"found word: {word}")
                has_found = True
                break
        if has_found:
            break
    if not has_found:
        print(f"not found")

        '''