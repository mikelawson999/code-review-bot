import unittest
from src.bot.code_review_bot import CodeReviewBot

class TestCodeReviewBot(unittest.TestCase):
    def test_analyze_code(self):
        bot = CodeReviewBot(repo_url='https://github.com/user/repo', openai_api_key='your-openai-api-key')
        feedback = bot.analyze_code('path/to/code.py')
        self.assertIsNotNone(feedback)

if __name__ == '__main__':
    unittest.main()