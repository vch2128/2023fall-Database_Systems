from linebot import LineBotApi,WebhookParser
from linebot.models import *
from settings import *
from sql import *
import psycopg2
import json
import os
from datetime import datetime

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
    

def statbutton(event):
    try:
        stat=TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='請選擇查看模式：',
                text='根據時間區段選擇查看模式',
                actions=[
                    PostbackAction(
                        label="查看單日",
                        data='action=view_1'
                    ),
                    PostbackAction(
                        label="查看過去一週",
                        data='action=view_2'
                    ),
                    PostbackAction(
                        label="查看過去一個月",
                        data='action=view_3'
                    ) 
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,stat)
    except Exception as e:
        print(f"Error in statbutton: {e}")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))


def choosedate(event):
    try:
        t=TextSendMessage(
            text='請選擇想查看的日期：',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=DatetimePickerAction(
                            label='選擇想查看的日期',
                            mode="date",
                            data='action=selectdate'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,t)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))


def oneday(event,date):
    try:
        uid=event.source.user_id
        profile=line_bot_api.get_profile(uid)
        user_id=profile.user_id
        user_name=profile.display_name

        sql="SELECT record_time,emotion FROM emotion_records WHERE user_id=%s AND record_time=%s"
        sql2="SELECT emotion_name FROM emotion_names WHERE emotion_id=%s"
        cur.execute(sql,(user_id,str(date)))
        rows=cur.fetchall()
        msg = []
        if rows:
             for row in rows:
                record_time,emotion=row
                cur.execute(sql2,(emotion,))
                emo=cur.fetchone()
                msg=user_name+"在"+str(record_time)+" 的心情是："+ emo[0]
        else:
            msg="您那天沒有記錄唷！"
     
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))

    except Exception as e:
        print(f"Error in oneday: {e}")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))    

def sevendays(event):            
    try:
        current_time = datetime.today().date()
        uid=event.source.user_id    
        profile=line_bot_api.get_profile(uid)
        user_id=profile.user_id
        user_name=profile.display_name
        
        cur.execute(SQL_SEVEN_DAYS,(current_time,user_id,))
        rows=cur.fetchall()
        alldata = []
        for row in rows:
            emo_name, cnt=row
            print(row)
            values = '%s： %s/7'%(emo_name,cnt)
            alldata.append(values)
        
        if alldata:
            cnt_str = "\n- ".join(alldata)
            msg = "%s過去一週的心情\n- %s" % (user_name,cnt_str)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您過去一週都沒有紀錄喔！"))
    
    except Exception as e:
        print(f"Error in sevendays: {e}")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))


def thirtydays(event):            
    try:
        current_time = datetime.today().date()
        uid=event.source.user_id
        profile=line_bot_api.get_profile(uid)
        user_id=profile.user_id
        user_name=profile.display_name

        cur.execute(SQL_THIRTY_DAYS,(current_time,user_id,))
        rows=cur.fetchall()
        alldata = []
        for row in rows:
            emo_name, cnt=row
            print(row)
            values = '%s： %s/30'%(emo_name,cnt)
            alldata.append(values)
        
        if alldata:
            cnt_str = "\n- ".join(alldata)
            msg = "%s過去一個月的心情\n- %s" % (user_name,cnt_str)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您過去三十天都沒有紀錄喔！"))
    
    except Exception as e:
        print(f"Error in thirtydays: {e}")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))