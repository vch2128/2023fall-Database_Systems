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


def introlist(event):
    try:
        cur.execute(SQL_ILL_INTRO_NAME)          #fetch data from rds ill_intros table
        conn.commit()
        rows = cur.fetchall()
        alldata = []
        for row in rows:
            # Extract values from the row
            id,name = row
            values={"id":id,"name":name}
            alldata.append(values)
        

        carouse=TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    #use for loop? to create five illness?
                    CarouselColumn(
                        thumbnail_image_url='https://image1.gamme.com.tw/news2/2018/74/09/pJyTn6CWj5_Zq6Q.jpg',
                        title=item["name"],
                        text='選擇你想查看的資訊吧',
                        actions=[
                            PostbackAction(
                                label='簡介說明',
                                data='action=intro_%s'%item["id"]
                            ),
                            PostbackAction(
                                label='常見症狀',
                                data='action=symptom_%s'%item["id"]
                            ),
                            PostbackAction(
                                label='各國盛行率',
                                data='action=arealist_%s'%item["id"]
                            )
                        ]
                    )
                    for item in alldata
                ]
            )   
        ) 
        line_bot_api.reply_message(event.reply_token,carouse)  
    except Exception as e:
        print(f"Error in introlist: {e}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='失敗'))


        
def intro(event,item_id):
    try:
        cur.execute(SQL_ILL_INTRO,(int(item_id),))          #fetch data from rds ill_intros table
        conn.commit()
        selected_row = cur.fetchall()
        # Find the row with the matching item_id

        if selected_row:
            id, name,en_name, intro = selected_row[0]
            msg = "%s簡介\n- 英文名：%s\n- 介紹：%s" % (name,en_name,intro)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="No matching data found"))

    except Exception as e:
        print("Error in handle_postback:", e)


def symptom(event,item_id):
    try:
        SQL_ILL_SYMPTOM = """
        select symptoms,name
        from ill_symptoms
        join ill_intros on ill_symptoms.id=ill_intros.id
        where ill_symptoms.id = %s
        """
        cur.execute(SQL_ILL_SYMPTOM,(int(item_id),))          #fetch data from rds ill_intros table
        conn.commit()
        rows = cur.fetchall()
        # Find the row with the matching item_id
        selected_row = []
        for row in rows:
            symp,name = row
            iname=name
            selected_row.append(symp)

        if selected_row:
            # Join the symptoms into a string
            symptoms_str = "\n- ".join(selected_row)
            msg = "%s的常見症狀：\n- %s" % (iname,symptoms_str)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="No matching data found"))

    except Exception as e:
        print("Error in symptom:", e)



def arealist(event,item_id):
    try:
        cur.execute(SQL_AREA_LIST)
        result_set = cur.fetchall()
        alldata=[]
        for row in result_set:
            area_id,area_name = row
            values={"id":area_id,"name":area_name}
            alldata.append(values)
                
            
        area=TextSendMessage(
            text='想要了解哪一個區域的各國盛行率？',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(
                        label=item["name"],
                        data='action=percent_%s_%s'%(item["id"],item_id)
                        )
                    )
                    for item in alldata
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,area)

    except Exception as e:
        print("Error in arealist:", e)


def percentagelist(event,area_id,ill_id):
    try:
        cur.execute (SQL_WANTED_AREA,(int(area_id),))          
        conn.commit()
        rows = cur.fetchall()
        selected_row = []
        for row in rows:
            country_name = row[0]
            perc = row[int(ill_id)]
            one_perc = '%s：%s'%(country_name,perc)
            selected_row.append(one_perc)

        cur.execute(SQL_ILL_INTRO_NAME)
        rows = cur.fetchall()
        for row in rows:
            if row[0]==int(ill_id):
                ill_name = row[1]

        cur.execute(SQL_AREA_LIST)
        result_set = cur.fetchall()
        for row in result_set:
            if row[0]==int(area_id):
                area_name = row[1]

        if selected_row:
            perc_str = "％\n- ".join(selected_row)
            msg = "%s在%s的盛行率：\n- %s％" % (ill_name,area_name,perc_str)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="No matching data found"))

    except Exception as e:
        print("Error in percentage list:", e)
