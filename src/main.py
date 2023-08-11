import os
import shutil
from utils import *



def main():
    """Iterates through each book in the Memorize novel, creates the prompts, sends api calls to ChatGPT for translation, and stitches translations together."""
    
    NOVEL_RAWS_DIR = '/Users/josh/Local Documents/Novels/Memorize/Raws/'
    OUTPUT_DIR_PROMPTS = '/Users/josh/Local Documents/Novels/Memorize/GPT-4 Input Prompts/'
    MODEL = 'gpt-4'
    MAX_PROMPT_TOKENS = 2700
 
    # Create prompts for each book
    for book_num in range(1, 42):
        
        # Wipe dir of previous contents
        book_dir = OUTPUT_DIR_PROMPTS + f'Book-{book_num}/'
        if os.path.exists(book_dir):
            shutil.rmtree(book_dir, ignore_errors=True)
        os.makedirs(book_dir)

        # Create prompts
        with open(NOVEL_RAWS_DIR + f'메모라이즈-{book_num}권.txt', 'r') as f:
            text = f.read()
            translation_prompts = generate_prompts(
                "Translate the following text to english. Do not include anything else in your response aside from the translation.\nText:\n", text, MODEL, MAX_PROMPT_TOKENS) 
        
        # Write prompts to files
        for j in range(len(translation_prompts)):
            with open(book_dir + f"translation-prompt-{j}.txt", "w") as f:
                f.write(translation_prompts[j])
  
    # Translate
    #   Start point
    
    # Stitch together translations

if __name__ == '__main__':
    main()