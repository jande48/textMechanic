from flask import Flask,  render_template, request, send_file
import json, random, os
# import flask WT forms
from flask_wtf import FlaskForm
from wtforms import FileField

# import flask uploads
from flask_uploads import configure_uploads, UploadSet


app=Flask(__name__)

# The secret key to prevent cross-domain attacks. For production, 
# we can choose a strong key and place it as a hidden environment variable
app.config['SECRET_KEY'] = 'thisisthedevelopmentsecretkey'

# Define the location of the text files
app.config['UPLOADS_DEFAULT_DEST'] = 'textFiles/'

# Define the location of download text files
app.config['DOWNLOAD_FOLDER'] = 'textFiles/downloads/'

# Define the location of upload text files
textFiles = UploadSet('uploads')
configure_uploads(app, textFiles)

# Use flask WT Forms to create file field form.  This may seem confusing
# because we are defining the other forms with HTML, but by giving this class
# to each of our routes, it makes it easy to accept a file
class MyForm(FlaskForm):
    textUpload = FileField('text')

# Create a route to download the chosen text file
@app.route('/downloads/<path>', methods=['GET', 'POST'])
def download(path):
    newPath = 'textFiles\\downloads\\'+path
    return send_file(newPath, as_attachment=True)

@app.route('/')
def home():
    app.route('/')
    return render_template("index.html")

@app.route('/addPrefixSuffix',methods=['POST','GET'])
def addPrefixSuffix():

    # define form as an instance of the WT forms class
    form = MyForm()

    if request.method == "GET":
        # If there a get request, just return the html template
        return render_template("addPrefixSuffix.html", form=form)

    # if there's a POST request sending data, then get the data
    else:
        prefix = request.form['Prefix']
        suffix = request.form['Suffix']
        original = request.form['Original']
        out = []

        # if theres an attached file, then open it and read lines
        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            # loop through each line
            for i in splitLinesString:
                # add the prefix and suffix to each line
                # for files, don't read the last two character [:-1] because they are /n
                out.append(prefix+i[:-1]+suffix) 
        
        # else use the form text
        else: 
            splitLinesString = original.splitlines()
            # loop through each line
            for i in splitLinesString:
                # add the prefix and suffix to each line
                out.append(prefix+i+suffix)
        
        # join each line into one string separated by \n so HTML makes a new line
        outFormmatted = '\n'.join(out)
        
        # create a random number for a download file
        randomNum = random.randint(0,999)
        outputTextFile = open("./textFiles/downloads/"+str(randomNum)+".txt","w")
        
        # write the data to this file
        for i in outFormmatted:
            outputTextFile.writelines(i)
        outputTextFile.close()
        message = 'Prefixes/Suffixes were Successfully Added'

        # using Jinja return the data to the template
        return render_template("addPrefixSuffix.html", message=message, json=outFormmatted, original=original, prefix=prefix, suffix=suffix, form=form, randomNum=randomNum)


@app.route('/removeLineBreaks',methods=['POST','GET'])
def removeLineBreaks():
    form = MyForm()
    # If there a get request, just return the html template
    if request.method == "GET":
        return render_template("removeLineBreaks.html",form=form)

    # if there's a POST request sending data, then get the data
    else:
        original = request.form['Original']
        
        # create a blank 'out' array
        out = []
        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            # loop through each line
            for i in splitLinesString:
                # add the prefix and suffix to each line
                out.append(i[:-1]) 
        else: 
            # loop through each line and add it to out
            splitLinesString = original.splitlines()
            for i in splitLinesString:
                out.append(i)
    
        # create a single string without any line breaks
        outFormmatted = ' '.join(out)
        randomNum = random.randint(0,999)
        outputTextFile = open("./textFiles/downloads/"+str(randomNum)+".txt","w")
        for i in outFormmatted:
            outputTextFile.writelines(i)
        outputTextFile.close()
        message = 'Line Breaks were Successfully Removed'
        # using Jinja return the data to the template
        return render_template("removeLineBreaks.html", message=message, json=outFormmatted, original=original, form=form, randomNum=randomNum)

@app.route('/removeLineNumbering',methods=['POST','GET'])
def removeLineNumbering():
    form = MyForm()
    # If there a get request, just return the html template
    if request.method == "GET":
        return render_template("removeLineNumbering.html",form=form)

    # if there's a POST request sending data, then get the data
    else:
        original = request.form['Original']
        # split the original text into an array for each line

        out = []

        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            # loop through each line
            for i in splitLinesString:
                iSplit = i.split()
                # concatenate each line, but remove everything before the first space
                iSplitCat = ' '.join(iSplit[1:])
                # join them back together added a new line at the end
                out.append(iSplitCat+'\n')
        else: 
            # loop through each line
            splitLinesString = original.splitlines()
            for i in splitLinesString:
                # split each line based on spaces
                iSplit = i.split()

                # concatenate each line, but remove everything before the first space
                iSplitCat = ' '.join(iSplit[1:])
                # join them back together added a new line at the end
                out.append(iSplitCat+'\n')
    
        # create a single string without any line breaks
        outFormmatted = ''.join(out)
        randomNum = random.randint(0,999)
        outputTextFile = open("./textFiles/downloads/"+str(randomNum)+".txt","w")
        for i in outFormmatted:
            outputTextFile.writelines(i)
        outputTextFile.close()
    
        message = 'Line Numbers were Successfully Removed'
        # using Jinja return the data to the template
        return render_template("removeLineNumbering.html", message=message, json=outFormmatted, original=original, form=form, randomNum=randomNum)


@app.route('/findReplace',methods=['POST','GET'])
def findReplace():
    form = MyForm()
    if request.method == "GET":
        
        # If there a get request, just return the html template
        return render_template("findReplace.html", form=form)
    
    else:
        # if there's a POST request sending data, then get the data
        find = request.form['Find']
        replace = request.form['Replace']
        original = request.form['Original']
        out = []

        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            # loop through each line
            for i in splitLinesString:

                # add the prefix and suffix to each line
                outReplaced = i[:-1].replace(find,replace)
                out.append(outReplaced)
        else: 
            splitLinesString = original.splitlines()
            # loop through each line
            for i in splitLinesString:
                # add the prefix and suffix to each line
                outReplaced = i.replace(find,replace)
                out.append(outReplaced)

        # join each line into one string separated by \n so HTML makes a new line
        outFormmatted = '\n'.join(out)
        randomNum = random.randint(0,999)
        outputTextFile = open("./textFiles/downloads/"+str(randomNum)+".txt","w")
        for i in outFormmatted:
            outputTextFile.writelines(i)
        outputTextFile.close()
        message = 'Successfully Found and Replaced'
        # using Jinja return the data to the template
        return render_template("findReplace.html", message=message, json=outFormmatted, original=original, find=find, replace=replace, form=form, randomNum=randomNum)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')