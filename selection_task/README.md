# Selection tasks

Warm-up for CAWS from CAR3S December 11, 2020

You need to do the following :-

1. Fix the bug and build ChampSim from this repository https://github.com/vishalgupta97/ChampSim-CAWS and mention the bugs.
2. Write a hello world program in C++, run it and use the instructions mentioned in README (refer Github link) to generate trace for this program, using Intel Pin tool. Compress the output trace file to .xz format.
3. Run the hello world trace file using README and report IPC number in the final stats file.

Deliverable:

Your Google form should have the following: (i) the bugs that you find on the repo., (ii) on a successful build and run, the IPC value from the final stats file.

All the best. Looking forward to the submissions !!
PS: You should use Linux based OS. We will not entertain any query related to the warm-up. Start Early. Deadline December 16 11:59 AM

## My notes

- no.l1i_pref basically means no l1 instruction prefetcher
  - The build script turns *_pref files into C++. You can edit ```{myname}_pref``` file with own algo. The build command takes ```myname``` as input to pick the right _pref file and replace it

## Debug

- First compile shows the following errors ```g!/ error:/d``` in the log to supress warnings for now
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

4. Bug4
   - Error message:
     - ChampSim-CAWS/prefetcher/llc_prefetcher.cc:2: multiple definition of `remove_this_var'; obj/prefetcher/l2c_prefetcher.o:ChampSim-CAWS/prefetcher/l2c_prefetcher.cc:2: first defined here
   - 