def combine_submission_together(file1,file2):
    submission2 = {}
    with open(file1,'r') as fread:
        for line in fread.readlines():
            line_list = line.split(",")
            device_id = line_list[0]
            info = ','.join(line_list[1:])
            submission2[device_id] = info
    with open(file2, 'r') as fread:
        with open('final_submission2.csv','w') as fwrite:
            for line in fread.readlines():
                line_list = line.split(",")
                device_id = line_list[0]
                if submission2.has_key(device_id):
                    info = submission2[device_id]
                else:
                    info = ','.join(line_list[1:])
                line_write = device_id+','+info
                fwrite.write(line_write)



if __name__ == '__main__':
    combine_submission_together('submission2_2.26726836242_2016-08-02-16-07.csv','submission2.csv')

