import subprocess
from flask import(
    Flask,
    make_response,
    request,
    render_template,
    redirect,
    send_file,
    session,
    url_for,
)
# from passlib.hash import sha512_crypt
import logging
# import spwd
import pwd
import os
import service
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', handlers=[
        logging.FileHandler('log.log'),
        logging.StreamHandler()
    ])

@app.route('/') 
def index():
    print('hi index')
    if 'username' in session:
        print('im in session')
        home_dir = pwd.getpwnam(session["username"]).pw_dir # type: ignore

        files = []
        dirs = []
        file_sizes = {}
        file_times = {}
        dir_times = {}
        
        current_dir = home_dir
        # list files and directories
        for item in os.listdir(current_dir):
            if os.path.isfile(os.path.join(home_dir, item)):
                files.append(item)
                file_sizes[item] = round(os.path.getsize(os.path.join(home_dir, item)) / 1024)
                file_times[item] = time.ctime(os.path.getmtime(os.path.join(home_dir, item)))
            elif os.path.isdir(os.path.join(home_dir, item)):
                dirs.append(item)
                dir_times[item] = os.path.getmtime(os.path.join(home_dir, item))

        allFiles = service.getAllFiles(home_dir)
        
        #get sapce
        space = service.getSpace(home_dir)

        # Search for files with specific name and extension
        search_text = request.args.get('search_text')
        if search_text:
            files = service.searchFile(search_text, allFiles)

        return render_template('home.html', username=session['username'], home_dir=current_dir, files=files, dirs=dirs, space=space,
                                file_sizes=file_sizes, file_times=file_times, dir_times=dir_times, 
                                search_text=search_text)
    else:
        print('im not in session')
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if service.authenticate(username, password):
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout',methods=['POST'])
def logout():
    username = session['username']
    session.pop('username', None)
    print('You were successfully logged out')
    logging.info(f'{username} logged out')
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return redirect(url_for('index'))

@app.route('/download')
def download():
    if 'username' in session:
        username = session['username']
        home_dir = pwd.getpwnam(session["username"]).pw_dir # type: ignore
        zip_filename = f'{session["username"]}_home.zip'
        zip_file = service.downloadFile(home_dir, username, zip_filename)
        return send_file(zip_file, as_attachment=True, download_name=zip_filename, mimetype='application/zip')
    else:
        return redirect(url_for('index'))

@app.route('/showFile')
def showFile():
    if 'username' in session:
        home_dir = pwd.getpwnam(session["username"]).pw_dir # type: ignore
        filename = request.args.get('filename')
        command = ['find', home_dir, '-name', filename]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        file_path = result.stdout.decode('utf-8').strip()
        print('output: ', file_path)
        with open(file_path, 'r') as f:
            content = f.read()
        return render_template('file_content.html', content=content)
        
    else:
        return redirect(url_for('index'))

@app.route('/showDirectory')
def showDirectory():
    if 'username' in session:
        home_dir = pwd.getpwnam(session["username"]).pw_dir # type: ignore
        directoryname = request.args.get('directoryname')
        command = ['find', home_dir, '-name', directoryname]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        dir_path = result.stdout.decode('utf-8').strip()
        print('dir output: ', dir_path)

        files = []
        dirs = []
        file_sizes = {}
        file_times = {}
        dir_times = {}
        
        current_dir = dir_path
        # list files and directories
        for item in os.listdir(current_dir):
            if os.path.isfile(os.path.join(current_dir, item)):
                files.append(item)
                file_sizes[item] = round(os.path.getsize(os.path.join(current_dir, item)) / 1024)
                file_times[item] = time.ctime(os.path.getmtime(os.path.join(current_dir, item)))
            elif os.path.isdir(os.path.join(current_dir, item)):
                dirs.append(item)
                dir_times[item] = time.ctime(os.path.getmtime(os.path.join(current_dir, item)))
            
        allFiles = service.getAllFiles(home_dir)
        space = service.getSpace(home_dir)

        # Search for files with specific name and extension
        search_text = request.args.get('search_text')
        if search_text:
            files = service.searchFile(search_text, allFiles)

        return render_template('home.html', username=session['username'], home_dir=dir_path, files=files, dirs=dirs, space=space,
                                file_sizes=file_sizes, file_times=file_times, dir_times=dir_times, 
                                search_text=search_text)
    else:
        return redirect(url_for('index'))

@app.errorhandler(Exception)
def error(exception):
    return render_template('error.html', error = 
    {
        "ip":request.remote_addr,
        "method":request.method,
        "error":exception
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)


# docker build -t web_home_space 'E:\3eme annee ESISA\Python\webHomeSpace'
# docker run -it -p 5000:5000 web_home_space /bin/bash