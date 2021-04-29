from flask import Flask, render_template, url_for, request, redirect, current_app, send_file, Response
from datetime import datetime
from werkzeug.utils import secure_filename
from config import *
import os
from os import listdir
from os.path import isfile, join
import cv2
from cascadeDetection import NoteRecognize
from livereload import Server
from werkzeug.datastructures import ImmutableMultiDict
import urllib.parse
import threading
from pdf2image import convert_from_path
from wand.image import Image as PDFImg
from wand.color import Color
import copy
from PIL import Image
from PyPDF2 import PdfFileMerger
import time
from flask_wtf import FlaskForm
from wtforms import SelectField
import os
import json

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

sheetIndicator = 0
single = False
sheetC = 0
x = 0
unitPlus = 0
paths = []
resultPaths = []
downloadPaths = []
# Sheet Details
detailSheets = []


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('./index.html')


def generate():
    global x
    print("process", x)
    yield "data:" + str(x) + "\n\n"


@app.route('/progress')
def progress():
    return Response(generate(), mimetype='text/event-stream')


def generateLast():
    global paths, x
    par = (x/len(paths) ) * 100
    yield "data:" + str(par) + "\n\n"


@app.route('/lastNote')
def LastNote():
    return Response(generateLast(), mimetype='text/event-stream')


@app.route('/sheet', methods=['POST', 'GET'])
def Sheet():
    print("Upload")
    return render_template('./Sheet.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    print("Upload kub")
    global sheetIndicator, paths, single, sheetC
    fileType = ""
    if request.method == 'POST':
        print("FIle ", request.files)
        imd = request.files
        files = imd.to_dict(flat=False)['file']
        if len(files) < 2:
            fileType = files[0].filename.split('.')[-1]
        if fileType == "pdf":
            process_pdf(files[0])
        else:
            fFiles(files)
        print("Paths in upload", single)
        data = {
            'singleOrNot': single,
            'path': paths,
            'ind': sheetIndicator,
            'resultPaths': resultPaths,
            'downloadPaths': downloadPaths
        }
        return render_template('/Sheet.html', imgData=data)
    return ''


def process_pdf(file):
    pdf_d = "./static/img/pdf/one.pdf"
    file.save(pdf_d)
    prepare_images(pdf_d)


def prepare_images(pdf_path):
    # Output dir
    output_dir = ('./static/img/temSheet/')
    global paths, single

    with (PDFImg(filename=pdf_path, resolution=300, width=600)) as source:
        images = source.sequence
        pages = len(images)
        if pages > 1:
            single = False
        for i in range(pages):
            images[i].background_color = Color(
                'white')  # Set white background.
            images[i].alpha_channel = 'remove'
            PDFImg(images[i]).save(filename=output_dir + str(i) + '.png')
            path = "./img/temSheet/" + str(i) + ".png"
            paths.append(path)
            print("Writing paths kub", paths)
        threadMain()


#12.528131008148193
def fFiles(files):
    global single, sheetC
    fileName = 0
    if len(files) > 1:
        for file in files:
            WriteImg(file, fileName)
            fileName += 1
            sheetC += 1
        fileName = 0
        single = False
    else:
        fileName = 0
        file = files[0]
        sheetC = 1
        WriteImg(file, fileName)
    threadMain()


def threadMain():
    global downloadPaths, x, unitPlus
    unitPlus = round(100 / len(paths), 2)
    img = "./img/resultSheet/" + str(sheetIndicator) + ".png"
    recognizedImg = NoteRecognize("./static/" + paths[0])
    cv2.imwrite("./static/" + img[1:], recognizedImg)
    pdfPath = './static/img/resultPDF/' + str(sheetIndicator) + ".pdf"
    imgPdf = Image.open("./static/" + img)
    imgPdf = imgPdf.convert('RGB')
    imgPdf.save(pdfPath, save_all=True)
    x += 1
    downloadPaths.append(pdfPath)
    resultPaths.append(img[1:])
    if len(paths) > 1:
        procMore = threading.Thread(target=ProcessThread, args=(paths, ))
        procMore.start()
    else:
        allPath = "./static/img/resultPDF/all.pdf"
        imgPdf.save(allPath, save_all=True)


def ProcessThread(paths):
    global sheetC, resultPaths, downloadPaths, x
    start = sheetIndicator + 1
    print("Processing ")
    nPath = copy.copy(paths)
    nPath.pop(0)
    last = 0
    for sheet in nPath:
        img = "./static/" + sheet[1:]
        recImg = NoteRecognize(img)
        pdfPath = './static/img/resultPDF/' + str(start) + ".pdf"
        img = "./static/img/resultSheet/" + str(start) + ".png"
        cv2.imwrite(img, recImg)
        imgPdf = Image.open(img)
        imgPdf = imgPdf.convert('RGB')
        imgPdf.save(pdfPath, save_all=True)
        pdf = './static/img/resultPDF/' + str(start) + ".pdf"
        img = Image.open(img)
        img = img.convert('RGB')
        img.save(pdf, save_all=True)
        downloadPaths.append(pdf)
        img = "./img/resultSheet/" + str(start) + ".png"
        resultPaths.append(img)
        x += 1
        start += 1
        if last == len(nPath) - 1:
            merger = PdfFileMerger()
            allPath = "./static/img/resultPDF/all.pdf"
            print("Make DownloadPTh", len(nPath))
            for p in downloadPaths:
                pathImg = "./" + p
                merger.append(pathImg)
            merger.write("./static/img/resultPDF/all.pdf")
        last += 1


@app.route("/download/<path:imgPath>")
def download(imgPath):
    print("IMG ", imgPath)
    pathImg = "./" + imgPath
    return send_file(pathImg, as_attachment=True)


@app.route("/dAll")
def DownloadAll():
    allPath = "./static/img/resultPDF/all.pdf"
    return send_file(allPath, as_attachment=True)


def WriteImg(file, filename):
    global paths
    path = "./img/temSheet/" + str(filename) + ".png"
    savePath = "./static/img/temSheet/" + str(filename) + ".png"
    print("SAVE PAth", savePath)
    file.save(savePath)
    paths.append(path)


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/uploadComp/<path:imgPath>", methods=['POST', 'GET'])
def RecognizeNote(imgPath):
    global resultPaths, paths, single
    query = urllib.parse.unquote(imgPath)
    fileType = query.split('.')[-1]
    if fileType == "pdf":
        query = "./static/" + query
        print(query)
        prepare_images(query)
    else:
        paths.append(query)
        print("242:", paths[0][1:])
        threadMain()
        single = True

    data = {
        'singleOrNot': single,
        'path': imgPath,
        'ind': sheetIndicator,
        'resultPaths': resultPaths,
        'downloadPaths': downloadPaths
    }
    return render_template('/CSheet.html', imgData=data)


@app.route("/backHome")
def backHome():
    global sheetIndicator, paths, single, sheetC, resultPaths, x, downloadPaths
    sheetIndicator = 0
    sheetC = 0
    x = 0
    paths = []
    resultPaths = []
    downloadPaths = []
    single = True
    return redirect("/")


@app.route("/backGroup")
def backGroup():
    global sheetIndicator, paths, single, sheetC, resultPaths, x, downloadPaths
    sheetIndicator = 0
    sheetC = 0
    x = 0
    paths = []
    resultPaths = []
    downloadPaths = []
    single = True
    return redirect("/group")


@app.route("/upload/<string:fb>", methods=['POST', 'GET'])
def MoveSheet(fb):
    global sheetIndicator, paths, single
    if fb == "f":
        sheetIndicator = sheetIndicator + 1
    else:
        sheetIndicator = sheetIndicator - 1
    print("Result", resultPaths)
    print("Path", paths)
    data = {
        'singleOrNot': single,
        'path': paths,
        'ind': sheetIndicator,
        'resultPaths': resultPaths,
        'downloadPaths': downloadPaths
    }
    return render_template('/Sheet.html', imgData=data)


@app.route('/group', methods=['POST', 'GET'])
def MajorScales():
    print("Group")
    nPath = "./static/img/sheets"
    rPath = ".//img/sheets"
    onlyfiles = []
    newOnly = []
    for scale in listdir(nPath):
        if scale != '.DS_Store' and scale != "":
            for level in listdir(nPath + "/" + scale):
                if level != "" and level != ".DS_Store":
                    for path in listdir(nPath + "/" + scale + "/" + level):
                        if path != "" and path != ".DS_Store":
                            onlyfiles.append({
                                'scale':
                                scale,
                                'name':
                                path.split('.')[0],
                                'path':
                                rPath + "/" + scale + "/" + level + "/" + path,
                                'level':
                                level
                            })

    form = Form()

    if request.method == 'POST':
        if 'songName' in request.form:
            songName = request.form['songName']
            songName = songName.title()
            print(songName)
            qSongArr = songName.split(" ")
            if qSongArr[0] != '':
                for q in qSongArr:
                    for b in onlyfiles:
                        bSongArr = b['name'].split(" ")
                        for comp in bSongArr:
                            if comp == q:
                                newOnly.append(b)
                onlyfiles = newOnly
                print("NEW ONLY", newOnly)
                print(" ONLY FILE", onlyfiles)
        else:
            level = form.level.data
            print("LEVEL", level)
            if level == 'e':
                for f in onlyfiles:
                    if f['level'] == "Easy":
                        newOnly.append(f)
            elif level == 'm':
                for f in onlyfiles:
                    if f['level'] == "Medium":
                        newOnly.append(f)
            else:
                for f in onlyfiles:
                    if f['level'] == "Hard":
                        newOnly.append(f)
            onlyfiles = newOnly
    print("STH here")
    onlyfiles = {'onlyfiles': onlyfiles, 'form': form}
    return render_template('./majorScales.html', sheetList=onlyfiles)


@app.route('/updateList', methods=['POST', 'GET'])
def UpdateList():
    form = Form()
    a = {"a": [1, 23]}
    if request.method == 'POST':
        print(form.level.data)
        return ""
    return json.dumps(a)


# FLASK_APP=app.py FLASK_ENV=development flask run --port 3080
class Form(FlaskForm):
    level = SelectField('level',
                        choices=[('e', 'Easy'), ('m', "Medium"),
                                 ('h', 'Hard')])


# Shut down server
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == "__main__":
    app.run(debug=True)
