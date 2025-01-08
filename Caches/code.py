import math
import matplotlib.pyplot as plt
import tarfile
import os
import pandas as pd

# Cache class to simulate cache behavior
class Cache:
    def __init__(self, cache_size_kb, block_size, associativity):
        # Convert cache size from KB to bytes
        self.cache_size = cache_size_kb * 1024
        self.block_size = block_size
        self.associativity = associativity
        self.num_blocks = self.cache_size // self.block_size
        self.num_sets = self.num_blocks // self.associativity
        
        # Initialize cache structure: list of sets with empty blocks
        self.cache = [[{'tag': None, 'valid': False} for _ in range(associativity)] for _ in range(self.num_sets)]
        # Initialize LRU tracking for each set
        self.lru_order = [[] for _ in range(self.num_sets)]
        # Initialize hit and miss counters
        self.hits = 0
        self.misses = 0

    # Simulate cache access for a given address
    def access_cache(self, address):
        # Calculate number of bits for block offset and index
        block_offset_bits = int(math.log2(self.block_size))
        index_bits = int(math.log2(self.num_sets))
        
        # Calculate block address, index, and tag
        block_address = address >> block_offset_bits
        index = block_address % self.num_sets
        tag = block_address >> index_bits
        
        # Check if there is a cache hit
        for i, line in enumerate(self.cache[index]):
            if line['valid'] and line['tag'] == tag:
                self.hits += 1
                # Update LRU order
                self.lru_order[index].remove(i)
                self.lru_order[index].append(i)
                return 'hit'
        
        # Handle cache miss
        self.misses += 1
        # Determine which block to replace (LRU)
        if len(self.lru_order[index]) >= self.associativity:
            lru_index = self.lru_order[index].pop(0)
        else:
            lru_index = len(self.lru_order[index])
        
        # Replace the LRU block or add a new one
        if lru_index < len(self.cache[index]):
            self.cache[index][lru_index] = {'tag': tag, 'valid': True}
        else:
            self.cache[index].append({'tag': tag, 'valid': True})
        
        # Update LRU order
        self.lru_order[index].append(lru_index)
        return 'miss'

    # Get cache statistics: hits, misses, and hit rate
    def get_stats(self):
        return self.hits, self.misses, self.hits / (self.hits + self.misses)

# Function to simulate cache performance using trace file
def simulate_cache(trace_file, cache_size_kb, block_size, associativity):
    cache = Cache(cache_size_kb, block_size, associativity)
    
    # Read memory addresses from the trace file
    with open(trace_file, 'r') as file:
        for line in file:
            _, address, _ = line.split()
            address = int(address, 16)
            cache.access_cache(address)
    
    # Get and return cache performance statistics
    hits, misses, hit_rate = cache.get_stats()
    return hits, misses, hit_rate

# Function to plot cache simulation results
def plot_graphs(results, x_labels, title, x_label, y_label, traces):
    plt.figure(figsize=(10, 6))
    for i, trace in enumerate(traces):
        y_values = [result[i] for result in results]
        plt.plot(x_labels, y_values, label=f'Trace {trace}')
    
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to extract trace files from a tar.gz archive
def extract_traces(archive_path):
    trace_files = []
    with tarfile.open(archive_path, 'r:gz') as tar:
        tar.extractall()
        for member in tar.getmembers():
            if member.isfile():
                trace_files.append(member.name)
    return trace_files

# Function to save results to an Excel file
def save_to_excel(results, x_labels, traces, file_name, result_type='miss'):
    data = {'Parameter': x_labels}
    for i, trace in enumerate(traces):
        if result_type == 'miss':
            data[f'Trace {trace}'] = [result[i] * 100 for result in results]  # Miss rate in percentage
        else:
            data[f'Trace {trace}'] = [result[i] * 100 for result in results]  # Hit rate in percentage
    
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)

# Extract trace files from the provided archive path
trace_files = extract_traces('C:/Users/raksh/OneDrive/Documents/VS code/ca_assignment/proj1-traces.tar.gz')

# Different parameters for cache simulation
cache_sizes = [128, 256, 512, 1024, 2048, 4096]  # in KB
block_sizes = [1, 2, 4, 8, 16, 32, 64, 128]  # in Bytes
associativities = [1, 2, 4, 8, 16, 32, 64]  # ways

# Simulate cache for each trace file and print the results
for trace in trace_files:
    hits, misses, hit_rate = simulate_cache(trace, 1024, 4, 4)
    print(f"Trace {trace} - Hits: {hits}, Misses: {misses}, Hit Rate: {hit_rate:.4f}, Miss Rate: {1 - hit_rate:.4f}")

# Simulate and save results for different cache sizes
results_cache_size = []
for cache_size in cache_sizes:
    trace_results = []
    for trace in trace_files:
        _, _, hit_rate = simulate_cache(trace, cache_size, 4, 4)
        trace_results.append(1 - hit_rate)  # Miss rate as percentage
    results_cache_size.append(trace_results)

save_to_excel(results_cache_size, cache_sizes, trace_files, 'miss_rate_vs_cache_size.xlsx', 'miss')

# Simulate and save results for different block sizes
results_block_size = []
for block_size in block_sizes:
    trace_results = []
    for trace in trace_files:
        _, _, hit_rate = simulate_cache(trace, 1024, block_size, 4)
        trace_results.append(1 - hit_rate)   # Miss rate as percentage
    results_block_size.append(trace_results)

save_to_excel(results_block_size, block_sizes, trace_files, 'miss_rate_vs_block_size.xlsx', 'miss')

# Simulate and save results for different associativities
results_associativity = []
for associativity in associativities:
    trace_results = []
    for trace in trace_files:
        _, _, hit_rate = simulate_cache(trace, 1024, 4, associativity)
        trace_results.append(hit_rate)  # Hit rate as percentage
    results_associativity.append(trace_results)

save_to_excel(results_associativity, associativities, trace_files, 'hit_rate_vs_associativity.xlsx', 'hit')

# Plot graphs for the simulation results
try:
    plot_graphs(results_cache_size, cache_sizes, 'Miss Rate vs Cache Size', 'Cache Size (KB)', 'Miss Rate (%)', trace_files)
    print("Plotted Miss Rate vs Cache Size")
except Exception as e:
    print(f"Error plotting Miss Rate vs Cache Size: {e}")

try:
    plot_graphs(results_block_size, block_sizes, 'Miss Rate vs Block Size', 'Block Size (Bytes)', 'Miss Rate (%)', trace_files)
    print("Plotted Miss Rate vs Block Size")
except Exception as e:
    print(f"Error plotting Miss Rate vs Block Size: {e}")

try:
    plot_graphs(results_associativity, associativities, 'Hit Rate vs Associativity', 'Associativity (ways)', 'Hit Rate (%)', trace_files)
    print("Plotted Hit Rate vs Associativity")
except Exception as e:
    print(f"Error plotting Hit Rate vs Associativity: {e}")
