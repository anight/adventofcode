#! /usr/bin/env python3

import os
import time
import argparse
from multiprocessing import Pool
from functools import partial
import numpy as np

def load_data(filename):
        with open(filename, 'r') as f:
                return list(map(int, f.readline().rstrip()))

def f(n_nodes, values, node_id):
    from numba import cuda

    start = node_id * values.size // n_nodes
    end = (node_id+1) * values.size // n_nodes

    print("running on", node_id, os.getpid(), "start:", start, "end:", end)

    cuda.select_device(node_id)

    @cuda.jit
    def calculate(d_in, d_out, start, end):
        tid = cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x
        if start <= tid < end:
            period = tid + 1
            for number_index in range(d_in.size):
                seq_value = 1-abs((((number_index+1) // period ) % 4)-1)
                d_out[tid] += d_in[number_index] * seq_value

    d_values = cuda.to_device(values)

    threads_per_block = 256
    blocks_per_grid = (values.size + (threads_per_block - 1)) // threads_per_block

    if blocks_per_grid < 16:
        blocks_per_grid = 16

    d_result = cuda.device_array(values.size, dtype=np.int32)
    calculate[blocks_per_grid, threads_per_block](d_values, d_result, start, end)
    result = d_result.copy_to_host()
    print("finished on", node_id)
    return np.abs(result[start:end]) % 10

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpus", type=int, default=1, help="Number of GPUs to use")
    args = parser.parse_args()

    values = np.array(load_data('input.txt') * 10000, dtype=np.int32)
    skip = int(''.join(map(str, values[:7])))

    for i in range(100):
        with Pool(args.gpus) as p:
            filename = f"{i+1:03}.txt"
            if os.path.exists(filename):
                print("loading from existing", filename)
                values = np.array(load_data(filename), dtype=np.int32)
                continue
            started = time.time()
            values = np.concatenate(p.map(partial(f, args.gpus, values), range(args.gpus)))
            elapsed = time.time() - started
            print(f"took {elapsed:.2f}")
            with open(filename, "w+") as w:
                w.write(''.join(map(str, values)) + "\n")
            print("wrote", filename)

    print(''.join(map(str, values[skip:skip+8])))
