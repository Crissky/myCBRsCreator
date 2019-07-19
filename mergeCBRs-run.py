from pyCBRsCreator import mergeCBRs
from os import listdir
from os.path import isfile
from os.path import join

diretorio = 'D:\Arquivos\#HQs\Vinland Saga'
save = 'D:\Arquivos\#HQs\Vinland Saga\\teste'
paths = listdir(diretorio)
paths = [x for x in paths if (not isfile(join(diretorio, x)))]
if('teste' in paths):
    paths.remove('teste')

for matchText in paths:
    print('Merging', matchText)
    mergeCBRs(diretorio, save, matchText)
