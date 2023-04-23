from flask import session
from passlib.hash import sha512_crypt
import logging
import spwd
import os
import shutil


def authenticate(username, password):
    try:
        encrypted_password = spwd.getspnam(username).sp_pwdp # type: ignore
        print('encrypted = ', encrypted_password)   
        if sha512_crypt.verify(password, encrypted_password):
            session['username'] = username
            print('You were successfully logged in')
            logging.info(f'{username} logged in')
            return True
            # return redirect(url_for('index'))
        else:
            print('Invalid username or password')
            logging.warning(f'Failed login attempt with username: {username}')
            return False
    except KeyError:
        print('Invalid username or password')
        logging.warning(f'Failed login attempt with username: {username}')
        return False

def searchFile(search_text, files):
    files = [f for f in files if os.path.basename(f).startswith(search_text.strip()) or os.path.splitext(f)[-1] == '.' + search_text.strip()]
    return files

def downloadFile(home_dir, username, zip_filename):
    zip_file = shutil.make_archive(zip_filename, 'zip', home_dir)
    logging.info(f'{username} just downloaded {home_dir}')
    return zip_file

def getAllFiles(home_dir):
    allFiles = []
    for root, _, filenames in os.walk(home_dir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                allFiles.append(path)
    return allFiles

def getSpace(home_dir):
    space = sum(os.path.getsize(os.path.join(home_dir, f)) for f in os.listdir(home_dir) if os.path.isfile(os.path.join(home_dir, f)))
    space = round(space / 1024)
    return space

