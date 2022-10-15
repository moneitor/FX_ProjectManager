node = hou.pwd()
geo = node.geometry()

import inlinecpp

geomodule = inlinecpp.createLibrary("FTL_init", acquire_hom_lock = True, catch_crashes = True, include_dirs=[], link_dirs=[], link_libs=[], includes="""#include <GU/GU_Detail.h>
#include <GOP/GOP_Manager.h>
#include <OP/OP_Director.h>
class Utils{
    public:
        static void parallelTransport(UT_Vector3 currP, UT_Vector3 parentP, UT_Vector3 parentN, UT_Vector3 parentT, UT_Vector3 &o_newN, UT_Vector3 &o_newT){
            UT_Vector3 currT;
            UT_Matrix3 parallelTransportM;

            currT = currP - parentP;
            parallelTransportM.identity();
            int k = parallelTransportM.dihedral(parentT, currT);
            if(k==1){ // the vectors are opposed, so just rotate 180 around an arbitrary axis
                UT_Vector3 Axis = parentT+UT_Vector3(0.1,0.2,0.3);
                parallelTransportM.rotate(Axis,M_PI);
            }
            
            parentT.multiply(o_newT,parallelTransportM);
            parentN.multiply(o_newN,parallelTransportM);                
         };
};

class CS{
    public:
        CS(GU_Detail *gdp, const char *normalVar, const char *tangentVar, const GA_PointGroup* fixedGroup);
        int validate(const char *normalVar, const char *tangentVar);
        void resetProcessed();
        void initData();
        void initRestAttribs(GA_Offset parentOffset, UT_Vector3 parentN, UT_Vector3 parentT);
        GU_Detail *m_gdp;
        GA_RWHandleV3  m_NormalHandle,m_TangentHandle,m_restLocalPHandle;
        GA_RWHandleI m_processedAttHandle;
        GA_RWHandleF m_restLHandle;
        GA_RWHandleIDA m_neighboursHandle;
        UT_Array<GA_OffsetArray> m_ringzero;
        int m_error;
        const GA_PointGroup* m_fixedGroup;    
};

CS::CS(GU_Detail *gdp, const char *normalVar, const char *tangentVar,const GA_PointGroup* fixedGroup):
m_gdp(gdp),
m_error(0),
m_fixedGroup(fixedGroup){
    m_error = validate(normalVar,tangentVar);
    if(m_error!=0)
        return;    
    initData();
}

int CS::validate(const char *normalVar, const char *tangentVar){

    UT_String normalVar_str(normalVar);
    UT_String tangentVar_str(tangentVar);
    
    // check first input
    if (m_gdp==0x0) return 101;
    else{
        GA_RWAttributeRef normalVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, normalVar_str);
        GA_RWAttributeRef tangentVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, tangentVar_str);
        if (!normalVar.isValid()) return 201;
        else if (!tangentVar.isValid()) return 202;
        else{
            m_NormalHandle = normalVar.getAttribute();
            m_TangentHandle = tangentVar.getAttribute();
        }
    }
    return 0;
}

void CS::resetProcessed(){
    GA_RWAttributeRef processedAttRef(m_gdp->findIntTuple(GA_ATTRIB_POINT, "__CS__Processed"));
    m_processedAttHandle = processedAttRef;
    if (processedAttRef.isInvalid()){ // create it if it doesn't exist
            processedAttRef = m_gdp->addIntTuple(GA_ATTRIB_POINT,/*GA_SCOPE_PRIVATE,*/ "__CS__Processed", 1, GA_Defaults(0));
            m_processedAttHandle = processedAttRef;
    }
    else{ // and reset it if it does exist
        GA_Offset ptoff;
        GA_FOR_ALL_PTOFF(m_gdp, ptoff){
            m_processedAttHandle.set(ptoff,0);
        }
    }
}

void CS::initData(){
    resetProcessed();
    
    m_gdp->buildRingZeroPoints(m_ringzero, NULL);
    
    GA_Offset ptoff;
    GA_RWAttributeRef restLVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, "restL");
    if (!restLVar.isValid()) restLVar = m_gdp->addFloatTuple(GA_ATTRIB_POINT, "restL", 1, GA_Defaults(0));
    GA_RWAttributeRef restLocalPVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, "restLocalP");
    if (!restLocalPVar.isValid()) restLocalPVar = m_gdp->addFloatTuple(GA_ATTRIB_POINT, "restLocalP", 3, GA_Defaults(0));
    GA_RWAttributeRef neighboursVar = m_gdp->findIntArray(GA_ATTRIB_POINT, "neighboursOffsets");
    if (!neighboursVar.isValid()) neighboursVar = m_gdp->addIntArray(GA_ATTRIB_POINT, "neighboursOffsets");
    
    m_restLHandle = restLVar;
    m_restLocalPHandle = restLocalPVar;
    m_neighboursHandle = neighboursVar;
    GA_FOR_ALL_GROUP_PTOFF(m_gdp, m_fixedGroup, ptoff){
        m_processedAttHandle.set(ptoff,1);
        initRestAttribs(ptoff,m_NormalHandle.get(ptoff),m_TangentHandle.get(ptoff));
    }
}

void CS::initRestAttribs(GA_Offset parentOffset, UT_Vector3 parentN, UT_Vector3 parentT){
    UT_Vector3 parentP,currP,diff,parentB,restLocalP,newN,newT;
    UT_Matrix3 m;

    GA_OffsetArray &rz = m_ringzero(m_gdp->pointIndex(parentOffset));
    m_neighboursHandle.set(parentOffset,rz);
    for (exint i = 0; i < rz.entries(); i++)
    {
        if(m_processedAttHandle.get(rz(i))!=1) {
            parentP = m_gdp->getPos3(parentOffset);
            currP = m_gdp->getPos3(rz(i));
            diff = currP-parentP;
            parentB = cross(parentN,parentT); // assuming parentN and parentT are perpendicular and normalized
            //parentB.normalize();
            m(0,0) = parentN[0]; m(0,1) = parentT[0]; m(0,2) = parentB[0];
            m(1,0) = parentN[1]; m(1,1) = parentT[1]; m(1,2) = parentB[1];
            m(2,0) = parentN[2]; m(2,1) = parentT[2]; m(2,2) = parentB[2];
            restLocalP = diff*m;
            m_restLHandle.set(rz(i), diff.length());
            m_restLocalPHandle.set(rz(i), restLocalP);
            m_processedAttHandle.set(rz(i),1);
            Utils::parallelTransport(currP, parentP, parentN, parentT, newN, newT);
            initRestAttribs(rz(i),newN, newT);
        }
    }
}
""" , function_sources=[ """int cookMySop(GU_Detail *gdp, const char *fixed_group, const char *normalVar, const char *tangentVar) {
    GA_Offset ptoff,ptoffTarget;
    const GA_PointGroup* fixedGroup = 0x0;
    UT_String fixed_group_str(fixed_group);
    if(fixed_group_str.isstring()){
        GOP_Manager *GM = new GOP_Manager();
        if(GM!=0x0)
            fixedGroup = GM->parsePointGroups(fixed_group_str,GOP_Manager::GroupCreator(gdp,0));
    }
    CS cs(gdp,normalVar,tangentVar,fixedGroup);
    if (cs.m_error>0)
        return cs.m_error;
    return 0;
}"""]) 
 
returnValue = geomodule.cookMySop(geo, "`chs("fixed_group")`", "`chs("normalVar")`", "`chs("tangentVar")`")
errors_dict = {101: "First input is invalid.", 201: "Normal Attribute not found on first input", 202: "Tangent Attribute not found on first input"}
if returnValue!=0:
    raise hou.Error(errors_dict[returnValue])
