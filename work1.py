import matplotlib.pyplot as plt
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from PIL import Image,ImageTk
import webbrowser
       
def openn():
    global name
    name=askopenfilename(title='选择一个文件',defaultextension='.txt')
    if name=='':
        name=None
    else:
        root.title("屁桃文本编辑器:"+os.path.basename(name))
        textpad.delete(1.0,END)
        text=open(name,'r')
        textpad.insert(1.0,text.read())
        text.close()

def new():
    global name
    root.title('屁桃文本编辑器:未命名.txt')
    name = None
    textpad.delete(1.0,END)
    
def save():
    global name
    try:
        f=open(name,'w')
        m=textpad.get(1.0,END)
        f.write(m)
        f.close()
    except:
        save_as()

def save_as():
    save_name=asksaveasfilename(initialfile='未命名.txt',defaultextension='.txt')
    global name
    name=save_name
    fh=open(save_name,'w')
    m=textpad.get(1.0,END)
    fh.write(m)
    fh.close()
    root.title("屁桃文本编辑器:"+os.path.basename(save_name))
    
def num():
    string0=str(textpad.get(1.0,END))
    lenth=len(string0)
    for i in string0:
        if i==' ':
            lenth-=1
    showinfo('字符数统计','共计字符（含空格）'+str(len(string0))+'个\n共计字符（不含空格）'+str(lenth)+'个')
    
def word_num():
    string0=str(textpad.get(1.0,END))
    string=string0.lower()
    for i in string:
        a=ord(i)
        if a<97 or a>122:
            if i!=' ' and i!="'" and i!='-':
                string=string.replace(i,'')
    lis=string.split()
    showinfo('词数统计','共计单词'+str(len(lis))+'个')
    
def frequency():
    global name
    string0=str(textpad.get(1.0,END))
    string=string0.lower()
    for i in string:
        a=ord(i)
        if a<97 or a>122:
            if i!=' ' and i!="'" and i!='-':
                string=string.replace(i,'')
    lis=string.split()
    good_words=[]
    s0=set(lis)
    stoplist=open('stop_words.txt','r')
    stopstring=stoplist.read()
    list_stop=stopstring.split('\n')
    for i in s0:
        if i not in list_stop:
            good_words.append([i,lis.count(i)])
    good_words0=good_words
    sorted_words=[]
    for i in range(len(good_words)):
        k=0
        max_index=0
        for j in range(len(good_words0)):
            if good_words0[j][1]>k:
                k=good_words0[j][1]
                max_index=j
        sorted_words.append(good_words0[max_index])
        good_words0.pop(max_index)
    b=Toplevel()
    b.geometry('450x500')
    b.title('词频统计')
    plot_x=[]
    plot_y=[]
    s=''
    for i in range(min(len(sorted_words),10)):
        plot_x.append('('+str(i+1)+')')
        plot_y.append(sorted_words[i][1])
        s+='('+str(i+1)+')'+sorted_words[i][0]+'  词频:'+str(sorted_words[i][1])+'\n'
    plt.bar(plot_x,plot_y,color='lightcoral')
    plt.title('Word Frequency Statistics')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.savefig(name+'.png')
    plt.show()
    la=Label(b,text=s).place(x=180,y=300)
    im=Image.open(name+'.png')
    photo=ImageTk.PhotoImage(im)
    img=Label(b,image=photo)
    img.image=photo
    img.place(x=0,y=0)

def keywords():
    string0=str(textpad.get(1.0,END))
    string=string0.lower()
    for i in string:
        a=ord(i)
        if a<97 or a>122:
            if i!=' ' and i!="'" and i!='-':
                string=string.replace(i,'')
    lis=string.split()   
    good_words=[]
    s0=set(lis)
    stoplist=open('stop_words.txt','r')
    stopstring=stoplist.read()
    list_stop=stopstring.split('\n')
    for i in s0:
        if i not in list_stop:
            good_words.append([i,lis.count(i)])
    good_words0=good_words
    sorted_words=[]
    for i in range(len(good_words)):
        k=0
        max_index=0
        for j in range(len(good_words0)):
            if good_words0[j][1]>k:
                k=good_words0[j][1]
                max_index=j
        if good_words0[max_index][1]>1:
            sorted_words.append(good_words0[max_index][0])
        good_words0.pop(max_index)
    nuum=askstring('关键词','请输入关键词数(关键词仅为词频大于等于2的词语)',initialvalue='范围1~'+str(len(sorted_words)))
    if nuum!=None:
        try:
            if int(nuum)>len(sorted_words) or int(nuum)<1:
                showerror('错误','关键词数范围1~'+str(len(sorted_words)))
            else:
                s=''
                for i in range(int(nuum)):
                    s+=('('+str(i+1)+')'+sorted_words[i]+'\n')
                showinfo('关键词',s)
        except:
            showerror('错误','请输入关键词数')
        
def search():
    string0=str(textpad.get(1.0,END)).lower()
    check=askstring('查找','输入查找内容',initialvalue=None)
    if check!=None:
        n=0
        for i in range(len(string0)-len(check)+1):
            if check==string0[i:i+len(check)]:
                n+=1
        showinfo('查找结果',check+'共出现'+str(n)+'次\n(仅为查找字符同时出现的次数，并非单词出现次数)')
    
def replace():
    string0=str(textpad.get(1.0,END))
    l=list(string0.split())
    origin=askstring('替换','输入要替换的单词',initialvalue='请输入小写字母')
    if origin!=None:
        new_word=askstring('替换','替换成',initialvalue='请输入小写字母')
        if new_word!=None:
            for i in range(len(l)):
                if l[i].lower()==origin:
                    if l[i].upper()==l[i]:
                        l[i]=new_word.upper()
                    elif l[i][0].upper()==l[i][0]:
                        l[i]=new_word[0].upper()+new_word[1:]
                    else:
                        l[i]=new_word
    string=''
    for i in l:
        string+=i+' '
    textpad.delete(1.0,END)
    textpad.insert(1.0,string)

def cursor1(event):
    textpad.config(cursor='arrow')
    
def cursor2(event):
    textpad.config(cursor='xterm')
  
def link(event):
    webbrowser.open('http://www.taobao.com')
    
def hyperlink():
    textpad.tag_add('link',1.0,1.1)
    textpad.tag_config('link',foreground='coral',underline=True)
    textpad.tag_bind('link','<Enter>',cursor1)
    textpad.tag_bind('link','<Leave>',cursor2)
    textpad.tag_bind('link','<Button-1>',link)

name=''
root=Tk()
root.title("屁桃文本编辑器")
root.geometry('800x700')

#工具栏
tool=Frame(root,height=30,bg='peachpuff')
photo=PhotoImage(file='peach.gif')
peach=Label(tool,image=photo,width=25,height=25)
peach.pack(side=LEFT,padx=5,pady=5)
p=0
c=[openn,save,word_num,frequency,keywords,hyperlink]
for item in ['打开','保存','词数统计','词频','关键词','添加超链接']:
    button=Button(tool,text=item,command=c[p],bg='snow')
    button.pack(side=LEFT,padx=5,pady=5)
    p+=1
tool.pack(expand=NO,fill=X)

#文本框
textpad = Text(root, undo=True)
textpad.pack(expand=YES, fill=BOTH)

#菜单
menubar=Menu(root)
root.config(menu=menubar)
c1=[openn,new,save,save_as]
menu1=Menu(menubar,tearoff=0)
i=0
for item in ['打开','新建','保存','另存为']:
    menu1.add_command(label=item,command=c1[i])
    menu1.add_separator()
    i+=1
menubar.add_cascade(label='文件',menu=menu1)

c2=[num,word_num,frequency,keywords]
menu2=Menu(menubar,tearoff=0)
j=0
for item in ['字符数','词数','词频','关键词']:
    menu2.add_command(label=item,command=c2[j])
    menu2.add_separator()
    j+=1
menubar.add_cascade(label='统计',menu=menu2)

c3=[replace,search,hyperlink]
menu3=Menu(menubar,tearoff=0)
k=0
for item in ['替换','查找','添加超链接']:
    menu3.add_command(label=item,command=c3[k])
    menu3.add_separator()
    k+=1
menubar.add_cascade(label='编辑',menu=menu3)

#滚动条
s=Scrollbar(textpad)
textpad.config(yscrollcommand=s.set,bg='snow',fg='saddlebrown')
s.config(command=textpad.yview)
s.pack(side=RIGHT,fill=Y)

#状态栏
status=Label(root,text='今天也要加油鸭!',bd=1,relief=SUNKEN,bg='peachpuff')
status.pack(side=BOTTOM,fill=X)

root.mainloop()