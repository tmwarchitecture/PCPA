import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc

import utils

__author__ = 'Tim Williams'
__version__ = "2.0.1"

###############################################################################
#This function not used
def SplitBREPwithCurve(brep, plane):
    interCrvs = rc.Geometry.Intersect.Intersection.BrepPlane(brep, plane, rs.UnitAbsoluteTolerance())[1]

    if interCrvs is None:
        testPt = brep.Vertices[0].Location
        dist =  plane.DistanceTo(testPt)
        print dist
        if dist < 0:
            print "Side A"
            #sc.doc.Objects.AddBrep(brep)
        else:
            print "Side B"

    for numFaces, each in enumerate(brep.Faces): pass
    numFaces += 1

    for i in range(0, numFaces):
        brep = brep.Faces[i].Split(interCrvs, rs.UnitAbsoluteTolerance())
        print ""
    sc.doc.Objects.AddBrep(brep)

###############################################################################

def IsObjIntersectingPlane(obj, plane):
    if isinstance(obj, rc.Geometry.Brep):
        interCrvs = rc.Geometry.Intersect.Intersection.BrepPlane(obj, plane, rs.UnitAbsoluteTolerance())
    if isinstance(obj, rc.Geometry.Curve):
        interCrvs = rc.Geometry.Intersect.Intersection.CurvePlane(obj, plane, rs.UnitAbsoluteTolerance())
    if interCrvs is not None:
        if interCrvs[0]:
            return True
        else: return False
    else:
        return False

def IsObjAbovePlane(obj, plane):
    dist = plane.DistanceTo(obj.GetBoundingBox(False).Center)
    if dist < 0: return True
    else: return False

def CutObjectWithPlane(obj, plane):
    """
    Splits each object with a plane
    inputs:
        obj (rhino object)
        plane (planar surface)
    returns:
        [0] trimmedObjs
        [1] visible objects
        [2] hidden objs
        [3] cut surfaces
    """
    trimmedObjs = []
    visibleOjects = []
    hiddenObjs = []
    cutSurfaces = []

    #EXTRUSIONS
    if isinstance(obj, rc.Geometry.Extrusion):
        temp = sc.doc.Objects.AddBrep(obj.ToBrep(False))
        obj = rs.coercebrep(temp)
        rs.DeleteObject(temp)

    #BREPS
    if isinstance(obj, rc.Geometry.Brep):
        if IsObjIntersectingPlane(obj, plane):
            #OBJECT INTERSECTS PLANE
            trimObjs = []
            splitObjects = obj.Trim(plane, rs.UnitAbsoluteTolerance())
            for eachSplitObj in splitObjects:
                trimmedObjs.append(sc.doc.Objects.AddBrep(eachSplitObj))
            if obj.IsSolid:
                #OBJECT INTERSECTS AND SOLID
                interCrvs = rc.Geometry.Intersect.Intersection.BrepPlane(obj, plane, rs.UnitAbsoluteTolerance())[1]
                sectionSrfs = rc.Geometry.Brep.CreatePlanarBreps(interCrvs)
                for eachSection in sectionSrfs:
                    cutSurfaces.append(sc.doc.Objects.AddBrep(eachSection))
        else:
            #OBJECT DOES NOT INTERSECT PLANE
            if IsObjAbovePlane(obj, plane):
                #OBJECT IS ABOVE THE PLANE
                visibleOjects.append(sc.doc.Objects.AddBrep(obj))
            else:
                #OBJECT IS BELOW THE PLANE (HIDDEN)
                hiddenObjs.append(obj)

    #CURVES
    if isinstance(obj, rc.Geometry.Curve):
        if IsObjIntersectingPlane(obj, plane): #curve intersecting plane
            intersection = rc.Geometry.Intersect.Intersection.CurvePlane(obj, plane, rs.UnitAbsoluteTolerance())
            params = []
            for each in intersection:
                params.append(each.ParameterA)
            splitCrvs = obj.Split(params)
            for eachCrv in splitCrvs:
                if IsObjAbovePlane(eachCrv, plane):
                    trimmedObjs.append(sc.doc.Objects.AddCurve(eachCrv))

        else:#object above the plane
            if IsObjAbovePlane(obj, plane):
                visibleOjects.append(sc.doc.Objects.AddCurve(obj))
            else:
                hiddenObjs.append(obj)

    return [trimmedObjs, visibleOjects, hiddenObjs, cutSurfaces]

###############################################################################
#MAIN
def CutModel(objs, srf):
    try:
        rhSrf = rs.coercesurface(srf)
        plane = rhSrf.TryGetPlane()[1]
        groupMain = rs.AddGroup('MainObjects')
        groupCut = rs.AddGroup('SectionSurfaces')
        groupVisible = rs.AddGroup('VisibleObjects')

        rs.HideObject(objs)

        for obj in objs:
            #BLOCKS
            if rs.IsBlockInstance(obj):
                matrix = rs.BlockInstanceXform(obj)
                blockObjs = rs.BlockObjects(rs.BlockInstanceName(obj))
                for eachBlockObj in blockObjs:
                    newCopy = rs.CopyObject(eachBlockObj)
                    xformedObj = rs.TransformObject(newCopy, matrix)
                    rhobj = rs.coercegeometry(xformedObj)
                    splitResults = CutObjectWithPlane(rhobj, plane)
                    if splitResults[0] is not None:
                        for eachObj in splitResults[0]:
                            rs.MatchObjectAttributes(eachObj, xformedObj)
                            rs.ShowObject(eachObj)
                            rs.AddObjectToGroup(eachObj, groupMain)
                        for eachObj in splitResults[1]:
                            rs.MatchObjectAttributes(eachObj, xformedObj)
                            rs.ShowObject(eachObj)
                            rs.AddObjectToGroup(eachObj, groupMain)
                        for eachObj in splitResults[3]:
                            rs.AddObjectToGroup(eachObj, groupCut)
                    rs.DeleteObject(xformedObj)

            #GEOMETRY
            else:
                rhobj = rs.coercegeometry(obj)
                splitResults = CutObjectWithPlane(rhobj, plane)
                if splitResults[0] is not None:
                    for eachObj in splitResults[0]:
                        rs.MatchObjectAttributes(eachObj, obj)
                        rs.ShowObject(eachObj)
                        rs.AddObjectToGroup(eachObj, groupMain)
                    for eachObj in splitResults[1]:
                        rs.MatchObjectAttributes(eachObj, obj)
                        rs.ShowObject(eachObj)
                        rs.AddObjectToGroup(eachObj, groupMain)
                    for eachObj in splitResults[3]:
                        rs.AddObjectToGroup(eachObj, groupCut)
        return True
    except:
        print "Cut Model failed"
        return False

#RHINO INTERFACE
def CutModel_Button():
    objs = rs.GetObjects("Select objects to cut", preselect = True)
    if objs is None: return

    srf = rs.GetObject("Select split surface", rs.filter.surface)
    if srf is None: return

    rs.EnableRedraw(False)
    result = CutModel(objs, srf)
    if result:
        utils.SaveToAnalytics('Drawing-cut Model')
    utils.SaveFunctionData('Drawing-Cut Model', [len(objs), result])
    rs.EnableRedraw(True)

if __name__ == "__main__":
    CutModel_Button()
