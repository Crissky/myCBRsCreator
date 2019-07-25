from pyCBRsCreator import mergeCBRs
from pyCBRsCreator import createCBRs
from os import listdir
from os.path import isfile
from os.path import join
from os import mkdir
from os import remove

def removeFiles(load_directory):
    print('Removing partial files in:', load_directory)
    paths = listdir(load_directory)
    files = [x for x in paths if ( isfile( join(load_directory, x) ) )]
    for file in files:
        print('Removing', file)
        remove( join(load_directory, file) )

def createFullCBRs(load_directory, save_directory=None):
    removeFiles(load_directory)
    print('Creating partial files in:', load_directory)
    if(not save_directory):
        save_directory = join(load_directory, 'CRBs')
    print('Cleaning save_directory:', save_directory)
    deleteFolder(save_directory)
    createCBRs(load_directory, mode='fatherpath', feedback=True)
    paths = listdir(load_directory)
    paths = [x for x in paths if ( not isfile( join(load_directory, x) ) )]
    mkdir(save_directory)
    for matchText in paths:
        print('Merging', matchText)
        mergeCBRs(load_directory, save_directory, matchText)
    removeFiles(load_directory)

def deleteFolder(directory):
    import os
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(directory)

if(__name__ == "__main__"):
    load_directory = 'D:\\Arquivos\\#HQs\\Vinland Saga'
    save_directory = 'D:\\Arquivos\\#HQs\\Vinland Saga\\CBRs'
    createFullCBRs(load_directory, save_directory)

    load_directory = 'D:\\Arquivos\\#HQs\\Claymore'
    save_directory = 'D:\\Arquivos\\#HQs\\Claymore\\CBRs'
    createFullCBRs(load_directory, save_directory)
