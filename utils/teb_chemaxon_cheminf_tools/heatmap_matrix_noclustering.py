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
        print "inconsitancy in numbers of rows and columns in the matrix."
        sys.exit()

    print m,n

    X = scipy.zeros([m,n])
    Xvec = scipy.zeros(n*(n-1)/2)

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

def import_mat(matfilename):
     # Import data from matrix file:
     file = open(matfilename)
     lines = file.readlines()
     file.close()
     
     
     m = len(lines)
     n = len(lines[0].split(','))
     
     if (m != n):
         print "inconsitancy in numbers of rows and columns in the matrix."
     
     print m,n
     
     X = scipy.zeros([m,n])
     Xvec = scipy.zeros(n*(n-1)/2)
    
     countline = 0
     count2    = 0 
     for line in lines:
         line = line.strip('\n')
         splitline = line.split(',')
         if (n != (len(splitline))):
             print "ERROR: n != (len(splitline), inconsitancy in number of elements in rows"
             sys.exit()
     
         for i in range(0,n):
             val = float(splitline[i])
             X[countline,i] = 1-val 
             #X[countline,i] = 1-val ## 1-Tc is a metric
         countline = countline + 1
     return X ,n,m

pylab.matplotlib.use('Agg')

ZERRO = 0.0

matfilename  = sys.argv[1]
labfilename1 = sys.argv[2]
labfilename2 = sys.argv[3]

print "mat_filename = "+ matfilename  
print "lab_filename1 = "+ labfilename1  
print "lab_filename2 = "+ labfilename2  

#Y = sch.linkage(Xvec, method='complete')
#Y = sch.linkage(Xvec, method='single')


labels1 = getlabel(labfilename1)
labels2 = getlabel(labfilename2)

X,n,m           = import_mat(matfilename)
#dist_mat1,n1,m1 = import_mat(dist_mat1_fn)

fig = pylab.figure(figsize=(8,8))

## Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
#idx1 = Z1['leaves']
#idx2 = Z2['leaves']
#X = X[idx1,:]
#X = X[:,idx1]
#X = X[:,idx2]

##labels_sort = labels[idx1]
## make sorted label list
#labels_sort = []
#for i in idx1:
#  labels_sort.append('c'+str(clusters[i]) + '-'+ labels[i])

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

#print "label1 size = ", len(labels1)
#print "label2 size = ", len(labels2)
#print "m = ", m
#print "n = ", n

#im.set_clim(0,threshold)
#im.set_clim(threshold,1)
im.set_clim(0.2,1)
axmatrix.set_ylim(-0.5, m-0.5)
axmatrix.set_xlim(-0.5, n-0.5)
#axmatrix.set_yticks([])
#axmatrix.set_xticks([])
axmatrix.set_yticks(range(0,m))
axmatrix.set_xticks(range(0,n))
axmatrix.set_xticklabels(labels2)
axmatrix.set_yticklabels(labels1)

#fontsizeval = 8
fontsizeval = 6
for i in range(0,n):
#    print i
    labels = axmatrix.xaxis.get_major_ticks()[i].label
    labels.set_fontsize(fontsizeval)
    labels.set_rotation('vertical')

for i in range(0,m): 
    labels = axmatrix.yaxis.get_major_ticks()[i].label
    labels.set_fontsize(fontsizeval)
    #labels.set_rotation('vertical')



# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
pylab.colorbar(im, cax=axcolor)
fig.show()
fig.savefig('matrix_nocluster.png',dpi=600)

