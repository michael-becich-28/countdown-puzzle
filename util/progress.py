import time


# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '='):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    timeleft = None # Format this to constant width

    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '.' * (length - filledLength)
    print('\r%s [%s] %s%% %s' % (prefix, bar, timeleft, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()



if __name__ == "__main__":

    # A List of Items
    nb_seconds = 30

    # Initial call to print 0% progress
    printProgressBar(0, nb_seconds, prefix = 'Timer:', suffix = 'seconds!', length=50)
    for i in range(1, nb_seconds+1):
        # Count 1 second
        time.sleep(1)

        # Update Progress Bar
        printProgressBar(i, nb_seconds, prefix = 'Timer:', suffix = 'seconds!', length=50)


