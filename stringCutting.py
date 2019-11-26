import os
def extractDate():
    partOfFilesName = 'listaAkcji'
    base_dir = os.path.join(os.curdir, 'sharesBase')
    list =[]
    for file in os.listdir(base_dir):
        if os.path.isfile(os.path.join(base_dir, file)):
            list.append(file)
    dateList = []
    for file in list :
        if file[:10] == partOfFilesName:
            if file[11:-4] == 'original':
                continue
            dateList.append( file[11:-4] )

    return dateList
