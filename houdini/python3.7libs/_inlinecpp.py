'''
This module lets you write functions in C++ that are accessible from Python.
When necessary, your C++ code is automatically compiled into a library and
the library is loaded, but the code won't be compiled when the library already
exists, and the library won't be reloaded when it's already loaded.

NOTE: The Python ctypes module does not support 64-bit Windows in Python 2.5,
      so this module requires Python 2.6 on 64-bit Windows.

Consider this example:
    mymodule = inlinecpp.createLibrary(
        name="example_string_library",
        includes="#include <UT/UT_String.h>",
        function_sources=[
    """
    int matchesPattern(const char *str, const char *pattern)
    {
        return UT_String(str).multiMatch(pattern);
    }
    """])

    string = "one"
    for pattern in "o*", "x*", "^o*":
        print "%s matches %s: %s" % (repr(string), repr(pattern),
            bool(mymodule.matchesPattern(string, pattern)))

The call to inlinecpp.createLibrary receives your C++ source code and returns a
module-like object (assigned to the variable mymodule).  You can then call
mymodule.matchesPattern to invoke the corresponding C++ function.  If you
forget which parameters to pass to matchesPattern, you can get the C++
signature with:
    >>> mymodule.matchesPattern.signature()
    'int matchesPattern(const char * str, const char * pattern)'

Note that subsequent calls to createLibrary with the exact same parameters will
not recompile your module, and will not reload it if it's been loaded in the
current session.

This module uses the hcustom HDK tool to compile your C++ code.  If your
code contains a compiler error, it raises a CompilerError exception.  You can
compile your code with debugging enabled by passing debug=True to
createLibrary.

If you want to check for compiler warnings, call the _compiler_output method
of the module-like object.  Note that if the library was already compiled when
it was loaded, calling _compiler_output will force it to be recompiled.
    >>> print mymodule._compiler_output()
    Making /home/user/houdiniX.Y/inlinecpp/example_string_library_Linux_x86_64_j5c9Dz
    T525OU0VdJ5uL0kw.o and /home/user/houdiniX.Y/inlinecpp/example_string_library_Lin
    ux_x86_64_j5c9DzT525OU0VdJ5uL0kw.so from /home/user/houdiniX.Y/inlinecpp/example_
    string_library_Linux_x86_64_j5c9DzT525OU0VdJ5uL0kw.C


Your C++ functions may have the following parameter types:
    int
    float              (pass a Python float)
    double             (pass a Python float)
    const char *       (pass a Python str object)
    bool               (Python 2.6 and up only)
    GU_Detail *        (pass a hou.Geometry object from inside a Python sop)
    const GU_Detail *  (pass a hou.Geometry object)
    OP_Node *          (pass a hou.Node object)
    CHOP_Node *        (pass a hou.ChopNode)
    COP2_Node *        (pass a hou.CopNode)
    DOP_Node *         (pass a hou.DopNode)
    OBJ_Node *         (pass a hou.ObjNode)
    ROP_Node *         (pass a hou.RopNode)
    SHOP_Node *        (pass a hou.ShopNode)
    SOP_Node *         (pass a hou.SopNode)
    VOP_Node *         (pass a hou.VopNode)
    VOPNET_Node *      (pass a hou.VopNetNode)
    OP_Operator *      (pass a hou.NodeType)
    PRM_Tuple *        (pass a hou.ParmTuple)
    CL_Track *         (pass a hou.Track)
    const SIM_Data *   (pass a hou.DopData)
    UT_Vector2D *      (pass a hou.Vector2)
    UT_Vector3D *      (pass a hou.Vector3)
    UT_Vector4D *      (pass a hou.Vector4)
    UT_DMatrix3 *      (pass a hou.Matrix3)
    UT_DMatrix4 *      (pass a hou.Matrix4)
    UT_BoundingBox *   (pass a hou.BoundingBox)
    UT_Color *         (pass a hou.Color)
    UT_QuaternionD *   (pass a hou.Quaternion)

Your C++ functions may have one of the following return values:
    void
    int
    float
    double
    const char *       (a null-terminated string that will not be freed)
    char *             (a null-terminated string that will be freed with free())
    bool               (Python 2.6 and up only)


The shared library file (.so on Linux, .dll on Windows, and .dylib on Mac) is
put in your $HOME/houdiniX.Y/inlinecpp directory.  It is named
    <name>_<platform>_<processor>_<houdini_version>_<checksum>.{so|dll|dylib}
where the name is the name you pass to createLibrary and the checksum is based
on the C++ source code.  When you change the source code, the shared library
name will be different, and this module recompiles the new library and
automatically deletes any old libraries.  As long as the C++ source code
doesn't change (for example, if it's embedded inside a digital asset), you can
be sure the checksum won't change and you can distribute the library within
your facility as you would with any other HDK library.

For more information and examples, see the "Extending with C++" subsection of
the "Houdini Object Module" section of Houdini's documentation.
'''

from __future__ import with_statement
import sys
import os
import types
import itertools
import struct
import platform
import re
import ctypes


shared_path = os.path.join(os.path.dirname(os.path.dirname(__file__))  , "inlinecpp").replace("\\", "/")

import hutil.cppinline
import hou

if platform.system() == "Windows" and sys.version_info[:2] == (2, 5):
    raise ImportError("inlinecpp requires Python 2.6 or greater on Windows")

#-----------------------------------------------------------------------------
# Code related to running hcustom:

class HcustomCompilerHook(hutil.cppinline.CompilerHook):
    def default_shared_library_directory(self):
        result =  "%s/%s" % (hou.homeHoudiniDirectory(), self._houdini_path_subdir_name())    
        result = shared_path    

        print ("Folder for compilation: {}".format(shared_path))
        return result


    def _houdini_path_subdir_name(self):
        return "inlinecpp"

    def find_shared_library(self, shared_library_file_name):
        try:
            return hou.findFile("%s/%s" % (
                self._houdini_path_subdir_name(), shared_library_file_name))
        except hou.OperationFailed:
            pass

        return hutil.cppinline.CompilerHook.find_shared_library(
            self, shared_library_file_name)

    def get_compile_command(
            self, cpp_file_path, output_shared_library_path, debug,
            include_dirs, link_dirs, link_libs):
        if platform.system() == "Windows":
            include_dir_format = "-I \"%s\" "
            lib_dir_format = "-L \"%s\" "
            lib_format = "-l %s "
        else:
            include_dir_format = "-I'%s' "
            lib_dir_format = "-L'%s' "
            lib_format = "-l%s "

        debug_option = ("-g " if debug else "")
        include_dirs_option = "".join(
            include_dir_format % include_dir for include_dir in include_dirs)

        link_dirs_option = "".join(
            lib_dir_format % link_dir for link_dir in link_dirs)

        link_libs_option = "".join(
            lib_format % link_lib for link_lib in link_libs)

        print ("include_dirs_option: {}".format(include_dirs_option))
        print ("link_dirs_option: {}".format(link_dirs_option))
        print ("link_libs_option: {}".format(link_libs_option))
        


        return "hcustom -i %s %s%s" % (
            self.default_shared_library_directory(),
                debug_option + include_dirs_option + link_dirs_option +
                    link_libs_option,
                cpp_file_path)

    def clean_up_after_compiling(
            self, cpp_file_path, output_shared_library_path, debug,
            include_dirs, link_dirs, link_libs):
        if platform.system() != "Windows":
            return

        # hcustom on windows leaves ".exp" and ".lib" files in the current
        # directory.
        for extension in ".lib", ".exp":
            self._delete_if_exists(self._replace_extension(
                os.path.basename(cpp_file_path), extension))

    def _replace_extension(self, file_path, new_extension):
        return os.path.splitext(file_path)[0] + new_extension

    def _delete_if_exists(self, file_path):
        try:
            os.unlink(file_path)
        except OSError:
            pass

#-----------------------------------------------------------------------------
# Code to convert from Python hou objects to C++ HDK objects.

# Going to a [const] GU_Detail * from a hou.Geometry object is more
# complicated than other types, since we need to hold onto the
# GeoDetailHandleWrapper for the duration of the call and release it only
# after the call.
class ConstGU_DetailHandle(hutil.cppinline.ConverterHandle):
    def __init__(self, geometry):
        hutil.cppinline.ConverterHandle.__init__(self, geometry, hou.Geometry)

        # Hold a GeoDetailHandleWrapper object until the call completes so
        # that a GU_DetailHandle can be locked for the duration of the call,
        # ensuring we have valid access to its GU_Detail.
        self.gu_detail_handle = geometry._guDetailHandle()

    def as_pointer(self):
        return self.gu_detail_handle._asVoidPointer()

    def destroy(self):
        self.gu_detail_handle.destroy()

class GU_DetailHandle(ConstGU_DetailHandle):
    def __init__(self, geometry):
        ConstGU_DetailHandle.__init__(self, geometry)

        # Make sure they're not trying to pass a read-only geometry object to
        # something expecting a non-const pointer.
        if self.gu_detail_handle.isReadOnly():
            self.gu_detail_handle.destroy()
            raise hou.GeometryPermissionError(
                "You cannot pass a read-only hou.Geometry object"
                " to a function expecting a non-const GU_Detail *")

def _hou_object_to_hdk_pointer(hou_object):
    return hou_object._asVoidPointer()

_hou_classes_and_hdk_conversions = (
    (hou.Node, "OP_Node"),
    (hou.ChopNode, "CHOP_Node"),
    (hou.CopNode, "COP2_Node"),
    (hou.DopNode, "DOP_Node"),
    (hou.LopNode, "LOP_Node"),
    (hou.ObjNode, "OBJ_Node"),
    (hou.RopNode, "ROP_Node"),
    (hou.ShopNode, "SHOP_Node"),
    (hou.SopNode, "SOP_Node"),
    (hou.VopNode, "VOP_Node"),
    (hou.VopNetNode, "VOPNET_Node"),
    (hou.ParmTuple, "PRM_Parm"),
    (hou.NodeType, "OP_Operator"),
    (hou.NodeTypeCategory, "OP_OperatorTable"),
    (hou.Track, "CL_Track"),
    # TODO: It would be nice to force them to accept only a const SIM_Data *.
    #       We could probably do this with a custom conversion function or
    #       a handle class.
    (hou.DopData, "SIM_Data"),
    (hou.Vector2, "UT_Vector2T<double>"),
    (hou.Vector3, "UT_Vector3T<double>"),
    (hou.Vector4, "UT_Vector4T<double>"),
    (hou.Matrix3, "UT_Matrix3T<double>"),
    (hou.Matrix4, "UT_Matrix4T<double>"),
    (hou.BoundingBox, "UT_BoundingBoxT<double>"),
    (hou.Color, "UT_Color"),
    (hou.Quaternion, "UT_QuaternionT<double>"),
    (hou.Ramp, "UT_Ramp"),
)

_hou_classes_to_cpp_class_names = dict(_hou_classes_and_hdk_conversions)
_hou_classes_to_cpp_class_names[hou.Geometry] = "GU_Detail"

_cppinline_config = None
def _get_cppinline_config():
    # For speed, we cache a copy of the config and reuse it.
    global _cppinline_config
    if _cppinline_config is None:
        _cppinline_config = _create_cppinline_config()
    return _cppinline_config

def _create_cppinline_config():
    config = hutil.cppinline.Config()
    config.compiler_hook = HcustomCompilerHook()

    # The output file name includes the Houdini build number so that it will
    # recompile the code if they upgrade Houdini, in case there are API
    # mismatches.
    config.version_info_string = hou.applicationVersionString()

    # On Windows, whether we're running in a debug interpreter matters so
    # include whether sys.gettotalrefcount exists because it is only present on
    # debug builds.
    if platform.system() == "Windows" and hasattr(sys, 'gettotalrefcount'):
        config.version_info_string += '_debug'

    # We can use this callback to change the source to create a HOM_AutoLock,
    # if the caller wants that.
    config.cpp_source_filtering_function = None

    # Try to catch crashes when calling the C++ function and convert them into
    # Python exceptions.  Otherwise, Houdini will crash.
    config.error_trapping_function = hou.runCallbackAndCatchCrashes

    # Note that we #include HOM_Module.h so they can use HOM_AutoLock.
    config.cpp_source_boilerplate_prefix = (
        "#include <UT/UT_DSOVersion.h>\n" +
        "#include <HOM/HOM_Module.h>\n")

    for hou_class, hdk_type_name in _hou_classes_and_hdk_conversions:
        config.register_type_conversion(
            hou_class, hdk_type_name, lambda obj: obj._asVoidPointer())

    config.register_handle_type("const GU_Detail *", ConstGU_DetailHandle)
    config.register_handle_type("GU_Detail *", GU_DetailHandle)

    config.known_typedefs_dict = {
        "UT_Vector2D": "UT_Vector2T<double>",
        "UT_Vector3D": "UT_Vector3T<double>",
        "UT_Vector4D": "UT_Vector4T<double>",
        "UT_DMatrix3": "UT_Matrix3T<double>",
        "UT_DMatrix4": "UT_Matrix4T<double>",
        "UT_BoundingBoxD": "UT_BoundingBoxT<double>",
        "UT_QuaternionD": "UT_QuaternionT<double>",
    }

    return config

_cppinline_config = _create_cppinline_config()

#-----------------------------------------------------------------------------
# Code for the publicly-visible functions.

def createLibrary(
        name, includes="", function_sources=(), debug=False,
        catch_crashes=None, acquire_hom_lock=False, structs=(),
        include_dirs=(), link_dirs=(), link_libs=(), config=None):
    # Get the configuration object that is tailored to Houdini.  If we're
    # supposed to acquire the HOM lock, set up a function to filter the source.
    if config is None:
        config = _get_cppinline_config()

    config.cpp_source_filtering_function = (
        (lambda source: source.replace(
            "{", "{\n    HOM_AutoLock _hom_lock;", 1))
        if acquire_hom_lock else None)

    return hutil.cppinline.create_library(
        name=name, includes=includes, function_sources=function_sources,
        debug=debug, catch_crashes=catch_crashes, structs=structs,
        include_dirs=include_dirs, link_dirs=link_dirs, link_libs=link_libs, 
        config=config)

createLibrary.__doc__ = hutil.cppinline.create_library.__doc__ + """
    acquire_hom_lock:
        If True, the code will be automatically modified to use a HOM_AutoLock,
        to ensure threadsafe access to the C++ object when the Python code
        is being run in a separate thread.  If your code modifies Houdini's
        internal state, set this parameter to True.
"""

def extendClass(
        cls, library_name, includes="", function_sources=(), debug=False,
        catch_crashes=None, structs=(), auto_add_include=True, include_dirs=(),
        link_dirs=(),
        link_libs=(),
        config=None):
    """Extend a hou class by adding methods implemented in C++.

    cls is the hou module class you're extending.  The rest of the arguments
    are the same as for createLibrary, except acquire_hom_lock is always True.
    Note that this function automatically adds a `#include` line for the
    underlying C++ class unless auto_add_include is False.

    The first parameter to your C++ functions must be a pointer to a C++ object
    corresponding to the hou object.  See the module documentation for the
    mapping from hou classes to C++ HDK classes.

    Note that if you are passing hou.Geometry objects, you must provide a
    const GU_Detail * if it can be called on a read-only hou.Geometry object
    and a GU_Detail * only if it can only be called on a hou.Geometry object
    from within a Python SOP.
    """
    # Setting catch_crashes to None indicates that it should be the same value
    # as debug.
    if catch_crashes is None:
        catch_crashes = debug

    try:
        cpp_class_name = _hou_classes_to_cpp_class_names[cls]
    except KeyError:
        raise TypeError("This class cannot be extended")

    if auto_add_include:
        # Automatically include the header for this class.
        includes = ("#include <%s/%s.h>\n" % (
                cpp_class_name[:cpp_class_name.index("_")], cpp_class_name) +
            includes)

    library = createLibrary(
        library_name, includes, function_sources, debug, catch_crashes,
        acquire_hom_lock=True, structs=structs, include_dirs=include_dirs,
        link_dirs=link_dirs, link_libs=link_libs, config=config)

    for function in library._functions:
        if sys.version_info.major >= 3:
            def _CPPFunctionWrapper(*args, **kwargs):
                return function(*args, **kwargs)

            unbound_method = _CPPFunctionWrapper
        else:
            unbound_method = types.MethodType(function, None, cls)
        setattr(cls, function.name, unbound_method)

