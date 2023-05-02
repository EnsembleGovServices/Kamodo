def unicode_to_latex_convertor(func):
    latex_func = "$f(x) = " + func._repr_latex_()[1:]
    return latex_func
