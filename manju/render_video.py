from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import math, random, subprocess, wave
W,H,FPS,LENGTH = 480,854,18,32
OUT=Path(__file__).with_name("demo.mp4")
font_path=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"] if Path(p).exists()),"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
title_font=ImageFont.truetype(font_path,46)
caption_font=ImageFont.truetype(font_path,27)
small_font=ImageFont.truetype(font_path,19)
STORY=[
 (0,4,"千年星渊，正在苏醒。","city"),
 (4,8,"而他，终于听见命运的召唤。","hero"),
 (8,13,"苏璃：林澈，你真的要进去吗？","girl"),
 (13,17,"林澈：这一次，我不会再逃。","hero"),
 (17,22,"黑暗吞没高塔，星火划破长夜。","rift"),
 (22,28,"林澈：以星为刃，斩开黑夜！","battle"),
 (28,32,"《星渊觉醒》· 第一集 觉醒","end")]
COLORS={"city":((9,23,55),(41,28,91)),"hero":((11,24,58),(29,60,110)),"girl":((18,21,58),(79,37,101)),"rift":((17,17,43),(79,24,83)),"battle":((6,21,50),(32,36,89)),"end":((8,15,40),(36,23,77))}
R=random.Random(101)
STARS=[(R.randrange(W),R.randrange(620),R.randrange(1,3),R.random()*math.tau) for _ in range(110)]
def background(kind):
 a,b=COLORS[kind]; m=Image.new("RGB",(W,H));d=ImageDraw.Draw(m)
 for y in range(H):
  v=y/H;d.line((0,y,W,y),fill=tuple(int(a[j]*(1-v)+b[j]*v) for j in range(3)))
 return m.convert("RGBA")
BG={k:background(k) for k in COLORS}
def eyes(d,x,y,color):
 for xx in (x-22,x+23):
  d.ellipse((xx-13,y-5,xx+13,y+5),fill=(247,248,255,255))
  d.ellipse((xx-5,y-5,xx+5,y+5),fill=(*color,255))
  d.ellipse((xx-2,y-4,xx+2,y+4),fill=(19,35,67,255))
  d.line((xx-14,y-5,xx+13,y-5),fill=(13,24,48,255),width=3)
def hero(img,t,x=224,y=460,scale=1):
 layer=Image.new("RGBA",(W,H));d=ImageDraw.Draw(layer);s=scale
 X=lambda q:x+q*s
 Y=lambda q:y+q*s
 flap=math.sin(t*4)*10
 d.polygon([(X(-58),Y(48)),(X(-97+flap),Y(300)),(X(79+flap),Y(300)),(X(62),Y(48))],fill=(27,51,110,255))
 d.polygon([(X(-47),Y(56)),(X(-88+flap),Y(277)),(X(-14),Y(230))],fill=(40,86,161,255))
 d.polygon([(X(-58),Y(44)),(X(-75),Y(153)),(X(74),Y(153)),(X(57),Y(43))],fill=(19,31,60,255))
 d.polygon([(X(-41),Y(47)),(X(-7),Y(115)),(X(20),Y(47))],fill=(235,236,240,255))
 d.polygon([(X(-15),Y(70)),(X(7),Y(123)),(X(-3),Y(145)),(X(-25),Y(110))],fill=(72,191,255,255))
 d.polygon([(X(-18),Y(22)),(X(17),Y(22)),(X(13),Y(49)),(X(-14),Y(50))],fill=(211,168,147,255))
 d.ellipse((X(-42),Y(-58),X(42),Y(36)),fill=(235,194,166,255))
 d.polygon([(X(-47),Y(-19)),(X(-73),Y(-61)),(X(-29),Y(-55)),(X(-53),Y(-92)),(X(-7),Y(-77)),(X(3),Y(-105)),(X(24),Y(-77)),(X(55),Y(-87)),(X(43),Y(-38)),(X(56),Y(10)),(X(26),Y(-16)),(X(-9),Y(-19)),(X(-33),Y(2))],fill=(16,26,53,255))
 d.polygon([(X(-45),Y(-35)),(X(-25),Y(-68)),(X(1),Y(-75)),(X(-1),Y(-45))],fill=(41,68,122,255))
 eyes(d,X(0),Y(8),(110,201,255))
 d.line((X(-2),Y(29),X(9),Y(29)),fill=(135,84,100,255),width=2)
 d.line((X(52),Y(57),X(92),Y(127)),fill=(20,30,54,255),width=20)
 d.line((X(92),Y(127),X(129),Y(77)),fill=(225,180,150,255),width=13)
 bend=math.sin(t*2)*8
 d.polygon([(X(128),Y(78)),(X(147+bend),Y(-180)),(X(158+bend),Y(-190)),(X(149),Y(80))],fill=(130,214,255,255))
 d.line((X(117),Y(78),X(158),Y(89)),fill=(218,187,105,255),width=6)
 return Image.alpha_composite(img,layer)
def girl(img,t,x=241,y=445):
 layer=Image.new("RGBA",(W,H));d=ImageDraw.Draw(layer);sway=math.sin(t*3)*14
 d.polygon([(x-44,y-50),(x-87+sway,y+270),(x+91+sway,y+270),(x+39,y-50)],fill=(218,227,249,255))
 d.polygon([(x-54,y+67),(x-104+sway,y+261),(x+95+sway,y+261),(x+51,y+63)],fill=(81,87,152,255))
 d.polygon([(x-53,y+86),(x-84+sway,y+259),(x-2,y+245)],fill=(142,147,214,255))
 d.ellipse((x-47,y-101,x+45,y+25),fill=(218,229,253,255))
 d.ellipse((x-36,y-61,x+35,y+23),fill=(243,200,182,255))
 d.polygon([(x-50,y-49),(x-55,y-115),(x+2,y-140),(x+56,y-87),(x+43,y-11),(x+21,y-72),(x-13,y-78)],fill=(225,237,253,255))
 d.polygon([(x+34,y-86),(x+70+sway,y+92),(x+45,y+228),(x+25,y+27)],fill=(217,228,250,255))
 eyes(d,x,y-12,(159,126,249))
 return Image.alpha_composite(img,layer)
def frame(t,ix):
 start,end,caption,kind=STORY[ix];v=(t-start)/(end-start)
 img=BG[kind].copy();d=ImageDraw.Draw(img,"RGBA")
 for sx,sy,size,phase in STARS:
  x=(sx+int(t*7*size))%W;y=(sy+int(18*math.sin(t*.6+phase)))%690
  a=int(100+100*(.5+.5*math.sin(t*2+phase)))
  d.ellipse((x,y,x+size,y+size),fill=(195,213,255,a))
 d.ellipse((313,112,431,231),fill=(176,211,255,43))
 d.ellipse((330,129,413,212),fill=(221,235,255,95))
 d.polygon([(0,618),(81,506),(190,612),(315,472),(W,658),(W,H),(0,H)],fill=(9,23,60,189))
 d.polygon([(0,705),(91,620),(197,702),(342,574),(W,711),(W,H),(0,H)],fill=(11,19,48,255))
 if kind in ("city","rift","end"):
  for k in range(10):
   xx=k*55+(k%3)*8;top=505+(k*79)%135
   d.polygon([(xx-12,750),(xx-12,top+20),(xx+7,top-22),(xx+27,top+20),(xx+27,750)],fill=(9,14,40,255))
   for wy in range(top+39,690,40):d.rectangle((xx,wy,xx+9,wy+14),fill=(103,136,251,102))
 if kind in ("city","rift","battle"):
  cx=250+int(13*math.sin(t*.6));cy=250;r=80+int(17*math.sin(t*2))
  for j in range(5):
   rad=r+j*10
   d.arc((cx-rad,cy-rad*1.6,cx+rad,cy+rad*1.6),start=25+j*29+int(t*35),end=295+j*29+int(t*35),fill=(100+j*19,125+j*8,255,207-j*28),width=5)
 if kind=="hero":img=hero(img,t,x=213,y=488,scale=1.27)
 elif kind=="girl":img=girl(img,t)
 elif kind=="battle":
  img=hero(img,t,x=208,y=499,scale=1.09+.05*math.sin(t*4))
  d=ImageDraw.Draw(img,"RGBA")
  for k in range(24):
   a=k*math.tau/24+t*2
   d.line((W/2,H*.5,W/2+210*math.cos(a),H*.5+345*math.sin(a)),fill=(131,201,255,65+(k%4)*17),width=1+k%3)
 elif kind=="end":img=hero(img,t,x=315,y=580,scale=.7)
 d=ImageDraw.Draw(img,"RGBA")
 for k in range(10):
  x=(k*53+t*(26+k*6))%W;y=215+(k*109)%420
  d.line((x-20,y,x+20,y-2),fill=(127,180,255,39),width=1)
 if kind=="end":
  d.rounded_rectangle((21,230,459,395),radius=18,fill=(10,17,45,226))
  d.text((W/2,265),"星 渊 觉 醒",anchor="mt",font=title_font,fill=(234,241,255,255))
  d.text((W/2,337),"第一集 · 觉醒",anchor="mt",font=caption_font,fill=(166,214,255,255))
 d.rounded_rectangle((18,25,178,67),radius=10,fill=(6,12,30,180))
 d.text((34,34),"星渊觉醒",font=small_font,fill=(217,234,255,255))
 d.rounded_rectangle((18,695,462,789),radius=16,fill=(5,9,23,226))
 chunks=[caption[k:k+16] for k in range(0,len(caption),16)]
 for k,c in enumerate(chunks[:2]):d.text((W/2,714+35*k),c,anchor="mt",font=caption_font,fill=(249,250,255,255))
 d.text((W/2,812),"原创动态国漫分镜样片 · 非 AI 视频模型",anchor="mt",font=small_font,fill=(182,196,220,255))
 return img.convert("RGB")
def make_music(path):
 sr=24000;t=np.arange(sr*LENGTH,dtype=np.float32)/sr;music=np.zeros(len(t),dtype=np.float32)
 chords=[(220,261.63,329.63),(196,246.94,293.66),(174.61,220,261.63),(164.81,196,246.94)]
 for k in range(0,LENGTH,2):
  z=t-k;mask=(z>=0)&(z<2);v=z[mask];env=np.minimum(1,v*6)*np.exp(-v*.7)
  tone=np.zeros(len(v),dtype=np.float32)
  for f in chords[(k//2)%4]:tone+=.05*np.sin(math.tau*f*v)+.022*np.sin(math.tau*f*v/2)
  music[mask]+=tone*env+.11*np.exp(-8*v)*np.sin(math.tau*68*v)
 music+=.012*np.sin(math.tau*47*t)*np.sin(math.tau*.21*t)
 music+=.028*np.sin(math.tau*(450+3*np.maximum(0,t-19)**2)*t)*(t>=19)*(t<28)
 pcm=(np.tanh(music*1.7)*.65*32767).astype("<i2")
 with wave.open(str(path),"wb") as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
def main():
 wav=OUT.with_name("temp-music.wav");make_music(wav)
 cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",str(wav),"-c:v","libx264","-preset","veryfast","-crf","27","-pix_fmt","yuv420p","-c:a","aac","-b:a","72k","-shortest","-movflags","+faststart",str(OUT)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(FPS*LENGTH):
   now=i/FPS
   idx=next((j for j,(a,b,_,_) in enumerate(STORY) if a<=now<b),len(STORY)-1)
   p.stdin.write(frame(now,idx).tobytes())
 finally:p.stdin.close()
 result=p.wait();wav.unlink(missing_ok=True)
 if result:raise RuntimeError("Render failed: "+str(result))
 print("Success",OUT,OUT.stat().st_size)
if __name__=="__main__":main()
