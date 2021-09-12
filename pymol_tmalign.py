from glob import glob
from pymol import cmd
from pathlib import Path
import psico.fullinit
import pymol
import multiprocessing
import time
import math
all_res = []
n_process = 16
files = glob('C:\\AlphaFold\\drosophila\\*pdb')


def splitList(lst, chunk_numbers):
    n = math.ceil(len(lst)/chunk_numbers)
    res=[]
    for x in range(0, len(lst), n):
        sub_list = lst[x: n+x]
        res.append(sub_list)
    return res
    
files_list = splitList(files, n_process)

path = "D:\\Benj\\KresslerLab_BP\\structures\AlphaFold\\"
test_prot = "CNOT11_D1"
q = multiprocessing.Queue()

def align(file_list, queue):
    cmd.load(path+test_prot+".pdb")
    results = []
    for file in file_list:
        if file is None:
            continue
        cmd.load(file)
        name = Path(file).stem
        res = cmd.tmalign(name,test_prot)
        results.append(name+","+str(res))
        cmd.delete(name)
    queue.put(results)

start_time = time.time()

if __name__ == '__main__':
    processes = []
    for i in range(n_process):
        p = multiprocessing.Process(target=align, args=(files_list[i], q))
        processes.append(p)
        p.start()

    for p in processes:
        ret = q.get()
        all_res.append(ret)
    for p in processes:
        p.join()

res_file = open(test_prot+"_dros_results.txt","w")
for element in all_res:
    for line in element:
        res_file.write(line + "\n")
res_file.close()

total_time = time.time()-start_time
print(total_time)
