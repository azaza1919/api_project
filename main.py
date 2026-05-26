from flask import Flask, render_template, request, jsonify

from mistral import mail_promt
from gmail_auth import mail_get
from configs import mistral_api_key as api_key
import database


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #отрисовка cайта


@app.route('/process', methods=['POST'])
def process():
    try:
        k = int(request.form.get('count', 5)) #кол-во почт (берется с сайта)
        mails = mail_get(k) 
        
        results = [] 
        for mail in mails:
            email_id = mail['id']
            subject = mail['subject']

            msg = database.get_cached(email_id)
            if msg is None:
                msg = mail_promt(mail['body'], api_key)
                database.save(email_id, subject, msg)

            results.append({
                'id': mail['id'],
                'subject': mail['subject'],
                'summary': msg
            })

        return jsonify({
            'status': 'success', 
            'data': results
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    

if __name__ == '__main__':
    with app.app_context():
        database.init_db()
    app.run(debug=True)