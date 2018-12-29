import redis
from rq import Queue
from flask import Flask, request, jsonify, send_from_directory, g, abort
import string_utils
import request_utils
import time
import os
import config
from flask_limiter import Limiter
from flask_expects_json import expects_json
from flask_cors import cross_origin
import LaTeXCompiler
RATELIMIT_STORAGE_URL = config.REDIS_URL
redis_instance = redis.from_url(config.REDIS_URL)
queue = Queue('latexcli', connection=redis_instance)
app = Flask(__name__)
app.config.from_object(__name__)

def share_key_func():
    return "guest"



limiter = Limiter(
    app,
    key_func=share_key_func,
)

@limiter.request_filter
def verify_token():
    s_token = request.headers.get('S-TOKEN', "00000000000000000000000000000000")
    if isinstance(s_token, str) and s_token == config.APIKEY:
        return True
    return False

compiler_schema = {
    'type': 'object',
    'properties':
    {
        'session': {'type': 'string'},
        'main': {'type': 'string'},
        'resources':
        {
            'type': 'array',
            'items':
            {
                'type': 'object',
                'properties':
                {
                    'url': {'type':'string'},
                    'name':{'type':'string'},
                    'modified_time':{'type':'integer'}
                },
                'required': ['url', 'name']

            }
        },
        'mode':{'type': 'string'}
    },
    'required': ['main', 'resources']
}


@app.route('/')
def hello_world():
    return jsonify({"result": "okay", "code": "00", "queue": len(queue)})

@app.route('/<path:path>')
@cross_origin()
def serve_file(path):
    if (path.endswith(".pdf") or path.endswith(".log")) and string_utils.is_secure_filename(path):
        return send_from_directory(config.WORKPLACE_DIR, path)
    return abort(404)


@app.route('/compiler', methods=['POST'])
@limiter.limit("60/minute")
@expects_json(compiler_schema)
def compile_endpoint():

    compile_session = ""
    mode = "simple"
    main_file = g.data['main']
    if len(main_file) < 5 and not main_file.endswith(".tex"):
        return jsonify({"result": "failed", "code": "-05", "reason": "invalid main file detected!"}), 500

    if 'mode' in g.data and g.data['mode'] == "full":
        mode = "full"

    build_session_path = True

    if 'session' in g.data:
        compile_session = g.data['session']
        if string_utils.is_valid_sessionid(compile_session) or not os.path.exists(os.path.join(config.WORKPLACE_DIR, compile_session)):
            build_session_path = False

    if build_session_path:
        compile_session = string_utils.gen_random_string(config.SESSION_LENGTH)
        os.mkdir(os.path.join(config.WORKPLACE_DIR, compile_session))

    outputpdfname = os.path.join(compile_session, main_file[:-3] + "pdf")
    outputlogname = os.path.join(compile_session, main_file[:-3] + "log")

    for res in g.data['resources']:
        if not string_utils.is_secure_filename(res['name']):
            return jsonify({"result": "failed", "code": "-01", "reason": "invalid filename detected"}), 500
        target_filename = os.path.join(config.WORKPLACE_DIR, compile_session, res['name'])

        target_dirname = os.path.dirname(target_filename)
        if not os.path.exists(target_dirname):
            os.makedirs(target_dirname, exist_ok=True)

        if res['url'].startswith('data://'):
            with open(target_filename, 'w') as fb:
                fb.write(res['url'][7:])
        else:
            need_download = True
            last_save_time = redis_instance.get(res['url'])
            if "modified_time" in res and res['modified_time'] != 0 and os.path.exists(target_filename) and \
                last_save_time is not None and int(last_save_time) == res['modified_time']:
                need_download = False
            if  need_download:
                if not request_utils.get_remote_file(res['url'], target_filename):
                    return jsonify({"result": "failed", "code": "-06",
                                    "reason": "Unable to fetch remote file, either it is too large or unreachable!"}), 500
                redis_instance.set(res['url'], res['modified_time'])



    job = queue.enqueue_call(LaTeXCompiler.compile_latex_project, args=(compile_session, main_file, mode),
                             timeout=config.TASK_TIMEOUT)

    wait_count = 0
    while job.result is None:
        time.sleep(config.TICKING_ACCURARCY)
        wait_count += 1
        if wait_count > config.TASK_TIMEOUT/config.TICKING_ACCURARCY:
            break

    if job.result is None:
        return jsonify({"result": "failed", "code": "-03", "reason": "task timeout"}), 500
    else:
        return jsonify({"result": "okay", "code": "00", "compile_result": job.result,
                        "pdf": outputpdfname, "log":outputlogname, "session": compile_session})



if __name__ == '__main__':
    app.run()
