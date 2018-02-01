
from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
stat = MPI.Status()

cols = 6
rows = 6

M=numpy.zeros((rows+2, cols))
M[0,:] = 1.
M[:,0] = 1.
initM = numpy.copy(M)
# print M

# partition = rows/number of workers
partition = rows/size
subsize = rows/size + 2

#sub matrix
subGrid = M[rank*partition:rank*partition+subsize,:]

#print subGrid
subGridCopy = numpy.copy(subGrid)

for i in xrange(100):
        for ROWelem in xrange(1,subsize-1):
                for COLelem in xrange(1,cols-1):
                        subGrid[ROWelem,COLelem] = (subGrid[ROWelem,COLelem-1]
                                                +subGrid[ROWelem,COLelem+1]
                                                +subGrid[ROWelem-1,COLelem]
                                                +subGrid[ROWelem+1,COLelem])/4.

	if rank == 0:
        	#message = subGrid[subsize -2,:]
		comm.send(subGrid[subsize -2,:], dest = rank + 1)
	        subGrid[subsize - 1,:] = comm.recv( source = rank + 1)
		#comm.recv(message, resource = rank + 1)
		#subGrid[subsize - 1,:] = message
	elif rank == size - 1:
		#message = subGrid[subsize -2,:]	        
		comm.send(subGrid[subsize -2,:], dest = rank - 1)
	        subGrid[subsize -1 ,:] = comm.recv( source = rank - 1)
		#subGrid[subsize -1 ,:] = message

	else:
	        comm.send(subGrid[subsize -2,:], dest = rank + 1)
	        comm.send(subGrid[1,:], dest = rank - 1)
	
	        subGrid[0,:] = comm.recv( source = rank - 1)
	        subGrid[subsize-1,:] = comm.recv( source = rank + 1)	


#print subGridCopy
#print subGrid

#if rank==0:
gridSet = comm.gather(subGrid[1:1+partition], root=0)
print("subgrid= ", gridSet)


if rank==0:
	newM=M
	for i in range(size):
		newM[i*partition+1:i*partition+subsize-1,:] = gridSet[i]
	print newM

