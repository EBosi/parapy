usage = """
	python parapy.py INPUT_FOLDER
"""
#######################

import os,sys,itertools,multithreading,shutil

#######################

def cpy_inparanoid(thread_dir):
	# list of files (ls -rt | awk '{print "\"" $9 "\"" ","}')
	files=["accessory_finder_multipara.pl",
	"all_genomes_DB",
	"antarctic_files",
	"blast_parser.pl",
	"blosum45",
	"blosum62",
	"blosum80",
	"conversion_table.txt",
	"ec",
	"error.log",
	"fasta_on_the_fly.pl",
	"fasta_parser.log",
	"fasta_parser_parapipe.pl",
	"formatdb.log",
	"inparanoid.pl",
	"input_list_NCBI",
	"input_prots_antarctic",
	"insert_NCBI_title.pl",
	"licence",
	"list_of_faa_files",
	"multiparanoid.pl",
	"multiparanoid.pl~",
	"multipara_seq_retriever_groups.pl",
	"multipara_seq_retriever.pl",
	"pam30",
	"pam70",
	"parapipe_NOBLAST.pl",
	"parapipe.pl",
	"parsoid_parapipe.pl",
	"parsoid.pl",
	"readme",
	"sc",
	"seqstat.jar",
	"seqstat_old.jar"]
	#
	for f in files:
		shutil.copy(f,thread_dir)

def get_all_pairs(proteomes):
	pairs=itertools.combinations(proteomes, 2)
	return pairs

def launch_inparanoid(genome1,genome2,dir_):
	os.system('inparanoid.pl %s %s' %(self.g1,self.g2))
	return 

def clear_all(thread_dir):
	for f in os.listdir(thread_dir):
		os.remove(f)

def get_outs(thread_dir):
	outs=[out for out in os.listdir(thread_dir) if out.startswith('Output.')]
	return outs
#######################

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
        return

class All_pairs_queue(multiprocessing.JoinableQueue):
	
	def __init__(self,dir_):
		multiprocessing.JoinableQueue.__init__(self)
		self.dir_=dir_
		genomes=os.listdir(dir_)

class InparanoidTask(object):
	#
	def __init__(self,genome1,genome2,name='Parapy_task'):
		self.name=name
		self.g1=genome1
		self.g2=genome2
		self.main=''
		self.sub =''
	#
	def __call__(self):
		# what to do for each task:
		#
		# 1) if it doesn't exist, creat a subdir
		if not os.path.exists(self.sub):
			os.makedir(self.sub)
		# 2) copy the files in it
		src1=self.main+self.g1
		src2=self.main+self.g2
		dst=self.sub
		shutil.copy(src1,dst)
		shutil.copy(src2,dst)
		# 3) move into it and launch Inparanoid
		os.chdir(dst)
		os.system('inparanoid.pl %s %s' %(self.g1,self.g2))
		# 4) move outputs into main and clean
		outputs=get_outs(self.sub)
		for out in outputs: shutil.move(out,self.main)
		clear_all(self.sub)
		# 5) print success, you've done it right son!
		print "successfully inparanoid'd %s , %s" %(self.g1,self.g2)
		

#######################

numb_threads=5

if __name__ == '__main__':
    jobs = []
    for i in range(numb_threads):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()

#######################

if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    num_jobs = 10
    for i in xrange(num_jobs):
        tasks.put(Task(i, i))
    
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1
