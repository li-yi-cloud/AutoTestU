'''
Created on 2018年8月3日

@author: cloud
'''
import jinja2

login_email = jinja2.Template('''
email: '{{email}}'
passwd: '{{passwd}}'
''')

sign_email = jinja2.Template('''
email: '{{email}}'
passwd: '{{passwd}}'
name: '{{name}}'
gender: '{{gender}}'
''')

match_perf = jinja2.Template('''
match_time_seconds: {{match_time_seconds}}
report: null
''')

match_perf_report = jinja2.Template('''
Account: '{{Account}}'
UserID: '{{UserID}}'
Identity: '{{Identity}}'
ClientMatchGender: '{{Gender}}'
ClientMatchRegion: '{{Region}}'
RequestTimes: null
MatchResult: 0
VideoResult: 0
ChannelID: null
MatchedUserID: null
''')

server_url = jinja2.Template("{{server}}/admin/match/getMatchInfo?userId={{UserID}}&matchedUserId={{MatchedUserID}}")

update_channel_url = jinja2.Template("{{server}}/admin/users/updateUserChannel")

