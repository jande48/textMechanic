from flask import Flask, flash, render_template, request
import json
# import flask WT forms
from flask_wtf import FlaskForm
from wtforms import FileField

# import flask uploads
from flask_uploads import configure_uploads, UploadSet
# here is where you probably want to import you pyUSB methods

app=Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthedevelopmentsecretkey'
app.config['UPLOADS_DEFAULT_DEST'] = 'textFiles/'

textFiles = UploadSet('uploads')
configure_uploads(app, textFiles)

class MyForm(FlaskForm):
    textUpload = FileField('text')

@app.route('/')
def home():
    app.route('/')
    return render_template("index.html")

@app.route('/addPrefixSuffix',methods=['POST','GET'])
def addPrefixSuffix():
    form = MyForm()
    if request.method == "GET":
        
        # If there a get request, just return the html template
        return render_template("addPrefixSuffix.html", form=form)
    
    else:
        # if there's a POST request sending data, then get the data
        prefix = request.form['Prefix']
        suffix = request.form['Suffix']
        original = request.form['Original']
        out = []

        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./uploads/textFiles/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            # loop through each line
            for i in splitLinesString:
                # add the prefix and suffix to each line
                out.append(prefix+i[:-1]+suffix) 
        else: 
            splitLinesString = original.splitlines()
            # loop through each line
            for i in splitLinesString:
                # add the prefix and suffix to each line
                out.append(prefix+i+suffix)
        

        
    
        # join each line into one string separated by \n so HTML makes a new line
        outFormmatted = '\n'.join(out)

        #outputTextFile = open("MyFile.txt","a")
        message = 'Prefixes/Suffixes were Successfully Added'
        # using Jinja return the data to the template
        return render_template("addPrefixSuffix.html", message=message, json=outFormmatted, original=original, prefix=prefix, suffix=suffix, form=form)


@app.route('/removeLineBreaks',methods=['POST','GET'])
def removeLineBreaks():
    # If there a get request, just return the html template
    if request.method == "GET":
        return render_template("removeLineBreaks.html")

    # if there's a POST request sending data, then get the data
    else:
        original = request.form['Original']

        # split the original text into an array for each line
        splitLinesString = original.splitlines()
        
        # create a blank 'out' array
        out = []

        # loop through each line and add it to out
        for i in splitLinesString:
            out.append(i)
    
        # create a single string without any line breaks
        outFormmatted = ' '.join(out)
        message = 'Line Breaks were Successfully Removed'
        # using Jinja return the data to the template
        return render_template("removeLineBreaks.html", message=message, json=outFormmatted, original=original)

@app.route('/removeLineNumbering',methods=['POST','GET'])
def removeLineNumbering():
    # If there a get request, just return the html template
    if request.method == "GET":
        return render_template("removeLineNumbering.html")

    # if there's a POST request sending data, then get the data
    else:
        original = request.form['Original']
        # split the original text into an array for each line
        splitLinesString = original.splitlines()
        
        # create a blank 'out' array
        out = []

        # loop through each line
        for i in splitLinesString:
            # split each line based on spaces
            iSplit = i.split()

            # concatenate each line, but remove everything before the first space
            iSplitCat = ' '.join(iSplit[1:])
            # join them back together added a new line at the end
            out.append(iSplitCat+'\n')
    
        # create a single string without any line breaks
        outFormmatted = ''.join(out)

        

        message = 'Line Numbers were Successfully Removed'
        # using Jinja return the data to the template
        return render_template("removeLineNumbering.html", message=message, json=outFormmatted, original=original)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')