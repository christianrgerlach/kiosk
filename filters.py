from app import app
from datetime import datetime

@app.template_filter()
def format_time(date_time):
	return date_time.strftime('%H:%M %b %d')

@app.template_filter()
def time_since(date_time):
	sec_since = (datetime.now() - date_time).total_seconds()
	m, s = divmod(sec_since, 60)
	h, m = divmod(m, 60)
	return '%d:%02d:%02d' % (h, m, s)
