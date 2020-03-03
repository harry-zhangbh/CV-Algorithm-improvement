import os

PATH = "/Users/wanglei/Downloads/SROIE2019_res/txt/"

'''
删除生成的bbox的最后一行的光标,错误在于没有判断文件内容为空的情况
'''
def delete_last_char():
    count = 0
    for parent, dirnames, filenames in os.walk(PATH):
        for fn in filenames:
            if fn.endswith("txt"):
                # pred_files.append(os.path.join(parent, fn))
                filepath = os.path.join(parent, fn)

                f = open(filepath,"rb+")
                f.seek(-1 ,os.SEEK_END)
                f.truncate()
                count += 1
                print(filepath, count)
                # if f.__next__() == "\n":
                #     f.seek(-1 ,os.SEEK_END)
                #     f.truncate()
                f.close()

'''
注意判断文件lines长度为0 的情况
删掉['256,253,320,253,320,270,256,270\n', '240,264,320,264,320,297,240,297\n', '112,290,176,290,176,305,112,305\n']最后一个\n
'''
def delete_last_line():
    for parent, dirnames, filenames in os.walk(PATH):
        for fn in filenames:
            if fn.endswith("txt"):
                # pred_files.append(os.path.join(parent, fn))
                filepath = os.path.join(parent, fn)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    size = len(lines)
                    print(filepath, size)
                with open(filepath, 'w') as f:
                    if size == 0:
                        continue
                    for i in range(size - 1):
                        f.write(lines[i])
                    f.write(lines[size - 1][:-1])

'''
将生成的（x1,y1,x2,y2,x3,y3,x4,y4)的format成(xmin,ymin,xmax,ymax)
'''
def format_icdar2013_true_labels():
    for parent, dirnames, filenames in os.walk(PATH):
        for fn in filenames:
            if fn.endswith("txt"):
                filepath = os.path.join(parent, fn)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    size = len(lines)
                    print(filepath, size)
                with open(filepath, 'w') as f:
                    if size == 0:
                        continue
                    for i in range(size):
                        line = lines[i].split(',')
                        line = line[0] + "," + line[1] + "," + line[4] + "," + line[5] + "\r\n"
                        f.write(line)
    return

def rename_filenames():
    for parent, dirnames, filenames in os.walk(PATH):
        for filename in filenames:
            os.rename(os.path.join(parent, filename), os.path.join(parent, filename[4:]))

def test():
    list = ['1,2,3,4,5,6,7,8\n', '2,3,4,5,6,7,8,9\n']
    res = list[0].split(',')
    res = res[0] + "," + res[1] + "," + res[4] + "," + res[5] + "\r\n"
    print(res)

if __name__ == '__main__':
    # rename_filenames()
    delete_last_line()
    # test()
    # format_icdar2013_true_labels()