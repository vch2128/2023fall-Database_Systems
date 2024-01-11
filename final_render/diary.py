from linebot import LineBotApi,WebhookParser
from linebot.models import *
from settings import *
from sql import *
import psycopg2
import json
import os
from datetime import datetime

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

conn=psycopg2.connect(host=host_name, 
                        user=user_name, 
                        password=password, 
                        dbname=db_name, 
                        port=port_num)
cur=conn.cursor()


def showtime(event):
    try:
        t=TextSendMessage(
            text='請選擇日期：',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=DatetimePickerAction(
                            label='選日期',
                            mode="date",
                            data='action=date'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,t)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))


def diarytest(event,date):
    try:
        #record previous or today?
        current_time = datetime.today().date()
        #record previous
        if (str(date) != str(current_time)):
            msg='日期:'+date+'\n'+'你那天心情感覺如何呢？'
        else:
            msg='你今天心情感覺如何呢？'

        d=str(date)
        t=TextSendMessage(
                text=msg,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                label='😢難過',
                                data='action=emotion_1&date=%s'%d            
                            )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label='😡生氣',
                                data='action=emotion_2&date=%s'%d               
                            )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label='😌平靜',
                                data='action=emotion_3&date=%s'%d               
                            )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label='😍開心',
                                data='action=emotion_4&date=%s'%d               
                            )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                            label='🤪興奮',
                            data='action=emotion_5&date=%s'%d   
                            )
                        )
                    ]
                )
        )
        line_bot_api.reply_message(event.reply_token,t)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))



def feedback(event ,emotiontype):
    try:
        if int(emotiontype) == 1:
            t=TextSendMessage(
                    text="很難過嗎？沒關係哦有我在！"
            )

        elif int(emotiontype) == 2:
            t=TextSendMessage(
                    text="很生氣嗎？深呼吸！"
            )
        
        elif int(emotiontype) == 3:
            t=TextSendMessage(
                    text="平靜是福！"
            )
        
        elif int(emotiontype) == 4:
            t=TextSendMessage(
                    text="繼續保持好心情哦！"
            )
        
        elif int(emotiontype) == 5:
            t=TextSendMessage(
                text="很興奮嗎？祝你一切順利！"
            )
        line_bot_api.reply_message(event.reply_token,t)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='feedback失敗'))
        

def check_signup(user_id):
    try:
        cur.execute(SQL_SIGNUP,(user_id,))
        user_info_rec = cur.fetchone()
        if user_info_rec is not None:
            print("User already registered")
            return False  # User is already registered
        else:
            return True  # User is not registered
    except psycopg2.Error as e:
        print(f"Error in check_signup: {e}")
        conn.rollback()
        return False


def insert_emotion_record(user_id, date, emotion_value):
    try:
        sql="INSERT INTO emotion_records (user_id,record_time,emotion) VALUES (%s, %s,%s);"
        cur.execute(sql, (user_id, str(date),emotion_value,))
        conn.commit()
        print("insert")
    except psycopg2.Error as e:
         print(f"Error in insert emotions: {e}")   
         conn.rollback()

def check_duplicate_record(user_id, date):
    try:
        sql = "SELECT * FROM emotion_records WHERE user_id = %s AND record_time = %s;"
        cur.execute(sql, (user_id, str(date),))
        existing_record = cur.fetchone()
        return existing_record is not None
    except psycopg2.Error as e:
        print(f"Error in checking duplicate record: {e}")
        conn.rollback()
        return False


#目前emotiontype是數字
def store_record(event,date,emotiontype):
     try:
        #拿取user id 
        uid=event.source.user_id
        profile=line_bot_api.get_profile(uid)
        user_id=profile.user_id
        #current_time = datetime.now()
        emotion_value = emotiontype
        if not check_signup(user_id):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請先註冊！'))
        elif not check_duplicate_record(user_id, date):
            insert_emotion_record(user_id, date, emotion_value)
            feedback(event, emotiontype)
        else:
            # 提供提示
            t = TextSendMessage(
                text='你已經存過當日心情啦！要覆寫紀錄嗎？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label='是', 
                                                text='是', 
                                                data='action=overwrite_%s_%s'%(emotion_value,str(date))
                                                ),
                        ),
                        QuickReplyButton(
                            action=MessageAction(label='否', text='否'),
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, t)
     except Exception as e:
         print(f"Error in store record: {e}")

def update_emotion_record(event, date, emotion_value):
    try:
        uid=event.source.user_id
        profile=line_bot_api.get_profile(uid)
        user_id=profile.user_id
        sql = "UPDATE emotion_records SET emotion = %s WHERE user_id = %s AND record_time = %s;"
        cur.execute(sql, (emotion_value, user_id, str(date),))
        conn.commit()
        feedback(event ,emotion_value)

    except psycopg2.Error as e:
        print(f"Error in updating emotion record: {e}")   