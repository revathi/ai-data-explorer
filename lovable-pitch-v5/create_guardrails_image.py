from pathlib import Path

ROOT = Path(__file__).parent
# Reuse only the drawing definitions, without regenerating existing diagrams.
scope = {'__file__': str(ROOT/'generate_diagrams.py')}
source = (ROOT/'generate_diagrams.py').read_text(encoding='utf-8').split('\nc=Canvas(',1)[0]
exec(compile(source, str(ROOT/'generate_diagrams.py'), 'exec'), scope)
Canvas=scope['Canvas']
c=Canvas('Human Oversight & Guardrails','Proposed policy  •  Every query is validated; only exceptional queries require human approval')
columns=[
 (60,'#61DEAA','Automatic path','check',[
   ('Generate read-only SQL','Use approved schema and business context'),
   ('Validate every query','Check syntax, access and permitted operations'),
   ('Execute within policy','Enforce row limits, timeouts and permissions'),
   ('Return authorised results','Record the query and execution outcome')]),
 (680,'#FF8C9A','Blocked by guardrails','cross',[
   ('No database changes','Block INSERT, UPDATE, DELETE and DROP'),
   ('No unauthorised access','Enforce permitted tables, columns and rows'),
   ('No unchecked execution','Reject invalid SQL and failed policy checks'),
   ('No hard-limit bypass','Human approval cannot override restrictions')]),
 (1300,'#71C9FF','Human review for\nexceptional queries','person',[
   ('1. Pause the query','Estimated cost or complexity exceeds\nthe configured review threshold'),
   ('2. Show the reviewer the details','Business question, generated SQL\nand the reason for review'),
   ('3. Approve, revise or reject','Revised queries must pass validation again'),
   ('4. Execute after approval','Recheck permissions and record the decision')])
]
for x,color,title,icon,rows in columns:
    c.rect(x,180,560,710,stroke=color)
    c.icon(x+255,208,icon,color)
    if '\n' in title:
        for j,line in enumerate(title.split('\n')):
            c.text(x+26,254+j*31,line,26,True,color)
    else:
        c.text(x+26,270,title,28,True,color)
    c.line([(x+28,327),(x+530,327)],color)
    for i,(heading,detail) in enumerate(rows):
        y=365+i*119
        c.icon(x+25,y+3,'shield' if x==680 else ('person' if x==1300 else 'check'),color)
        c.text(x+81,y,heading,24,True)
        for j,line in enumerate(detail.split('\n')):
            c.text(x+28,y+43+j*27,line,20,color=scope['MUTED'])
c.rect(60,937,1800,84,stroke=scope['ORANGE'])
c.text(105,957,'Routine queries run automatically. Exceptional queries require approval. Unsafe queries are blocked.',27,True)
c.save('04-human-oversight-and-guardrails')
print(ROOT/'assets/04-human-oversight-and-guardrails.png')
