<!--notoc-->
# Selection task: ChampSim-CAWS

Rajesh Shashi Kumar (rajesh109876@gmail.com)

- [Bugs in building ChampSim](#bugs-in-building-champsim)
- [Tracer and PINtools](#tracer-and-pintools)

## Bugs in building ChampSim

- First compile shows the following errors. Using ```g!/ error:/d``` in the log to supress warnings for now
- I recorded the compile logs each time using the linux ```script <filename>``` command and some post processing to remove weird characters ```cat compile_log2 | perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' | col -b > compilelog2```

1. Bug1: Incorrectly defined value_type on line 317 in main.cc. Needs to be of type <uint64_t, uint64_t> page_table
   - Error message: src/main.cc:317:57: error: conversion from ‘_Rb_tree_iterator<pair<[...],long unsigned int>>’ to non-scalar type ‘_Rb_tree_iterator<pair<[...],char>>’ requested
   - Fix 1
     - page_table is of the type <uint64_t, uint64_t> page_table
     - The value type on line 317 reads char instead, map <uint64_t, char>::iterator pr = page_table.begin();
   - To fix, I changed this to map <uint64_t, uint64_t>::iterator pr = page_table.begin();

== Compiled again with fix1 ==

2. Bug2: page_table.end/begin() map function call missing parantheses
   - Issues of this type:
     - page_table.end() on lines (in main.cc) 330,339,351,457
     - page_table.begin() on lines (in main.cc) 339
   - Error message: src/main.cc:330:12: error: no match for ‘operator==’ (operand types are ‘std::map<long unsigned int, long unsigned int>::iterator’ {aka ‘std::_Rb_tree_iterator<std::pair<const long unsigned int, long unsigned int> >’} and ‘<unresolved overloaded function type>’)
   - Fix 2
     - Line 330 reads  if (pr == page_table.end) { // no VA => PA translation found
     - end() is a built-in function of map. Function call is missing parantheses

== Compiled again with fix2 ==

3. Bug3: Misspelled member functions (erase,insert) of map
   - Error message:
     - src/main.cc:360:24: error: ‘class std::map<long unsigned int, long unsigned int>’ has no member named ‘erse’; did you mean ‘erase’? 360 | page_table.erse(pr);
     - src/main.cc:361:24: error: ‘class std::map<long unsigned int, long unsigned int>’ has no member named ‘isert’; did you mean ‘insert’? 361 | page_table.isert(make_pair(vpage, mapped_ppage));
     - src/main.cc:430:24: error: ‘class std::map<long unsigned int, long unsigned int>’ has no member named ‘inset’; did you mean ‘insert’? 430 | page_table.inset(make_pair(vpage, random_ppage));
   - Fix 3
     - The misspelled function of map corrected for insert and erase

== Compiled again with fix3 ==

4. Bug4: Stray variable remove_this_var declared in multiple files that all contain separated (for ease of configuration) function definitions outside the CACHE class. The Makefile picks all 4 generated (from *pref) cc files (eg:llc_prefetcher.cc) for compilation, creating redundant definitions
   - Error message:
     - ChampSim-CAWS/prefetcher/llc_prefetcher.cc:2: multiple definition of `remove_this_var'; obj/prefetcher/l2c_prefetcher.o:ChampSim-CAWS/prefetcher/l2c_prefetcher.cc:2: first defined here
   - Fix
     - The *pref file contains functions defined outside the CACHE class. The build script copies *pref files to *.cc to pick the right configuration.
     - Removing the variable declaration from the 3 files no.l1d_pref, no.l1i_pref, no.l2c_pref resolves the error in build. Removed it from the 4th file (no.llc_pref) as well since this variable is not used anywhere

== Build clean! ==

## Tracer and PINtools

The runs was attempted with the following settings:

- Number of instructions for detailed simulation (10 million)
- Number of instructions for warmup (1 million)
- lscpu: i7-4700MQ
- PIN tool version 3.17 (PIN3.2 is dated has issues on newer linux kernels such as [1](https://github.com/ChampSim/ChampSim/issues/102),[2](https://stackoverflow.com/questions/55698095/intel-pin-tools-32-bit-processsectionheaders-560-assertion-failed),[3](https://stackoverflow.com/questions/43589174/pin-tool-segmentation-fault-for-ubuntu-17-04)). ChampSim tracer works fine with 3.17

Ubuntu 20.04.1 LTS (Compiler: g++ 9.3.0; Linux Kernel: 5.4.0-54-generic)
*** Reached end of trace for Core: 0 Repeating trace: /home/rajesh/work/CAWS/fixes/ChampSim-CAWS/dpc3_traces/hello_world.trace.xz
Finished CPU 0 instructions: 10000000 cycles: 8891568 cumulative IPC: 1.12466 (Simulation time: 0 hr 0 min 20 sec)