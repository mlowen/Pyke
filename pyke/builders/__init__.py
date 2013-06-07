from . import gplusplus

def factory(compiler, output_type):
    if output_type not in [ 'executable', 'sharedlib', 'dynamiclib' ]:
        raise Exception('Unknown output type: %s' % output_type)
    
    if compiler == 'g++':
        if output_type == 'executable':
            return gplusplus.ExecutableCompiler()
        elif output_type == 'sharedlib':
            return gplusplus.SharedLibraryCompiler()
        elif output_type == 'dynamiclib':
            return gplusplus.DynamicLibraryCompiler()
    
    raise Exception('Unknown compiler: %s' % compiler)