import config
import subprocess
import time
import logging
import os

def compile_latex_project(project_dir, main_file, mode):
    cmd = ["latexmk", "-pdf", main_file]

    if mode == "simple":
        cmd = ["pdflatex", "-interaction", "nonstopmode", main_file]
    elif mode == "partial":
        cmd = ["pdflatex", "-interaction", "nonstopmode", main_file]
        # my_env = os.environ.copy()
        # my_env['LD_PRELOAD'] = path_utils.get_pmalloc_path()

    pro = subprocess.Popen(cmd, cwd=os.path.join(config.WORKPLACE_DIR, project_dir))

    wait_count = 0
    r = None
    while wait_count <= config.TASK_TIMEOUT / config.TICKING_ACCURARCY:
        wait_count += 1
        time.sleep(config.TICKING_ACCURARCY)
        r = pro.poll()
        if r is not None:
            break

    if r is None:
        pro.kill()
        logging.error("LaTeX compiler task (%s/%s/%s) timeout" % (project_dir, main_file, mode))
        return -1
    else:
        if r == 0:
            logging.info("LaTeX compilation finished without warnings")
            return 0
        else:
            logging.error("LaTeX compilation failed with syntax errors (%s/%s/%s/%d)" % (project_dir, main_file, mode, r))
            return -1


