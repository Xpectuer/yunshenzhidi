'''
Author: XPectuer
LastEditor: XPectuer
'''
import os 
def process_directory(directory, g):
    """
    This function will process all PNG files in the specified directory
    """
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            print(f"Processing {filename}")
            path = os.path.join(directory, filename)
            next(g)
            v = g.send(path)

            print(v)


def rename():
    cnt = 0
    while True:
        # os.rename(path, "card_"+ cnt +".png")
        path = yield
        name = "card_" + str(cnt) + ".png"
        os.rename(path, os.path.join(os.path.dirname(path), name))
        # print(path)
        cnt = cnt + 1
        yield cnt

renameg = rename()
process_directory("imgs/", renameg)