from datetime import datetime,timedelta,timezone
import re,dateparser
RELATIVE=re.compile(r'^(?:about\s+)?(\d+)\s+(minute|minutes|hour|hours|day|days)\s+ago$',re.I)
def normalize_date(value,now=None):
    if not value:return None
    now=now or datetime.now(timezone.utc); text=' '.join(value.strip().split()); m=RELATIVE.match(text)
    if m:
        amount,unit=int(m.group(1)),m.group(2).lower()
        if unit.startswith('minute'):return now-timedelta(minutes=amount)
        if unit.startswith('hour'):return now-timedelta(hours=amount)
        return now-timedelta(days=amount)
    parsed=dateparser.parse(text,settings={'RETURN_AS_TIMEZONE_AWARE':True,'TO_TIMEZONE':'UTC'})
    return parsed.astimezone(timezone.utc) if parsed else None
def is_fresh_24h(dt,now=None):
    if dt is None:return False
    now=now or datetime.now(timezone.utc); age=now-dt.astimezone(timezone.utc)
    return timedelta(0)<=age<=timedelta(hours=24)
