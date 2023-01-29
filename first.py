from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
from email_validator import validate_email,EmailNotValidError

def check_username(user_name):
    con = sqlite3.connect('cse123.db')
    cur=con.cursor()
    cur.execute('select username from students where username=?',[user_name])
    nam=cur.fetchall()
    if len(nam)!=0:
        return True
    else:
        return False
def check_user(user_name,password):
    conn = sqlite3.connect('cse123.db')
    cur=conn.cursor()
    cur.execute("select username,enterpass  from students where username=? and enterpass=?",(user_name,password))
    data=cur.fetchall()
         
    if len(data)!=0:
        return True
    else:
        return False
def check_mail(mail):
    try:
        v=validate_email(mail)
        mail=v["email"]
        if 'gmail.com' in mail:
            return False
        elif 'acoe.edu.in' in mail:
            return False
        elif 'yahoo.com' in mail:
            return False
        return False
    except EmailNotValidError:
        return False


def check_mobile(mobile):
    if len(mobile)!=10:
        return True
    else:
        return False
       
app = Flask(__name__)
app.secret_key='hello'

@app.route('/')
def home():
    return render_template('nwp.html')
  
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=='POST':    
        user_name=request.form['n']
        pass_word=request.form['p']
        mail=request.form['gm']
        mobile=request.form['pn']
        f = request.files['img']
          
    
        conn = sqlite3.connect('cse123.db')
        conn.cursor()
        if check_username(user_name):
            return('username already exists , please try another username')
        elif check_mail(mail):
            return("incorrect email")
        elif check_mobile(mobile):
            return ('incorrect mobile number')
        
        f.save(f.filename)
        conn.execute("INSERT INTO students(username, email, enterpass,mobile) values(?,?,?,?)",(user_name,mail,pass_word,mobile))
        conn.commit()
        conn.close()
        return render_template('nlog.html')
    
    return render_template('nreg.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    
    return render_template('dashboard.html',name=session['user'])
       
@app.route('/login', methods=["GET","POST"])
def login():
    
    if request.method=='POST':  
        user_name=request.form['n']
        password=request.form['p']
       
        if check_user(user_name,password):
            session['user']=user_name
            return redirect(url_for('user'))
        else:
            return ('username or password is incorrect')
    else:
        if 'user' in session:
            return redirect(url_for('user'))
       
    return render_template('nlog.html')

@app.route('/user',methods=['GET','POST'])
def user():
    if 'user' in session:
        user=session['user']
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))    
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user',None)
    return redirect(url_for("login"))
if __name__ == '__main__':
    app.run(debug=True)