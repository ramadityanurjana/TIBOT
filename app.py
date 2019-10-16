# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
from datetime import date

# initialize the flask app
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))
connection = pymysql.connect(host='db4free.net', user='ramaditya', password='osesehat019', db='tibotdb',
                             cursorclass=pymysql.cursors.DictCursor)

# create a route for webhook
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")

    if intent_name == "list-kepanitiaan":
        return list_kepanitiaan(data)

    return jsonify(request.get_json())


def list_kepanitiaan(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["callback_query"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["callback_query"]["message"]["message_id"]
    pesan = data['queryResult']['queryText']

    try:
        result = None

        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_kegiatan"
            cursor.execute(sql)
            result = cursor.fetchall()

        print(result)
    except Exception as error:
        print(error)


        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
        #     cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
        #     idterakhir = cursor.lastrowid
        #     sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
        #     cursor.execute(sql, (idterakhir, pesan, date.today().strftime("%Y-%m-%d")))
        #
        # connection.commit()

def order(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["message_id"]
    pesan = data['queryResult']['queryText']
    text = ""

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
            idterakhir = cursor.lastrowid
            sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (idterakhir, pesan, date.today().strftime("%Y-%m-%d")))
        connection.commit()
        text = "Berhasil"
    except Exception as error:
        print(error)
        text = "Terjadi kesalahan, silahkan coba lagi"

    response = {
        'fulfillmentText': text
    }

    return jsonify(response)


# run the app
if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
