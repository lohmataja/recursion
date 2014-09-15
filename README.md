Recursion.
==================
This project explores a variety of ways to optimize recursion in Python.
 So far, the following approaches have been explored:
Trampolines.
-----------------
TCO using Python standard means. Taking a tail-recursive function that returns a thunk in place of a recursive call, the trampoline function keeps calling the thunked result until a non-callable value is reached.
>Associated files:<br>
>trampolines.py - all source code for trampolines<br>
>trampolines_in_Python.ipynb

AST trampolines.
--------------------------------
TCO by manipulating AST of the function (with Paul Tagliamonte).
The ast of the tail-recursive function is altered so that all returns are "thunked", a trampolining decorator is injected into the tree.
>Associated files:<br>
>ast_trampoline.py

Tailbytes.
---------
TCO using direct bytecode manipulation (with Allison Kaptur).
By swapping the bytecode representation of a tail-recursive function, the recursive call is substituted by resetting the variables and jumping to the beginning of the function.
Problems we've faced and resolved so far:

* _Problem:_ Deleting and inserting bytes into the bytecode changes the location of the original bytes. 
_Solution:_ Absolute jumps are updated after bytecode alternation has been performed.
* _Problem:_ Our initial algorithm was removing all calls to *any* function. This caused a problem if the function involve non-recursive function calls.
_Solution:_ Remove a CALL_FUNCTION instruction only if it is a part of the recursive call (to determine that, we keep track of the stack size). We target the CALL_FUNCTION instructions which return the stack to the same size that it had when the recursive function was loaded onto it.

>Associated files:<br>
>tailbytes.py<br>
>stack_heights.py<br>
>See also [presentation slides](http://www.slideshare.net/lnikolaeva/tailbytes-pygotham)

Transform regular recursion into tail recursion.
-------------------------------
Interpreter that reads an ast representation of a regular recursion and mutates it to a tree that compiles to the same function using tail recursion.
>Associated files:<br>
>translator.py

Further goals:
--------
* Transform binary recursion (i.e. fibonacci-like functions) into tail-recursion.
* Find a way to optimize mutual recursion.

Tools:
-----------
* ast_pretty_printer.py<br>
print_ast takes an ast tree and prettyprints it, working off of ast.dump
