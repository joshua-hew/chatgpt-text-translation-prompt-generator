import os
import json
import shutil
import logging
from openai_utils import *

BOOK_RANGE = list(range(1, 42)) # 41 books, so 42 is the end range
NOVEL_RAWS_DIR = '/Users/josh/Local Documents/Novels/Memorize/Raws/'
GPT_INPUT_DIR = '/Users/josh/Local Documents/Novels/Memorize/ChatGPT Input Prompts/Book-{}/'
GPT_OUTPUT_DIR = '/Users/josh/Local Documents/Novels/Memorize/ChatGPT Output Responses/Book-{}/'
FINAL_OUTPUT_DIR = '/Users/josh/Local Documents/Novels/Memorize/Translated/Book-{}/'
# MODEL = 'gpt-4'
MODEL = 'gpt-3.5-turbo'
MAX_PROMPT_TOKENS = 2048

# Create logger
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


def reset_directory(dir_path):
    logger.info(f"Resetting directory: {dir_path}")
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)
    os.makedirs(dir_path)


def list_txt_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]


def create_prompt_files():
    # Create prompts for each book
    logger.info(f"Creating input prompts. Model: {MODEL}. Prompt token limit: {MAX_PROMPT_TOKENS}")
    for book_num in BOOK_RANGE:
        
        # Wipe input prompt dir of previous contents
        prompts_dir = GPT_INPUT_DIR.format(book_num)
        reset_directory(prompts_dir)

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


def create_translation_files():
    """Translates each prompt via ChatGPT"""

    for book_num in BOOK_RANGE:
        # Wipe input prompt dir of previous contents
        translation_outputs_dir = GPT_OUTPUT_DIR.format(book_num)
        reset_directory(translation_outputs_dir)
        
        logger.info(f"Starting translation: Book {book_num}")
        prompts_dir = GPT_INPUT_DIR.format(book_num)
        prompt_files = sorted(list_txt_files(prompts_dir))
   
        # Call ChatGPT API. Translate each prompt
        for i in range(len(prompt_files)):
            logger.info(f"Translating: {prompt_files[i].split('/')[-1]}")
            with open(prompt_files[i], 'r') as f:
                prompt = f.read()

            try:
                response = translate(MODEL, prompt)

            except Exception as e:
                logger.error("Error translating text.", e)

            r_metadata = {}
            r_metadata["finish_reason"] = response["choices"][0]["finish_reason"]
            r_metadata["usage"] = response["usage"]
            r_metadata["usage"]["completion_over_prompt_%"] = f'{100 * r_metadata["usage"]["completion_tokens"] / r_metadata["usage"]["prompt_tokens"]}'
            logger.info(f"Response: {json.dumps(r_metadata)}")


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
                
                try:
                    response = translate(MODEL, prompt)

                except Exception as e:
                    logger.error("Error translating text.", e)

                r_metadata = {}
                r_metadata["finish_reason"] = response["choices"][0]["finish_reason"]
                r_metadata["usage"] = response["usage"]
                r_metadata["usage"]["completion_over_prompt_%"] = f'{100 * r_metadata["usage"]["completion_tokens"] / r_metadata["usage"]["prompt_tokens"]}'
                logger.info(f"Response: {json.dumps(r_metadata)}")
                
                finish_reason = response["choices"][0]["finish_reason"]
                retry_counter += 1

            # Write translation to file
            translation_file = translation_outputs_dir + f"translation-output-{i:02d}.txt"
            logger.info(f"Saving translation to {translation_file}")
            translation = response_content.split("==START==\n", 1)[1]
            with open(translation_file, "w") as f:
                f.write(translation)

            # DEBUG - stop after first prompt
            # break

        # DEBUG - stop after first book
        break


def create_final_book_files():
    """Stitch translations together"""

    for book_num in BOOK_RANGE:
        # Wipe input prompt dir of previous contents
        book_dir = FINAL_OUTPUT_DIR.format(book_num)
        reset_directory(book_dir)
        
        logger.info(f"Stitching together translations: Book {book_num}") 
        translation_files = sorted(list_txt_files(GPT_OUTPUT_DIR.format(book_num)))
        with open(book_dir + f"Memorize Book {book_num}.txt", "w") as book_file:
            
            for i in range(len(translation_files)):
                logger.info(f"Appending translation: {translation_files[i].split('/')[-1]}")
                with open(translation_files[i], "r") as f:
                    text = f.read()
                    book_file.write(text)


def main():
    """Iterates through each book in the Memorize novel, creates the prompts, sends api calls to ChatGPT for translation, and stitches translations together."""
    
    logger.info(f"Running {__name__}")
    # create_prompt_files()
    # create_translation_files
    create_final_book_files()
    logger.info("Done!")


if __name__ == '__main__':
    main()