# Overview

ChatGPT and GPT-4 are very good at translating texts from other languages to English. Unfortunately, you might come across token or rate limits when trying to translate large bodies of text. In those cases, you can use this tool to break up a single large text files into chunks that fit within ChatGPT's limits.

# How to Use this Tool  

1. Upload your text file (or copy and paste your text into the box).
2. Choose your model (if unsure, use GPT-4 as that is the latest).
3. Click "Generate Prompts".
4. Open ChatGPT of GPT-4 in your web browser.
5. Copy and Paste the prompt into the chatbox.
6. Submit and receive your translated text.


# TODO  
- Implement tokenization logic
- Create unittests
- Test with book 1. Compare with official translation
- Create locally running web server using django rest
- Implement UI
- Create Docker file
  - pip3 freeze > requirements.txt
- Deploy to AWS?