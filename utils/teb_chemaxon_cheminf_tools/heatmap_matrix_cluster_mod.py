#! /raid1/people/tbalius/zzz.virtualenvs/sgehead_python_env/bin/python

## Writen by Trent E. Balius in B. Shoichet group

## This was adapted from the web:
## http://stackoverflow.com/questions/2982929/plotting-results-of-hierarchical-clustering-ontop-of-a-matrix-of-data-in-python

import matplotlib  # must import first
matplotlib.use('Agg')  # allows you to not have an x-server running
#these lines must be first, if pylab is imported first it ruins this

import sys, os
import copy
import math
#import matplotlib
import scipy
import numpy
import pylab
import scipy.cluster.hierarchy as sch


def getlabel(labfilename):
  # import the label information
  
  file = open(labfilename)
  lines = file.readlines()
  file.close()
  
  #m_lab = len(lines)
  labels = []
  
  for line in lines:
      splitline = line.split(',')
      labels.append(splitline[0].strip())
      #print splitline[0], splitline[1]
  return labels


def mat_to_vector(Mat):
    m = len(Mat)
    n = len(Mat[0])

    if (m != n):
        print ("inconsitancy in numbers of rows and columns in the matrix.")
        sys.exit()

    print (m,n)

    #X = scipy.zeros([m,n])
    X = numpy.zeros([m,n])
    #Xvec = scipy.zeros(n*(n-1)/2)
    #Xvec = scipy.zeros(int(n*(n-1)/2))
    Xvec = numpy.zeros(int(n*(n-1)/2))

    count2    = 0

    ## converts from a 2D array to Scipy Matrix 
    for i in range(0,n):
        for j in range(0,n):
               ## 1 - tc is more like a distance than tc.
               #X[i,j] = -Mat[i][j] + 1.0
               X[i,j] = Mat[i][j]

    for i in range(0,n):
        for j in range(i+1,n):
               ## 1 - tc is more like a distance than tc.
               #Xvec[count2] = -Mat[i][j] + 1.0
               Xvec[count2] = Mat[i][j]
               count2 = count2+1

    return X,Xvec

# for each molecule calculate the variance of distances to its other cluster members. 
# this will tell us how close to the center of the cluster it is. 
def cal_mol_cluster_variance(matrix,clusters): 

    # matrix is the distance matrix
    # clusters is the list of elements (index) with cluster asignment. 
    N = len(clusters)
    
    numOfClusters = clusters.max()
    print ("cluster =", clusters.max(), clusters.min() )
    #exit()
    cluster_rep  = []
    min_var_dist = []
    # each cluster will have one rep. intialize to one
    for i in range(numOfClusters):
        cluster_rep.append(-1)
        min_var_dist.append(1000.0)

    # for each molecule calculate the mean of distance, the mean of the squared distance, and the count of distances (n-1, where n is the number of members). 
    Ex  = []
    Ex2 = []
    Var = []
    num = []
    # here we intialize the arrays for each molecule
    for i in range(N):
        Ex.append(0.0) 
        Ex2.append(0.0) 
        Var.append(0.0) 
        num.append(0) 

    # calcuate and sum. 
    for i in range(N): 
        for j in range(N): 
            #if (i != j): 
                if (clusters[i] == clusters[j]):
                     Ex[i]  = Ex[i] + matrix[i,j]
                     Ex2[i] = Ex2[i] + matrix[i,j]**2
                     num[i] = num[i] + 1
    # divid by num of cluster members
    for i in range(N):
        if (num[i] == 0):
            print ("warning: Num == 0")
            print ('i==%d,Ex[i]==%f'%(i,Ex[i]))
            num[i] = 1
        Ex[i]  = Ex[i]  / num[i] 
        Ex2[i] = Ex2[i] / num[i]
        Var[i] = Ex2[i] - Ex[i]**2
        clust = clusters[i]-1 
        if (min_var_dist[clust] > Var[i]):
            cluster_rep[clust] = i
            min_var_dist[clust] = Var[i]
    print ("mol_num cluster mean mean_of_squares var num")
    for i in range(N):
        print (i, clusters[i], Ex[i], Ex2[i], Var[i], num[i] )
        

    for i in range(numOfClusters): 
          print (i, cluster_rep[i], min_var_dist[i])

    return cluster_rep
        

def get_cluster(X,labels,clusttype,threshold,dirname):
    print ("in function get_cluster")
    if len(X) != len(labels):
       print ("len(X) != len(labels)")
       print (len(X), len(labels))
       exit()

    Xnew,Xvec = mat_to_vector(X)

    #Y = sch.linkage(Xvec, method='complete')
    #Y = sch.linkage(Xvec, method='single')
    Y = sch.linkage(Xvec, method=clusttype)
    clusters = sch.fcluster(Y, threshold, 'distance')
    print (clusters)
    cluster_list  = [] # list of pdb names in each cluster
    cluster_sizes = [] # list of the size of each cluster

    numOfClusters = clusters.max()

    ## intialize array that will store the labels for each cluster
    for i in range(numOfClusters):
        cluster_list.append('c'+ str(i+1)+' -- ')
        cluster_sizes.append(0)
    #
    ## fill array with labels by appending the string assosiated with each cluster
    for i in range(len(clusters)):
        cluster_list[clusters[i]-1] = cluster_list[clusters[i]-1] + labels[i] + ','
        cluster_sizes[clusters[i]-1] = cluster_sizes[clusters[i]-1] + 1

    ## write the cluster
    for i in range(numOfClusters):
        print (cluster_list[i])

    filename = "mol_cluster_list.txt"
    fh_mcl = open(filename,'w')
    for i in range(len(clusters)): 
       fh_mcl.write('%s %d\n'%(labels[i],clusters[i]))
        

    ## write the cluster with more than 3 members
#    os.system('rm -rf   large_clusters'+dirname)
#    os.system('mkdir -p large_clusters'+dirname)
#    os.chdir('large_clusters'+dirname)

    # pick a member of the cluster to be the representive member. 
    # Right now this is done by picking the molecule with the minimum variance. 
    reps = cal_mol_cluster_variance(X,clusters) 
    filename = "cluster_rep.txt"
    fh_rep = open(filename,'w')
    print (" larger clusters: ")
    for i in range(numOfClusters):
       filename = "cluster" + str(i+1) + ".txt"
       fh = open(filename,'w')
       fh.write(cluster_list[i].replace(' ','').replace(',','\n').replace('-','\n'))
       fh.close()
       fh_rep.write("cluster"+str(i+1)+','+str(reps[i])+","+labels[reps[i]]+'\n')

       if cluster_sizes[i] > 3:
           print ("  " + cluster_list[i])
#           name = cluster_list[i].split('--')[0].replace(' ','')
#           mols = cluster_list[i].split('--')[1].split(',')
           ## get images from zinc
#           os.system('mkdir -p '+ name)
#           os.chdir(name)
#           fout = open( name+"_info.txt",'w')
#           for mol in mols:
#               print mol
#               fout.write(mol+'\n')
#               os.system('wget http://zinc.docking.org/img/sub/' + mol.replace('C','').replace(' ','')+'.gif')
#               #os.system('wget http://zinc.docking.org/substance/' + mol.replace('C','').replace(' ','')+'')
#           fout.close()
#           os.chdir('../')
#    os.chdir('../')
    fh_rep.close()
              
    return Y

#def get_vec_2(mat,index):
#    vec = scipy.zeros([len(index),1])
#    if len(index) != len(mat):
#       print "warning"
#       print len(index), len(mat)
#       exit()
#    j = 0
#    for i in index:
#        vec[j] = mat[j,i]
#        j=j+1
#    return vec
#
#def get_vec_1(mat,index):
#    vec = scipy.zeros([len(index),1])
#    if len(index) != len(mat[0,:]):
#       print "warning"
#       print len(index), len(mat)
#       exit()
#    j = 0
#    for i in index:
#        vec[j] = mat[i,j]
#        j=j+1
#    return vec

#def get_min(Xorg,label1,label2,N):
#  X = copy.copy(Xorg)
#  print "In function get_min"
#  print "loop over matix", N, "times"
#  count = 0
#
#  os.system('rm -rf   min_pairs')
#  os.system('mkdir -p min_pairs')
#  os.chdir('min_pairs')
#  fout = open("links_info.txt",'w')
#  #os.system('cd       min_pairs')
#  while (count < N):
#    minname = 'minpair'+str(count)
#    os.system('mkdir -p minpair'+str(count))
#    os.chdir('minpair'+str(count))
#    indecies1 = numpy.argmin(X,axis=0)
#    indecies2 = numpy.argmin(X,axis=1)
#
#    vec1 = numpy.amin(X,axis=0)
#    vec2 = numpy.amin(X,axis=1)
#
#    j1 = numpy.argmin(vec1)
#    i1 = indecies1[j1]
#
#    i2 = numpy.argmin(vec2)
#    j2 = indecies2[i2]
#
#    print i1,j1, X[i1,j1]
#    print i2,j2,label1[j2],label2[i2], X[i2,j2]
#
#    fout.write('%s,%s,%s,%d,%d,%f\n' % (minname,label2[i2],label1[j2],i2,j2,X[i2,j2]))
#    # get images from zinc:
#    #os.system('wget http://zinc.docking.org/substance/' + label1[j2].replace('C',''))
#    #os.system('wget http://zinc.docking.org/substance/' + label2[i2].replace('C',''))
#    os.system('wget http://zinc.docking.org/img/sub/' + label2[i2].replace('C','') +'.gif')
#    os.system('wget http://zinc.docking.org/img/sub/' + label1[j2].replace('C','') +'.gif')
#
##    if ( i1 != i2 or j1 != j2): 
##        print "Error:: i1!=i2 or j1 == j2"
##        print j1, j2, i1, i2
##        continue
#    X[i2,j2] = 100
#    count = count + 1
#    os.chdir('../')
##    os.system('cd ../')
#  os.chdir('../')
#  fout.close()
#  #exit() 
#  return

def import_mat(matfilename):
     # Import data from matrix file:
     file = open(matfilename)
     lines = file.readlines()
     file.close()
     
     
     m = len(lines)
     n = len(lines[0].split(','))
     
     if (m != n):
         print ("inconsitancy in numbers of rows and columns in the matrix.")
     
     print (m,n)
     
     #X = scipy.zeros([m,n])
     X = numpy.zeros([m,n])
     #print(n*(n-1)/2)
     #Xvec = scipy.zeros(int(n*(n-1)/2))
     Xvec = numpy.zeros(int(n*(n-1)/2))
    
     countline = 0
     count2    = 0 
     for line in lines:
         line = line.strip('\n')
         splitline = line.split(',')
         if (n != (len(splitline))):
             print ("ERROR: n != (len(splitline), inconsitancy in number of elements in rows")
             sys.exit()
     
         for i in range(0,n):
             val = float(splitline[i])
             X[countline,i] = 1-val 
             #X[countline,i] = 1-val ## 1-Tc is a metric
         countline = countline + 1
     return X ,n,m

print (" This script takes 4 inputs mat_filename, lab_filename, threshold, cluster type (complete or single), label type (false, true) ")

pylab.matplotlib.use('Agg')

ZERRO = 0.0

matfilename  = sys.argv[1]
labfilename = sys.argv[2]
threshold   = float(sys.argv[3])
clustertype = sys.argv[4]
label_on  = sys.argv[5]

print ("mat_filename = "+ matfilename  )
print ("lab_filename = "+ labfilename  )
print ("threshold = "+ str(threshold)  )
print ("cluster type = "+ clustertype  )
print ("label type = "+ label_on       )   

#Y = sch.linkage(Xvec, method='complete')
#Y = sch.linkage(Xvec, method='single')


if not ( clustertype == "complete" or clustertype == "single"):
    print ("cluster type must be complete or single")

labels1 = getlabel(labfilename)
#labels2 = getlabel(lab2filename)

X,n,m           = import_mat(matfilename)
#dist_mat1,n1,m1 = import_mat(dist_mat1_fn)

#threshold =  0.7
#threshold =  0.47
#threshold = 0.51
#threshold =  0.4
## create a distance matrix --> dendogram by comparing all rows
Y1 = get_cluster(X,labels1,clustertype,threshold,'set2')

#get_min(X,labels1,labels2,50)

#
fig = pylab.figure(figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
##Z1 = sch.dendrogram(Y, orientation='right')
Z1 = sch.dendrogram(Y1, orientation='right',color_threshold=threshold)
matplotlib.pyplot.plot([threshold,threshold],[0,10*m],'k--') # draws a datshed line where dendogram is cut.

##help(sch.dendrogram)
#ax1.set_xticks([])
ax1.set_yticks([])
ax1.invert_xaxis()
##exit()
##print ax1.get_ylim()
##ax1.set_ylim(-1, n)
ticks = ax1.get_xticks()
fontsizeval = 6
for i in range(0,len(ticks)):
    print (i)
    labels = ax1.xaxis.get_major_ticks()[i].label1
    labels.set_fontsize(fontsizeval)
    labels.set_rotation('vertical')

## Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
#idx2 = Z2['leaves']
X = X[idx1,:]
X = X[:,idx1]
#X = X[:,idx2]

#labels_sort = labels1[idx1]
## make sorted label list
labels_sort = []
for i in idx1:
  #labels_sort.append('c'+str(clusters[i]) + '-'+ labels[i])
  labels_sort.append(labels1[i])

cdict = {'red': ((0.0, 0.0, 0.0),
                  (0.0, 0.0, 0.0), 
                  (1.0, 1.0, 1.0)),
          'green': ((0.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          'blue': ((0.0, 0.0, 0.0),
                   (0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))}


my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,20)

im = axmatrix.imshow(X, aspect='auto', origin='lower',interpolation='nearest', cmap=my_cmap)


#im.set_clim(0,threshold)
#im.set_clim(threshold,1)
im.set_clim(0.2,1)
axmatrix.set_ylim(-0.5, m-0.5)
axmatrix.set_xlim(-0.5, n-0.5)
axmatrix.set_yticks([])
#axmatrix.set_xticks([])

if (label_on == "true"): 

  axmatrix.set_xticks(range(0,n))
  
  axmatrix.set_xticklabels(labels_sort)
  #axmatrix.set_yticklabels(labels1)

  #fontsizeval = 8
  #fontsizeval = 6
  for i in range(0,n):
  #    print i
      labels = axmatrix.xaxis.get_major_ticks()[i].label1
      labels.set_fontsize(fontsizeval)
      labels.set_rotation('vertical')
else: # label_on == "false"
   axmatrix.set_xticks([])

# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
fig.savefig('dendrogram.png',dpi=600)

