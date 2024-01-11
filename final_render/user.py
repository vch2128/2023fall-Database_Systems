
from linebot import LineBotApi,WebhookParser
from linebot.models import *
from settings import *
from sql import *
import psycopg2
import json
import os

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

def createuser(event):
    try:
        #  cur.execute(SQL_USER)          #fetch data from rds ill_intros table
        #  conn.commit()
        #  rows = cur.fetchall()
         uid=event.source.user_id
         profile=line_bot_api.get_profile(uid)
         user_id=profile.user_id
         user_name=profile.display_name

         sql="SELECT COUNT(*) FROM User_info WHERE user_id = %s;"
         cur.execute(sql, (user_id,))
         count = cur.fetchone()[0]
         if(count>0):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您已註冊'))
         else:
            insert_user_record(user_id,user_name)
            msg = f"歡迎 {user_name} 加入心輔小幫手~"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))
            conn.commit()
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))

def insert_user_record(user_id,user_name):
    try:
        sql = "INSERT INTO User_info (user_id,user_name) VALUES (%s, %s);"
        cur.execute(sql, (user_id,user_name))
        conn.commit()
        print("Record inserted successfully!")
    except psycopg2.Error as e:
        print(f"Error: {e}")

    # finally:
    #     # 关闭游标和连接
    #     if cur:
    #         cur.close()
    #     if conn:
    #         conn.close()
        
#  msg = f"User ID: {userid}\nDisplay Name: {name}"
        #  line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        #user_exists = False
        #  for row in rows:
        #      user_id,user_name=row
        #      if user_id==userid:
        #          user_exists = True
        #          break
        #  if user_exists:
        #      line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已註冊'))
        #  else:
        #      insert_user_record(userid,name)
        #      msg="Record inserted successfully!"
        #      #msg = f"User ID: {userid}\nDisplay Name: {name}"
        #      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
# Find the row with the matching item_id
                #selected_row = None
                # msg=[] 
                # flag=False
                # for row in rows:
                #     id = row
                #     if id == int(userid):
                #         print("id",id)
                #         flag=True
                #         msg.append(TextSendMessage(text='您已註冊過'))
                #         line_bot_api.reply_message(event.reply_token,msg)
                #         #selected_row = {"id": id, "en_name": en_name, "intro": intro}
                #         break  
                # if(flag==False): 
                #         #User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,points=points)  
                #         createuser(event) 
'''
def createuser(event):
    try:
        progress=0
        regi=[]
        regi.append(TextSendMessage(text="請填寫會員資料~~~"))
        #姓名
        regi.append(TextSendMessage(text="請輸入姓名:"))
        line_bot_api.reply_message(event.reply_token,regi)
        if isinstance(event, MessageEvent):
            user_name = event.message.text #修改:存到DB
            line_bot_api.reply_message(event.reply_token,'thankyou')

        # #性別
        # sex=TextSendMessage(
        #     text="請選擇性別:",
        #     quick_reply=QuickReply(
        #         items=[
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='男',
        #                     data='action=save_user&item=sex&sex=b',            
        #                 )
        #             ),
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='女',
        #                     data='action=save_user&item=sex&sex=g',            
        #                 )
        #             )
        #         ]
        #     )
        # )
        # regi.append(sex)
        # #年齡
        # age=TextSendMessage(
        #     text="請選擇年齡區間:",
        #     quick_reply=QuickReply(
        #         items=[
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='12~20',
        #                     data='action=save_user&item=age&option=1',            
        #                 )
        #             ),
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='21~30',
        #                     data='action=save_user&item=age&option=2',            
        #                 )
        #             ),
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='31~40',
        #                     data='action=save_user&item=age&option=3',            
        #                 )
        #             )
        #         ]
        #     )
        # )
        # regi.append(age)
        # #國家
        # nation=TextSendMessage(
        #     text="請選擇國家:",
        #     #修改:DB_country匯入!!
        #     quick_reply=QuickReply(
        #         items=[
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='country_1',
        #                     data='action=save_user&item=country&option=1',            
        #                 )
        #             ),
        #             QuickReplyButton(
        #                 action=PostbackAction(
        #                     label='country_2',
        #                     data='action=save_user&item=country&option=2',            
        #                 )
        #             )
        #         ]
        #     )
        # )
        # regi.append(nation)
        # line_bot_api.reply_message(event.reply_token,regi)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))
'''
