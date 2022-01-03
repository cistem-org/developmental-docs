# **Testing**

Support for continuous integration and testing is provided under rapid development as of early 2022. The current framework uses GitHub Actions and is testing builds of the cpu code path only, using Intel icpc.

TODO: 
- add gcc and clang for additional basic linting.
- gpu support is hardware limited in github actions, and local runners are not safe. Considering alternatives.


### Unit tests

Unit tests are contained in the program:
```c++
src/programs/console_test.cpp
```

TODO:
- add logic description for the tests (test dependency, pass/fail method logic etc.)
- simple list of test cases.


The logic and limitations of the following tests are expanded on in the [testing discussion page.](../discussions/testing.md)



### Integration tests

Integration tests are contained in the program.
```c++
src/programs/samples_functional_testing.cpp
```

TODO:
- add logic description for the tests (test dependency, pass/fail method logic etc.)
- document helper classes (and also think about how the could/should be used in unit testing)
