node hou.pwd()
geo = node.geometry()

geomodule = inlinecpp.createLibrary("FTL_init", acquire_hom_lock=True, catch_crashes=True, include_dirs=[], link_libs=[], includes="""
#include <GU/GU_Detail.h>
#include <OP/OP_Director.h>


class Utils{
  public:
    static void parallelTransport(UT_Vector3 currP, UT_Vector3 parentP, UT_Vector3 parentN, UT_Vector3 parentT, UT_Vector3 &o_newN, UT_Vector3 &o_newT){
    UT_Vector3 currT;
    UT_Matrix3 parallelTransportM;
    
    currT = currP - parent;
    int k = parallelTranportM.dihedral(parenT, currT);

    }
}
