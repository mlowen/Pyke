from . import gpp

def factory(compiler, output_type):
    if output_type not in [ 'executable', 'sharedlib', 'dynamiclib' ]:
        raise Exception('Unknown output type: %s' % output_type)
    
    if compiler == 'g++':
        if output_type == 'executable':
            return gpp.ExecutableCompiler()
        elif output_type == 'sharedlib':
            return gpp.SharedLibraryCompiler()
        elif output_type == 'dynamiclib':
            return gpp.DynamicLibraryCompiler()
    
    raise Exception('Unknown compiler: %s' % compiler)