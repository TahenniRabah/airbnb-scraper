from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime.today()

next_month = today + relativedelta(months=1)
print(next_month)
