Wkzg is a tool to add a field 'instanceId' in C++ classes, which can serve debug purposes. Its name comes from the German word "werkzeug", which means "tool".
Such field can be useful to give an idea of which instances are associated with a problem.
Classes with higher instance ids were instantiated after classes with lower instance ids, and often when reproducing a bug the instance ids of the objects involved in the problem are going to be the same.
Obs: the tool, at its current state, makes a bunch of assumptions about the structure of the C++ code. In some cases, it does not work (e.g. when there is a bracket inside a *string* in the constructor); feel welcome to contribute
