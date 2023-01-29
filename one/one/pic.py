
from fileinput import filename
from flask import *  
app = Flask(__name__)  
  
@app.route('/')  
def main():  
    return render_template("./index.html")  
  
@app.route('/out', methods = ['POST'])  
def out():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        return render_template("out.html", name = f.filename) 
  
if __name__ == '__main__':  
    app.run(debug=True)