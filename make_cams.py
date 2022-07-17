from model_analysis import analyze
import threading

def start_analytics(cam_id):
    analyze(cam_id)
    print("processing finished", threading.current_thread().name)

def create_cams():

    cam_id1 = "http://techslides.com/demos/sample-videos/small.mp4"
    cam_id2 = "http://techslides.com/demos/sample-videos/small.mp4"
    cam_id3 = "http://techslides.com/demos/sample-videos/small.mp4"

    cams = [cam_id1, cam_id2, cam_id3]
    threads = []
    for cam_id in cams:
        thread = threading.Thread(target=start_analytics, args=(cam_id, ))
        thread.start()
        threads.append(thread)
    #wait for all threads to complete before main program exits
    for thread in threads:
        thread.join()
    