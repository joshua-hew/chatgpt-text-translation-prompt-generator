import os
from tokenizer import generate_prompts

# Translation Notes:
# Kim Su-hyun
# Kim Yoo-hyun
# Han So-young - deceased wife?

def main():
    """Generates normal and dramatic translation prompts for GPT-4 using ChatGPT Plus."""
    
    CHAPTER_NUM = 1
    TEXT_FILE = f'/Users/josh/Local Documents/Novels/Memorize/Raws/메모라이즈-{CHAPTER_NUM}권.txt'
    OUTPUT_DIR = f'/Users/josh/Local Documents/Novels/Memorize/GPT-4 Input Prompts/ch-{CHAPTER_NUM}/'
    MODEL = 'gpt-4'
    MAX_TOKENS = 2700

    # Create output dir if not exists already
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(TEXT_FILE, 'r') as f:
        text = f.read()
        normal_translation_prompts = generate_prompts(
            "Translate this to english:\n", text, MODEL, MAX_TOKENS)
        dramatic_translation_prompts = generate_prompts(
            "Translate this to english and give it a serious tone:\n", text, MODEL, MAX_TOKENS)

    for i in range(len(normal_translation_prompts)):
        with open(OUTPUT_DIR + f"normal-{i}.txt", "w") as f:
            f.write(normal_translation_prompts[i])
    
    for i in range(len(dramatic_translation_prompts)):
        with open(OUTPUT_DIR + f"serious-{i}.txt", "w") as f:
            f.write(dramatic_translation_prompts[i])
    



if __name__ == '__main__':
    main()
