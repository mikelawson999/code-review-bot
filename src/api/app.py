from flask import Flask, request, jsonify
from src.bot.code_review_bot import CodeReviewBot
from src.config import Config

app = Flask(__name__)
bot = CodeReviewBot(repo_url=Config.REPO_URL, openai_api_key=Config.OPENAI_API_KEY)

@app.route('/review', methods=['POST'])
def review():
    try:
        data = request.get_json()
        if 'pr_url' not in data:
            return jsonify({'error': 'Missing pr_url'}), 400

        pr_url = data['pr_url']
        bot.review_pull_request(pr_url)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
