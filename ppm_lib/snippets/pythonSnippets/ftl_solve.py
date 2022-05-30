node = hou.pwd()
geoOne = node.geometry()

dummyException = 0;

inputs = node.inputs()
try:
    geoTwo = inputs[1].geometry()
except IndexError:
    dummyException = 0;
try:
    geoThree = inputs[2].geometry()
except IndexError:
    dummyException = 0;

import inlinecpp

geomodule = inlinecpp.createLibrary("FTL_solve_v4", acquire_hom_lock = True, catch_crashes = True, include_dirs=[], link_dirs=[], link_libs=[], includes="""#include <GU/GU_Detail.h>
#include <GOP/GOP_Manager.h>
#include <OP/OP_Director.h>
#define EPSILOM 0.0001
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
        CS(GU_Detail *gdp, const GU_Detail *gdp2, const GU_Detail *gdp3, const char *normalVar, const char *tangentVar, const GA_PointGroup* fixedGroup, 
            float enforceLength, float enforceAngle, int substeps, int outputDampedV, float minDampCoeff, float maxDampCoeff,
            int adaptiveEnforceAngle, float adaptiveEnforceAngle_lowerThreshold, float adaptiveEnforceAngle_upperThreshold,
            int angleLimit, float angleLimit_lowerThreshold, float angleLimit_upperThreshold, float angleLimit_lowerLimit, float angleLimit_upperLimit);
        int validate(const char *normalVar, const char *tangentVar);
        void resetProcessed();
        void solve();
        void getLeadersAnim();
        void processAll(GA_Offset ptoff,float dampingCoeff,int leader);
        UT_Vector3 processPoint(GA_Offset ptoff, GA_Offset parentOffset, float dampingCoeff);
        fpreal lerp( fpreal a, fpreal b, fpreal bias){ return (1-bias)*a + bias*b; }
        GU_Detail *m_gdp;
        const GU_Detail *m_gdp2,*m_gdp3;
        GA_RWHandleV3  m_NormalHandle,m_TangentHandle,m_velHandle,m_velDampedHandle,m_localPHandle;
        GA_ROHandleV3 m_restLocalPHandle, m_NormalHandleRef, m_TangentHandleRef, m_NormalHandleTarget, m_TangentHandleTarget, m_VelHandleTarget;
        GA_RWHandleI m_processedAttHandle;
        GA_ROHandleF m_restLHandle;
        GA_ROHandleIDA m_neighboursHandle;
        int m_error, m_substeps, m_outputDampedV, m_adaptiveEnforceAngle, m_angleLimit;
        const GA_PointGroup* m_fixedGroup;
        float m_enforceLength, m_enforceAngle, m_minDampCoeff, m_maxDampCoeff, m_samplesPerSec; 
        float m_adaptiveEnforceAngle_lowerThreshold, m_adaptiveEnforceAngle_upperThreshold;
        float m_angleLimit_lowerThreshold, m_angleLimit_upperThreshold, m_angleLimit_lowerLimit, m_angleLimit_upperLimit;
};

CS::CS(GU_Detail *gdp, const GU_Detail *gdp2, const GU_Detail *gdp3, const char *normalVar, const char *tangentVar,const GA_PointGroup* fixedGroup, 
        float enforceLength, float enforceAngle, int substeps, int outputDampedV, float minDampCoeff, float maxDampCoeff,
        int adaptiveEnforceAngle, float adaptiveEnforceAngle_lowerThreshold, float adaptiveEnforceAngle_upperThreshold,
        int angleLimit, float angleLimit_lowerThreshold, float angleLimit_upperThreshold, float angleLimit_lowerLimit, float angleLimit_upperLimit):
m_gdp(gdp),
m_gdp2(gdp2),
m_gdp3(gdp3),
m_error(0),
m_fixedGroup(fixedGroup),
m_enforceLength(enforceLength),
m_enforceAngle(enforceAngle),
m_substeps(substeps),
m_outputDampedV(outputDampedV),
m_minDampCoeff(minDampCoeff),
m_maxDampCoeff(maxDampCoeff),
m_adaptiveEnforceAngle(adaptiveEnforceAngle),
m_angleLimit(angleLimit),
m_adaptiveEnforceAngle_lowerThreshold(adaptiveEnforceAngle_lowerThreshold),
m_adaptiveEnforceAngle_upperThreshold(adaptiveEnforceAngle_upperThreshold),
m_angleLimit_lowerThreshold(angleLimit_lowerThreshold),
m_angleLimit_upperThreshold(angleLimit_upperThreshold),
m_angleLimit_lowerLimit(angleLimit_lowerLimit*M_PI/180),
m_angleLimit_upperLimit(angleLimit_upperLimit*M_PI/180){
    //std::cout<<"initializing "<<std::endl;
    m_error = validate(normalVar,tangentVar);
    if(m_error!=0)
        return;    
    resetProcessed();
    m_samplesPerSec = m_substeps*OPgetDirector()->getChannelManager()->getSamplesPerSec();
}

int CS::validate(const char *normalVarName, const char *tangentVarName){

    if (m_gdp==0x0) return 101;
    if (m_gdp2==0x0) return 102;
    if (m_gdp3==0x0) return 103;
    
    UT_String normalVar_str(normalVarName);
    UT_String tangentVar_str(tangentVarName);
    
    
    
    if(m_gdp->getNumPoints() != m_gdp2->getNumPoints())
        return 501;
    if(m_gdp->getNumPoints() != m_gdp3->getNumPoints())
        return 502;
        
    // check first input attribs
    GA_RWAttributeRef normalVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, normalVar_str);
    GA_RWAttributeRef tangentVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, tangentVar_str);
    if (!normalVar.isValid()) return 201;
    else if (!tangentVar.isValid()) return 202;
    else{
        m_NormalHandle = normalVar.getAttribute();
        m_TangentHandle = tangentVar.getAttribute();
    }
    
    // check second input attribs
    GA_ROAttributeRef normalVarRef = m_gdp2->findFloatTuple(GA_ATTRIB_POINT, normalVar_str);
    GA_ROAttributeRef tangentVarRef = m_gdp2->findFloatTuple(GA_ATTRIB_POINT, tangentVar_str);
    if (!normalVarRef.isValid()) return 301;
    else if (!tangentVarRef.isValid()) return 302;
    else{
        m_NormalHandleRef = normalVarRef.getAttribute();
        m_TangentHandleRef = tangentVarRef.getAttribute();
    }
    
    // check third input attribs
    GA_ROAttributeRef normalVarTarget = m_gdp3->findFloatTuple(GA_ATTRIB_POINT, normalVar_str);
    GA_ROAttributeRef tangentVarTarget = m_gdp3->findFloatTuple(GA_ATTRIB_POINT, tangentVar_str);
    GA_ROAttributeRef velVarTarget = m_gdp3->findFloatTuple(GA_ATTRIB_POINT, "v");
    if (!normalVarTarget.isValid()) return 301;
    else if (!tangentVarTarget.isValid()) return 302;
    else{
        m_NormalHandleTarget = normalVarTarget.getAttribute();
        m_TangentHandleTarget = tangentVarTarget.getAttribute();
        if (velVarTarget.isValid()) m_VelHandleTarget = velVarTarget.getAttribute();
    }
    
    GA_ROAttributeRef restLVarRef = m_gdp2->findFloatTuple(GA_ATTRIB_POINT, "restL");
    if (!restLVarRef.isValid()) return 401;
    
    GA_ROAttributeRef restLocalPVarRef = m_gdp2->findFloatTuple(GA_ATTRIB_POINT, "restLocalP");
    if (!restLocalPVarRef.isValid()) return 402;
    
    GA_ROAttributeRef neighboursVar = m_gdp2->findIntArray(GA_ATTRIB_POINT, "neighboursOffsets");
    if (!neighboursVar.isValid()) return 403;
    
    GA_RWAttributeRef velVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, "v");
    if (!velVar.isValid()) velVar = m_gdp->addFloatTuple(GA_ATTRIB_POINT, "v", 3, GA_Defaults(0));
    
    m_restLHandle = restLVarRef;
    m_restLocalPHandle = restLocalPVarRef;
    m_velHandle = velVar;
    m_neighboursHandle = neighboursVar;
    
    if(m_enforceAngle>EPSILOM)
    {
        GA_RWAttributeRef localPVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, "localP");
        if (!localPVar.isValid()) localPVar = m_gdp->addFloatTuple(GA_ATTRIB_POINT, "localP", 3, GA_Defaults(0));
        m_localPHandle = localPVar;
    }
    
    if(m_outputDampedV){
        GA_RWAttributeRef velDampedVar = m_gdp->findFloatTuple(GA_ATTRIB_POINT, "v_damped");
        if (!velDampedVar.isValid()) velDampedVar = m_gdp->addFloatTuple(GA_ATTRIB_POINT, "v_damped", 3, GA_Defaults(0));
        m_velDampedHandle = velDampedVar;
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

void CS::solve(){
    GA_Offset ptoff;
    float r;
    resetProcessed();
    getLeadersAnim();
    
    GA_FOR_ALL_GROUP_PTOFF(m_gdp, m_fixedGroup, ptoff){
        m_processedAttHandle.set(ptoff,1);
        if(m_outputDampedV){
            srand (m_gdp->pointIndex(ptoff)); // random value for each leader
            r = ((double) rand() / (RAND_MAX));
            r = m_minDampCoeff + r*(m_maxDampCoeff-m_minDampCoeff);
        }
        else
            r = 0;
        processAll(ptoff,r,1);
    }
}

void CS::getLeadersAnim(){
    GA_Offset ptoff,ptoffTarget;
    UT_Vector3 targetN, targetT;
    GA_FOR_ALL_GROUP_PTOFF(m_gdp, m_fixedGroup, ptoff){
        ptoffTarget = m_gdp3->pointOffset(m_gdp->pointIndex(ptoff));
        m_gdp->setPos3(ptoff, m_gdp3->getPos3(ptoffTarget)); // inherit P
        targetN = m_NormalHandleTarget.get(ptoffTarget); // no need to normalize, assuming N input is normalized
        targetT = m_TangentHandleTarget.get(ptoffTarget); // no need to normalize, assuming T input is normalized 
        m_NormalHandle.set(ptoff, targetN); // inherit N
        m_TangentHandle.set(ptoff, targetT); // inherit T
        
        if (m_VelHandleTarget.isValid()) // vel is valid
            m_velHandle.set(ptoff, m_VelHandleTarget.get(ptoffTarget)); // inherit v
    }
}

void CS::processAll(GA_Offset ptoff, float dampingCoeff, int leader){
    
    GA_OffsetArray rz;
    m_neighboursHandle.get(ptoff,rz);
    UT_Vector3 delta(0,0,0), totalDelta(0,0,0);
    bool leafPt = true;
    int totalChildren = 0;
    for (int i = 0; i < rz.entries(); i++){
        if(m_processedAttHandle.get(rz(i))!=1){ // if it is not processed already, process it
            leafPt = false;
            delta = processPoint(rz(i), ptoff, dampingCoeff);
            totalDelta+=delta;
            totalChildren++;
        }
    }
    
    if(m_outputDampedV && !leader){
        UT_Vector3 damping(0,0,0), updatedVel(0,0,0);
        if(!leafPt) damping = dampingCoeff*(-totalDelta*m_samplesPerSec)/totalChildren;
        updatedVel = m_velHandle.get(ptoff)+damping;
        m_velDampedHandle.set(ptoff, updatedVel);
    }
}

UT_Vector3 CS::processPoint(GA_Offset ptoff, GA_Offset parentOffset, float dampingCoeff){
    UT_Vector3 parentP,parentN,parentT,parentB,currP,currV,newP;
    UT_Vector3 newN, newT,currT, localP, restLocalP, Axis;
    fpreal restL,currL,dotProd,dotProd_;
    UT_Matrix3 parentM, parentMInv, rotM;
    UT_Quaternion q;

    parentP = m_gdp->getPos3(parentOffset);
    parentN = m_NormalHandle.get(parentOffset);
    parentT = m_TangentHandle.get(parentOffset);

    currP = m_gdp->getPos3(ptoff);
    newP = currP;

    if(m_enforceLength>EPSILOM)
    {
        //std::cout<<"enforcing length"<<std::endl;
        // length constraint
        restL = m_restLHandle.get(ptoff);
        currL = (newP-parentP).length();
        newP = newP - (currL-lerp(currL, restL, m_enforceLength))*((newP-parentP)/currL);
        // end
    }

    if(m_enforceAngle>EPSILOM)
    {
        //std::cout<<"enforcing angles"<<std::endl;
        // to local space
        parentB = cross(parentN,parentT); // no need to normalize parentB, assuming parentN and parentT are normalized and orthogonal
        parentM(0,0) = parentN[0]; parentM(0,1) = parentN[1]; parentM(0,2) = parentN[2];
        parentM(1,0) = parentT[0]; parentM(1,1) = parentT[1]; parentM(1,2) = parentT[2];
        parentM(2,0) = parentB[0]; parentM(2,1) = parentB[1]; parentM(2,2) = parentB[2];
        parentMInv = parentM;
        parentMInv.transpose();
        localP = (newP-parentP)*parentMInv;
        // end
    
        // rot quat        
        restLocalP = m_restLocalPHandle.get(ptoff);
        rotM.identity();
        UT_Vector3 localP_n = localP;
        UT_Vector3 restLocalP_n = restLocalP;
        localP_n.normalize();
        restLocalP_n.normalize();
        int k = rotM.dihedral(localP_n, restLocalP_n, 0);
        if(k==1){ // the vectors are opposed, so just rotate 180 around an arbitrary axis
            UT_Vector3 Axis = localP+UT_Vector3(0.1,0.2,0.3);
            rotM.rotate(Axis,M_PI);
        }
        q.updateFromRotationMatrix(rotM);        
        // end
    
        
        // refA : because we might correct the angle to a certain percentage and not a full 100% - based on m_enforceAngle
        // combined with the fact that the correction can happen clockwise or counter clockwise depending on what happened to the point and its chain of parents
        // we end up with this area around the reference direction that we never access
        // if on one frame we go from clock to counterclock wise we jump from one side to the other
        // the smaller the edge the more risk there is of its parent jumping all over the place around it and triggering the above mentioned issue
        // to workaround that, I am introducing adaptive enforce angle which helps us force small edges closer to 100% correction
        // adaptive enforce angle
        float enforceAngle = m_enforceAngle;
        if(m_adaptiveEnforceAngle){
            float l = restL;
            if(l < m_adaptiveEnforceAngle_lowerThreshold) l = m_adaptiveEnforceAngle_lowerThreshold;
            else if(l > m_adaptiveEnforceAngle_upperThreshold) l = m_adaptiveEnforceAngle_upperThreshold;
            enforceAngle = 1+(((enforceAngle-1)*(l-m_adaptiveEnforceAngle_lowerThreshold))/(m_adaptiveEnforceAngle_upperThreshold-m_adaptiveEnforceAngle_lowerThreshold));
        }
        // end
                
        // apply rot
        UT_Quaternion qidentity = UT_Quaternion(0,0,0,1);
        q = qidentity.interpolate(q, enforceAngle);
        localP =  q.rotate(localP);
        // end
        
        // another way to combat the above mentioned issue (refA) is to limit the angle that any one edge can move during one step
        // similar to the adaptive enforceAngle, we can control this by edgeLength as well
        // another instability helped by the below solution, is the leaf points sometimes jumping from side to side
        // caused by us artificially correcting them after having applied their velocity and them not having any damping
        // limit angle per step
        if(m_angleLimit){
            UT_Vector3 prevLocalP = m_localPHandle.get(ptoff);
            if(prevLocalP.length2()>0){
                UT_Vector3 prevLocalP_n = prevLocalP;
                prevLocalP_n.normalize();
                localP_n = localP;
                localP_n.normalize();
                rotM.identity();
                q.identity();
                k = rotM.dihedral(prevLocalP_n, localP_n, 0);
                if(k==1){ // the vectors are opposed, so just rotate 180 around an arbitrary axis
                    UT_Vector3 Axis = localP+UT_Vector3(0.1,0.2,0.3);
                    rotM.rotate(Axis,M_PI);
                }
                q.updateFromRotationMatrix(rotM);
                
                UT_Vector3 axis;
                float angle;
                q.getAngleAxis(angle,axis);

                float l = restL;
                if(l < m_angleLimit_lowerThreshold) l = m_angleLimit_lowerThreshold;
                else if(l > m_angleLimit_upperThreshold) l = m_angleLimit_upperThreshold;
                float limit = m_angleLimit_lowerLimit+(((m_angleLimit_upperLimit-m_angleLimit_lowerLimit)*(l-m_angleLimit_lowerThreshold))/(m_angleLimit_upperThreshold-m_angleLimit_lowerThreshold));
            
                if(angle>limit){
                    angle = limit;
                    UT_Quaternion qUpdate(angle,axis,0);
                    localP =  qUpdate.rotate(prevLocalP);
                }
            }
        }
        // end
        
        // set newP
        newP = (localP*parentM)+parentP; // back to world space
        
        // set localP
        m_localPHandle.set(ptoff, localP);
    }

    Utils::parallelTransport(newP, parentP, parentN, parentT, newN, newT); // get newT and newN

    // update vel
    UT_Vector3 movement = newP-currP;
    UT_Vector3 updatedVel = m_velHandle.get(ptoff) + movement*m_samplesPerSec;
    //end    
    
    // set attribs
    m_gdp->setPos3(ptoff,newP);
    m_NormalHandle.set(ptoff, newN);
    m_TangentHandle.set(ptoff, newT);
    m_velHandle.set(ptoff, updatedVel);
    m_processedAttHandle.set(ptoff,1);
    // end
    processAll(ptoff,dampingCoeff,0);
    
    return movement;
}
""" , function_sources=[ """int cookMySop(GU_Detail *gdp, const GU_Detail *gdp2, const GU_Detail *gdp3, const char *fixed_group, const char *normalVar, const char *tangentVar,
                                            float enforceLength, float enforceAngle, int substeps, int outputDampedV, float minDampCoeff, float maxDampCoeff,
                                            int adaptiveEnforceAngle, float adaptiveEnforceAngle_lowerThreshold, float adaptiveEnforceAngle_upperThreshold,
                                            int angleLimit, float angleLimit_lowerThreshold, float angleLimit_upperThreshold, float angleLimit_lowerLimit, float angleLimit_upperLimit) {
    // Because it is a python inlinecpp currently the data initializaiton in CS happens on every frame
    // Including building the neighbours map ... not great ...
    // one possible solution is to split the initilization into a separate node
    // that saves the needed data as attributes passed in on the second (static) input
 
    GA_Offset ptoff,ptoffTarget;
    const GA_PointGroup* fixedGroup = 0x0;
    UT_String fixed_group_str(fixed_group);
    if(fixed_group_str.isstring()){
        GOP_Manager *GM = new GOP_Manager();
        if(GM!=0x0)
            fixedGroup = GM->parsePointGroups(fixed_group_str,GOP_Manager::GroupCreator(gdp,0));
    }
    
    //std::cout<<"before CS "<<std::endl;
    CS cs(gdp,gdp2,gdp3,normalVar,tangentVar,fixedGroup,
            enforceLength,enforceAngle,substeps,outputDampedV,minDampCoeff,maxDampCoeff,
            adaptiveEnforceAngle, adaptiveEnforceAngle_lowerThreshold, adaptiveEnforceAngle_upperThreshold,
            angleLimit, angleLimit_lowerThreshold, angleLimit_upperThreshold, angleLimit_lowerLimit, angleLimit_upperLimit);
    //std::cout<<"after CS "<<std::endl;
    
    if (cs.m_error>0)
        return cs.m_error;

    cs.solve();
    
    return 0;
}"""]) 

returnValue = geomodule.cookMySop(geoOne, geoTwo, geoThree, "`chs("fixed_group")`", "`chs("normalVar")`", "`chs("tangentVar")`",\
`chs("enforceLength")`, `chs("enforceAngle")`, `chs("substeps")`, `chs("outputDampedV")`, `chs("minDampCoeff")`, `chs("maxDampCoeff")`,\
`chs("adaptiveEnforceAngle")`, `chs("adaptiveEnforceAngle_lowerThreshold")`, `chs("adaptiveEnforceAngle_upperThreshold")`,\
`chs("angleLimit")`, `chs("angleLimit_lowerThreshold")`, `chs("angleLimit_upperThreshold")`, `chs("angleLimit_lowerLimit")`, `chs("angleLimit_upperLimit")`\
)

errors_dict = {101: "First input is invalid.", 102: "Second input is invalid.", 103: "Third input is invalid.", \
               201: "Normal Attribute not found on first input", 202: "Tangent Attribute not found on first input",\
               301: "Normal Attribute not found on second input", 302: "Tangent Attribute not found on second input",\
               401: "restL Attribute not found on second input", 402: "restLocalP Attribute not found on second input", 403: "neighboursOffsets Attribute not found on second input",\
               501: "The first and second Inputs have different point numbers", 502: "The first and third Inputs have different point numbers"}
if returnValue!=0:
    raise hou.Error(errors_dict[returnValue])
