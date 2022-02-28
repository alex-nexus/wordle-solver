# wordle solver

## Preprocessing 
1. process all_words.txt with 470,000 words 
2. filter out any words which are not 5 letters
3. filter out any words with symbols
4. write the remaining ~21,000 words back to wordle_words.txt

## Game Init Logic
1. Load all the words into memory
2. Loop through all the words and count the total occurences of all pair of character and its position. The result is a 130-entry dictionary, e.g. {'c:1': 2345, 'a:2': 5432, ...}
3. Loop through all the wordle words and calculate each word's total score based on its character/position tuples
4. Sort the words by scores desc. The sorted list has words sorted from most frequent used characters to the least

## Game Loop Logic
1. The software makes 6 recommendations of the qualified words with the most frequently used characters
2. A user would choose from the recommendations and enter the world on wordle website and receive responses (5 colors)
3. Then enters the 5 colors in the command line
4. the software then would re-filter based on the latest colors and return the new recommendations while the total number of candidates reduces
5. Repeat until the user gets all 5 letters correctly



## Run
`python3 wordle_solver.py`
