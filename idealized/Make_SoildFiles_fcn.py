import os
import numpy as np

def make_solid_file(nx, ny, bottom_val, side_val, top_val1, top_val2, top_val3, latsize, zdepth, river_dir, root_name, out_dir, pftools_path='./'):
    '''Make soild files for Tilted-V domain
    
    Inputs:
    _______
    nx (int) = number of grid cells in x
    ny (int) = number of grid cells in y
    bottom_val (int) = value for bottom patch
    side_val (int) = value for side patch 
    pftools_path (str)= path to the pfmask-to-pfsol utility
    top_val1 (int) = value for first top patch 
    top_val2 (int) = value for second top patch 
    top_val3 (int) = value for third top patch 
    latsize (float) = size of grid cell in lateral dimension
    zdepth (float) = vertical thickness of grid cells
    river_dir = 1 for river in x direction and 2 for y
    root_name = root name for file outputs
    out_dir  (str)= directory to write files to
    pftools_path (str)= path to te pfmask-to-pfsol utility
    '''
    # setup the asc file header
    header1 = "ncols          " + str(nx) + "\n"
    header2 = "nrows          " + str(ny) + "\n"
    header3 = "xllcorner          0" + "\n"
    header4 = "yllcorner          0" + "\n"
    header5 = "cellsize          " + str(latsize) + "\n"
    header6 = "NODATA_value          0"
    header = header1 + header2 + header3 + header4 + header5 + header6

    # %%
    #Make top mask in for river
    mask = np.ones((ny,nx))
    patch=np.zeros((ny,nx))

    if river_dir == 1:
        patch[0:int(np.floor(ny/2)),] = top_val1
        patch[int(np.floor(ny/2)), ] = top_val2
        patch[(int(np.floor(ny/2))+1):, ] = top_val3
    else:
        patch[: , 0:int(np.floor(nx/2))] = top_val1
        patch[: , int(np.floor(nx/2))] = top_val2
        patch[:,(int(np.floor(nx/2))+1):] = top_val3

    # %%
    #  Make arrays for asc files
    #front
    front =  np.zeros(nx*ny)
    front[(nx*ny-nx):] = side_val
    file = os.path.join(out_dir, (root_name+"_front.asc"))
    np.savetxt(file, front, fmt='%i', header=header, comments="")

    #back
    back = np.zeros(nx*ny)
    back[0:nx] = side_val
    file = os.path.join(out_dir, (root_name+"_back.asc"))
    np.savetxt(file, back, fmt='%i', header=header, comments="")

    #left
    left = np.zeros(nx*ny)
    left[::nx] = side_val
    file = os.path.join(out_dir, (root_name+"_left.asc"))
    np.savetxt(file, left, fmt='%i', header=header, comments="")

    #right
    right = np.zeros(nx*ny)
    right[(nx-1)::nx] = side_val
    file = os.path.join(out_dir, (root_name+"_right.asc"))
    np.savetxt(file, right, fmt='%i', header=header, comments="")

    #bottom
    bottom = np.ones(nx*ny)*bottom_val
    file = os.path.join(out_dir, (root_name+"_bottom.asc"))
    np.savetxt(file, bottom, fmt='%i', header=header, comments="")

    #top
    top = patch.reshape(nx*ny)
    file = os.path.join(out_dir, (root_name+"_top.asc"))
    np.savetxt(file, top, fmt='%i', header=header, comments="")

    # run the pfmask-to-pfsol tool
    vtk_name = root_name + '.vtk'
    vtk_file = os.path.join(out_dir, vtk_name)

    pfsol_name = root_name + '.pfsol'
    pfsol_file = os.path.join(out_dir, pfsol_name)

    pftool_path = os.path.join("/Users/ben/parflow_installation/parflow/bin", 'pfmask-to-pfsol')

    my_command2 = pftool_path + \
              '  --mask-top ' + root_name +'_top.asc' \
              ' --mask-bottom ' + root_name + '_bottom.asc' \
              ' --mask-left ' + root_name + '_left.asc' \
              ' --mask-right ' + root_name + '_right.asc' \
              '  --mask-front ' + root_name + '_front.asc' \
              '  --mask-back ' + root_name + '_back.asc' \
              ' --z-top ' + str(zdepth) + ' --z-bottom 0.0' + \
              ' --vtk ' + vtk_file + ' --pfsol ' + pfsol_file
    os.system(my_command2)
    print(my_command2)

    #clean up the asc files
    os.remove(root_name+"_back.asc")
    os.remove(root_name+"_front.asc")
    os.remove(root_name+"_left.asc")
    os.remove(root_name+"_right.asc")
    os.remove(root_name+"_top.asc")
    os.remove(root_name+"_bottom.asc")
    #' --z-top ' + str(zdepth) + ' --z-bottom 0.0' + \
    #' --z-top 0.0 --z-bottom ' + str(zdepth) + \

