from zipfile import ZipFile
import os

numExtra = 1
#Create folders for manga volumes
#'directory' path where folders will be created
#'mangaName' Start folder name
#'sizeCap' Minimum size for the volume number. (zerofill)
def createVolFolders(directory, mangaName, volumeName='Vol', sizeCap=2, start=1, end=2):
    for i in range(start, end+1):
        foldername = ('{0} {1} {2:0%dd}'%(sizeCap)).format(mangaName, volumeName, i)
        completeFolderName = os.path.join(directory, foldername)
        try:
            os.mkdir(completeFolderName)
        except:
            print(completeFolderName, "was not created.")
            continue

def rename(filename, numbername):
    file_basename = os.path.basename(filename)
    file_basename, extension = os.path.splitext(file_basename)

    return '{:03d}{}'.format(numbername, extension)
    
    
def isImage(filename):
    image_extensions = ['.png', '.jpg']
    image_extensions = [x.lower() for x in image_extensions]
    extension = os.path.splitext(filename)[1].lower()

    return (extension in image_extensions)

#Returns a dict where the keys are the names of the folder that contains files
#and the value is a list with the paths of the files
#mode='localpath' Files will have the name equal to the folder
        #that the files were
#mode='fatherpath' Files will have the same name as the parent folder
        #+ chapter number of the folder where the files are
def getAllFilePaths(directory, mode='localpath'):
    if(mode!='localpath' and mode!='fatherpath'):
        raise ValueError('unknown mode, use "localpath" or "fatherpath"')
    file_paths = dict()
    
    #crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        filepath_list = list()
        if(directory == root):
            continue
        for filename in files:
            if(not isImage(filename)):
                continue
            #join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            filepath_list.append(filepath)
        if(filepath_list and mode.lower()=='localpath'):
            file_paths[os.path.basename(root)] = filepath_list
        if(filepath_list and mode.lower()=='fatherpath'):
            base = os.path.basename(os.path.dirname(root))
            capNum = getCap(root)
            file_paths[base + ", Cap " + str(capNum)] = filepath_list
            
    #returning all file paths
    return file_paths

#Returns the chapter number if the filename has at least two numbers
#and extra if it has less than two numbers
def getCap(filename):
    from re import findall
    global numExtra
    filename = os.path.basename(filename)
    numList = findall(r'\d+', filename)
    if( not numList[-1] == filename[-len(numList[-1]):] or 'extra' in filename.lower()):
        numList = ['Extra {:03d}'.format(numExtra)]
        numExtra += 1
    try:
        cap = '{:03d}'.format(int(numList[-1]))
    except:
        cap = numList[-1]
    return cap
    
#Create a zip file based on a list of file paths
def zipFileList(listPaths, zipname, directory, extension='zip'):
    zipname = zipname+'.'+extension
    pathZip = os.path.join(directory, zipname)
    with ZipFile(pathZip,'w') as mZip:
        for file in listPaths:
            mZip.write(file, os.path.basename(file))

#Create zips for files in all subfolders 
def createZips(load_directory, save_directory=None, extension='zip', mode='localpath', feedback=False):
    count = 0
    file_paths = getAllFilePaths(load_directory, mode)
    if(not save_directory):
        save_directory = load_directory
        print('save directory not informed, files will be created in the load directory')
    for key in file_paths.keys():
        if(feedback):
            print('Zipping '+ key)
        zipFileList(file_paths[key], key, save_directory, extension)
        count += 1
    print('End zipping')
    print('%s created'%count)

#Create CBRs for files in all subfolders
def createCBRs(load_directory, save_directory=None, mode='localpath', feedback=False):
    createZips(load_directory, save_directory, 'cbr', mode, feedback)

def mergeCBRs(load_directory, save_directory=None, matchText=None, filesList=None):
    extension = ".cbr"
    if(not save_directory):
        save_directory = load_directory
        print('save directory not informed, files will be created in the load directory')
    if(not matchText):
        raise ValueError('Not informed "matchText"')
    if(not filesList):
        filesList = [x for x in os.listdir(load_directory)\
                     if ( os.path.isfile(os.path.join(load_directory, x)) and matchText in x)]

    targetfile = os.path.join(save_directory, (matchText+extension))
    try:
        os.remove(targetfile)
    except:
        pass
    with ZipFile(targetfile, 'a') as mainCBR:
        count = 0
        for file in filesList:
            print('Copiando', file, 'para', matchText)
            with ZipFile(os.path.join(load_directory, file), 'r') as tempCBR:
                for name in tempCBR.namelist():
                    extension = os.path.splitext(name)[1].lower()
                    mainCBR.writestr('{:03d}{}'.format(count, extension), tempCBR.open(name).read())
                    count +=1
    
    
if(__name__ == "__main__"):
    import sys
    print("Argumentos", sys.argv)
    load_directory = sys.argv[1]
    mode = 'localpath' if len(sys.argv) <= 2 else sys.argv[2]
    feedback = False if len(sys.argv) <= 3 else (sys.argv[3].lower()=='true')
    save_directory = None if len(sys.argv) <= 4 else sys.argv[4]

    createCBRs(load_directory, mode=mode, feedback=feedback, save_directory=save_directory) 
    '''createCBRs('D:\Arquivos\#HQs\Vinland Saga', mode='fatherpath')'''
    
