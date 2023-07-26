# Overview

ChatGPT and GPT-4 are very good at translating texts from other languages to English. Unfortunately, you might come across token or rate limits when trying to translate large bodies of text. In those cases, you can use this tool to break up a single large text files into chunks that fit within ChatGPT's limits.

# How to Use this Tool  

1. Upload your text file (or copy and paste your text into the box).
2. Choose your token limit (GPT-4 using ChatGPt Plus has around 4000 tokens).
3. Click "Generate Prompts".
4. Open ChatGPT of GPT-4 in your web browser.
5. Copy and Paste the prompt into the chatbox.
6. Submit and receive your translated text.

I recommend keeping "Hit Exact Token Limit"

# TODO  
- Implement tokenization logic
- Create unittests
- Test with book 1. Compare with official translation
- Create locally running web server using django rest
- Implement UI
- Create Docker file
  - pip3 freeze > requirements.txt
- Deploy to AWS?

# Interesting response as to why GPT-4 says that my 4000 token prompt is too long
1. Differences in Tokenization: The GPT-4 model might be using a different tokenizer or slightly different tokenization rules than GPT-3 (which is what tiktoken was originally designed to work with). It might be splitting certain words into more tokens than expected.

2. Encoding Differences: It's also possible that some form of encoding or preprocessing is being performed on the prompt before it's sent to the GPT-4 model. This could potentially increase the number of tokens.

3. Special Tokens: If there are additional special tokens being appended or prepended to your text (like EOS or BOS tokens), they count towards the total limit as well.

4. Updates in tiktoken: The version of tiktoken you are using might not be the latest one or it might have some bugs or issues.