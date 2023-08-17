import os
import copy
import shutil
import openai
import logging
from utils import *

logger = logging.getLogger('GPT-Translator')
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
f_handler = logging.FileHandler('../logs/main.log')
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def main():
    """Iterates through each book in the Memorize novel, creates the prompts, sends api calls to ChatGPT for translation, and stitches translations together."""
    
    NOVEL_RAWS_DIR = '/Users/josh/Local Documents/Novels/Memorize/Raws/'
    GPT_INPUT_DIR = '/Users/josh/Local Documents/Novels/Memorize/GPT-4 Input Prompts/Book-{}/'
    GPT_OUTPUT_DIR = '/Users/josh/Local Documents/Novels/Memorize/GPT-4 Output Responses/Book-{}/'
    # MODEL = 'gpt-4'
    MODEL = 'gpt-3.5-turbo'
    MAX_PROMPT_TOKENS = 2048
 
    # Create prompts for each book
    logger.info(f"Creating input prompts. Model: {MODEL}. Prompt token limit: {MAX_PROMPT_TOKENS}")
    for book_num in range(1, 42):
        
        # Wipe input prompt dir of previous contents
        prompts_dir = GPT_INPUT_DIR.format(book_num)
        if os.path.exists(prompts_dir):
            shutil.rmtree(prompts_dir, ignore_errors=True)
        os.makedirs(prompts_dir)

        # Create prompts
        with open(NOVEL_RAWS_DIR + f'메모라이즈-{book_num}권.txt', 'r') as f:
            text = f.read()
            translation_prompts = generate_prompts(
                "Translate the following text to english. Do not include anything else in your response aside from the translation. Prepend your translation with '==START=='.\nText:\n", text, MODEL, MAX_PROMPT_TOKENS) 
        
        # Write prompts to files
        for i in range(len(translation_prompts)):
            with open(prompts_dir + f"translation-prompt-{i:02d}.txt", "w") as f:
                f.write(translation_prompts[i])
    
    logger.info(f"Finished creating input prompts")

    ####################
    # Translate
    ####################
    # In case of failure, manually define a start / continue point
    # TODO: Test resuming from a random book, file
    book_range = range(1, 42)
    prompt_start = None     # Name of input prompt file

    for book_num in book_range:
        logger.info(f"Starting translation: Book {book_num}")
        prompts_dir = GPT_INPUT_DIR.format(book_num)
        prompt_files = sorted(list_txt_files(prompts_dir))

        if prompt_start:
            start_index = prompt_files.index(prompt_start)
            prompt_files = prompt_files[start_index:]
   
        # Call ChatGPT API. Translate each prompt
        for i in range(len(prompt_files)):
            logger.info(f"Translating: {prompt_files[i]}")
            with open(prompt_files[i], 'r') as f:
                prompt = f.read()

            try:
                response = translate(MODEL, prompt)

            except Exception as e:
                logger.error("Error translating text.", e)

            r_metadata = copy.deepcopy(response)
            r_metadata["choices"][0]["message"].pop("content")
            logger.info(f"Response: {r_metadata}")


            # Validate that translation was not curtailed
            # TODO: Test what is received when token limit exceeded.
            response_content = response["choices"][0]["message"]["content"]
            finish_reason = response["choices"][0]["finish_reason"]
            retry_counter = 1
            max_retries = 3 
            while finish_reason != "stop":

                if retry_counter > max_retries:
                    raise Exception("Max retries exceeded. Total token limit possibly exceeded. Exiting out.")
                
                logger.warning(f"Incomplete response received. Retrying. Retry attempt: {retry_counter}")
                
                response = translate(MODEL, prompt)
                r_metadata = copy.deepcopy(response)
                r_metadata["choices"][0]["message"].pop("content")
                logger.info(f"Response: {r_metadata}")
                
                finish_reason = response["choices"][0]["finish_reason"]
                retry_counter += 1

            # Wipe input prompt dir of previous contents
            translation_outputs_dir = GPT_OUTPUT_DIR.format(book_num)
            if os.path.exists(translation_outputs_dir):
                shutil.rmtree(translation_outputs_dir, ignore_errors=True)
            os.makedirs(translation_outputs_dir)

            # Write translation to file
            translation = response_content.split("==START==\n", 1)[1]
            with open(translation_outputs_dir + f"translation-output-{i:02d}.txt", "w") as f:
                f.write(translation)

            # DEBUG - stop after first prompt
            break
        
        # DEBUG - stop after first book
        break
    
    # Stitch together translations

if __name__ == '__main__':
    main()