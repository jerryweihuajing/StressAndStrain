# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:50:34 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Calculate boundaries from spheres system
"""

"""
1 Rasterization and calculate the pixels which spheres take up
2 Boundary Tracking: a method in Computer Vision
"""

'''
demand:
simple spheres boundary np.where to calculate the content 
'''

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append(r'C:\Users\whj\Desktop\Spyder\YADE\Stress Strain')

from Object import o_mesh
from Object import o_circle

from Module import Image as Img
from Module import ContentBoundary as CB

#============================================================================== 
#Calculate the pixels up which the spheres take
#length: length of every single grid
#factor: expand ratio
#return: a mesh object presenting content and img
def SpheresContent(which_spheres,length,factor=1,show=False):
    
    #首先找出网格的坐标范围
    x_spheres=[this_sphere.position[0] for this_sphere in which_spheres]
    y_spheres=[this_sphere.position[1] for this_sphere in which_spheres]
    
    #xy边界
    boundary_x=[min(x_spheres),max(x_spheres)]
    boundary_y=[min(y_spheres),max(y_spheres)]
    
    #xy边长
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
        
    #xy方向上的网格数
    amount_grid_x=int(np.ceil(length_x/length))
    amount_grid_y=int(np.ceil(length_y/length))
    
    #xy方向上的网格交点数
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    #total pixels
    spheres_content=[]
                 
    #traverse spheres
    for this_sphere in which_spheres:
            
        #new 2D circle
        new_circle=o_circle.circle()
        
        new_circle.radius=this_sphere.radius*factor
        new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])
        
        new_circle.Init()
        
        for this_pos in new_circle.points_inside:
            
            this_x=int(np.floor(this_pos[0]/length))
            this_y=int(np.floor(this_pos[1]/length))
            
            if 0<=this_x<amount_mesh_points_x and 0<=this_y<amount_mesh_points_y:
                    
                if [this_x,this_y] not in spheres_content:
                    
                    spheres_content.append([this_x,this_y])  

    #check the shape
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
   
#    print(np.shape(img_tag_mesh))
    
    for this_i,this_j in spheres_content:
               
        #restrict the boundary  
        if 0<=this_i<amount_grid_x and 0<=this_j<amount_grid_y:

            img_tag_mesh[this_i,this_j]=1
     
#        print(this_i,this_j)
               
    #define new mesh
    that_mesh=o_mesh.mesh()
    
    #Rotatation is in need
    that_mesh.img_tag=Img.ImgFlip(Img.ImgRotate(img_tag_mesh),0)
    that_mesh.content=spheres_content   
    
    if show:
        
        plt.imshow(img_tag_mesh)
    
    return that_mesh

'''
Calculate the elavation
the surface could be calculated, do do the 'left' 'right' 'top' 'bottom'
'''
#============================================================================== 
#Calculate spheres surface from a mesh object
#return: an dictionary presenting the elavation and coordinates
def SpheresSurfaceMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_j_i_surface={}
    
    #img tag
    for j in range(np.shape(that_mesh.img_tag)[1]):
        
        map_j_i_surface[j]=np.shape(that_mesh.img_tag)[0]
        
        for i in range(np.shape(that_mesh.img_tag)[0]):

            if that_mesh.img_tag[i,j]!=0:
                
#                print(np.shape(that_mesh.img_tag)[0]-i)
                
                map_j_i_surface[j]=i
                
                break
            
    return map_j_i_surface  
 
#==============================================================================     
#img to map: convenient to plot
#return: an img tag presenting the elavation
def SpheresSurfaceImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the surface map
    map_j_i_surface=SpheresSurfaceMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan) 
    
    #surface map to img tag
    for k in range(len(map_j_i_surface)):
        
        this_j=list(map_j_i_surface.keys())[k]
        this_i=list(map_j_i_surface.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag)
      
    return that_img_tag
 
#============================================================================== 
#Calculate spheres bottom from a mesh object
#return: an dictionary presenting the elavation and coordinates
def SpheresBottomMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_j_i_bottom={}
    
    #img tag
    for j in range(np.shape(that_mesh.img_tag)[1]):
        
        map_j_i_bottom[j]=np.shape(that_mesh.img_tag)[0]
        
        for i in range(np.shape(that_mesh.img_tag)[0]-1,-1,-1):

            if that_mesh.img_tag[i,j]!=0:
                
#                print(np.shape(that_mesh.img_tag)[0]-i)
                
                map_j_i_bottom[j]=i
                
                break
            
    return map_j_i_bottom 

#==============================================================================     
#img to map: convenient to plot
#return: an img tag presenting the elavation
def SpheresBottomImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the bottom map
    map_j_i_bottom=SpheresBottomMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan) 
    
    #bottom map to img tag
    for k in range(len(map_j_i_bottom)):
        
        this_j=list(map_j_i_bottom.keys())[k]
        this_i=list(map_j_i_bottom.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag)
      
    return that_img_tag

#============================================================================== 
#Calculate Left boundary from a mesh object
#return: an dictionary presenting the positions
def SpheresLeftMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_i_j_left={}
    
    #img tag
    for i in range(np.shape(that_mesh.img_tag)[0]):
        
        map_i_j_left[i]=np.shape(that_mesh.img_tag)[1]
        
        for j in range(np.shape(that_mesh.img_tag)[1]):

            if that_mesh.img_tag[i,j]!=0:
                
#                print(np.shape(that_mesh.img_tag)[0]-i)
                
                map_i_j_left[i]=j
                
                break
            
    return map_i_j_left 

#==============================================================================     
#img to map: convenient to plot
#return: an img tag presenting the left boundary
def SpheresLeftImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the bottom map
    map_i_j_left=SpheresLeftMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan)    
    
    #bottom map to img tag
    for k in range(len(map_i_j_left)):
        
        this_i=list(map_i_j_left.keys())[k]
        this_j=list(map_i_j_left.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag)
      
    return that_img_tag

#============================================================================== 
#Calculate right boundary from a mesh object
#return: an dictionary presenting the positions
def SpheresRightMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_i_j_right={}
    
    #img tag
    for i in range(np.shape(that_mesh.img_tag)[0]):
        
        map_i_j_right[i]=np.shape(that_mesh.img_tag)[1]
        
        for j in range(np.shape(that_mesh.img_tag)[1]-1,-1,-1):

            if that_mesh.img_tag[i,j]!=0:
                
#                print(np.shape(that_mesh.img_tag)[0]-i)
                
                map_i_j_right[i]=j
                
                break
            
    return map_i_j_right   
 
#==============================================================================     
#img to map: convenient to plot
#return: an img tag presenting the right boundary
def SpheresRightImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the bottom map
    map_i_j_right=SpheresRightMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan)    
    
    #bottom map to img tag
    for k in range(len(map_i_j_right)):
        
        this_i=list(map_i_j_right.keys())[k]
        this_j=list(map_i_j_right.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag)
      
    return that_img_tag

#==============================================================================   
#simple spheres boudary calculation
def SimpleSpheresBoundary(which_spheres,length,factor=1,show=False):
   
    #img_tag to present 4 boundary
    img_tag_left=SpheresLeftImg(which_spheres,length,factor)
    img_tag_right=SpheresRightImg(which_spheres,length,factor)
    img_tag_bottom=SpheresBottomImg(which_spheres,length,factor)
    img_tag_surface=SpheresSurfaceImg(which_spheres,length,factor)
    
    #result
    boundary=[]
    
    #4 boundaries
    img_tags=[img_tag_left,img_tag_right,img_tag_bottom,img_tag_surface]

    #traverse all tag img
    for this_img_tag in img_tags:
        
        #tag==1 content
        I=np.where(this_img_tag==1)[0]
        J=np.where(this_img_tag==1)[1]
        
        for k in range(len(I)):
            
            if [I[k],J[k]] not in boundary:
                
                boundary.append([I[k],J[k]])
    
    if show:
        
        #fetch the mesh object
        that_mesh=SpheresContent(which_spheres,length,factor)
        
        #img to present the elavation
        that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan) 
        
        #draw boundary
        for this_pos in boundary:
            
            this_i,this_j=this_pos[0],this_pos[1]
            
            that_img_tag[this_i,this_j]=1
            
            plt.imshow(that_img_tag)
            
    return boundary
 
#==============================================================================     
#edge tracing of spheres
def SpheresEdge(which_spheres,pixel_step,show=False):
    
    #edge tracing of content
    content=SpheresContent(which_spheres,pixel_step).content
    img_tag=SpheresContent(which_spheres,pixel_step).img_tag
    
    #final edge
    edge=CB.Find1stPixel(1,img_tag,content)
    
    #初始化循环中止判别标志
    flag_stop=False
    
    #初始化绝对索引
    index=-4
    
    #进行第一次邻居搜索
    edge,index,flag_stop=CB.Find1stNeighbor(1,flag_stop,edge,img_tag,index) 
    
    while len(edge)>1 and flag_stop is False:
        
        edge,index,flag_stop=CB.Find1stNeighbor(1,flag_stop,edge,img_tag,index) 
    
    #show the edge        
    if show: 
        
        for this_pos in edge:
            
            this_i,this_j=this_pos[0],this_pos[1]
            
            img_tag[this_i,this_j]=2

        plt.imshow(img_tag)
        
    return edge
        
#txt_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 0'
#ax=plt.subplot()
#this_mesh=SP.SpheresGrids(ax,spheres,1)
#
#plt.figure()
#plt.imshow(this_mesh.img_tag)
    