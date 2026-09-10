from datetime import datetime,timezone
from src.dates import normalize_date,is_fresh_24h
def test_relative_hour():
    now=datetime(2026,9,10,12,tzinfo=timezone.utc)
    assert normalize_date('2 hours ago',now)==datetime(2026,9,10,10,tzinfo=timezone.utc)
def test_freshness():
    now=datetime(2026,9,10,12,tzinfo=timezone.utc)
    assert is_fresh_24h(datetime(2026,9,10,1,tzinfo=timezone.utc),now)
    assert not is_fresh_24h(datetime(2026,9,8,1,tzinfo=timezone.utc),now)
