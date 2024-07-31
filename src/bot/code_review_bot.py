import os
import logging
import requests
from git import Repo
import openai
from src.config import Config
import bandit
from bandit.core import manager, config



class CodeReviewBot:
    def __init__(self):
        self.repo = Repo.clone_from(Config.REPO_URL, '/tmp/repo')
        openai.api_key = Config.OPENAI_API_KEY

    def run_security_scan(self, file_path):
        b_conf = config.BanditConfig()
        b_mgr = manager.BanditManager(b_conf, "json")
        b_mgr.discover_files([file_path])
        b_mgr.run_tests()
        results = b_mgr.get_issue_list()
        return results

    def analyze_code(self, file_path):
        try:
            with open(file_path, 'r') as file:
                code = file.read()
        except IOError as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return "Error reading file."

        try:
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=f"Review the following code and provide feedback:\n\n{code}. "
                       f"The feedback should include any errors, and an estimate of complexity. "
                       f"Additionally, you should highlight any security issues.",
                max_tokens=Config.MAX_TOKENS,
                n=1,
                stop=None,
                temperature=Config.TEMPERATURE,
            )
            feedback = response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Error from OpenAI API: {e}")
            feedback = "Error from OpenAI API."

        security_issues = self.run_security_scan(file_path)
        security_feedback = "\n".join([str(issue) for issue in security_issues])
        return f"{feedback}\n\nSecurity Issues:\n{security_feedback}"

    def send_slack_notification(self, message, webhook_url):
        payload = {"text": message}
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Error sending Slack notification: {e}")
            return None
        return response.status_code


def review_pull_request(self, pr_url):
    try:
        pr_data = requests.get(pr_url).json()
    except requests.RequestException as e:
        logging.error(f"Error fetching PR data: {e}")
        return

    files = pr_data.get('files', [])
    comments = []

    for file in files:
        file_path = os.path.join(self.repo_dir, file['filename'])
        feedback = self.analyze_code(file_path)
        if feedback:
            comments.append(f'Feedback for {file_path}:\n{feedback}')

    self.post_comments(pr_url, comments)

    slack_webhook_url = Config.SLACK_WEBHOOK_URL
    message = f"Code review completed for PR: {pr_url}\nComments: {comments}"
    self.send_slack_notification(message, slack_webhook_url)

    def post_comments(self, pr_url, comments):
        headers = {
            'Authorization': f'token {Config.GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }

        pr_number = pr_url.split('/')[-1]
        repo_owner = Config.REPO_URL.split('/')[-2]
        repo_name = Config.REPO_URL.split('/')[-1]

        for comment in comments:
            comment_data = {'body': comment}
            response = requests.post(
                f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments',
                headers=headers,
                json=comment_data
            )

            if response.status_code == 201:
                print(f'Successfully posted comment: {comment}')
            else:
                print(f'Failed to post comment: {response.content}')

# Example usage
if __name__ == '__main__':
    bot = CodeReviewBot()
    bot.review_pull_request(Config.PR_URL)