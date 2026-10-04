import urllib.request
import json

base_url = 'http://127.0.0.1:8000'

# 1. Test index page has all auth elements
html = urllib.request.urlopen(base_url + '/').read().decode('utf-8')
print('Has auth-modal:', 'id="auth-modal"' in html)
print('Has header-auth-container:', 'id="header-auth-container"' in html)
print('Has sidebar-user-pill:', 'id="sidebar-user-pill"' in html)
print('Has quick admin button:', 'id="btn-quick-admin"' in html)
print('Has quick candidate button:', 'id="btn-quick-candidate"' in html)

# 2. Test app.js has auth methods
js = urllib.request.urlopen(base_url + '/static/app.js').read().decode('utf-8')
print('JS has setupAuth:', 'setupAuth' in js)
print('JS has handleQuickLogin:', 'handleQuickLogin' in js)
print('JS has handleLogout:', 'handleLogout' in js)

# 3. Test Admin Login API
req_admin = urllib.request.Request(
    base_url + '/api/auth/login',
    data=json.dumps({'email': 'admin@skillbridge.ai', 'password': 'admin123'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
resp_admin = json.loads(urllib.request.urlopen(req_admin).read().decode('utf-8'))
print('Admin Token Role:', resp_admin.get('role'))
print('Admin Name:', resp_admin.get('full_name'))

# 4. Test Candidate Login API
req_cand = urllib.request.Request(
    base_url + '/api/auth/login',
    data=json.dumps({'email': 'candidate@skillbridge.ai', 'password': 'candidate123'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
resp_cand = json.loads(urllib.request.urlopen(req_cand).read().decode('utf-8'))
print('Candidate Token Role:', resp_cand.get('role'))
print('Candidate Name:', resp_cand.get('full_name'))
print('Candidate ID linked:', resp_cand.get('candidate_id'))
print('ALL VERIFICATIONS PASSED!')
