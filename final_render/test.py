from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import*
from intro import *
from settings import *
from user import *
from diary import *
from scale import *
from clinic import *
from statistic import *
from urllib.parse import parse_qsl
import psycopg2


app = Flask(__name__)

# LINE BOT info
try: 
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    parser = WebhookParser(LINE_CHANNEL_SECRET)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)
except:
    print("Error while connecting to LineBot")


try:
    conn=psycopg2.connect(host=HOST_NAME, 
                        user=USER_NAME, 
                        password=PASSWORD, 
                        dbname=DB_NAME, 
                        port=PORT_NUM)
    cur=conn.cursor()

    print ("success")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)




@app.route("/callback", methods=['POST'])
def callback():
    global chat_button
    request_data = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    body = request_data

    try:
        events = parser.parse(body, signature)  # 傳入的事件
    except InvalidSignatureError:
        abort(400)
    except LineBotApiError:
        abort(400) 

    for event in events:
        if isinstance(event, MessageEvent):  # 如果有訊息事件
            #quickreply
            if event.message.text == "@intro":
                introlist(event)
            #button template
            elif  event.message.text == "@scale":
                quickscale(event)
            elif  event.message.text == "@clinic":
                buttonregion(event)
            elif event.message.text == "@user": 
                createuser(event)
            #diary
            elif event.message.text == "@diary":
                showtime(event)
            #stat
            elif event.message.text == "@stat":
                statbutton(event)

                
            

        

        #POST---------------------------------------------------------
        if isinstance(event, PostbackEvent):
            backdata=dict(parse_qsl(event.postback.data))
        
            #@SCALE switch case : different scale
            if backdata.get('action') and backdata['action'].startswith('scale_'):
                scaletype = backdata['action'].split('_')[1]
                score = backdata['action'].split('_')[2]
                handle_scale(event, scaletype, score)
                
            elif backdata.get('action') and backdata['action'].startswith('nextquestion_'):
                _,scaletype,q_id,score = backdata['action'].split('_')
                nextquestion(event, scaletype, q_id, score)
                
            
            #@CLINIC
            elif  backdata.get('action') and backdata['action'].startswith('region_'):
                region_num = backdata['action'].split('_')[1]
                quickclinic(event,region_num)   
            elif  backdata.get('action') and backdata['action'].startswith('clinic_'):
                clinic_num = backdata['action'].split('_')[1]
                cliniclist(event,clinic_num)
            
                
            #@INTRO
            elif backdata.get('action') and backdata['action'].startswith('intro_'):
                item_id = backdata['action'].split('_')[1]
                intro(event, item_id)
            elif backdata.get('action') and backdata['action'].startswith('symptom_'):
                item_id = backdata['action'].split('_')[1]
                symptom(event, item_id)
            elif backdata.get('action') and backdata['action'].startswith('arealist_'):
                item_id = backdata['action'].split('_')[1]
                arealist(event, item_id)
            elif backdata.get('action') and backdata['action'].startswith('percent_'):
                _,area_id,ill_id = backdata['action'].split('_')
                percentagelist(event, area_id,ill_id)
            
            #@DIARY
            elif backdata.get('action') and backdata['action'].startswith('date'): 
                data = event.postback.params
                date = data['date']
                diarytest(event,date)
                #date_record(event,date)
                #print("called date func")

            elif backdata.get('action') and backdata['action'].startswith('emotion_'):
                emotiontype = backdata['action'].split('_')[1]
                date=backdata['date']
                store_record(event, date, emotiontype)
                feedback(event ,emotiontype)
            
            elif backdata.get('action') and backdata['action'].startswith('overwrite_'):
                emotiontype = backdata['action'].split('_')[1]
                date = backdata['action'].split('_')[2]
                update_emotion_record(event, date, emotiontype)
                

            #@STAT
            elif backdata.get('action') and backdata['action'].startswith('selectdate'): 
                data = event.postback.params
                date = data['date']
                oneday(event,date)

            elif backdata.get('action') and backdata['action'].startswith('view'):
                viewtype = backdata['action'].split('_')[1] 
                if(int(viewtype)==1):
                    choosedate(event)      
                elif(int(viewtype)==2):
                    #drawsevendays(event)
                    sevendays(event)
                elif(int(viewtype)==3):
                    thirtydays(event)


    return "OK"



if conn:
    cur.close()
    conn.close()
    print("PostgreSQL connection is closed.")



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

