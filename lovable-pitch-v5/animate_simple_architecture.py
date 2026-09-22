from pathlib import Path
import importlib.util
from PIL import Image, ImageDraw

ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('drawing', ROOT/'generate_diagrams.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
c=m.Canvas('GenAI Data Explorer | System Architecture','Proposed design')
c.rect(70,160,330,150,stroke=m.ORANGE)
c.icon(100,185,'person')
c.text(163,181,'User',32,True)
c.text(100,248,'Business / DevOps',25)
c.text(422,190,'Question',22,color=m.ORANGE)
c.arrow(400,240,600,240)

c.rect(600,160,1260,120)
c.icon(630,180,'shield');c.text(690,173,'API Layer',30,True)
c.text(630,230,'Authentication & role-based access  •  Question validation',26)
c.arrow(1230,280,1230,325)

c.rect(600,325,1260,300)
c.icon(630,344,'chip');c.text(690,338,'Query Orchestration Layer',30,True)
c.chip(630,400,550,'Approved schema & business context','database')
c.chip(1260,400,570,'LLM: Natural language → SQL')
c.arrow(1180,431,1260,431)
c.text(1280,473,'Result-bounded read-only query generation',22,color=m.MUTED)
c.arrow(1550,499,1550,530)
c.chip(1260,530,570,'SQL syntax & policy validation','shield')
c.rect(630,530,550,82,fill=m.BG)
c.icon(644,546,'person')
c.text(700,539,'Human review & approval',22)
c.text(700,577,'(Only when configured review thresholds are exceeded)',16,color=m.MUTED)
c.arrow(1260,561,1180,561)
c.arrow(900,625,900,685)

c.rect(600,685,1260,140)
c.icon(630,706,'database');c.text(690,700,'Data & Audit Layer',30,True)
c.text(630,765,'Read-only query execution  •  Audit log',26)
c.arrow(1230,825,1230,870)

c.rect(600,870,1260,125)
c.icon(630,891,'chat');c.text(690,885,'Response Layer',30,True)
c.text(630,945,'Authorised results',26)
c.line([(600,933),(235,933),(235,335)],m.BLUE)
c.arrow(235,335,235,310,m.BLUE)
c.text(280,785,'Authorised results',23,True,color=m.BLUE)
c.text(280,825,'returned to the user',22,color=m.MUTED)
c.text(160,1030,'AI-powered intelligence accelerates operations within controlled boundaries.',28,True)
c.save('01-system-architecture')

# Animate a moving highlight over the complete diagram; preserve every label.
# Frames remain full diagrams, making the GIF readable at any point in its loop.
stages=[
    ((70,160,400,310),[(400,240),(600,240)]),
    ((600,160,1860,280),[(1230,280),(1230,325)]),
    ((630,400,1180,462),[(1180,431),(1260,431)]),
    ((1260,400,1830,505),[(1550,499),(1550,530)]),
    ((1260,530,1830,592),[(1260,561),(1180,561)]),
    ((630,530,1180,612),[(900,612),(900,685)]),
    ((600,685,1860,825),[(1230,825),(1230,870)]),
    ((600,870,1860,995),[(600,933),(235,933),(235,310)]),
    ((70,160,400,310),[]),
]
frames=[]
for box,path in stages:
    for step in range(10):
        frame=c.im.copy();d=ImageDraw.Draw(frame)
        d.rounded_rectangle(box,radius=16,outline=m.ORANGE,width=5)
        if len(path)>1:
            lengths=[abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(path,path[1:])]
            distance=sum(lengths)*step/9
            for a,b,length in zip(path,path[1:],lengths):
                if distance<=length:
                    t=distance/length;x=a[0]+t*(b[0]-a[0]);y=a[1]+t*(b[1]-a[1])
                    d.ellipse((x-9,y-9,x+9,y+9),fill=m.ORANGE)
                    break
                distance-=length
        frames.append(frame.resize((1600,900),Image.Resampling.LANCZOS))
frames.extend([c.im.resize((1600,900),Image.Resampling.LANCZOS)]*15)
frames[0].save(ROOT/'assets/01-system-architecture-animated.gif',save_all=True,append_images=frames[1:],duration=160,loop=0,optimize=True,disposal=2)
print('Updated PNG, SVG and animated GIF. Runtime:',len(frames)*.16,'seconds')
