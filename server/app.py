from flask import Flask,  render_template, request, send_file
import json, random, os
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
    newPath = 'textFiles/downloads/'+path
    return send_file(newPath, as_attachment=True)

@app.route('/')
def home():
    app.route('/')
    return render_template("index.html")

@app.route('/addPrefixSuffix/clear',methods=['POST','GET'])
def addPrefixSuffixClear():
    form = MyForm()
    return render_template("addPrefixSuffix.html", form=form)
    
@app.route('/addPrefixSuffix',methods=['POST','GET'])
def addPrefixSuffix():

    # define form as an instance of the WT forms class
    form = MyForm()

    if request.method == "GET":
        # If there a get request, just return the html template
        return render_template("addPrefixSuffix.html", form=form)

    # if there's a POST request sending data, then get the data
    else:
        # if theres an attached file, then open it and read lines
        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            originalFromFile = "".join(splitLinesString)
            return render_template("addPrefixSuffix.html",original=originalFromFile,form=form)

        else: 
            prefix = request.form['Prefix']
            suffix = request.form['Suffix']
            original = request.form['Original']
            #print(original)
            out = []
        
            # else use the form text
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
        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            originalFromFile = "".join(splitLinesString)
            return render_template("removeLineBreaks.html",original=originalFromFile,form=form)

        else: 
            original = request.form['Original']
            # create a blank 'out' array
            out = []
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
        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            originalFromFile = "".join(splitLinesString)
            return render_template("removeLineNumbering.html",original=originalFromFile,form=form)

        else: 
            original = request.form['Original']
            # split the original text into an array for each line

            out = []
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
        if len(form.textUpload.data.filename) > 0:
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            originalFromFile = "".join(splitLinesString)
            return render_template("findReplace.html",original=originalFromFile,form=form)
        else:
        # if there's a POST request sending data, then get the data
            find = request.form['Find']
            replace = request.form['Replace']
            original = request.form['Original']
            out = []

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

@app.route('/removeDuplicateLines',methods=['POST','GET'])
def removeDuplicateLines():
    form = MyForm()
    # If there a get request, just return the html template
    if request.method == "GET":
        return render_template("removeDuplicateLines.html", form=form)
    # or for post requests:
    else:
        # check to see if there's an attached file
        if len(form.textUpload.data.filename) > 0:
            # if so, create text file in uploads and add the posted data from the user
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            originalFromFile = "".join(splitLinesString)
            # then return the text file in the 'original' text box
            return render_template("removeDuplicateLines.html",original=originalFromFile,form=form)
        else:
            # if there's no attached file, then take the data from the form boxes
            original = request.form['Original']
            out = []

            splitLinesString = original.splitlines()
            # loop through each line
            for i in splitLinesString:
                # check if the line is aleady in out, if not, then add it
                if i not in out:
                    out.append(i)

            # join each line into one string separated by \n so HTML makes a new line
            outFormmatted = '\n'.join(out)
            randomNum = random.randint(0,999)

            # create a text file of the formatted data, if the user would like to download
            outputTextFile = open("./textFiles/downloads/"+str(randomNum)+".txt","w")
            for i in outFormmatted:
                outputTextFile.writelines(i)
            outputTextFile.close()
            message = 'Successfully Removed Duplicate Lines'
            # using Jinja return the data to the template
            return render_template("removeDuplicateLines.html", message=message, json=outFormmatted, original=original, form=form, randomNum=randomNum)

@app.route('/removeDuplicateWords',methods=['POST','GET'])
def removeDuplicateWords():
    form = MyForm()
    # If there a get request, just return the html template
    if request.method == "GET":
        return render_template("removeDuplicateWords.html", form=form)
    # or for post requests:
    else:
        # check to see if there's an attached file
        if len(form.textUpload.data.filename) > 0:
            # if so, create text file in uploads and add the posted data from the user
            filename = textFiles.save(form.textUpload.data)
            f = open("./textFiles/uploads/"+filename, "r")
            splitLinesString = f.readlines()
            f.close()
            originalFromFile = "".join(splitLinesString)
            # then return the text file in the 'original' text box
            return render_template("removeDuplicateWords.html",original=originalFromFile,form=form)
        else:
            # if there's no attached file, then take the data from the form boxes
            original = request.form['Original']
            out = []
            outWords = []
            splitLinesString = original.splitlines()
            # loop through each line
            for i in splitLinesString:
                # split each line into each words
                outTemp = []
                splitLinesWords = i.split()

                # for each word, check if it's a dup
                for j in splitLinesWords:
                    if j not in outWords:
                        outWords.append(j)
                        outTemp.append(j)

                out.append(' '.join(outTemp))

            # join each line into one string separated by \n so HTML makes a new line
            outFormmatted = '\n'.join(out)
            randomNum = random.randint(0,999)

            # create a text file of the formatted data, if the user would like to download
            outputTextFile = open("./textFiles/downloads/"+str(randomNum)+".txt","w")
            for i in outFormmatted:
                outputTextFile.writelines(i)
            outputTextFile.close()
            message = 'Successfully Removed Duplicate Words'
            # using Jinja return the data to the template
            return render_template("removeDuplicateWords.html", message=message, json=outFormmatted, original=original, form=form, randomNum=randomNum)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')