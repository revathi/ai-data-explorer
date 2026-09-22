from pathlib import Path
from html import escape
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)
BG, PANEL, BORDER = '#0D1230', '#171F43', '#38456D'
WHITE, MUTED, ORANGE = '#F5F7FF', '#C2CBE2', '#FF7900'
GREEN, RED, BLUE = '#61DEAA', '#FF8C9A', '#71C9FF'

class Canvas:
    def __init__(self, title, subtitle):
        self.im = Image.new('RGB', (1920,1080), BG)
        self.d = ImageDraw.Draw(self.im)
        self.s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">', f'<rect width="1920" height="1080" fill="{BG}"/>']
        self.text(60,30,title,40,True)
        self.text(60,88,subtitle,22,color=MUTED)
    def text(self,x,y,t,size=23,bold=False,color=WHITE):
        font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',size)
        self.d.text((x,y),t,font=font,fill=color)
        self.s.append(f'<text x="{x}" y="{y+size}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(t)}</text>')
    def rect(self,x,y,w,h,fill=PANEL,stroke=BORDER,r=16):
        self.d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=2)
        self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    def line(self,pts,color=ORANGE,width=3):
        self.d.line(pts,fill=color,width=width)
        self.s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
    def ellipse(self,x,y,w,h,color):
        self.d.ellipse((x,y,x+w,y+h),outline=color,width=3)
        self.s.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="none" stroke="{color}" stroke-width="3"/>')
    def arrow(self,x,y,a,b,color=ORANGE):
        self.line([(x,y),(a,b)],color)
        ang=math.atan2(b-y,a-x)
        self.line([(a-12*math.cos(ang-.5),b-12*math.sin(ang-.5)),(a,b),(a-12*math.cos(ang+.5),b-12*math.sin(ang+.5))],color)
    def icon(self,x,y,kind,color=ORANGE):
        if kind=='database':
            self.ellipse(x,y,36,12,color);self.line([(x,y+6),(x,y+34)],color);self.line([(x+36,y+6),(x+36,y+34)],color);self.ellipse(x,y+28,36,12,color)
        elif kind=='shield':
            self.line([(x+18,y),(x+36,y+8),(x+32,y+27),(x+18,y+40),(x+4,y+27),(x,y+8),(x+18,y)],color)
            self.line([(x+9,y+19),(x+16,y+26),(x+28,y+12)],color)
        elif kind=='person':
            self.ellipse(x+10,y,16,16,color);self.line([(x,y+39),(x+3,y+25),(x+18,y+21),(x+33,y+25),(x+36,y+39)],color)
        elif kind=='chat':
            self.rect(x,y,38,30,fill=PANEL,stroke=color,r=6);self.line([(x+10,y+30),(x+10,y+40),(x+22,y+30)],color)
        elif kind=='cross':
            self.ellipse(x,y,40,40,color);self.line([(x+12,y+12),(x+28,y+28)],color);self.line([(x+12,y+28),(x+28,y+12)],color)
        elif kind=='check':
            self.ellipse(x,y,40,40,color);self.line([(x+9,y+21),(x+18,y+29),(x+31,y+12)],color)
        else:
            self.rect(x+3,y+3,32,32,stroke=color,r=5)
            for k in (10,26):
                self.line([(x+k,y-3),(x+k,y+3)],color);self.line([(x+k,y+35),(x+k,y+41)],color)
                self.line([(x-3,y+k),(x+3,y+k)],color);self.line([(x+35,y+k),(x+41,y+k)],color)
    def chip(self,x,y,w,label,kind='chip'):
        self.rect(x,y,w,62,fill=BG)
        self.icon(x+14,y+11,kind)
        self.text(x+70,y+14,label,22)
    def save(self,name):
        self.im.save(OUT/f'{name}.png')
        (OUT/f'{name}.svg').write_text('\n'.join(self.s+['</svg>']),encoding='utf-8')

c=Canvas('GenAI Data Explorer | System Architecture','Proposed design  •  Plain-English questions to controlled database access')
c.rect(60,150,1260,120)
c.icon(85,168,'shield');c.text(143,163,'API Layer',27,True)
c.text(90,214,'Authentication & role-based access    •    Question validation    •    Question endpoint',23)
c.arrow(690,270,690,300)
c.rect(60,300,1260,340)
c.icon(85,320,'chip');c.text(143,315,'Query Orchestration Layer',28,True)
c.chip(85,378,580,'Authorised schema & business context','database')
c.chip(715,378,580,'LLM: Natural language → SQL')
c.arrow(665,409,715,409)
c.chip(715,465,580,'SQL syntax & policy validation','shield')
c.arrow(1005,440,1005,465)
c.chip(85,465,580,'Human review & approval','person');c.arrow(715,496,665,496)
c.chip(85,552,580,'Read-only SQL execution','shield');c.arrow(375,527,375,552)
c.text(715,565,'Recheck permissions and exact approved SQL',22,color=MUTED)
c.arrow(375,614,375,715)
c.rect(610,652,710,39,fill=BG,stroke=ORANGE,r=8)
c.text(628,656,'Validated & authorised execution boundary',22,True,color=ORANGE)
c.rect(60,715,1260,120)
c.icon(85,734,'database');c.text(143,729,'Data & Audit Layer',27,True)
c.text(90,779,'Production read replica    •    Private database connection    •    Near-real-time freshness',23)
c.arrow(690,835,690,870)
c.rect(60,870,1260,140)
c.icon(85,890,'chat');c.text(143,886,'Answer Layer',27,True)
c.text(90,947,'Query results  →  LLM: Results → plain-English answer  →  User',25)
c.rect(1400,150,460,305,stroke=BLUE)
c.icon(1427,176,'chip',BLUE);c.text(1485,170,'Approved Model',27,True)
c.text(1427,232,'Replaceable model adapter',24)
for i,t in enumerate(['Call 1: schema + question → SQL','Call 2: authorised result → answer','No database execution by the LLM']): c.text(1427,285+i*45,t,21,color=MUTED)
c.arrow(1320,409,1400,409,BLUE)
c.line([(1370,970),(1370,435),(1400,435)],BLUE);c.arrow(1320,970,1370,970,BLUE)
c.rect(1400,505,460,275,stroke=ORANGE)
c.icon(1427,530,'shield');c.text(1485,525,'Approval State & Audit',25,True)
for i,t in enumerate(['Question, SQL and verified role','Validation and review decisions','Execution time, status and scope','Persistent, access-controlled store']): c.text(1427,590+i*39,t,21,color=MUTED)
c.arrow(1320,605,1400,605)
c.rect(1400,825,460,185)
c.text(1427,845,'Two distinct boundaries',24,True)
for i,t in enumerate(['Execution: enforced query controls','Network: private database access','Model connection: separately approved']): c.text(1427,892+i*32,t,20,color=MUTED)
c.text(60,1030,'Audit records span the workflow. Human approval persists and resumes; changes require renewed validation and review.',21,color=MUTED)
c.save('01-system-architecture')

c=Canvas('Trust Boundaries | AI Autonomy, Controlled Execution','Proposed controls  •  The AI generates SQL; application controls determine what may execute')
cols=[(60,GREEN,'AI capabilities','check',[
    ('Generate SQL','Use approved schema and definitions'),
    ('Combine permitted data','Filter, join, sort and aggregate'),
    ('Explain results','Summarise authorised query results'),
    ('Continue the conversation','Clarify and refine business questions')]),
    (680,RED,'Execution restrictions','cross',[
    ('No database changes','Restricted read-only database account'),
    ('No unauthorised data access','Approved tables, columns and rows'),
    ('No unchecked execution','Validation and required approval'),
    ('No unbounded queries','Configured result limits and timeouts')]),
    (1300,BLUE,'Enforced controls','shield',[
    ('Verified identity and role','Company IAM + data access policies'),
    ('SQL syntax and policy checks','Validation enforced in application code'),
    ('Human review and approval','Exact SQL approved; access rechecked'),
    ('Traceability','Recorded decisions and executions')])]
for x,color,title,icon,rows in cols:
    c.rect(x,190,560,680,stroke=color)
    c.icon(x+28,223,icon,color);c.text(x+88,218,title,29,True,color)
    c.line([(x+28,285),(x+530,285)],color)
    for i,(heading,detail) in enumerate(rows):
        y=327+i*124
        c.text(x+30,y,heading,25,True);c.text(x+30,y+45,detail,21,color=MUTED)
c.rect(60,925,1800,95,stroke=ORANGE)
c.text(90,946,'Model instructions guide generation. Application and database controls enforce the boundaries.',29,True)
c.save('02-trust-boundaries')

c=Canvas('Portable by Design | Extensible by Choice','Proposed architecture  •  Stable workflow, replaceable integrations')
c.rect(60,175,1800,150,stroke=ORANGE)
c.icon(90,201,'chip');c.text(155,197,'Portable Application Core',32,True)
c.text(90,266,'API  •  Context retrieval  •  SQL generation  •  Validation  •  Human approval  •  Execution  •  Answers',27)
for x,title,kind,lines in [
    (60,'Model Adapter','chip',['Approved model endpoint','Evaluate when changing models']),
    (680,'Database Adapter','database',['Supported production replica','Test dialect and access policies']),
    (1300,'Platform Integrations','shield',['Identity, secrets and audit state','Configure for the target platform'])]:
    c.arrow(x+280,325,x+280,390)
    c.rect(x,390,560,205)
    c.icon(x+27,417,kind);c.text(x+85,411,title,29,True)
    for i,t in enumerate(lines): c.text(x+28,476+i*40,t,24,color=MUTED)
c.text(60,645,'Future extensions',30,True,color=ORANGE)
for x,title,kind,lines in [
    (60,'Schema RAG','database',['Retrieve relevant authorised metadata','Keep model context focused']),
    (680,'Controlled SQL Agent','chip',['Bounded query refinement','Repeat validation and approval']),
    (1300,'Business Predictions','chat',['Forecast demand and service risks','Evaluate with suitable historical data'])]:
    c.rect(x,707,560,210)
    c.icon(x+27,735,kind);c.text(x+85,729,title,28,True)
    for i,t in enumerate(lines): c.text(x+28,800+i*40,t,23,color=MUTED)
c.text(60,979,'Portability needs working adapters and testing. Future extensions retain the same access and execution controls.',26,color=MUTED)
c.save('03-portability-and-extensions')
print('Generated three PNG and three SVG diagrams in',OUT)
