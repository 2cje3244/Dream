import os
import random
from flask import Flask, request, render_template
from pathlib import Path

app = Flask(__name__)

# 夢解釈用の辞書を定義
dream_dictionary = {
    "飛": "飛ぶ夢は、一般に次のようなことをあらわしています。\n１.現実のさまざまな制約から解放されて空想の世界を飛びまわりたいという願望充足。心の自由。\n２.単調な毎日から抜け出して、自分を向上させたいという願望。可能性の探求。\n３.精神的な高ぶり。高揚した気持ち。\n４.他人を超える期待。優越感。\n５.性的願望。",
    "溺": "おぼれることは死に関係があるように思われますが、夢の中では必ずしもそうではありません。おぼれることは水と結びつくので、子どものときのように安全でいたいという願望をあらわしています。しかし、次のような意味もあります。\n・あなたが、自分は愛（母親の愛）によって押しつぶされていると感じていること\n・難問に押しつぶされるのではないかという不安。自分だけとり残されるという心配",
    "落": "落ちる夢を見ることはよくありますが、それは次のことを象徴しています。\n・道徳的な堕落をこうむることの恐れ。\n・高い地位やよい職などから脱落することの恐れ。\n・名声を失うことの恐れ。\nこうした不安は自分への要求や期待が高い場合に覚えがちなので、落ちる夢はむしろその重圧を緩和しようという自己調整ともいえます。したがって落ちる夢を見たからといって、現実に失敗するわけではなく、むしろピンチを回避する可能性が高いでしょう。",
    "迷": "必死に歩き回っても、目的地につけない夢は、何をやっても思いどおりに運ばないといういらだちや、焦りを表しています。難問が続いているときに見ることが多い。"
}

IMAGE_FOLDER = 'static/images'

# ランダムに取得する関数
def get_random_image(dream_key):
    images_dir = os.path.join(IMAGE_FOLDER, dream_key)
    if os.path.exists(images_dir):
        images = os.listdir(images_dir)
        if images:
            return f"/static/images/{dream_key}/{random.choice(images)}"
    return None

# 夢の解釈関数
def interpret_dream_with_dictionary(dream_text):
    """辞書を使って夢の内容を解釈する"""
    for key, interpretation in dream_dictionary.items():
        if key in dream_text:
            interpretation = interpretation.replace('\n', '<br>')
            return {
                "interpretation": interpretation,
                "image_url": get_random_image(key),  
                "success": True
            }
    return {
        "interpretation": "その夢に関する解釈は見つかりませんでした。",
        "image_url": None,
        "success": True
    }

@app.route('/interpret', methods=['GET', 'POST'])
def interpret():
    """フォームで夢を解釈"""
    if request.method == 'POST':
        dream_text = request.form.get('dream_text', '')
        result = interpret_dream_with_dictionary(dream_text)
        return render_template('index.html', interpretation=result['interpretation'], image_url=result['image_url'])
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
