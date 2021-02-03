from flask import Flask, render_template, request, redirect, flash, session
import requests, random
from flask_mysqldb import MySQL
app=Flask(__name__)
app.secret_key='man'
app.config['MYSQL_USER'] = 'sql12384556'
app.config['MYSQL_PASSWORD'] = 'QNJIsufXGi'
app.config['MYSQL_DB'] = 'sql12384556'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)
l={'0','1','2','3','4','5','6','7','8','9'}
k='' 
for i in random.sample(l, 4):
    k=k+i
print(k)
@app.route('/',methods=['POST','GET'])
def index():
    session.pop('otp1',None)
    session.pop('otp',None)
    session.pop('nam',None)
    session.pop('us',None)
    session.pop('no',None)
    if request.method=='POST':
        if request.form.get("lin"):
            return redirect('/login')
        elif request.form.get("sup"):
            return redirect('/signup') 
        elif request.form.get("adim"):
            return redirect('/alog')
    else:
        return render_template('home.html')
@app.route('/signup',methods=['POST','GET'])
def sup():
    if request.method=='POST':
        nam = request.form['nam']
        no = request.form['mob']
        us = request.form['unam']
        session['nam']=nam
        session['no']=no
        session['us']=us
        s=0
        if request.form.get("ck"):
            us = request.form['unam']
            d=1
            values = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            for i in us:
                if i not in values:
                    d=0
            if us.split()==[] or len(us.split())>1 or d==0:
                flash("Input a valid username!","info")
                session.pop('us',None)
                return redirect('/signup')                
            else:
                cur=mysql.connection.cursor()
                cur.execute("select * from user where unam like %s",(us,))
                mysql.connection.commit()
                r=cur.fetchall()
                if len(r)==0 :
                    s=1
                    flash(f"You can continue with your username: {us}","info")
                    return redirect('/signup')
                if s==0:
                    flash("try with another username","info")
                    session.pop('us',None)
                    return redirect('/signup')
                
            
        if request.form.get("bkk"):
            session.pop('nam',None)
            session.pop('us',None)
            session.pop('no',None)
            return redirect('/')
        if request.form.get("lg"):
            session.pop('nam',None)
            session.pop('us',None)
            session.pop('no',None)
            return redirect('/login')
        
        elif request.form.get("se"):
            nam = request.form['nam']
            no = request.form['mob']
            pp = request.form['pas']
            cpp = request.form['cpas']
            us = request.form['unam']
            if us.split()==[] or len(us.split())>1:
                flash("Input a valid username!","info")
                session.pop('us',None)
                return redirect('/signup')                
            else:
                cur=mysql.connection.cursor()
                cur.execute("select * from user where unam like %s",(us,))
                mysql.connection.commit()
                r=cur.fetchall()
                if len(r)==0:
                    s=1
                if s==1 and pp==cpp:
                    s=2
                if s==0:
                    session.pop('us',None)
                    flash("Try with another username","info")
                    return redirect('/signup')
                elif s==1:
                    flash("Wrong confirm password","info")
                    return redirect('/signup')
                elif s==2 and set(nam)!={' '} and set(pp)!={' '} and len(no)==10:
                    cur=mysql.connection.cursor()
                    cur.execute("insert into user values(%s,%s,%s,%s)",(nam,no,us,pp))
                    mysql.connection.commit()
                    session['co']=0
                    session.pop('nam',None)
                    session.pop('us',None)
                    session.pop('no',None)
                    return redirect('/login')
    else:
        return render_template('signup.html')
    
@app.route('/login',methods=['POST','GET'])
def lin():
    if 'co' in session:
        flash("Successful signup continue to login","info")
        session.pop('co',None)
    if request.method=='POST':
        if request.form.get("bkk"):
            return redirect('/')
        elif request.form.get("se"):
            us = request.form['unam']
            pp = request.form['pas']
            oot=k
            session['otp']=oot
            cur=mysql.connection.cursor()
            cur.execute("select * from user where unam like %s",(us,))
            mysql.connection.commit()
            r=cur.fetchall()
            if  len(r)!=0:
                o=r[0]['Number']
                na=r[0]['Name']
                msg=f'OTP is {oot}'
                url='https://www.fast2sms.com/dev/bulk'
                para={'authorization':'Bpvi8RswfETPal7UeFS1hzXIHD0VqQYkobuNG4ZLCOAd932WnxwSbFxRr2jMau6cHGYCtUpNsfnW4Vok',
                          'sender_id':'FSTSMS',
                          'message':msg,
                          'language':'english',
                          'route':'p',
                          'numbers':o}
                req=requests.get(url,params=para)
                dic=req.json()
                p=dic.get('return')
                cur.execute("insert into SMS_API values (%s,%s,%s,%s)",(na,o,msg,p))
                mysql.connection.commit()
            if  len(r)==0:
                flash("Username not registered","info")
                return redirect('/login')
            elif  pp==r[0]['pass']:
                return redirect('/otp3')
            elif pp!=r[0]['pass']:
                flash("Wrong password","info")
                return redirect('/login')
    else:
        return render_template('login.html')
    
@app.route('/form',methods=['POST','GET'])
def amp():
    if 'otp' in session:
        if request.method=='POST':
            if request.form.get("lg"):
                session.pop('otp',None)
                return redirect('/')
            elif request.form.get("sen"):
                na = request.form['nam']
                msg = request.form['sms']
                no = request.form['no']
                url='https://www.fast2sms.com/dev/bulk'
                para={'authorization':'Bpvi8RswfETPal7UeFS1hzXIHD0VqQYkobuNG4ZLCOAd932WnxwSbFxRr2jMau6cHGYCtUpNsfnW4Vok',
                          'sender_id':'FSTSMS',
                          'message':msg+f'      -by {na}',
                          'language':'english',
                          'route':'p',
                          'numbers':no}
                req=requests.get(url,params=para)
                dic=req.json()
                p=dic.get('return')
                cur=mysql.connection.cursor()
                cur.execute("insert into SMS_API values (%s,%s,%s,%s)",(na,no,msg,p))
                mysql.connection.commit()
                if p ==True:
                    flash("Last massages was successfully sent","info")
                    return redirect('/form')
                else:
                    flash("somthing went wrong","info")
                    return redirect('/form')
        else:
            return render_template('form.html')
    else:
        return redirect('/')
    
@app.route('/alog',methods=['POST','GET'])
def adimlog():
    if request.method=='POST':
        if request.form.get("li"):
            usn = request.form['un']
            pas = request.form['pass']
            mno = '9479557075'
            oot=k
            session['otp1']=oot
            msg=f'OTP is {oot}'
            url='https://www.fast2sms.com/dev/bulk'
            para={'authorization':'Bpvi8RswfETPal7UeFS1hzXIHD0VqQYkobuNG4ZLCOAd932WnxwSbFxRr2jMau6cHGYCtUpNsfnW4Vok',
                      'sender_id':'FSTSMS',
                      'message':msg,
                      'language':'english',
                      'route':'p',
                      'numbers':mno}
            req=requests.get(url,params=para)
            dic=req.json()
            p=dic.get('return')
            cur=mysql.connection.cursor()
            cur.execute("insert into SMS_API values ('admin',%s,%s,%s)",(mno,msg,p))
            mysql.connection.commit()
            if usn=='himreal9' and pas=='12345' and p==True:
                return redirect('/otp1')
            else:
                flash("Wrong Credentials","info")
                return redirect('/alog')
        if request.form.get("lo"):
            return redirect('/')
    else:
        return render_template('adminlog.html')

@app.route('/otp1',methods=['POST','GET'])
def ottp2():
    if 'otp1' in session:
        if request.method=='POST':
            o = request.form['otp']
            if  o==session['otp1']:
                return redirect('/adinp1')
            else:
                flash("Wrong OTP","info")
                return redirect('/otp1')
        else:
            return render_template('otp.html')
    else:
        return redirect('/')
    
@app.route('/adinp1',methods=['POST','GET'])
def p1():
    if 'otp1' in session:
        if request.method=='POST':
            if request.form.get("uu"):
                return redirect('/p2')
            elif request.form.get("sh"):
                return redirect('/p3') 
            elif request.form.get("lg"):
                session.pop('otp1',None)
                return redirect('/')
        else:
            return render_template('adminp1.html')
    else:
        return redirect('/')

@app.route('/p2',methods=['POST','GET'])
def p2():
    if 'otp1' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from user")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['Name','Number','Username']
        l1=[]
        for i in r:
            l=[i['Name'],i['Number'],i['unam']]
            l1.append(l)
        if request.method=='POST':
            if request.form.get("dl"):
                us = request.form['unam']
                cur=mysql.connection.cursor()
                cur.execute("delete from user where unam like %s",(us,))
                mysql.connection.commit()
                flash(f"Successfully deleted user: {us}")
                return redirect('/p2')
            elif request.form.get("bkk"):
                return redirect('/adinp1') 
            elif request.form.get("lg"):
                session.pop('otp1',None)
                return redirect('/')  
        else:
            return render_template('p2.html',h=h,l1=l1)
    else:
        return redirect('/')

@app.route('/p3',methods=['POST','GET'])
def p3():
    if 'otp1' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from SMS_API")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['Name' , 'Number', 'SMS', 'Status']
        l1=[]
        for i in r:
            l=list(i.values())
            l1.append(l)
        if request.method=='POST':
            if request.form.get("dl"):
                cur=mysql.connection.cursor()
                cur.execute("delete from SMS_API")
                mysql.connection.commit()
                flash("Successfully deleted all messages")
                return redirect('/p3')
            if request.form.get("df"):
                cur=mysql.connection.cursor()
                cur.execute("delete from SMS_API where success is False")
                mysql.connection.commit()
                flash("Successfully deleted failed messages")

                return redirect('/p3')
            if request.form.get("dt"):
                cur=mysql.connection.cursor()
                cur.execute("delete from SMS_API where success is True")
                mysql.connection.commit()
                flash("Successfully deleted success messages")
                return redirect('/p3')
            elif request.form.get("bkk"):
                return redirect('/adinp1') 
            elif request.form.get("lg"):
                session.pop('otp1',None)
                return redirect('/')        
        else:
            return render_template('p3.html',h=h,l1=l1)
    else:
        return redirect('/')
    
@app.route('/otp3',methods=['POST','GET'])
def ottp():
    if 'otp' in session:
        if request.method=='POST':
            o = request.form['otp']
            if  o==session['otp']:
                return redirect('/form')
            else:
                flash("Wrong OTP","info")
                return redirect('/otp3')
        else:
            return render_template('otp.html')
    else:
        return redirect('/')

@app.route('/about')
def abt():
    session.pop('otp1',None)
    session.pop('otp',None)
    session.pop('nam',None)
    session.pop('us',None)
    session.pop('no',None)
    return render_template('abt.html')

@app.route('/ct')
def ct():
    session.pop('otp1',None)
    session.pop('otp',None)
    session.pop('nam',None)
    session.pop('us',None)
    session.pop('no',None)
    return render_template('cont.html')

if __name__=='__main__':
    app.run()