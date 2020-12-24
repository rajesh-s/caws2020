# Day 4: Performance Analysis

- [Performance tools: Prof. KV Subramaniam](#performance-tools-prof-kv-subramaniam)
  - [Questions I posted](#questions-i-posted)
- [Pre-silicon performance analysis using simulators: Dr. Kanishka Lahiri, AMD](#pre-silicon-performance-analysis-using-simulators-dr-kanishka-lahiri-amd)

## Performance tools: Prof. KV Subramaniam

![Professor KVS](images/2020-12-24-09-47-58.png)

![Where Performance profiling is necessary?](images/2020-12-24-09-11-05.png)

![Software stack impact on measurements](images/2020-12-24-09-22-06.png)

![Instrumentation based profilers](images/2020-12-24-09-35-34.png)

Tool examples:

- prof: Function calls only
- gprof: Call graphs
- htop: Thread mapping on each core
- sar: Paging/disk activity

![Instrumentation](images/2020-12-24-09-43-36.png)

![Sampling based profilers](images/2020-12-24-09-49-52.png)

![Sampling based Profilers](images/2020-12-24-09-52-05.png)

Measuring OS activity:

Peeking into the OS

Proc file system (virtual). Eg. cat /proc/cpuids
![Proc](images/2020-12-24-10-02-38.png)

Measuring microarchitectural activity:

![1](images/2020-12-24-10-04-34.png)

![2s](images/2020-12-24-10-05-12.png)

### Questions I posted

[9:35 AM] WS-Rajesh Shashi Kumar
The software impact on getting reliable performance measurements was mentioned earlier. How does one ensure that the performance instrumentation itself does not affect the accuracy of measurements? Also, for granular measurements (when there are overheads of instrumentation etc.), the OS can probably distinguish between processes, but at the cycle level I can't think of anything to be able to have the same level of granularity.

More detailed the instrumentation/measurements reduce the accuracy of time (less we can rely on the performance numbers due to overhead but more we can rely on counts). The tradeoff needs to be made. For more detailed timing, instru. should be less

## Pre-silicon performance analysis using simulators: Dr. Kanishka Lahiri, AMD

- Notion of Cycle-Accuracy: Ability of a simulator to be able to predict the cycle-by-cycle behavior of RTL
- Physical cores is called the CPU
- Cores (logical CPUs) are logical views (can be multiple) to software by simultaneous multi-threading
- "A great model is useless without proper workloads to drive it. Representativeness is key". Workloads to drive server CPU performance models:
  - SPEC CPU 2006/2017
    - Workhorse CPU throughput/speed benchmark
    - GCC/Optimizing compilers
  - Enterprise
    - SPECJbb15
    - Traditional Databases (TPC-C)
  - Cloud
    - Spark/Hadoop
    - ML
  - HPC
    - DGEMM, FFT
    - LS-Dyna3D
  - Virtualization
    - SPECVirtSC 2013
    - VMMark
  - Microbenchmarks
- Cycle acccurate simulators run at very low frequencies (~10KHz)