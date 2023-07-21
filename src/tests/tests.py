import os
import sys
import unittest
import tiktoken

# Allow this file to import from the parent dir
this_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(this_dir)
sys.path.append(parent_dir)

from tokenizer import tokenize

class TestTokenizer(unittest.TestCase):

    def validate_prompt_sizes(self, prompts, model, max_tokens):
        for prompt in prompts:
            encoding = tiktoken.encoding_for_model(model)
            tokens = encoding.encode(prompt)
            print(len(tokens))
            if len(tokens) > max_tokens:
                return False
        return True

    def test_empty_string(self):
        model = 'gpt-4'
        max_tokens = 10
        prompts = tokenize("", model, max_tokens)
        self.assertEqual(prompts, [])
        self.assertTrue(self.validate_prompt_sizes(prompts, model, max_tokens))

    def test_last_token_is_delimiter(self):
        model = 'gpt-4'
        max_tokens = 5
        prompts = tokenize("This is a test.", model, max_tokens)
        self.assertEqual(prompts, ['This is a test.'])
        self.assertTrue(self.validate_prompt_sizes(prompts, model, max_tokens))

    def test_last_token_is_not_delimiter(self):
        model = 'gpt-4'
        max_tokens = 5
        text = "Test. This is a really long sentence."
        prompts = tokenize(text, model, max_tokens)
        self.assertEqual(prompts, ['Test.', ' This is a really long', ' sentence.'])
        self.assertTrue(self.validate_prompt_sizes(prompts, model, max_tokens))
        # print("prompts:", prompts)

    def test_single_token_no_delimiter(self):
        pass

    def test_multiple_tokens_no_delimiter(self):
        pass

    def test_korean(self):
        with open(this_dir + "/inputs/memorize-ch-1.txt", "r") as f:
            text = f.read()
        model = 'gpt-4'
        max_tokens = 4000
        prompts = tokenize(text, model, max_tokens)
        print("Here!")
        self.assertTrue(self.validate_prompt_sizes(prompts, model, max_tokens))
        
        with open(this_dir + "/outputs/memorize-ch-1.txt", "w") as f:
            # f.writelines(prompts)
            f.write(prompts[0])

if __name__ == '__main__':
    unittest.main()
