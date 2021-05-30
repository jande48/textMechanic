from flask import Flask, flash, render_template, request
import json
# here is where you probably want to import you pyUSB methods

app=Flask(__name__)

@app.route('/')
def home():
    app.route('/')
    return render_template("index.html")

@app.route('/addPrefixSuffix',methods=['POST','GET'])
def addPrefixSuffix():
    if request.method == "GET":
        return render_template("addPrefixSuffix.html")
    
    else:

        # response1 is a string (i.e. text) from the first text box
        prefix = request.form['Prefix']
        suffix = request.form['Suffix']
        original = request.form['Original']
        splitLinesString = original.splitlines()
        
        out = []
        for i in splitLinesString:
            out.append(prefix+i+suffix)
    
        outFormmatted = '\n'.join(out)
        message = 'Your text was successfully formatted'
        return render_template("addPrefixSuffix.html", message=message, json=outFormmatted, original=original, prefix=prefix, suffix=suffix)


@app.route('/removeLineBreaks',methods=['POST','GET'])
def removeLineBreaks():
    if request.method == "GET":
        return render_template("removeLineBreaks.html")
    
    else:
        original = request.form['Original']
        splitLinesString = original.splitlines()
        
        out = []
        for i in splitLinesString:
            out.append(i)
    
        outFormmatted = ''.join(out)
        message = 'Your text was successfully formatted'
        return render_template("removeLineBreaks.html", message=message, json=outFormmatted, original=original)

@app.route('/removeLineNumbering',methods=['POST','GET'])
def removeLineNumbering():
    if request.method == "GET":
        return render_template("removeLineNumbering.html")
    
    else:
        original = request.form['Original']
        splitLinesString = original.splitlines()
        
        out = []
        for i in splitLinesString:
            iSplit = i.split()
            #print(iSplit)
            iSplitCat = ' '.join(iSplit[1:])
            print(iSplitCat)
            out.append(iSplitCat+'\n')
    
        outFormmatted = ''.join(out)
        message = 'Your text was successfully formatted'
        return render_template("removeLineNumbering.html", message=message, json=outFormmatted, original=original)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')