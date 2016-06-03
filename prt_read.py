def find_runs(rf, wf):
    previous_line = ""

    for line in rf:
        if line.startswith(' Run'):
            try:
                break_up = previous_line.strip().split()
                for each in break_up[1:]:
                    try:
                        float(each)
                        wf.write('\n')
                        break
                    except ValueError:
                        wf.write(each + " ")
            except:
                print(previous_line)
        previous_line = line

if __name__ == '__main__':
    from sys import argv

    rf = open(argv[1])
    wf = open(argv[2], 'w')

    find_runs(rf, wf)
