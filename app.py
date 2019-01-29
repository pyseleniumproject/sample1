from flask import Flask,request,render_template,redirect,jsonify
from flask_mysqldb import MySQL
from sqlalchemy import create_engine,Table,Column, Integer, String, MetaData,select
from sqlalchemy.engine import reflection 
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os

#UPLOAD_FOLDER = '/static/images/'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
app.secret_key='random'
engine = create_engine("mysql://root:@localhost/myfirst")
con=engine.connect()
meta = MetaData()
meta.reflect(bind=engine)
emp = meta.tables['emp']
@app.route('/')
def index():
    return render_template('sample.html')
@app.route('/sample',methods=['post'])
def sample():
    name=request.form['nm']
    age=request.form['age']
    ide=request.form['id']
    fil=request.files['file']
    btn=request.form['submit']
    if btn=='save':
        b=insert(name,age,fil)
        return render_template('sample.html')
   
    elif btn=='update':
        up=update(ide,name,age,fil)
        return render_template('sample.html')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def insert(name,age,fil):
    if fil and allowed_file(fil.filename):
            filename = secure_filename(fil.filename)
            fil.save(os.path.join(app.config['UPLOAD_FOLDER'],'static/images/', filename))
            ins = emp.insert().values(name=name,age=age,file=filename)
            a=con.execute(ins)
            return a
@app.route('/view')
def view():
    sel=select([emp])
    result=con.execute(sel)
    #return jsonify(resul=result)
    return render_template('view.html',resul=result)
def update(ide,name,age,fil):
    if fil and allowed_file(fil.filename):
            filename = secure_filename(fil.filename)
            fil.save(os.path.join(app.config['UPLOAD_FOLDER'],'static/images/', filename))
            up=emp.update().values(name=name,age=age,file=filename).where(emp.c.id==ide)
            res=con.execute(up)
            return res
@app.route('/edit')
def edit():
    id=request.args.get('id')
    sel=select([emp.c.id,emp.c.name,emp.c.age,emp.c.file]).where(emp.c.id==id)
    result=con.execute(sel)
    return render_template('update.html',resul=result)
@app.route('/delete')
def dele():
    id=request.args.get('id')
    delet=emp.delete().where(emp.c.id==id)
    con.execute(delet)
    return render_template('sample.html')

@app.route('/deta',methods=['POST'])
def deta():
    id=request.form['id']
    print(id)
    sel=select([emp.c.id,emp.c.name,emp.c.age,emp.c.file]).where(emp.c.id==id)
    result=con.execute(sel)
    res=[dict(r) for r in result]
    print(res)
    return jsonify(res)

    # Ceate a blade file - for loop
    # x  render_template('abc.html', reultres)
# return x

    #{'result': [dict(row) for row in result]}
    #return 'result'
    #return jsonify({'output': result})
    #return json.dumps({"result":result})
