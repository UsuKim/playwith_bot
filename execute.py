import datetime
from datetime import timedelta

today = datetime.datetime.today()
tomorrow = today + timedelta(days=1)
t = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0) - today
h = t.seconds // 3600
m = (t.seconds % 3600) // 60
s = t.seconds % 60
print(h, m, s)