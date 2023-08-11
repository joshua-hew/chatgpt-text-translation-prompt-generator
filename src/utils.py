import os
import tiktoken

def list_txt_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]


def check_if_token_is_delimiter(token, encoding):
    """Returns bool
    Basially, we want to split up text according to a delimiter so that we do not cut a multi-token in half by accident.
    A delimiter in this case will contain one or more sentence end markers.
    Examples of tokens (using the GPT-4 model encoder) that would be considered  
    a delimiter are: ('.', '!', '?', '.\n', '!!!', '?\n', '."', etc...)"""

    sentence_end_markers = ['.', '?', '!', '\n']  

    text = encoding.decode([token])
    for marker in sentence_end_markers:
        if marker in text:
            return True

    return False   
    

def split_text(text, model, max_tokens):
    """ Returns: arrays of strings of token size <= max_tokens
    Args:
        text: string
        model: one of []
        max_tokens: int
        match_exact_token_limit: bool
    Break text into segments that have size <= max_tokens.
    Each segment should end with a delimiter. If not, find the previous delimiter.
    If no previous delimiter found in segment, then just append entire segment.
    """

    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    start = 0
    end = min(max_tokens, len(tokens))
    text_segments = []

    # DEBUG
    # print("# tokens", len(tokens))
    # print("tokens", tokens)
    # for token in tokens:
    #     print(token, repr(encoding.decode([token])))

    while start < len(tokens):
        
        i = end - 1 # Start at last token, search backwards for delimiter
        delimiter_found = False
        while start < i and not delimiter_found:
            if check_if_token_is_delimiter(tokens[i], encoding):
                segment = encoding.decode(tokens[start:i+1])
                text_segments.append(segment)
                
                start = i+1
                end = min(start + max_tokens, len(tokens))
                delimiter_found = True
            else:
                i -= 1

        if not delimiter_found:
            segment = encoding.decode(tokens[start:end])
            text_segments.append(segment)

            start = end
            end = min(start + max_tokens, len(tokens))

    return text_segments


def generate_prompts(prompt_prefix, text, model, prompt_token_limit):
    """Generates the prompts that can be copied / pasted into the ChatGPT web interface."""
    
    # Append \n to prompt_prefix if not present already
    pass

    # Count tokens in prompt_prefix
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(prompt_prefix)
    
    # Subtract from prompt_token_limit
    segment_token_limit = prompt_token_limit - len(tokens)

    # Error handling: check that max_tokens is longer than prompt_prefix tokens
    pass

    # Split texts into segments
    segments = split_text(text, model, segment_token_limit)

    # Prepend prefix to each segment to form the final prompt
    prompts = [prompt_prefix + x for x in segments]
    return prompts


def translate():
    """Sends API call to ChatGPT to translate the text."""
    pass


if __name__ == "__main__":
    pass