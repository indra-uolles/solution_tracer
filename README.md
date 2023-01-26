Welcome to the **Solution_tracer** - the open-source component written in **Python**. This component is intended for checking students' input in model tracing intelligent tutoring systems (ITS).

To be short, a model-tracing ITS - is a system where students can enter full solutions of multi-step problems like it is shown here (this is a screenshot of Andes Physics Tutor, probably the most advanced model-tracing ITS):

![screenshot of Andes Physics Tutor](http://volga.asmon.ru/images/andes.gif)

Users of model-tracing ITS can check their solution steps for correctness, receive hints, receive grades for their solutions - all of that is done automatically.

Why would we need yet another component for tracing students' solutions? What's wrong with Andes solution subsystem? It's cool, but...Here are the answers:

1. Andes Physics Tutor is a desktop application and it is not open-source. Lots of labs all over the world keep reinventing their mini-bicycles of ITS's. **It is so sad. We should join our forces.**  We can develop this component and try to plug it in EdX (because it's open-source, too).

2. Andes algorithm of dependency checking [1] is too complicated. When you aim to find out what formulas that you know student has used to form his formula, and you use Andes method, you have to calculate gradients, generate systems of linear equations and solve some of them. This component is based on a much simpler method. Also, when using Andes method, you don't know what to do with formulas that contain vectors and matrices. Our method doesn't care about such things, it just chews them in and chews out the result.

3. As far as I know, in Andes solutions subsystem there are no heuristics for checking whether student has tried to imitate a correct step. 

###Requirements

You need to install SymPy: http://sympy.org/
This project works with SymPy 0.7.2. Might work with newer versions.

###Project structure

1. Package "archive" contains Andes Physics Tutor algorithm of dependency checking (see files andes.py, test_andes.py). I realized it as it was described in [1] to examine its properties. "archive" also contains my old versions of the algorithm of dependency checking (my_method.py, deps.py, test_my_methods.py) They cover some cases of students' input but not all cases.

2. My newer version of the algorithm of dependency checking consists of code from packages "common", "progress", "solutions". To see how it works you should examine tests.py in the project root. Some tests fail, but soon I'll make them pass. Stay tuned!

###Literature

1 - [J.A.Shapiro. An Algebra Subsystem for Diagnosing Students' Input in a Physics Tutoring System](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=A4CDE3B32ABCB3250B3DF96A0612AF75?doi=10.1.1.87.9408&rep=rep1&type=pdf)


