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



def quickscale(event):
    try:
        try:
            cur.execute(SQL_SCALE_NAME)          #fetch data from rds ill_intros table
            conn.commit()
            rows = cur.fetchall()
            alldata = []
            for row in rows:
                # Extract values from the row
                id,name = row
                values={"id":id,"name":name}
                alldata.append(values)
            msg='action=scale_%s'
        except Exception as e:
            print(f"SQL error: {e}")

        t=TextSendMessage(
            text='要選擇哪一量表呢?',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(
                        label=item["name"],
                        #data = msg % (item["id"] if item["id"] is not None else '')
                        data = 'action=scale_%s_0' % item["id"]
                        #data=msg%item["id"]
                        )
                    )
                    for item in alldata
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,t)
    except Exception as e:
        print(f"Error in scale: {e}")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='失敗'))


button_scores = {}  
def handle_scale(event,scaletype,score):
    try:
        global button_scores
        score = int(score)
        msg=[]
        msg.append(TextSendMessage(text="開始測驗"))
        #顯示量表
        #修改:使用者選完選項後，能夠get使用者選擇的
        SQL_SCALE_Q = """
        select question_id,content,indicator from scales
        where ill_id = %s and question_id=%s
        """
        cur.execute(SQL_SCALE_Q,(int(scaletype),1,))          #fetch data from rds ill_intros table
        conn.commit()
        rows = cur.fetchall()
        # Find the row with the matching item_id
        if rows:
            q_id, content, ind = rows[0]
            #print(q_id,content)
        print(score)
        if int(scaletype) == 1:
            print("scale1")
            button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
            q=TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        title='第%s題'%q_id,
                        text=content,
                        actions=[
                            PostbackAction(
                                label='是',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                            ),
                            PostbackAction(
                                label='否',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                            )
                        ]
                    )
            )
        elif int(scaletype) == 2:
            print("scale2")
            button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
            q=TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        title='第%s題'%q_id,
                        text=content,
                        actions=[
                            PostbackAction(
                                label='沒有問題',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                            ),
                            PostbackAction(
                                label='些微',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                            ),
                            PostbackAction(
                                label='中等',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+2)
                            ),
                            PostbackAction(
                                label='嚴重',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                            )
                        ]
                    )
                )
        elif int(scaletype) == 3:
            print("scale3")
            button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
            q=TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        title='第%s題'%q_id,
                        text=content,
                        actions=[
                            PostbackAction(
                                label='沒有或極少(少於1天 /週)',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                            ),
                            PostbackAction(
                                label='有時 (1~2 天 /週)',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                            ),
                            PostbackAction(
                                label='時常 (3~4 天 /週)',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+2)
                            ),
                            PostbackAction(
                                label='常常/總是 (5~7 天 /週)',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                            )
                        ]
                    )
                )
        elif int(scaletype) == 4:
            print("scale4")
            button_scores[event  .source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
            q=TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        title='第%s題'%q_id,
                        text=content,
                        actions=[
                            PostbackAction(
                                label='從不/很少',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                            ),
                            PostbackAction(
                                label='偶爾',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                            ),
                            PostbackAction(
                                label='常常',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+2)
                            ),
                            PostbackAction(
                                label='總是',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                            )
                        ]
                    )
                )
        elif int(scaletype) == 5:
            print("scale5")
            button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
            q=TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        title='第%s題'%q_id,
                        text=content,
                        actions=[
                            PostbackAction(
                                label='從不',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                            ),
                            PostbackAction(
                                label='偶爾',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                            ),
                            PostbackAction(
                                label='常常',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                            ),
                            PostbackAction(
                                label='非常頻繁',
                                data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+4)
                            )
                        ]
                    )
                )

        msg.append(q)
        line_bot_api.reply_message(event.reply_token,msg)

    except Exception as e:
        print("Error in handle_scale:", e)
        print("score:", score)

# total_score_threshold = 8
def nextquestion(event,scaletype,q_id,score):
    try:
        global button_scores
        cur.execute(SQL_SCALE_Q,(int(scaletype),q_id,))          
        conn.commit()
        rows = cur.fetchall()
        # Find the row with the matching item_id
        if rows:
            q_id, content, ind = rows[0]
            print(score)
            
            if int(scaletype) == 1:
                button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)
                q=TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='第%s題'%q_id,
                            text=content,
                            actions=[
                                PostbackAction(
                                    label='是',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                                ),
                                PostbackAction(
                                    label='否',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                                )
                            ]
                        )
                )
                # total_score = button_scores.get(event.source.user_id, 0)
                # if total_score >= total_score_threshold:
                ##     region = TemplateSendMessage(
                #     alt_text='Buttons template',
                #     template=ButtonsTemplate(
                #         title='請選擇地區',
                #         text='新竹',
                #         actions=[
                #             PostbackAction(
                #                 label=item["region_name"],
                #                 data=f'action=region_{item["region_id"]}'
                #             ) 
                #             for item in alldata
                #         ]
                #     )
                # )
                # line_bot_api.reply_message(event.reply_token, [region])
                    

            elif int(scaletype) == 2:
                button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
                q=TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='第%s題'%q_id,
                            text=content,
                            actions=[
                                PostbackAction(
                                    label='沒有問題',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                                ),
                                PostbackAction(
                                    label='些微',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                                ),
                                PostbackAction(
                                    label='中等',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+2)
                                ),
                                PostbackAction(
                                    label='嚴重',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                                )
                            ]
                        )
                )
            elif int(scaletype) == 3:
                button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
                q=TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='第%s題'%q_id,
                            text=content,
                            actions=[
                                PostbackAction(
                                    label='沒有或極少(少於1天 /週)',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                                ),
                                PostbackAction(
                                    label='有時 (1~2 天 /週)',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                                ),
                                PostbackAction(
                                    label='時常 (3~4 天 /週)',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+2)
                                ),
                                PostbackAction(
                                    label='常常/總是 (5~7 天 /週)',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                                )
                            ]
                        )
                    )
            elif int(scaletype) == 4:
                button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
                q=TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='第%s題'%q_id,
                            text=content,
                            actions=[
                                PostbackAction(
                                    label='從不/很少',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                                ),
                                PostbackAction(
                                    label='偶爾',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                                ),
                                PostbackAction(
                                    label='常常',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+2)
                                ),
                                PostbackAction(
                                    label='總是',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                                )
                            ]
                        )
                    )
            elif int(scaletype) == 5:
                button_scores[event.source.user_id] = button_scores.get(event.source.user_id, 0) + int(score)   
                q=TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='第%s題'%q_id,
                            text=content,
                            actions=[
                                PostbackAction(
                                    label='從不',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score))
                                ),
                                PostbackAction(
                                    label='偶爾',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+1)
                                ),
                                PostbackAction(
                                    label='常常',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+3)
                                ),
                                PostbackAction(
                                    label='非常頻繁',
                                    data='action=nextquestion_%s_%s_%s'%(scaletype,q_id+1,int(score)+4)
                                )
                            ]
                        )
                    )

            line_bot_api.reply_message(event.reply_token,q)

        else:
            if int(scaletype) == 1:
                if int(score) >= 8:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n建議向身心科、精神科醫師諮詢" % score))  
                elif 7 >= int(score) >= 3:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n建議向身心科、精神科醫師進行諮詢" % score)) 
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n未符合上述之情形，但自覺有思考與知覺困擾，也值得諮詢專業人員" % score))
            elif int(scaletype) == 2:
                if int(score) <= 7:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n測試者屬於正常" % score))    
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n很可能患有雙相情緒障礙症(躁鬱症)，建議接受專業治療評估" % score))     
            elif int(scaletype) == 3:
                if int(score) <= 8:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n真是令人羨慕！你目前的情緒狀態很穩定，是個懂得適時調整情緒及抒解壓力的人，繼續保持下去" % score))
                elif 9 <= int(score) <= 14:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n最近的情緒是否起伏不定？或是有些事情在困擾著你？給自己多點關心，多注意情緒的變化，試著瞭解心情變的緣由，做適時的處理，比較不會陷入憂鬱情緒" % score))
                elif 15 <= int(score) <= 18:  
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n你是不是想笑又笑不太出來，有很多事壓在心上，肩上總覺得很沈重？因為你的壓力負荷量已經到了臨界點了！千萬別再「撐」了！趕快找個有相同經驗的朋友聊聊，給心情找個出口，把肩上的重膽放下，這樣才不會陷入憂鬱症的漩渦" % score))
                elif 19 <= int(score) <= 28:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n現在的你必定感到相當不順心，無法展露笑容，一肚子苦惱及煩悶，連朋友也不知道如何幫你，趕緊找專業機構或醫療單位協助，透過專業機構的協助，必可重拾笑容" % score))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n你是不是感到相當的不舒服，會不由自主的沮喪、難過，覺得無法掙脫？因為你的心已「感冒」，心病需要心藥醫，趕緊到醫院找專業及可信賴的醫師檢查，透過他們的診療與治療，你將不會覺得孤單、無助！" % score))
            elif int(scaletype) == 4:
                if 0 <= int(score) <= 10:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n大致正常" % score))
                elif 11 <= int(score) <= 20:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n你可能有進食失調的傾向" % score)) 
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n你很大機會患上進食失調症" % score)) 
            elif int(scaletype) == 5:
                if 0 <= int(score) <= 16:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n不太可能有ADHD" % score))
                elif 17 <= int(score) <= 23:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n很可能有ADHD" % score)) 
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測驗完成！ \n總分:%s \n非常可能有ADHD" % score)) 
            
    except Exception as e:
        print("Error in next:", e)
        print("score:", score)