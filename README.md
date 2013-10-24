Welcome to the **Solution_tracer** - the open-source component written in **Python**. This component is intended for checking students' input in model tracing intelligent tutoring systems (ITS).

If you don't know what a model-tracing ITS is and you know Russian, please read this article before proceeding: http://habrahabr.ru/post/194240/

To be short, a model-tracing ITS - is a system where students can enter full solutions of multi-step problems like it is shown here (this is a screenshot of Andes Physics Tutor, probably the most advanced model-tracing ITS):

![screenshot of Andes Physics Tutor](http://volga.asmon.ru/images/andes.gif)

Users of model-tracing ITS can check their solution steps for correctness, receive hints, receive grades for their solutions - all of that is done automatically.

Why would we need yet another component for tracing students' solutions? What's wrong with Andes solution subsystem? It's cool, but...Here are the answers:

1. Andes Physics Tutor is a desktop application and it is not open-source. Lots of labs all over the world keep reinventing their mini-bicycles of ITS's. **It is so sad. We should join our forces.**  We can develop this component and try to plug it in EdX (because it's open-source, too).

2. Andes algorithm of dependency checking [1] is too complicated. When you aim to find out what formulas that you know student has used to form his formula, and you use Andes method, you have to calculate gradients, generate systems of linear equations and solve some of them. This component is based on a much simpler method. Also, when using Andes method, you don't know what to do with formulas that contain vectors and matrices. Our method doesn't care about such things, it just chews them in and chews out the result.

3. As far as I know, in Andes solutions subsystem there are no heuristics for checking whether student has tried to imitate a correct step. Maybe that is because students from other countries are not such hackers as Russian students are. But in Russia we need such heuristics.

1 - [J.A.Shapiro. An Algebra Subsystem for Diagnosing Students' Input in a Physics Tutoring System](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=A4CDE3B32ABCB3250B3DF96A0612AF75?doi=10.1.1.87.9408&rep=rep1&type=pdf)
