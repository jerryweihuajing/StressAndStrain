# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:59:21 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-boundary for global
"""

from script_thesis import *
from script_boundary import TagBoundaryExtraction
        
'''outline'''
#plot image
#import matrix from txt
case_path_global=r'E:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single'

# progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'
progress_path=case_path_global.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M_O.AddBound(C_I_S.TagImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path),bound_value=-1)),bound_value=-1)
img_rgb_from_data=C_Im.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

img_strain=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Strain-Cumulative'))))),axis=0)
img_stress=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Stress'))))),axis=0)

img_boundary=TagBoundaryExtraction(img_tag_from_data,tag_foreground=4)
            
'''strain for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_strain,cmap='PuOr',norm=colors.Normalize(vmin=-1,vmax=1))
plt.imshow(C_M_O.OutlineFromMatrix(img_strain),cmap='gray')
plt.imshow(img_boundary,cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('strain-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''stress for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_stress,cmap='ocean')
plt.imshow(C_M_O.OutlineFromMatrix(img_stress),cmap='gray')
plt.imshow(img_boundary,cmap='gray_r')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('stress-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''boundary for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_M_O.OutlineFromImgTag(img_tag_from_data),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('boundary-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''structrual deformation for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_rgb_from_data)
plt.imshow(C_M_O.OutlineFromImgTag(img_tag_from_data),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('structural deformation-global.png',dpi=300,bbox_inches='tight')
plt.close()