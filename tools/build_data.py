import json, re
OUT='public/driverdecider/'
from PIL import Image, ImageStat
P='/mnt/project-files/car-comparison/photos/'
r=json.load(open('data/sheet-rows.json')); H=r['1']
rows=[dict(zip(H,r[k])) for k in sorted(r,key=int) if k!='1']
# generation groups: id, test, title, brand line, gen label, ext photo, int photo, slugs
G=[
 ('ilx',lambda x:x['Model']=='ILX','ILX','Acura','1st generation','acura-ilx','acura-ilx'),
 ('civic',lambda x:x['Model']=='Civic','Civic','Honda','9th generation','civic-9','civic-9'),
 ('accord',lambda x:x['Model']=='Accord','Accord','Honda','9th generation','accord-9','accord-9'),
 ('miata',lambda x:x['Model']=='Miata','Miata','Mazda','3rd generation (NC)','mazda-miata','mazda-miata'),
 ('mazda3s',lambda x:x['Model'].startswith('Mazda3') and x['Body style']=='Sedan','Mazda3 Sedan','Mazda','3rd generation','mazda3-bm-sedan','mazda3-bm'),
 ('mazda3h',lambda x:x['Model'].startswith('Mazda3') and x['Body style']=='Hatchback','Mazda3 Hatchback','Mazda','3rd generation','mazda3-bm','mazda3-bm'),
 ('mazda6',lambda x:x['Model']=='Mazda6','Mazda6','Mazda','3rd generation','mazda6-gj','mazda6-gj'),
 ('cooper',lambda x:x['Model']=='Cooper','Cooper','MINI','2nd generation','mini-r56','mini-r56'),
 ('coopers',lambda x:x['Model']=='Cooper S','Cooper S','MINI','2nd generation','mini-r56-s','mini-r56-s'),
 ('im',lambda x:x['Model']=='iM','iM','Scion','1st generation','scion-im','scion-im'),
 ('impreza4',lambda x:x['Model']=='Impreza' and x['Description'].startswith('4th'),'Impreza','Subaru','4th generation','impreza-4','impreza-4'),
 ('impreza5',lambda x:x['Model']=='Impreza' and x['Description'].startswith('5th'),'Impreza','Subaru','5th generation','impreza-5','impreza-5'),
 ('legacy',lambda x:x['Model']=='Legacy','Legacy','Subaru','6th generation','legacy-6','legacy-6'),
 ('yaris',lambda x:x['Model']=='Yaris','Yaris','Toyota','3rd generation','yaris-xp130','yaris-xp130'),
 ('corolla10',lambda x:x['Model']=='Corolla' and x['Description'].startswith('10th'),'Corolla','Toyota','10th generation','corolla-e140','corolla-e140'),
 ('corolla11',lambda x:x['Model']=='Corolla' and x['Description'].startswith('11th'),'Corolla','Toyota','11th generation','corolla-e170','corolla-e170'),
 ('prius',lambda x:x['Model']=='Prius','Prius','Toyota','3rd generation','prius-xw30','prius-xw30'),
 ('priusc',lambda x:x['Model']=='Prius C','Prius c','Toyota','1st generation','prius-c','prius-c'),
 ('beetle',lambda x:x['Model']=='Beetle','Beetle','Volkswagen','3rd generation','vw-beetle-a5','vw-beetle-a5'),
 ('jetta',lambda x:x['Model'].startswith('Jetta'),'Jetta','Volkswagen','6th generation','jetta-a6fl','jetta-6'),
 ('passat',lambda x:x['Model']=='Passat','Passat','Volkswagen','7th generation','passat-nms-fl','passat-nms'),
 ('golf',lambda x:x['Model'].startswith('Golf'),'Golf','Volkswagen','7th generation (Mk7)','golf-mk7','golf-mk7'),
]
SL={ # make slug, model slug for CR/RepairPal/KBB/Autotrader/Edmunds ; IIHS slug ; NHTSA model
 'ilx':('acura','ilx','acura/ilx-4-door-sedan','ILX'),'civic':('honda','civic','honda/civic-4-door-sedan','CIVIC'),
 'accord':('honda','accord','honda/accord-4-door-sedan','ACCORD'),'miata':('mazda','mx-5-miata',None,'MX-5'),
 'mazda3s':('mazda','mazda3','mazda/3-4-door-sedan','3'),'mazda3h':('mazda','mazda3','mazda/3-4-door-hatchback','3'),
 'mazda6':('mazda','mazda6','mazda/6-4-door-sedan','6'),'cooper':('mini','cooper','mini/cooper-2-door-hatchback','COOPER'),
 'coopers':('mini','cooper','mini/cooper-2-door-hatchback','COOPER%2520S'),'im':('scion','im','scion/im-4-door-hatchback','IM'),
 'impreza4':('subaru','impreza','subaru/impreza-4-door-sedan','IMPREZA'),'impreza5':('subaru','impreza','subaru/impreza-4-door-sedan','IMPREZA'),
 'legacy':('subaru','legacy','subaru/legacy-4-door-sedan','LEGACY'),'yaris':('toyota','yaris','toyota/yaris-4-door-hatchback','YARIS'),
 'corolla10':('toyota','corolla','toyota/corolla-4-door-sedan','COROLLA'),'corolla11':('toyota','corolla','toyota/corolla-4-door-sedan','COROLLA'),
 'prius':('toyota','prius','toyota/prius-4-door-hatchback','PRIUS'),'priusc':('toyota','prius-c','toyota/prius-c-4-door-hatchback','PRIUS%2520C'),
 'beetle':('volkswagen','beetle','volkswagen/beetle-2-door-hatchback','BEETLE'),'jetta':('volkswagen','jetta','volkswagen/jetta-4-door-sedan','JETTA'),
 'passat':('volkswagen','passat','volkswagen/passat-4-door-sedan','PASSAT'),'golf':('volkswagen','golf','volkswagen/golf-4-door-hatchback','GOLF'),
}
KBBM={'cooper':'hardtop','coopers':'hardtop'}
creds=json.load(open(P+'credits.json'))
def clean(v):
    if isinstance(v,float) and v.is_integer(): return int(v)
    if v=='NA' or v is None: return v
    return v
def variant(x,g):
    m=x['Model']; t=''
    for b in ['Mazda3','Jetta','Golf']:
        if m.startswith(b): t=m[len(b):].strip()
    d=x['Description']
    if g=='golf' and '2-door' in d: t=(t+' ' if t else '')+('Launch Edition 2-door' if 'Launch' in d else 'Base 2-door')
    if g in('impreza4',) and x['Body style']!='Sedan or hatchback': t=x['Body style']
    return t
used=set(); out=[]
def photo(slug,kind,w):
    src=P+f'{slug}_{kind}.jpg'; dst=f'img/{slug}_{kind}.jpg'
    if dst not in used:
        im=Image.open(src).convert('RGB'); im.thumbnail((w,w*2)); im.save(OUT+dst,quality=80,optimize=True,progressive=True); used.add(dst)
    return dst
def tone(slug):
    im=Image.open(P+f'{slug}_ext.jpg').convert('RGB').resize((60,40))
    # dominant non-gray-ish color, darkened
    px=list(im.getdata()); px.sort(key=lambda p:-(max(p)-min(p)))
    top=px[:400]; c=[sum(p[i] for p in top)//len(top) for i in range(3)]
    k=0.32; return '#%02x%02x%02x'%tuple(int(v*k+12) for v in c)
taken=set()
for gid,test,title,brand,gen,ext,intr in G:
    rs=[x for x in rows if test(x)]; assert rs,gid
    for x in rs: taken.add(id(x))
    rs.sort(key=lambda x:(x['Year'],x['KBB private party $']))
    items=[]
    for x in rs:
        d={k:clean(v) for k,v in x.items()}; d['variant']=variant(x,gid); items.append(d)
    ms,mm,iihs,nh=SL[gid]
    out.append(dict(id=gid,title=title,brand=brand,gen=gen,ext=photo(ext,'ext',900),int=photo(intr,'int',900),tone=tone(ext),
        credExt=creds.get(ext+'_ext',''),credInt=creds.get(intr+'_int',''),make=ms,model=mm,kbbModel=KBBM.get(gid,mm),iihs=iihs,nhtsa=nh,rows=items))
left=[x['Model']+str(x['Year']) for x in rows if id(x) not in taken]; assert not left,left
open(OUT+'data.js','w').write('window.CARS='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
print(len(out),sum(len(g['rows']) for g in out))
for g in out: print(g['id'],g['tone'],[ (r['Year'],r['variant']) for r in g['rows']])
