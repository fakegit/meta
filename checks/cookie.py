def check(cookie):
	if 'HttpOnly' not in cookie:
		return 'Cookie can be accessed by JS.'
	if 'secure' not in cookie:
		return 'Cookie can be sent over an unencrypted HTTP connection.'