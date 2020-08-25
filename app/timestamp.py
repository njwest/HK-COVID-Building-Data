from datetime import datetime
from pytz import timezone


class Timestamp(object):
    @staticmethod
    def get_hk_time():
        hong_kong = timezone('Asia/Hong_Kong')
        now = datetime.now(hong_kong)

        month_ary = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                     'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        month = month_ary[now.month + 1]

        time_dict = {
            'hours': now.hour,
            'minutes': now.minute,
            'day': now.day,
            'month': month,
            'year': now.year}
        return time_dict
