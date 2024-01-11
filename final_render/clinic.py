from settings import *
from linebot import LineBotApi,WebhookParser
from linebot.models import *
from sql import *
import psycopg2

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

try:
    conn=psycopg2.connect(host=HOST_NAME, 
                        user=USER_NAME, 
                        password=PASSWORD, 
                        dbname=DB_NAME, 
                        port=PORT_NUM)
    cur=conn.cursor()

    #conn.commit()

    print ("success")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

#-----------------------------------------------------------------
#先選擇地區
def buttonregion(event):
    try:
        cur.execute(SQL_REGION)          #fetch data from rds ill_intros table
        conn.commit()
        rows = cur.fetchall()
        alldata = []
        for row in rows:
            # Extract values from the row
            region_id,region_name = row
            values={"region_id":region_id,"region_name":region_name}
            alldata.append(values)
       
        region = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='請選擇地區',
                text='新竹市/縣',
                actions=[
                    PostbackAction(
                        label=item["region_name"],
                        data=f'action=region_{item["region_id"]}'
                    ) 
                    for item in alldata
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token,region)
    except Exception as e:
        print("Error in buttonregion:", e)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))


def quickclinic(event,region_num):
    try:
        sql="SELECT region_id,clinic_id,clinic_name FROM clinic"
        cur.execute(sql)
        result_set = cur.fetchall()
        alldata=[]
        for row in result_set:
            region_id,clinic_id,clinic_name = row
            if region_id==int(region_num):
                values={"clinic_id":clinic_id,"clinic_name":clinic_name}
                alldata.append(values)
                
            
        clinic=TextSendMessage(
            text='要選擇哪個診所機構呢?',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(
                        label=item["clinic_name"],
                        data='action=clinic_%s'%item["clinic_id"]
                        )
                    )
                    for item in alldata
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,clinic)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))  
        
def cliniclist(event,clinic_num):
    try:
        sql="SELECT clinic_name,address,phone,latitude,longitude FROM clinic WHERE clinic_id=%s"%clinic_num
        cur.execute(sql)
        result_set = cur.fetchall()

        if result_set:
            info = result_set[0]
            clinic_name,address,phone,latitude,longitude = info
            
        location=LocationSendMessage(
            title=clinic_name,
            address=address+'\n'+phone,
            latitude=latitude,
            longitude=longitude
        )
        line_bot_api.reply_message(event.reply_token,location)
    except Exception as e:
        print("Error in cliniclist:",e)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))