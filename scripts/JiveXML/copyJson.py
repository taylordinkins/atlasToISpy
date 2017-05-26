# Copy JSON files into an properly structured directory for usage with iSpy
import glob, os, shutil

# Change dest as required
dest = '/home/dink/Documents/proj/iSpy/ispy-webgl/data/test/Events/Run_Test'

for filename in glob.glob('*.json'):
    shutil.copy(filename, dest)
