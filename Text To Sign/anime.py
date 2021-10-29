from bvh import Bvh
import numpy as np
import copy



def parse(seq):
    sequence = []
    for w in seq:
        with open(w) as f:
            sequence.append(Bvh(f.read()))
    return sequence


def make_anime_transition(args):
    args.insert(0,"Moves/base_coord_main.bvh")
    args.append("Moves/base_coord_main.bvh")
    sequence = parse(args)
    # initalize the List of Motion With First Move
    tot = []
    tot = [i for i in sequence[0].frames]

    # Looping in Sequence and Calculate The Transition and append Next seq
    for x in range(len(sequence)-1):
        transtion_frames=np.linspace(np.array(sequence[x].frames[-1],dtype=np.float) ,
                                     np.array(sequence[x+1].frames[0],dtype=np.float32) ,
                                     num=30 ,endpoint=False )

        for i in range (transtion_frames.shape[0]):
            window = []
            for j in transtion_frames[i]:
                window.append("{:.6f}".format(j))
            tot.append(window)

        for i in sequence[x+1].frames:
            tot.append(i)


    temp = copy.deepcopy(sequence[0])
    temp.setFrames(tot)
    temp.save('Moves/base_coord.bvh')
    return len(tot)