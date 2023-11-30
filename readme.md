To get a solution, I run main.py and enter the challenge I want to run. main.py reads the appropriate challenge, gets
its input, does some preprocessing, and then prints the result of running the challenge on the input.

To do this properly, the challenges should be at paths of the form 2022/day03/day03.py, and their inputs at
2022/day03/inp.txt, relative to the location of main.py.

By default, main.py splits the input on \n before passing to the challenge. There is a mini-language providing a
variety of pre-processing options - see examples.py.