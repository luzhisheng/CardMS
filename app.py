import os
import time
from urllib.parse import quote_plus
import zipstream
from flask import Flask, render_template, request, Response, send_from_directory
from settings import root_dir

app = Flask(__name__)


@app.route('/output/')
def document():
    os.chdir(root_dir)
    current_dir = os.getcwd()
    current_list = os.listdir(current_dir)
    contents = []
    for i in sorted(current_list):
        full_path = current_dir + os.sep + i
        # 如果是目录，在后面添加一个sep
        if os.path.isdir(full_path):
            extra = os.sep
        else:
            extra = ''
        content = {}
        content['filename'] = i + extra
        if "temp_dict.txt" in content['filename'] or "stopwords.txt" in content['filename']:
            continue
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(full_path).st_mtime))
        content['size'] = str(round(os.path.getsize(full_path) / 1024)) + 'k'
        contents.append(content)
    contents = sorted(contents, key=lambda x: x['mtime'], reverse=True)
    return render_template('shared.html', contents=contents, subdir="", ossep=os.sep)


@app.route('/output/<subdir>/')
@app.route('/output/<subdir>/<fullname>')
def detail(subdir, fullname=''):
    if fullname:
        os.chdir(root_dir)
        current_dir = os.getcwd()
        dir_path = current_dir + os.sep + subdir
        filename = fullname.split(os.sep)[-1]
        return send_from_directory(dir_path, filename, as_attachment=True)
    else:
        fullname = root_dir + os.sep + subdir
        dir_path = root_dir + os.sep

        #  如果是文件，则下载
        if os.path.isfile(fullname):
            return send_from_directory(dir_path, subdir, as_attachment=True)

        os.chdir(fullname)
        current_dir = os.getcwd()
        current_list = os.listdir(current_dir)
        contents = []
        for i in sorted(current_list):
            full_path = current_dir + os.sep + i
            # 如果是目录，在后面添加一个sep
            if os.path.isdir(full_path):
                extra = os.sep
            else:
                extra = ''
            content = {}
            content['filename'] = i + extra
            content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(full_path).st_mtime))
            content['size'] = str(round(os.path.getsize(full_path) / 1024)) + 'k'
            contents.append(content)
        return render_template('detail.html', contents=contents, subdir=subdir, ossep=os.sep)


@app.route('/output/<subdir>/', methods=['POST'])
def downloader(subdir):
    filename_list = request.values.getlist('filename[]')
    os.chdir(root_dir)
    current_dir = os.getcwd()
    dir_path = current_dir + os.sep + subdir

    if len(filename_list) == 1:
        return send_from_directory(dir_path, filename_list[0], as_attachment=True)
    else:
        def generator(filename_list):

            z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
            for f in filename_list:
                z.write(os.path.join(dir_path, f), arcname=f)
            for chunk in z:
                yield chunk

        response = Response(generator(filename_list), mimetype='application/zip')
        response.headers['Content-Disposition'] = 'attachment; filename={}.zip'.format(quote_plus(subdir))
        return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
