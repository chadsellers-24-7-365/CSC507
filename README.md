# Evaluating Line Summation Methods: Single-Threaded vs. Multithreaded vs. Parallel Processing in Python

## Overview

This project demonstrates three methods for processing large datasets efficiently using Python:
1. **Single-threaded Processing**: Sequentially processes data line-by-line.
2. **Multithreaded Processing**: Uses threads for concurrent data processing.
3. **Parallel Processing**: Leverages multiprocessing to utilize multiple CPU cores for faster execution.

The program adds corresponding numbers from two large files (`hugefile1.txt` and `hugefile2.txt`) and writes the results to a new file (`totalfile.txt`). It is designed to handle datasets of up to 1 million lines (or more with appropriate configuration).

---

## Features

- **Synthetic Data Generation**: Creates `hugefile1.txt` and `hugefile2.txt` with configurable numbers of lines for testing.
- **Execution Metrics**:
  - Tracks and logs execution times for each method.
  - Provides insights into the performance of single-threaded, multithreaded, and parallel approaches.
- **Error Handling**:
  - Skips invalid lines with detailed logging.
- **File Cleanup**:
  - Automatically removes temporary files after parallel processing.

---

## Requirements

- Python 3.7 or later
- Modules:
  - `os`
  - `time`
  - `threading`
  - `multiprocessing`

---

## How to Run

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install Python (if not already installed).

3. Run the script:
   ```bash
   python main.py
   ```

---

## Results and Summary

After execution, the program generates:
1. **Execution Times**:
   - Single-threaded
   - Multithreaded (with configurable thread count)
   - Parallel Processing (with configurable parts)
2. **Output File**:
   - `totalfile.txt`: Contains the sum of corresponding numbers from `hugefile1.txt` and `hugefile2.txt`.

Example Summary:
```text
=== Summary Report ===
File 1 Size: 6.57 MB
File 2 Size: 7.10 MB
Single-threaded Execution: 0.46 seconds
Multithreaded Execution: 15.73 seconds with 8 threads
Parallel Processing Execution: 0.59 seconds with 10 parts
```

---

## Configuration

- **Dataset Size**: Adjust the `lines_per_file` parameter to increase or decrease file sizes.
- **Thread/Process Count**:
  - Set `num_threads` for multithreaded execution.
  - Set `num_parts` for parallel processing.

---

## Recommendations for Improvement

1. Optimize multithreaded execution by integrating libraries like `concurrent.futures`.
2. Use memory-mapped files to further reduce I/O overhead.
3. Explore distributed frameworks like Apache Spark for multi-node scalability.

---

## References

1. McKinney, W. (2017). *Python for Data Analysis*. O'Reilly Media.
2. Silberschatz, A., Galvin, P., & Gagne, G. (2020). *Operating System Concepts* (10th ed.). Wiley.
3. Zaharia, M., Chowdhury, M., Das, T., & others. (2016). *Apache Spark: A Unified Engine for Big Data Processing*. ACM Press.

---


