import requests
import pandas as pd
import pymysql
import paramiko
from sshtunnel import SSHTunnelForwarder
from datetime import datetime

mypkey = paramiko.RSAKey.from_private_key_file("C:\\Users\\shih\\ActuaViz\\docs\\treasurance_info_yoyo_actuviz.pem")
sql_hostname = 'treasurance-info-db.ciiomwpipnuy.ap-northeast-1.rds.amazonaws.com'
sql_username = 'yoyo'
sql_password = 'Xgeej6534'
sql_main_database = 'treasurance_info_db'
sql_port = 3306
ssh_host = 'ec2-18-181-70-135.ap-northeast-1.compute.amazonaws.com'
ssh_user = 'yoyo_actuviz'
ssh_port = 22
sql_ip = '1.1.1.1.1'

headers = {'X-Token': 'f313@edf34&4*33#324gj56'}
mortality_rate_id = 6

# DB Operations
def getLifeTable():
   url = 'https://library.treasurance.info/out-api/v2/mortality-rate/get-value?id=%s' % mortality_rate_id
   response = requests.post(url, headers=headers)
   res = response.json()['data']['data']
   result = pd.DataFrame(res, columns=['gender', 'age', 'value'])
   result.columns = ['Gender', 'Age', 'MortRate']
   result['MortRate'] = pd.to_numeric(result['MortRate'])
   return result

def pullPremiumTable(premiums):
   with SSHTunnelForwarder(
      (ssh_host, ssh_port),
      ssh_username=ssh_user,
      ssh_pkey=mypkey,
      remote_bind_address=(sql_hostname, sql_port)) as tunnel:
      conn = pymysql.connect(
         host='127.0.0.1',
         user=sql_username,
         passwd=sql_password,
         db=sql_main_database,
         port=tunnel.local_bind_port,
         autocommit=True
         )
      cursor = conn.cursor()
      sql = "SELECT count(*) FROM `table_3factors`"
      cursor.execute(sql)
      current_id = cursor.fetchone()[0]
      sql = "Insert Into `table_3factors` (`id`, `factor1`, `factor2`, `factor3`, `value`, `tableable_type`, `tableable_id`, `created_at`, `updated_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
      time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      for row in premiums.itertuples(index=False):
         cursor.execute(sql, (current_id+1+row.id ,row.Age, row.Gender, row.PPP, row.GP,'premiums', 22, time, time))
      conn.close()