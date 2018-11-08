/* HOW TO EXTEND PYTHON WITH C / C++ */

/* More information?: https://docs.python.org/3.7/extending/extending.html */

/* This file Python.h already includes:
 * <stdio.h>
 * <string.h>
 * <stdlib.h>
 * It always needs to be at first, it changes headers.
 */
#include <Python.h>

static PyObject* say_hello(PyObject *self, PyObject *args)
{
        const char *name;

        /* The function PyArg_ParseTuple checks the argument types and convert them to C values,
         * it uses a template string to determine the required types of the arguemtns as well as
         * the types of the C variables into which to store the converted values.
         */
        if(!PyArg_ParseTuple(args, "s", &name))
        {
                return NULL;
        }

        fprintf(stdout, "Hello %s!\n", name);

        /* Missing Py_INCREF will result in an incorrect counting of references for
         * Py_None, which may lead the interpreter to deallocate Py_None.
         * Since Py_None is allocated statically in the Objects/objects.c file.
         */
        Py_INCREF(Py_None);
        return Py_None;
}

/* Before calling the function from the Python program, we should list its name and address 
 * in a method table.
 */
static PyMethodDef HelloMethods[] =
{
        /* The third entry METH_VARARGS is a flag telling the interpreter the calling convention
         * to be used for the C function. It should normally be METH_VARARGS or METH_VARARGS | METH_KEYWORDS;
         * a value of 0 means that an obsolete variant of PyArg_ParseTuple is used.
         * If only using METH_VARARGS, the function should expect Python-level parameters to be
         * passed in as a tuple acceptable for parsing via PyArg_ParseTuple.
         * The METH_KEYWORDS may be set if keywords arguments should be passed to the function.
         * In this case, the C function should accept a third PyObject * parameter which will be 
         * a dictionary of keywords, use PyArg_PareTupleAndKeywords() to parse the arguments to
         * such a function.
         */
        {"say_hello", say_hello, METH_VARARGS, "Greet somebody"},
        {NULL, NULL, 0, NULL}
};

/* This structure must be passed to the interpreter in the module's initialization function, the 
 * initialization function must be named PyInit_name(), where name is the name of the module, and
 * should be the only non-static item defined in the module file.
 */
static struct PyModuleDef hello =
{
        PyModuleDef_HEAD_INIT,
        "hello", /* name of the module*/
        NULL, /* module documentation*/
        -1, /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables*/
        HelloMethods /* this is the reference to the method table*/
};

/* This is the initialization function, MUST be non-static, and it will receive the PyModuleDef structure.
 * The PyMODINIT_FUNC declares the functions as PyObject * return type, declares any special linkage 
 * declarations required by the platform.
 */
PyMODINIT_FUNC PyInit_hello(void)
{
        return PyModule_Create(&hello);
}

/* When creating the setup.py file to build the extension for Python, there are some parameters to pass through:
 *
 * setup.py:
 *
 * from distutils.core import setup, Extension
 * module1 = Extension('hello', sourcers = ['hellomodule.c'])
 * setup(name = 'PackageName'. version = '1.0', description = 'This is a nice description', ext_modules = [module1])
 *
 * Then, we can build our module with:
 * python setup.py build
 *
 * The file will be saved in build/lib.linux-x_86-x-y, we should go to that folder and run our file or our shell.
 *
 * And run the module, with test.py or in an interactive shell:
 *
 * >> import hello
 * >> hello.say_hello("Emilio")
 * Hello Emilio!
 * >>
 */
 

 