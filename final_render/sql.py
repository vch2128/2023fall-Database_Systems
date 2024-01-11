
SQL_ILL_INTRO= """
select * from ill_intros
where id = %s
"""

SQL_ILL_INTRO_NAME = """
select id,name from ill_intros
"""

SQL_USER = """
select user_id,user_name from User_info
"""

SQL_REGION = """
select * from region_name
"""

SQL_ILL_SYMPTOM = """
select symptoms,name
from ill_symptoms
join ill_intros on ill_symptoms.id=ill_intros.id
where ill_symptoms.id = %s
"""

SQL_SCALE_NAME = """
select * from scale_names
"""

SQL_SCALE_Q = """
select question_id,content,indicator from scales
where ill_id = %s and question_id=%s
"""

SQL_AREA_LIST = """
select * from asian_areas
"""

SQL_WANTED_AREA = """
select country_name,dep_p,bip_p,sch_p,ano_p,att_p
from overall_percentages
where area_id = %s
"""

SQL_ONE_DAY = """
select emotion from emotion_records
where user_id = %s and record_time = %s
"""

SQL_SEVEN_DAYS = """
with aweek(user_id,record_time,emotion) as (
select * from emotion_records
where record_time > %s - interval '7 days' and user_id=%s
),
cnt(emo_id,cnt) as (
select emotion, count(*) 
from aweek
group by emotion
)
select emotion_name,cnt
from cnt
join emotion_names on emotion_id=emo_id
""" 

SQL_THIRTY_DAYS = """
with aweek(user_id,record_time,emotion) as (
select * from emotion_records
where record_time > %s - interval '30 days' and user_id=%s
),
cnt(emo_id,cnt) as (
select emotion, count(*) 
from aweek
group by emotion
)
select emotion_name,cnt
from cnt
join emotion_names on emotion_id=emo_id
""" 