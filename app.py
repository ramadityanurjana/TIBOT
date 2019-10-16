from flask import Flask, request, jsonify
import os
import pymysql.cursors
from datetime import date
import json

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

connection = pymysql.connect(host='db4free.net',
                             user='ramaditta',
                             password='osesehat019',
                             db='tibotdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)

    if intent_name == 'order':
        return Order(data)
    # elif intent_name == 'Awalcustom':
    #     return AwalCustom(data)

    return jsonify(request.get_json())

def Order(data):
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("id")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_inbox = ""

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d")))
            # id_inbox = cursor.lastrowid
        connection.commit()

        response = {
            'fulfillmentText': "Ini Respon dari Webhook"
        }
        return response

    except Exception:
        response = {
            'fulfillmentText': "Data anda gagal di Daftarkan"
        }
        return jsonify(response)

# run the app
if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
