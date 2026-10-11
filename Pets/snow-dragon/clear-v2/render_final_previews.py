from pathlib import Path
from PIL import Image, ImageDraw
import subprocess
root=Path(__file__).parent
atlas=Image.open(root/'final/spritesheet-extended.png').convert('RGBA')
out=root/'qa/final-previews'; out.mkdir(exist_ok=True)
states=['idle','running-right','running-left','waving','jumping','failed','waiting','running','review']
counts=[6,8,8,4,5,8,6,6,6]
framesroot=out/'frames'; framesroot.mkdir(exist_ok=True)
allframes=[]
def cell(row,col):
 return atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
def previewframe(c,label):
 b=Image.new('RGB',(240,256),(234,232,241)); b.paste(c,(24,32),c); ImageDraw.Draw(b).text((10,8),label,fill=(30,25,45)); return b
def gif(frames,path,duration=160):
 frames[0].save(path,save_all=True,append_images=frames[1:],loop=0,duration=duration)
for row,(state,count) in enumerate(zip(states,counts)):
 d=framesroot/state; d.mkdir(exist_ok=True)
 fs=[]
 for col in range(count):
  c=cell(row,col); c.save(d/f'{col:02d}.png'); fs.append(previewframe(c,f'{state} {col+1}/{count}'))
 gif(fs,out/f'{state}.gif'); allframes+=fs
gif(allframes,out/'all-states.gif')
jumps=[cell(0,i) for i in range(6)]+[cell(4,i) for i in range(5)]+[cell(0,i) for i in range(6)]
gif(jumps,out/'idle-jump-idle.gif')
looks=[previewframe(cell(9+i//8,i%8),f'look {i*22.5:05.1f}') for i in range(16)]
gif(looks,out/'look-loop.gif')
for idx in [0,7,27,42]: allframes[idx].save(out/f'still-{idx:02d}.png')
seq=out/'video-frames'; seq.mkdir(exist_ok=True)
for i,f in enumerate(allframes): f.save(seq/f'{i:03d}.png')
subprocess.run(['ffmpeg','-y','-framerate','6','-i',str(seq/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(out/'all-states.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
print(out)
