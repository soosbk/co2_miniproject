# Import the module
import dropfile

# Call it and assign your filepath (pathlib.Path object)
p = dropfile.get()

# use Path methods, etc on your object
print(p)  # 'C:\somefolder\testfile.pdf'
print(p.parent)  # 'C:\somefolder'
print(p.stem)  # 'testfile'
print(p.suffix)  # '.pdf'