import os, time, config, shutil

while True:
    time.sleep(3600)
    #time.sleep(10)
    now = time.time()
    cutoff = now - (config.FILE_STORAGE_TIME)
    files = os.listdir(config.WORKPLACE_DIR)
    for xfile in files:
        targetF = os.path.join(config.WORKPLACE_DIR, xfile)
        print(targetF)
        if os.path.isdir(targetF):
            t = os.stat(targetF)
            c = t.st_ctime
            if c < cutoff:
                shutil.rmtree(targetF)
                print("Removing %s" % targetF)
