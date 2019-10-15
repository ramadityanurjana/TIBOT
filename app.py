# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
from datetime import date

# initialize the flask app
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

# create a route for webhook
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    pesan = data['queryResult']['queryText']
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)
    connection = pymysql.connect(host='db4free.net', user='ramaditya', password='osesehat019', db='tibotdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox(pesan,date) VALUES (%s,%s)"
            cursor.execute(sql, (date.today().strftime("%Y-%m-%d"), pesan))
        connection.commit()
    finally:
        connection.close()

    if intent_name == "order":
        return order(data)

    return jsonify(request.get_json())

def order(data):
    response = {
        'fulfillmentText': "Ini Balasan dari Webhook"
    }

    return jsonify(response)

# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')