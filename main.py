import os
import time
from multiprocessing import Process, cpu_count, Manager
from threading import Thread

# Utility Function: Get human-readable file size
# Converts file size in bytes to a more human-readable format (e.g., KB, MB, GB).
def get_file_size(file_path):
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

# Generate synthetic test data
# Creates two large files filled with integer data for testing purposes.
def generate_files(file1, file2, lines_per_file=10**6):
    with open(file1, 'w') as f1, open(file2, 'w') as f2:
        for i in range(lines_per_file):
            f1.write(f"{i}\n")
            f2.write(f"{2 * i}\n")
    print(f"[INFO] Files generated: {file1} ({get_file_size(file1)}), {file2} ({get_file_size(file2)})")

# Single-threaded processing
# Reads corresponding lines from both files, calculates their sum, and writes the result to the output file.
def single_threaded(file1, file2, output_file):
    start_time = time.time()  # Record the start time
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out:
        for line1, line2 in zip(f1, f2):
            try:
                # Convert strings to integers, calculate their sum, and write the result
                sum_value = int(line1.strip()) + int(line2.strip())
                out.write(f"{sum_value}\n")
            except ValueError as e:
                # Handle cases where a line cannot be converted to an integer
                print(f"[ERROR] Skipping invalid line: {line1.strip()}, {line2.strip()}: {e}")
    execution_time = time.time() - start_time  # Calculate elapsed time
    print(f"[Single-threaded] Execution Time: {execution_time:.2f} seconds")
    return execution_time

# Multithreaded processing
# Uses threads to process chunks of lines concurrently.
def multithreaded(file1, file2, output_file, num_threads=8):
    # Worker function for each thread
    def worker(start, end, output_list, idx):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            # Skip lines until reaching the starting position for this thread
            for _ in range(start):
                f1.readline()
                f2.readline()
            # Process the assigned chunk of lines
            for i in range(end - start):
                line1 = f1.readline()
                line2 = f2.readline()
                try:
                    sum_value = int(line1.strip()) + int(line2.strip())
                    output_list[idx].append(sum_value)
                except ValueError as e:
                    print(f"[ERROR] Skipping invalid line: {line1.strip()}, {line2.strip()}: {e}")

    lines = sum(1 for _ in open(file1))  # Count total lines in the file
    chunk_size = lines // num_threads  # Determine lines per thread
    manager = Manager()
    output_list = manager.list([[] for _ in range(num_threads)])  # Shared list for thread results
    threads = []

    start_time = time.time()  # Record the start time
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else lines
        # Create and start a thread for each chunk
        t = Thread(target=worker, args=(start, end, output_list, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # Wait for all threads to finish

    # Write the aggregated results to the output file
    with open(output_file, 'w') as out:
        for result in output_list:
            for value in result:
                out.write(f"{value}\n")

    execution_time = time.time() - start_time  # Calculate elapsed time
    print(f"[Multithreaded] Execution Time: {execution_time:.2f} seconds, Threads: {num_threads}")
    return execution_time

# Parallel Processing
# Splits the input files into parts, processes each part using separate processes, and combines the results.
def process_part(file1_part, file2_part, output_part):
    with open(file1_part, 'r') as f1, open(file2_part, 'r') as f2, open(output_part, 'w') as out:
        for line1, line2 in zip(f1, f2):
            try:
                sum_value = int(line1.strip()) + int(line2.strip())
                out.write(f"{sum_value}\n")
            except ValueError as e:
                print(f"[ERROR] Skipping invalid line: {line1.strip()}, {line2.strip()}: {e}")

def parallel_processing(file1, file2, output_file, num_parts=10):
    start_time = time.time()  # Record the start time

    lines_per_part = sum(1 for _ in open(file1)) // num_parts  # Calculate lines per part

    # Splits a file into smaller parts
    def split_file(file, prefix):
        with open(file, 'r') as f:
            for idx in range(num_parts):
                with open(f"{prefix}_part{idx}.txt", 'w') as part_file:
                    for _ in range(lines_per_part):
                        line = f.readline()
                        if not line:
                            break
                        part_file.write(line)

    # Split both files
    split_file(file1, "file1")
    split_file(file2, "file2")

    processes = []
    output_files = []
    for idx in range(num_parts):
        file1_part = f"file1_part{idx}.txt"
        file2_part = f"file2_part{idx}.txt"
        output_part = f"output_part{idx}.txt"
        output_files.append(output_part)
        # Create and start a process for each part
        p = Process(target=process_part, args=(file1_part, file2_part, output_part))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()  # Wait for all processes to finish

    # Combine all results into the final output file
    with open(output_file, 'w') as out:
        for output_part in output_files:
            with open(output_part, 'r') as part_file:
                out.writelines(part_file.readlines())

    # Cleanup temporary files
    for temp_file in output_files + [f"file1_part{idx}.txt" for idx in range(num_parts)] + [f"file2_part{idx}.txt" for idx in range(num_parts)]:
        os.remove(temp_file)

    execution_time = time.time() - start_time  # Calculate elapsed time
    print(f"[Parallel Processing] Execution Time: {execution_time:.2f} seconds, Parts: {num_parts}")
    return execution_time

if __name__ == "__main__":
    # Configuration
    file1 = "hugefile1.txt"
    file2 = "hugefile2.txt"
    output_file = "totalfile.txt"
    lines_per_file = 10**6  # Adjust for testing purposes

    # Generate test files
    generate_files(file1, file2, lines_per_file)

    # Single-threaded execution
    single_threaded_time = single_threaded(file1, file2, output_file)

    # Multithreaded execution
    multithreaded_time = multithreaded(file1, file2, output_file, num_threads=8)

    # Parallel processing execution
    parallel_processing_time = parallel_processing(file1, file2, output_file, num_parts=10)

    # Summary of results
    print("\n=== Summary Report ===")
    print(f"File 1 Size: {get_file_size(file1)}")
    print(f"File 2 Size: {get_file_size(file2)}")
    print(f"Single-threaded Execution: {single_threaded_time:.2f} seconds")
    print(f"Multithreaded Execution: {multithreaded_time:.2f} seconds with 8 threads")
    print(f"Parallel Processing Execution: {parallel_processing_time:.2f} seconds with 10 parts")
