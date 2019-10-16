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
    elif intent_name == "daftar-kepanitiaan":
        return daftar_kepanitiaan(data)
    elif intent_name == "daftar-nama":
        return daftar_nama(data)
    elif intent_name == "daftar-nim":
        return daftar_nim(data)
    elif intent_name == "daftar-sie":
        return daftar_sie(data)
    elif intent_name == "daftar-alasan":
        return daftar_panitia(data)

    return jsonify(request.get_json())


def list_kepanitiaan(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["callback_query"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["callback_query"]["message"]["message_id"]
    pesan = data['queryResult']['queryText']

    try:
        result = None
        id_terakhir = None

        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_kegiatan"
            cursor.execute(sql)
            result = cursor.fetchall()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
            id_terakhir = cursor.lastrowid

        connection.commit()

        with connection.cursor() as cursor:
            for kegiatan in result:
                sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id_terakhir, kegiatan["id"], date.today().strftime("%Y-%m-%d")))

            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_terakhir))

        connection.commit()

        respon = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": kegiatan["nama_kegiatan"],
                        "subtitle": kegiatan["status"]
                    }
                }
                for kegiatan in result
            ]
        }

        return jsonify(respon)

    except Exception as error:
        print(error)
        respon = {"fulfillmentText": "Mohon maaf, terjadi kesalahan"}
        return jsonify(respon)


def daftar_kepanitiaan(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["callback_query"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["callback_query"]["message"]["message_id"]
    pesan = data['queryResult']['queryText']
    text = ""

    try:
        id_terakhir = None
        text = "Masukan nama Anda"

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
            id_terakhir = cursor.lastrowid

        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id_terakhir, text, date.today().strftime("%Y-%m-%d")))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_terakhir))

        connection.commit()
    except Exception as error:
        print(error)
        text = "Terjadi kesalahan, silahkan coba lagi"

    return jsonify({'fulfillmentText': text})


def daftar_nama(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["message_id"]
    pesan = data['queryResult']['queryText']
    text = ""

    try:
        id_terakhir = None
        text = "Masukan NIM Anda"

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
            id_terakhir = cursor.lastrowid

        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id_terakhir, text, date.today().strftime("%Y-%m-%d")))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_terakhir))

        connection.commit()
    except Exception as error:
        print(error)
        text = "Terjadi kesalahan, silahkan coba lagi"

    return jsonify({'fulfillmentText': text})


def daftar_nim(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["message_id"]
    pesan = data['queryResult']['queryText']
    text = ""

    try:
        id_terakhir = None
        text = "Masukan nama sie yang diinginkan.\nSie yang tersedia yaitu:\n1. Kamper\n2. Lomba\n3. Sekre\n" \
               "4. Konsum\n5. Acara\n6. Rohani"

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
            id_terakhir = cursor.lastrowid

        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id_terakhir, text, date.today().strftime("%Y-%m-%d")))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_terakhir))

        connection.commit()
    except Exception as error:
        print(error)
        text = "Terjadi kesalahan, silahkan coba lagi"

    return jsonify({'fulfillmentText': text})


def daftar_sie(data):
    id_user = data["originalDetectIntentRequest"]["payload"]["from"]["id"]
    id_pesan = data["originalDetectIntentRequest"]["payload"]["message_id"]
    pesan = data['queryResult']['queryText']
    text = ""

    try:
        id_terakhir = None
        text = "Berikan alasan mengapa Anda memilih sie tersebut"

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, tanggal, user_id, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, date.today().strftime("%Y-%m-%d"), id_user, '0'))
            id_terakhir = cursor.lastrowid

        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id_terakhir, text, date.today().strftime("%Y-%m-%d")))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_terakhir))

        connection.commit()
    except Exception as error:
        print(error)
        text = "Terjadi kesalahan, silahkan coba lagi"

    return jsonify({'fulfillmentText': text})


def daftar_panitia(data):
    print(data)


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
