import pandas as pd #数据分析
import numpy as np #科学计算
from pandas import Series,DataFrame
import pymysql.cursors
import datetime
import time
from dateutil import rrule
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

def fiber_fault(province):
    # 连接配置信息
    # province = 'jiangxi'
    save_path = '/Users/gubaidan/Downloads/2/' + province + '_fiber_fault.csv'

    # config = {
    #     'host': "172.16.135.8",
    #     'port': 3306,
    #     'user': 'jiangxi',
    #     'password':'456123',
    #     'db': province,
    #     'charset':'utf8',
    #     'cursorclass':pymysql.cursors.DictCursor,
    # }
    # connection = pymysql.connect(**config)

    config = {
        'host': "172.16.135.8",
        'port': 3306,
        'user': 'jiangxi',
        'password': '456123',
        'db': province,
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)


    # 光缆
    sql_fiber = "SELECT OBJ_ID, A_RESTYPE, A_RESOBJID, Z_RESTYPE, Z_RESOBJID, LENGTH, LINE_NUMBER, PRODUCER_ID, FIBER_TYPE FROM t_fiber_seg"
    df_fiber = pd.read_sql(sql_fiber,connection)
    df_fiber['ALARM_NUM'] = ''  # 增加一列，告警次数
    df_fiber['ALARM_TIME'] = ''  # 增加一列，告警时间
    # 机房与站点的关系，字典存储
    sql_room_site = "select OBJ_ID,PAR_SITE from t_spc_room"
    df_room_site = pd.read_sql(sql_room_site, connection)
    room_site = {}
    for i in range(df_room_site.shape[0]):
        room_site[df_room_site.iloc[i, 0]] = df_room_site.iloc[i, 1]
    # print("机房与站点关系", room_site)

    for i in range(df_fiber.shape[0]):
        a_type = df_fiber.iloc[i, 1]
        z_type = df_fiber.iloc[i, 3]
        a_id = df_fiber.iloc[i, 2]
        z_id = df_fiber.iloc[i, 4]
        # 若是机房，转化成站点
        if a_type == '10102':
            if room_site.__contains__(a_id):
                a_id = room_site[a_id]
            else:
                continue
        if z_type == '10102':
            if room_site.__contains__(z_id):
                z_id = room_site[z_id]
            else:
                continue

        # 江西16.01-16.11月份的告警数据
        # sql_fiber_fault_a_1 = "select ALARM_EMS_TIME, ALARM_EMS_RESUME_TIME from history_alarm where ALARM_CAUSE = 'Loss Of Signal' and PROCESS_STATE not in ('2','3') and STATION_ID='" + a_id + "'"
        # df_fiber_fault_a_1 = pd.read_sql(sql_fiber_fault_a_1, connection1)
        #
        # sql_fiber_fault_z_1 = "select ALARM_EMS_TIME, ALARM_EMS_RESUME_TIME from history_alarm where ALARM_CAUSE = 'Loss Of Signal' and PROCESS_STATE not in ('2','3') and STATION_ID='" + z_id + "'"
        # df_fiber_fault_z_1 = pd.read_sql(sql_fiber_fault_z_1, connection1)
        # 江西16.12-17.03月份的告警数据
        sql_fiber_fault_a = "select ALARM_EMS_TIME, ALARM_EMS_RESUME_TIME from t_rt_history_alarm where (ALARM_CAUSE ='lossOfSignal' or ALARM_CAUSE ='Loss Of Signal') and PROCESS_STATE not in ('2','3') and STATION_ID='" + a_id + "'"
        df_fiber_fault_a = pd.read_sql(sql_fiber_fault_a, connection)

        sql_fiber_fault_z = "select ALARM_EMS_TIME, ALARM_EMS_RESUME_TIME from t_rt_history_alarm where (ALARM_CAUSE ='lossOfSignal' or ALARM_CAUSE ='Loss Of Signal') and PROCESS_STATE not in ('2','3') and STATION_ID='" + z_id + "'"
        df_fiber_fault_z = pd.read_sql(sql_fiber_fault_z, connection)

        # 结合
        df_fiber_fault_a = df_fiber_fault_a.drop_duplicates()
        df_fiber_fault_z = df_fiber_fault_z.drop_duplicates()

        for j in range(df_fiber_fault_a.shape[0]):
            for k in range(df_fiber_fault_z.shape[0]):
                a_fault_time = int(df_fiber_fault_a.iloc[j, 1]) - int(df_fiber_fault_a.iloc[j, 0])
                z_fault_time = int(df_fiber_fault_z.iloc[k, 1]) - int(df_fiber_fault_z.iloc[k, 0])
                if df_fiber_fault_a.iloc[j, 0] == df_fiber_fault_z.iloc[k, 0] and (a_fault_time > 0 or z_fault_time > 0):
                    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(df_fiber_fault_a.iloc[j, 0]) / 1000))  # 告警开始时间
                    start_time = datetime.datetime(2016, 1, 1)
                    until_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    months = rrule.rrule(rrule.MONTHLY, dtstart=start_time, until=until_time).count() - 1

                    if a_fault_time > z_fault_time:
                        fault_time = a_fault_time
                    else:
                        fault_time = z_fault_time

                    if months >= 0 and months <= 14 and fault_time >= 3600:  # 只考虑2016.01到2017.03的告警数据,并且修复时间至少一个小时
                        if str(df_fiber.iat[i, 9]) in '':
                            df_fiber.iat[i, 9] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                            df_fiber.iat[i, 9][months] = 1
                        else:
                            df_fiber.iat[i, 9][months] += 1  # 当前月份告警次数加1

                        if str(df_fiber.iat[i, 10]) in '':
                            df_fiber.iat[i, 10] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                            df_fiber.iat[i, 10][months] = fault_time
                        else:
                            df_fiber.iat[i, 10][months] += fault_time  # 当前月份的告警时间
        print(i)
    df_fiber.to_csv(save_path, index=False, header=True)


province_list = ['xizang', 'zhejiang']
for i in range(len(province_list)):
    print(province_list[i])
    fiber_fault(province_list[i])
