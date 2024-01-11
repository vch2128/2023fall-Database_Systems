import os


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
host_name = os.getenv('HOST_NAME', None)
user_name = os.getenv('USER_NAME', None)
password = os.getenv('PASSWORD', None)
db_name = os.getenv('DB_NAME', None)
port_num = os.getenv('PORT_NUM', None)