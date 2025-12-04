from datetime import datetime, timedelta

def estimate_time(npx, npy, exposure, repeat, overhead):
    time_now = datetime.now()
    scan_sec = (npx +1)* (npy+1)*exposure + (npy + 1)*overhead
    hh_mm_s = timedelta(seconds = scan_sec*repeat)
    total_time = (datetime.combine(datetime.today(), time_now.time()) + hh_mm_s)
    return str(hh_mm_s).split(".")[0], total_time
