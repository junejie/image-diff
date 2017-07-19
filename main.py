import argparse
import os
import shutil
import subprocess
from PIL import Image
from PIL import ImageChops


class Diff(object):
    def __init__(self, source, otherSource, diff):
        self.source = source
        self.otherSource = otherSource

        if os.path.exists(diff):
            shutil.rmtree(diff)
        os.mkdir(diff)
        self.diff = diff

    def trace(self):

        for filename_ in os.listdir(self.source):
            file_ = self.source + '/' + filename_
            otherFile_ = self.otherSource + '/' + filename_
            filename, file_extension = os.path.splitext(file_)
            if file_extension == '.png':

                # validate file in destination dir
                if os.path.exists(otherFile_) is True:
                    im1 = Image.open(file_)
                    im2 = Image.open(otherFile_)
                    diff = ImageChops.difference(im1, im2).getbbox()
                    if diff is None:
                        print('match in', file_, otherFile_)
                    else:
                        print('miss match', file_, otherFile_)
                        with open(os.devnull, 'w') as devnull:
                            subprocess.call(['magick', 'compare',
                                             '-compose', 'src',
                                             '-metric', 'AE', file_,
                                             otherFile_,
                                             self.diff + '/' + filename_],
                                            stdout=devnull, stderr=devnull)
                else:
                    print('skip', otherFile_)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process Diff')
    parser.add_argument('-s', '--source', required=True,
                        help='Source folder')
    parser.add_argument('-ss', '--other', required=True,
                        help='Other Source folder')
    parser.add_argument('-d', '--diff', required=True,
                        help='Diff directory')
    args = parser.parse_args()
    diff = Diff(
        args.source,
        args.other,
        args.diff
    )
    diff.trace()
