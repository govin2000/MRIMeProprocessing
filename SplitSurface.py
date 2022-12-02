import nibabel as nb
import os
import numpy as np
import re

def get_mode(nums):
    nums.sort()
    counts = dict()
    for i in nums:
        counts[i] = counts.get(i, 0) + 1
    mode = max(counts, key=counts.get)

    return mode

def write_obj(fname, vtx, fac):
    f = open(fname, 'w')
    for dt in vtx:
        str_val='v\t'+str(round(dt[0],3))+'\t'+str(round(dt[1],3))+'\t'+str(round(dt[2],3))+'\n'
        f.write(str_val)  # python will convert \n to os.linesep
    for vt in fac:
        ftr_val='f\t'+str(round(vt[0]))+'\t'+str(round(vt[1]))+'\t'+str(round(vt[2]))+'\n'
        f.write(ftr_val)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it


def create_cortical_objects(pialfile, annotfile, objdir):
    dirname, objprefix = os.path.split(pialfile)
    pial_geom = nb.freesurfer.io.read_geometry(pialfile)
    annot_value = nb.freesurfer.io.read_annot(annotfile)
    vtx = pial_geom[0]
    fac = pial_geom[1]
    lab = annot_value[0]
    struct_name = annot_value[2]
    dpx = lab
    nV = len(vtx)
    nF = len(fac)
    labels = np.delete(struct_name, 4)  # delete corpus callosum

    label_names = []
    for lb in labels:
        label_names.append(re.findall(r"'(.*?)'", str(lb), re.DOTALL))

    udpx = np.unique(dpx)  # Unique labels
    nL = len(udpx)
    uidx = range(0, nL)  # Unique corresponding indices
    dpxidx = np.zeros(len(dpx))

    for i in uidx:
        dpxidx[np.where(dpx == udpx[i])] = i  # Replace labels by indices

    vtxL = [[]] * nL
    facL = [[]] * nL

    for f in range(0, nF):
        # f=0
        Cfac = fac[f, :]
        Cidx = dpxidx[Cfac]
        # print(Cfac)
        # print(Cidx)
        nuCidx = len(np.unique(Cidx))
        # print(nuCidx)
        if nuCidx == 1:
            a = facL[int(Cidx[0])]
            b = Cfac
            facL[int(Cidx[0])] = np.vstack((a, b)) if np.size(a) else b
        else:
            vtxCfac = vtx[Cfac, :]
            vtxnew = (vtxCfac + vtxCfac[[1, 2, 0], :]) / 2
            vtx = np.append(vtx, vtxnew, axis=0)

            facnew = [[Cfac[0], nV + 0, nV + 2],
                      [nV + 0, Cfac[1], nV + 1],
                      [nV + 2, nV + 1, Cfac[2]],
                      [nV + 0, nV + 1, nV + 2]]

            nV = len(vtx)

            c = facL[int(Cidx[0])]
            d = facnew[0]
            facL[int(Cidx[0])] = np.vstack((c, d)) if np.size(c) else d

            e = facL[int(Cidx[1])]
            f = facnew[1]
            facL[int(Cidx[1])] = np.vstack((e, f)) if np.size(e) else f

            g = facL[int(Cidx[2])]
            h = facnew[2]
            facL[int(Cidx[2])] = np.vstack((g, h)) if np.size(g) else h

            mode_cidx = int(get_mode(Cidx))

            i = facL[mode_cidx]
            j = facnew[3]
            facL[mode_cidx] = np.vstack((i, j)) if np.size(i) else j

    for lb in range(1, nL):  # ignore the first unknown object

        # Vertices for the current label
        vidx = np.unique(facL[lb].ravel())
        vtxL_val = vtx[vidx.astype(int), :]

        tmp = np.zeros(nV)
        tmp[vidx.astype(int)] = range(0, len(vidx))
        facL_val = np.array(facL[lb][:]).ravel()
        facL_final = np.reshape(tmp[facL_val.astype(int)], np.shape(facL[lb]))

        lb_name = label_names[lb]
        fname = os.path.join(objdir, objprefix + '.' + lb_name[0] + '.obj');
        write_obj(fname, vtxL_val, facL_final + 1)

def main():

    subj = 'pid_007_AO'
    sdir = '/Users/gopoudel/Documents/Personal/MRIMe/webdata'
    hemi = 'lh'

    pial = hemi + '.pial'
    annot = hemi + '.aparc.annot'
    pialfile = os.path.join(sdir, 'FreeSurfer', subj, 'surf', pial)
    annotfile = os.path.join(sdir, 'FreeSurfer', subj, 'label', annot)
    objdir = os.path.join(sdir, 'objects', subj)

    if not os.path.exists(objdir):
        os.makedirs(objdir)

    # Create cortical parcellations file
    create_cortical_objects(pialfile, annotfile, objdir)


    #create_ssubcortical_objects(pialfile, annotfile, objdir)
    SUBJECTS_DIR=os.path.join(sdir, 'FreeSurfer')
    command='./aseg2srf '+subj+' '+SUBJECTS_DIR
    os.system(command)

    #Loop through  srf files sand convert them to objects
    srf_dir=os.path.join(SUBJECTS_DIR, subj, 'ascii')
    for filename in os.listdir(srf_dir):
        #print(filename)
        f = os.path.join(srf_dir, filename)
        if f.endswith(".srf"):
            fname=os.path.splitext(filename)[0]+'.obj'
            cmd2='./srf2obj '+f+' > '+os.path.join(objdir, fname)
            #print(fname)
            os.system(cmd2)



if __name__ == "__main__":
    main()
