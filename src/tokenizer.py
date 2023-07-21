import tiktoken

def tokenize(text, model, max_tokens, match_exact_token_limit=False):
    """ Returns: array of strings
    Args:
        text: string
        model: one of []
        max_tokens: int
        match_exact_token_limit: bool
    Break text into segments that have size < max_tokens.
    Each segment should end with a delimiter. If not, find the previous delimiter.
    If no previous delimiter found in segment, then just append entire segment.
    """

    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    delimiters = ['.', '?', '!', '\n']
    delimiters = [encoding.encode(x)[0] for x in delimiters]

    start = 0
    end = min(max_tokens, len(tokens))
    prompts = []

    # DEBUG
    # print(len(tokens))

    while start < len(tokens):
        
        i = end - 1 # Start at last token, search backwards for delimiter
        delimiter_found = False
        while start < i and not delimiter_found:
            if tokens[i] in delimiters:
                prompt = encoding.decode(tokens[start:i+1])
                prompts.append(prompt)
                
                start = i+1
                end = min(start + max_tokens, len(tokens))
                delimiter_found = True
            else:
                i -= 1

        if not delimiter_found:
            prompt = encoding.decode(tokens[start:end])
            prompts.append(prompt)

            start = end
            end = min(start + max_tokens, len(tokens))

    return prompts

if __name__ == "__main__":
    pass