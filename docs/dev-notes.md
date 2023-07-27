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

# ChatGPT sometimes stops generating
Token limit was reached.
Makes sense as both the input and response messages count towards the token limit. ChatGPT contonues generating until it hits that limit. Theoretically if the korean input is 2000 tokens, then the english translation should be a similar 2000? Then that would all fit under the 4096 token limit.

Or, as per 3500 Token Test 2, I could do a higher input message token size, 3000, and continually ask ChatGPT to continue the translation. Prone to error as if the prompt to continue isn't specific, ChatGPT will start creating its own fictional narrative.

After testing again, even when using a more specific prompt, "Continue translating from the last word you translated". It still missed a large chunk (3500 Token Test 3). In fact this chunk is consistently ommitted when I ask to continue the translation. Not sure why.

# 2000 Token Limit Test 0
Segment 1 of chapter 1: 1998 tokens
Translated text: 893 tokens

Roughly 44%
x + .45x = 4096 (give or take 10. apparently some tokens are added by the api, pre-processing, etc... source below)
x = 2824.82

[source](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions)


# 2700 Token Limit Test 0
Giving a buffer of around 100 tokens.

Segment 1: 2666 tokens
Translated text: 1224 tokens

Roughly 45% still. Nice.

# 2700 Token Dramatic Translation Test 0
Very interesting!! By asking ChatGPT to translate it to make it sound dramatic, it improved the readability of the overall transalation by a lot. The changes in specific words used, sentence structure and overall pacing were changed. Its a much better fit for the context / event that's unfolding in that part of the story.

Hmm, not only is this an awesome capability, but it seems like the intended tone is an important factor when considering how to translate a piece of text.

The prompt prefix I used was:
"Translate this to english and make it sound dramatic"