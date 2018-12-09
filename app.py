from redis import Redis
from rq import Queue
from flask import Flask, request, jsonify, send_from_directory
import string_utils
import time
import os
import config

queue = Queue(connection=Redis())
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/compile', methods=['POST'])
def compile_endpoint():
    jsonr = request.get_json()
    compile_session = ""
    allow_cached = False
    main_file = ""
    resources = []
    if 'main' not in jsonr or 'resources' not in jsonr or not isinstance(jsonr['resources'], list):
        return jsonify({"result": "failed", "code": "-01", "reason": "invalid request detected!"}), 500

    for res in jsonr['resources']:
        if not isinstance(res, dict):
            continue
        if 'filename' not in res or 'url' not in 


    if 'session' in jsonr:
        compile_session = jsonr['session']
        if len(compile_session) != config.SESSION_LENGTH or not os.path.exists(os.path.join(config.WORKPLACE_DIR, compile_session)):
            return jsonify({"result": "failed", "code": "-05", "reason": "invalid session detected!"}), 500
        allow_cached = True
    else:
        compile_session = string_utils.gen_random_string(config.SESSION_LENGTH)
        os.mkdir(os.path.join(config.WORKPLACE_DIR, compile_session))
        allow_cached = False


    if remote_url == "" or not remote_url.startswith("http"):
        return jsonify({"result": "failed", "code": "-05", "reason": "invalid url detected!"}), 500
    page = "1"
    if 'page' in jsonr:
        page = jsonr['page']
    zoom_ratio = "1"
    if 'zoom_ratio' in jsonr:
        zoom_ratio = jsonr['zoom_ratio']
    use_cache = "no"
    if 'use_cache' in jsonr:
        use_cache = jsonr['use_cache']

    save_filename = os.path.join(config.WORKPLACE_DIR, string_utils.hash_filename(remote_url) + ".pdf")
    output_filename = string_utils.gen_random_string(16) + ".html"
    if use_cache != "no":
        if not os.path.exists(os.path.join(config.WORKPLACE_DIR, save_filename)):
            return jsonify({"result": "failed", "code": "-07",
                            "reason": "Cache not existed"}), 500
    else:
        if not get_remote_file(remote_url, save_filename):
            return jsonify({"result": "failed", "code": "-06", "reason": "Unable to fetch remote file, either it is too large or unreachable!"})

    job = queue.enqueue_call(htmlizer.convert_pdf_to_html, args=(save_filename, output_filename, page, zoom_ratio,),
                             timeout=config.TASK_TIMEOUT)

    wait_count = 0
    while job.result is None:
        time.sleep(config.TICKING_ACCURARCY)
        wait_count += 1
        if wait_count > config.TASK_TIMEOUT/config.TICKING_ACCURARCY:
            break

    if job.result is None:
        return jsonify({"result": "failed", "code": "-03", "reason": "task timeout"})
    elif job.result == -1:
        return jsonify({"result": "failed", "code": "-04", "reason": "malformed pdf detected"})
    else:
        return jsonify({"result": "okay", "code": "00", "url": output_filename})



if __name__ == '__main__':
    app.run()
