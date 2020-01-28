from network.huawei import *
from datetime import datetime
import argparse
import threading
import time

# create parser
# parser = argparse.ArgumentParser('Monitor Huawei E5576c')

# # add arguments
# parser.add_argument(
#     'SessionID',
#     metavar='sid',
#     type=str,
#     help='SessionID used to access huaweu e5776c dashboard'
# )

# args = parser.parse_args()



def get_usage(api):
    while True:
        resp = api.get_traffic()
        if resp is not None:
            total_upload = int(resp.TotalUpload)
            total_download = int(resp.TotalDownload)

            ttotal_upload = total_upload
            ttotal_download = total_download

            udtype = 'B'
            if len(str(total_upload)) >= 7:
                ttotal_upload = total_upload/1024/1024
                udtype = 'MB'
            elif len(str(total_upload)) >= 4:
                ttotal_upload = total_upload/1024
                udtype = 'KB'

            ddtype = 'B'
            if len(str(total_download)) >= 7:
                ttotal_download = total_download/1024/1024
                ddtype = 'MB'
            elif len(str(total_download)) >= 4:
                ttotal_download = total_download/1024
                ddtype = 'KB'

            print(f'U{ttotal_upload:.2f}{udtype} : D{ttotal_download:.2f}{ddtype}\n' + '*'*24)

            with open(f'traffic_{datetime.now().strftime("%d-%m-%Y")}.log', 'at+') as f:
                f.write(f'{datetime.now()}:{total_upload}:{total_download}\n')
        else: 
            break
        time.sleep(30)

api = HuaweiApi()
threading.Thread(target=get_usage, args=[api, ], daemon=True).start()
while True:
    traffic_resp = api.get_traffic()

    if traffic_resp is not None:
        up_rate = int(traffic_resp.CurrentUploadRate)
        down_rate = int(traffic_resp.CurrentDownloadRate)

        udtype = 'B'
        if len(str(up_rate)) >= 7:
            up_rate = up_rate/1024/1024
            udtype = 'MB'
        elif len(str(up_rate)) >= 4:
            up_rate = up_rate/1024
            udtype = 'KB'

        ddtype = 'B'
        if len(str(down_rate)) >= 7:
            down_rate = down_rate/1024/1024
            ddtype = 'MB'
        elif len(str(down_rate)) >= 4:
            down_rate = down_rate/1024
            ddtype = 'KB'

        out = (
            f'{up_rate:.2f}{udtype}/s - {down_rate:.2f}{ddtype}/s{" "*12}'
        )
        print(out, end='\r')
        time.sleep(1)
# else:
#     api.session_id = input(f"{HuaweiApi.BASE_URL}:SESSION_ID")






