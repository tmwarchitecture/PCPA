import utils

__author__ = 'Tim Williams'
__version__ = "2.2.0"

def GetDict():
    fileLocationsPCPNY = {
    'Template File' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\06 TEMPLATE\PCPA_Template.3dm',
    'Template Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\06 TEMPLATE',
    'Project Folders' : r'J:',
    'ACAD Scheme Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\01 ACAD SCHEMES',
    'Display Mode Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\03 DISPLAY MODES',
    'Analytics' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\data\raw\Analytics.csv',
    'Data Folder' : r'X:\22_REACH\03 TOOLS\USER DATA\PCPA_RHINO_TOOLBAR\raw',
    'PCPA Layers' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\05 LAYERS\PCPA_Layers.csv',
    'PCPA Layers_V1' : r'X:\05_RHINO STANDARDS\13 PCPA LAYERS\1.0\PCPA LAYERS_V1.csv',
    'CSV' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\SCRIPTS\libs\csv.py',
    'PCPA GH Components' : r'X:\22_REACH\03 TOOLS\PCPA_GH_TOOLBAR\CURRENT',
    'GH Dependencies' : r'X:\22_REACH\03 TOOLS\PCPA_GH_STANDARD SET',
    'GH Dependencies_Libraries' : r'X:\22_REACH\03 TOOLS\PCPA_GH_STANDARD SET\PCPA_GH_STANDARD SET_LIBRARIES',
    'GH Dependencies_User Objects' : r'X:\22_REACH\03 TOOLS\PCPA_GH_STANDARD SET\PCPA_GH_STANDARD SET_USER OBJECTS',
    'Material File' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\04 MATERIALS\PCPA_Materials.3dm',
    'People 3D Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\02 BLOCKS\PEOPLE\3D',
    'People 2D Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\02 BLOCKS\PEOPLE\2D',
    'Vegetation 3D Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\02 BLOCKS\VEGETATION\3D',
    'Vegetation 2D Folder' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\02 BLOCKS\VEGETATION\2D',
    'Help File' : r'X:\22_REACH\03 TOOLS\PCPA_RHINO_TOOLBAR\02 SUPPORT FILES\00 MANUAL\PCPA Rhino Tools Manual.pdf',
    '3d Blocks' : r'X:\13_3D MODELS LIBRARY'
    }

    fileLocationsPCPNH = {
    'Template File' : r'D:\PCPA_Toobar_local\PCPA_TOOLS_dup\RHINO TEMPLATE\0.2\PCPA_TEMPLATE.3dm',
    'Template Folder' : r'D:\PCPA_Toobar_local\PCPA_TOOLS_dup\RHINO TEMPLATE\0.2',
    'ACAD Scheme Folder' : r'',
    'Display Mode Folder' : r'',
    'Analytics' : r'D:\PCPA_TOOLS\SCRIPTS\data\Analytics.csv',
    'PCPA Layers' : r'D:\PCPA_TOOLS\SCRIPTS\data\PCPA LAYERS_V2.csv',
    'PCPA Layers_V1' : r'D:\PCPA_TOOLS\SCRIPTS\data\PCPA LAYERS_V1.csv',
    'CSV' : r'D:\PCPA_TOOLS\SCRIPTS\libs\csv.py',
    'PCPA GH Components' : r'D:\PCPA_TOOLS\GH\PCPA_GH_TOOLBAR',
    'GH Dependencies' : r'D:\REACHCampus\00_PCPA Standard Set',
    'Material File' : r'',
    'Material Folder' : r'',
    'People 3D Folder' : r'',
    'People 2D Folder' : r'',
    'Vegetation 2D Folder' : r'',
    'Help File' : r'',
    }

    location = utils.GetNetworkLocation()
    if location == 0:
        return fileLocationsPCPNY
    elif location == 1:
        return fileLocationsPCPNH
    else:
        print "Network Location Error"

if __name__ == "__main__":
    GetDict()
