import os
import sys
import zipfile

def zip_fmu(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """
    Create a zip archive from a directory.

    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations.

    :param dirPath(str): String path to the directory to archive. This is the only
            required argument. It can be absolute or relative, but only one or zero
            leading directories will be included in the zip archive.

    :param zipFilePath(str): String path to the output zip file. This can be an absolute
            or relative path. If the zip file already exists, it will be updated. If
            not, it will be created. If you want to replace it from scratch, delete it
            prior to calling this function. (default is computed as dirPath + ".zip")

    :param includeDirInZip(bool): Boolean indicating whether the top level directory
            should be included in the archive or omitted. (default True)

    Author: http://peterlyons.com/problog/2009/04/zip-dir-python

    """
    if not zipFilePath:
        zipFilePath = dirPath + '.zip'
    if not os.path.isdir(dirPath):
        raise OSError('dirPath argument must point to a directory. '
                      "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    # Little nested function to prepare the proper archive path

    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        # return os.path.normcase(archivePath)
        return archivePath

    outFile = zipfile.ZipFile(zipFilePath, "w",
                              compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        # Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            outFile.writestr(zipInfo, "")
    outFile.close()
