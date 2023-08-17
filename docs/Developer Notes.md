# TODO  
- Create unittests


# 2000 Token Limit Test 0
Segment 1 of chapter 1 (prompt): 1998 tokens
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

# GPT-3.5 Turbo 16k
Cheaper to use 16k context.
Math:
x + .45x = 16,000 tokens
x = 11,034 tokens

buffer of 100
prompt token limit = 11,034 - 100 = 10,934 
round ~ 10,930
final buffer of 104 tokens.

Test 1:
First run of 16k model produced a 50% ratio of prompt to copletion tokens...
Might have to re-adjust ratio.
Also, for some reason, python just... stops...

x + .55x = 16,000
x = 10,322
round ~ 10,320

No I included a buffer of 5% when computing the korean-to-english token ratio. So that should be account for any additional tokens used. 

# GPT-3.5 Turbo 4k
Cheaper to use if ratio of korean to english tokens is 1:1 (2k in and 2k out).
Not typically the case, bust safest option as the ratio can vary (pretty wildly sometimes)
