from skimage import io
import numpy as np
import timeit
import os
from os import listdir
from os.path import isfile,join,isdir
from tkinter import *
from tkinter import messagebox, filedialog
import platform
    
def Derivatives(order,F,begin_timer):
    deriv_axis = []
    
    dF = np.zeros(F.shape)
    First_Derivative_Check = 0
    for derivatives in range(3):
        order_axis = np.zeros(3)
        if derivatives == 0:
            order_axis[1] = 1
        if derivatives == 1:
            order_axis[2] = 1
        if derivatives == 2:
            order_axis[0] = 1
        if order[derivatives] > 0:
            for derivs in range(order[derivatives]):
                if First_Derivative_Check != 0:
                    Upper = F[0:int(dF.shape[0]-2*order_axis[0]),0:int(dF.shape[1]-2*order_axis[1]),0:int(dF.shape[2]-2*order_axis[2])]
                    Middle = F[int(1*order_axis[0]):int(dF.shape[0]-1*order_axis[0]),int(1*order_axis[1]):int(dF.shape[1]-1*order_axis[1]),int(1*order_axis[2]):int(dF.shape[2]-1*order_axis[2])]
                    Lower = F[int(2*order_axis[0]):dF.shape[0],int(2*order_axis[1]):dF.shape[1],int(2*order_axis[2]):dF.shape[2]]
                    dF = -Upper+Middle+Lower
                if First_Derivative_Check == 0:
                    First_Derivative_Check = 1
                    Upper = F[0:int(F.shape[0]-2*order_axis[0]),0:int(F.shape[1]-2*order_axis[1]),0:int(F.shape[2]-2*order_axis[2])]
                    Middle = F[int(1*order_axis[0]):int(F.shape[0]-1*order_axis[0]),int(1*order_axis[1]):int(F.shape[1]-1*order_axis[1]),int(1*order_axis[2]):int(F.shape[2]-1*order_axis[2])]
                    Lower = F[int(2*order_axis[0]):F.shape[0],int(2*order_axis[1]):F.shape[1],int(2*order_axis[2]):F.shape[2]]
                    dF = -Upper+Middle+Lower
            
            '''
                Uncomment out the following section if smoothing is desired.  Applies 1 more level of smoothing in each axis than there a derivative was taken.
            '''
            '''
            c5 = np.array([-3,12,17,12,-3])/35
            c7 = np.array([-2,3,6,7,6,3,-2])/21
            #for smooth in range(order[derivatives]+1):
            print(dF.shape[1]-4)
            print(dF.shape[2]-4)
            print(dF.shape[0]-4)
            if order[0] > 0:
                for x_smooth in range(order[0]+1):
                    print(f'Starting to smooth {x_smooth+1} of {order[1]+1} for x ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
                    dF[:,order[0]+1,:] = (dF[:,order[0],:]+dF[:,order[0]+1,:]+dF[:,order[0]+2,:])/3
                    dF[:,dF.shape[1]-2-order[0],:] = (dF[:,dF.shape[1]-3-order[0],:]+dF[:,dF.shape[1]-2-order[0],:]+dF[:,dF.shape[1]-1-order[0],:])/3
                    dF[:,order[0]+2,:] = c5[0]*dF[:,order[0],:]+c5[1]*dF[:,order[0]+1,:]+c5[2]*dF[:,order[0]+2,:]+c5[3]*dF[:,order[0]+3,:]+c5[4]*dF[:,order[0]+4,:]
                    dF[:,dF.shape[1]-4-order[0],:] = c5[0]*dF[:,dF.shape[1]-5-order[0],:]+c5[0]*dF[:,dF.shape[1]-4-order[0],:]+c5[2]*dF[:,dF.shape[1]-3-order[0],:]+c5[3]*dF[:,dF.shape[1]-2-order[0],:]+c5[4]*dF[:,dF.shape[1]-1-order[0],:]
                    for x in range(4+order[0],dF.shape[1]-4-2*order[0]):
                        dF[:,4+x,:] =  c7[0]*dF[:,x-3,:]+c7[1]*dF[:,x-2,:]+c7[2]*dF[:,x-1,:]+c7[3]*dF[:,x,:]+c7[4]*dF[:,x+1,:]+c7[5]*dF[:,x+2,:]+c7[6]*dF[:,x+3,:]
            if order[1] > 0:
                for y_smooth in range(order[1]+1):
                    print(f'Starting to smooth {y_smooth+1} of {order[2]+1} for y ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
                    dF[:,:,2] = (dF[:,:,1]+dF[:,:,2]+dF[:,:,3])/3
                    dF[:,:,dF.shape[2]-3] = (dF[:,:,dF.shape[2]-4]+dF[:,:,dF.shape[2]-3]+dF[:,:,dF.shape[2]-2])/3
                    dF[:,:,3] = c5[0]*dF[:,:,1]+c5[1]*dF[:,:,2]+c5[2]*dF[:,:,3]+c5[3]*dF[:,:,4]+c5[4]*dF[:,:,5]
                    dF[:,:,dF.shape[2]-4] = c5[0]*dF[:,:,dF.shape[2]-6]+c5[1]*dF[:,:,dF.shape[2]-5]+c5[2]*dF[:,:,dF.shape[2]-4]+c5[3]*dF[:,:,dF.shape[2]-3]+c5[4]*dF[:,:,dF.shape[2]-2]
                    for y in range(dF.shape[2]-4):
                        dF[:,:,4+y] =  c7[0]*dF[:,:,1+y]+c7[1]*dF[:,:,2+y]+c7[2]*dF[:,:,3+y]+c7[3]*dF[:,:,4+y]+c7[4]*dF[:,:,5+y]+c7[5]*dF[:,:,6+y]+c7[6]*dF[:,:,7+y]
            if order[2] > 0:
                for z_smooth in range(order[2]+1):
                    print(f'Starting to smooth {z_smooth+1} of {order[0]+1} for z ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
                    dF[2,:,:] = (dF[1,:,:]+dF[2,:,:]+dF[3,:,:])/3
                    dF[dF.shape[0]-3,:,:] = (dF[dF.shape[0]-4,:,:]+dF[dF.shape[0]-3,:,:]+dF[dF.shape[0]-2,:,:])/3
                    dF[3,:,:] = c5[0]*dF[1,:,:]+c5[1]*dF[2,:,:]+c5[2]*dF[3,:,:]+c5[3]*dF[4,:,:]+c5[4]*dF[5,:,:]
                    dF[dF.shape[0]-4,:,:] = c5[0]*dF[dF.shape[0]-6,:,:]+c5[1]*dF[dF.shape[0]-5,:,:]+c5[2]*dF[dF.shape[0]-4,:,:]+c5[3]*dF[dF.shape[0]-3,:,:]+c5[4]*dF[dF.shape[0]-2,:,:]
                    for z in range(dF.shape[0]-4):
                        dF[4+z,:,:] =  c7[0]*dF[1+z,:,:]+c7[1]*dF[2+z,:,:]+c7[2]*dF[3+z,:,:]+c7[3]*dF[4+z,:,:]+c7[4]*dF[5+z,:,:]+c7[5]*dF[6+z,:,:]+c7[6]*dF[7+z,:,:]
            '''
    return dF
    
def Order_Holograms_After_Reconstruction(folderPath):
    
    File_Names = np.array([(f,float(f.name)) for f in os.scandir(folderPath)])
    #Descending_Order = File_Names[(-File_Names[:,1]).argsort()]
    Ascending_Order = File_Names[File_Names[:,1].argsort()]
    file_names_combined = np.zeros((len(Ascending_Order),len(listdir(Ascending_Order[0,0].path)))).astype(np.unicode_)
    Organized_Files = []
    for x in range(len(Ascending_Order)):
        onlyfiles = [onlyfiles for onlyfiles in listdir(Ascending_Order[x,0].path) if isfile(join(Ascending_Order[x,0],onlyfiles))]
        z_slice_time_stamp_names = np.array([onlyfiles[x].split('.') for x in range(len(onlyfiles))])
        file_names_combined[x] = np.array([z_slice_time_stamp_names[z_slice_time_stamp_names[:,0].astype(np.float).argsort()][x][0]+'.'+z_slice_time_stamp_names[z_slice_time_stamp_names[:,0].astype(np.float).argsort()][x][1] for x in range(len(onlyfiles))])
        
    for x in range(len(file_names_combined[:,0])):
        for y in range(len(file_names_combined[0,:])):
            Organized_Files.append(Ascending_Order[x,0].path+'/'+str(file_names_combined[x,y]))
    Organized_Files = np.array(Organized_Files).reshape((len(file_names_combined[:,0]),len(file_names_combined[0,:])))
    
    return Organized_Files


def Derivative_Start(folderPath_Input,folderPath_Output,deriv_order):
    begin_timer = timeit.default_timer()
    
    GUI.update()
    
    Organize_Start = timeit.default_timer()
    Organized_Files = Order_Holograms_After_Reconstruction(folderPath_Input)
    Organized_End = timeit.default_timer()
    print(f'Time to organize Reconstruction Files ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
    
    Array_Shape = io.imread(Organized_Files[0,0])
    
    maximum_time_z_slices = 5000
    maximum_time_slices_allowed = int(np.floor(maximum_time_z_slices/Organized_Files.shape[0]))
    
    Number_of_Holograms_Needed = int(np.ceil(Organized_Files.shape[1]/maximum_time_slices_allowed))
    save_points = np.zeros(Number_of_Holograms_Needed)
    holograms_made = 0
    t_slice_counter = 0
    first_slice = 1
    
    slices_to_run_if_testing = 1
    
    if Save_As_Singles_Check.get() == 1:
        Deriv_Stack = np.zeros((Organized_Files.shape[0]-2*deriv_order[2],Array_Shape.shape[0]-2*deriv_order[0],Array_Shape.shape[1]-2*deriv_order[1]),'<f4')
        for time_slice in range(Organized_Files.shape[1]):
            Input_Stack = np.zeros((Organized_Files.shape[0],Array_Shape.shape[0],Array_Shape.shape[1]),'<f4')
            for z_slice in range(Organized_Files.shape[0]):
                if time_slice == 0:
                    if z_slice == 0:
                        Input_Stack[0,:,:] = Array_Shape
                    if z_slice != 0:
                        Input_Stack[z_slice,:,:] = io.imread(Organized_Files[z_slice,time_slice],'<f4')
                if time_slice != 0:
                    Input_Stack[z_slice,:,:] = io.imread(Organized_Files[z_slice,time_slice],'<f4')
            Deriv_Stack = Derivatives(deriv_order,Input_Stack,begin_timer)
            print(f'\nFinished derivative of time slice {time_slice+1} ({np.round(timeit.default_timer() - begin_timer,3)} seconds)\n')
        
            print(f'Started Saving time slice {time_slice+1} ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
            io.imsave(folderPath_Output+'/'+str(time_slice+1)+'_Deriv_'+str(int(deriv_order[0]))+'_'+str(int(deriv_order[1]))+'_'+str(int(deriv_order[2]))+'.tif',Deriv_Stack)
            print(f'Finished Saving time slice {time_slice+1} ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
    
    if Save_As_Hyperstack_Check.get() == 1:
    
        if Number_of_Holograms_Needed > 1:
            for x in range(Number_of_Holograms_Needed-1):
                save_points[x] = save_points[x-1]+maximum_time_slices_allowed
            save_points[Number_of_Holograms_Needed-1] = save_points[Number_of_Holograms_Needed-2] + Organized_Files.shape[1]%maximum_time_slices_allowed
            Deriv_Stack = np.zeros((maximum_time_slices_allowed,Organized_Files.shape[0]-2*deriv_order[2],Array_Shape.shape[0]-2*deriv_order[0],Array_Shape.shape[1]-2*deriv_order[1]),'<f4')
        if Number_of_Holograms_Needed == 1:
            save_points[0] = Organized_Files.shape[1]%maximum_time_slices_allowed
            Deriv_Stack = np.zeros((Organized_Files.shape[1],Organized_Files.shape[0]-2*deriv_order[2],Array_Shape.shape[0]-2*deriv_order[0],Array_Shape.shape[1]-2*deriv_order[1]),'<f4')
        
        for time_slice in range(Organized_Files.shape[1]):
            Input_Stack = np.zeros((Organized_Files.shape[0],Array_Shape.shape[0],Array_Shape.shape[1]),'<f4')
            for z_slice in range(Organized_Files.shape[0]):
                if time_slice == 0:
                    if z_slice == 0:
                        Input_Stack[0,:,:] = Array_Shape
                    if z_slice != 0:
                        Input_Stack[z_slice,:,:] = io.imread(Organized_Files[z_slice,time_slice],'<f4')
                if time_slice != 0:
                    Input_Stack[z_slice,:,:] = io.imread(Organized_Files[z_slice,time_slice],'<f4')
            Deriv_Stack[t_slice_counter,:,:,:] = Derivatives(deriv_order,Input_Stack,begin_timer)
            print(f'Finished derivative of time slice {time_slice+1} ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
            
            t_slice_counter += 1
            
            if time_slice == save_points[holograms_made]-1:
                if Number_of_Holograms_Needed > 1:
                    print(f'\nMaximum Time Slices Allowed in One Array - Saving Full Array ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
                    io.imsave(folderPath_Output+'/'+str(first_slice)+'_'+str(time_slice+1)+'_Deriv_'+str(int(deriv_order[0]))+'_'+str(int(deriv_order[1]))+'_'+str(int(deriv_order[2]))+'.tif',Deriv_Stack)
                    print(f'Finished Saving Full Array ({np.round(timeit.default_timer() - begin_timer,3)} seconds)\n')
                    if Organized_Files.shape[1]-time_slice-1>=maximum_time_slices_allowed:
                        Deriv_Stack = np.zeros((maximum_time_slices_allowed,Organized_Files.shape[0]-2*deriv_order[2],Array_Shape.shape[0]-2*deriv_order[0],Array_Shape.shape[1]-2*deriv_order[1]),'<f4')
                    if Organized_Files.shape[1]-time_slice-1<maximum_time_slices_allowed:
                        Deriv_Stack = np.zeros((Organized_Files.shape[1]-time_slice-1,Organized_Files.shape[0]-2*deriv_order[2],Array_Shape.shape[0]-2*deriv_order[0],Array_Shape.shape[1]-2*deriv_order[1]),'<f4')
            
                
            if (time_slice+1)%maximum_time_slices_allowed==0:
                holograms_made += 1
                first_slice += maximum_time_slices_allowed
                t_slice_counter = 0
    if Save_As_Hyperstack_Check.get() == 1:
        if Number_of_Holograms_Needed == 1:
            print(f'\nStarted Saving ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
            io.imsave(folderPath_Output+'/'+str(first_slice)+'_'+str(time_slice+1)+'_Deriv_'+str(int(deriv_order[0]))+'_'+str(int(deriv_order[1]))+'_'+str(int(deriv_order[2]))+'.tif',Deriv_Stack)
            print(f'Finished Saving ({np.round(timeit.default_timer() - begin_timer,3)} seconds)')
    
def Error_Check():
    Errors_Found = np.zeros(3)
    Overall_Error_Message_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Overall_Error_Spacing.get(),window=Overall_Error_Message)
    Input_Error_Label_Canvas = GUI_canvas.create_window(Input_Output_Error_Symbol_Horizontal.get(),Input_Spacing.get(),window=Input_Error_Symbol)
    Output_Error_Label_Canvas = GUI_canvas.create_window(Input_Output_Error_Symbol_Horizontal.get(),Output_Spacing.get(),window=Output_Folder_Error_Symbol)
    Input_Folder_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Input_Error_Spacing.get(),window=Input_Folder_Error)
    Input_Subfolder_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Input_Error_Spacing.get(),window=Input_Subfolder_Error)
    Input_Reconstruction_File_Name_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Input_Error_Spacing.get(),window=Input_Reconstruction_File_Name_Error)
    Input_Reconstruction_File_Type_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Input_Error_Spacing.get(),window=Input_Reconstruction_File_Type_Error)
    Input_Reconstruction_No_Files_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Input_Error_Spacing.get(),window=Input_Reconstruction_No_Files_Error)
    Input_Reconstruction_Invalid_Files_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Input_Error_Spacing.get(),window=Input_Reconstruction_Invalid_Files_Error)
    Output_Directory_Folder_Error_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Output_Error_Spacing.get(),window=Output_Folder_Error_Message)
    Deriv_Summation_Error_Message_Canvas = GUI_canvas.create_window(Derive_Error_Message_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_Summation_Error_Message)
    Deriv_Error_Symbol_Canvas = GUI_canvas.create_window(Deriv_Error_Symbol_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_Error_Symbol)
    Deriv_Positive_Error_Message_Canvas = GUI_canvas.create_window(Derive_Error_Message_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_Positive_Error_Message)
    Deriv_Incorrect_Characters_Error_Message_Canvas = GUI_canvas.create_window(Derive_Error_Message_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_Incorrect_Characters_Error_Message)
    Overall_Error_Message_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Overall_Error_Spacing.get(),window=Overall_Error_Message)
    
    
    '''
        Check if reconstructions in the input folder selected are formatted properly
    '''
    
    if not isdir(Input_Directory_Text.get()):
        Errors_Found[0] = 1
        Input_Folder_Error_Check.set(1)
        
    if Input_Folder_Error_Check.get() == 0:
        try:
            np.array([(f,float(f.name)) for f in os.scandir(Input_Directory_Text.get())])
        except ValueError:
            Errors_Found[0] = 1
            Input_Subfolder_Error_Check.set(1)
        else:
            Folder_Names = np.array([(f,float(f.name)) for f in os.scandir(Input_Directory_Text.get())])
            Descending_Order = Folder_Names[(-Folder_Names[:,1]).argsort()]
            if len(Folder_Names) == 0:
                Errors_Found[0] = 1
                Input_Subfolder_Error_Check.set(1)
            if len(Folder_Names) > 0:
                pass
                
        if Input_Subfolder_Error_Check.get() == 0:
            for folders in range(len(Descending_Order)):
                try:
                    [[File_Names.split('.')[0],File_Names.split('.')[1]] for File_Names in listdir(Descending_Order[folders,0].path) if isfile(join(Descending_Order[folders,0],File_Names))]
                except:
                    Input_Reconstruction_Invalid_Files_Error_Check.set(1)
                    issues_found = 1
                else:
                    File_Names = [[File_Names.split('.')[0],File_Names.split('.')[1]] for File_Names in listdir(Descending_Order[folders,0].path) if isfile(join(Descending_Order[folders,0],File_Names))]
                    if len(File_Names) == 0:
                        Input_Reconstruction_No_Files_Error_Check.set(1)
                    if len(File_Names)>0:
                        filename_check = np.zeros(len(File_Names))
                        filetype_check = np.zeros(len(File_Names)).astype(np.unicode_)
                        issues_found = 0
                        for x in range(len(File_Names)):
                            proceed = 0
                            try:
                                filename_check[x] = File_Names[x][0]
                            except ValueError:
                                issues_found = 1
                                Input_Reconstruction_File_Name_Error_Check.set(1)
                                break
                            if File_Names[x][1] != 'tif' and File_Names[x][1] != 'tiff':
                                issues_found = 1
                                Input_Reconstruction_File_Type_Error_Check.set(1)
                                break
                        if issues_found==1:
                            Errors_Found[0] = 1
                            break
               
    if Input_Folder_Error_Check.get() == 1:
        GUI_canvas.delete(Input_Subfolder_Error_Canvas)
        GUI_canvas.delete(Input_Reconstruction_Invalid_Files_Error_Canvas)
        GUI_canvas.delete(Input_Reconstruction_No_Files_Error_Canvas)
        GUI_canvas.delete(Input_Reconstruction_File_Name_Error_Canvas)
        GUI_canvas.delete(Input_Reconstruction_File_Type_Error_Canvas)
    if Input_Folder_Error_Check.get() == 0:
        GUI_canvas.delete(Input_Folder_Error_Canvas)
    
        if Input_Subfolder_Error_Check.get() == 1:
            GUI_canvas.delete(Input_Folder_Error_Canvas)
            GUI_canvas.delete(Input_Reconstruction_Invalid_Files_Error_Canvas)
            GUI_canvas.delete(Input_Reconstruction_No_Files_Error_Canvas)
            GUI_canvas.delete(Input_Reconstruction_File_Name_Error_Canvas)
            GUI_canvas.delete(Input_Reconstruction_File_Type_Error_Canvas)
        if Input_Subfolder_Error_Check.get() == 0:
            GUI_canvas.delete(Input_Subfolder_Error_Canvas)
            
            if Input_Reconstruction_Invalid_Files_Error_Check.get() == 1:
                GUI_canvas.delete(Input_Folder_Error_Canvas)
                GUI_canvas.delete(Input_Subfolder_Error_Canvas)
                GUI_canvas.delete(Input_Reconstruction_No_Files_Error_Canvas)
                GUI_canvas.delete(Input_Reconstruction_File_Name_Error_Canvas)
                GUI_canvas.delete(Input_Reconstruction_File_Type_Error_Canvas)
            if Input_Reconstruction_Invalid_Files_Error_Check.get() == 0:
                GUI_canvas.delete(Input_Reconstruction_Invalid_Files_Error_Canvas)
                
                if Input_Reconstruction_No_Files_Error_Check.get() == 1:
                    GUI_canvas.delete(Input_Folder_Error_Canvas)
                    GUI_canvas.delete(Input_Subfolder_Error_Canvas)
                    GUI_canvas.delete(Input_Reconstruction_Invalid_Files_Error_Canvas)
                    GUI_canvas.delete(Input_Reconstruction_File_Name_Error_Canvas)
                    GUI_canvas.delete(Input_Reconstruction_File_Type_Error_Canvas)
                if Input_Reconstruction_No_Files_Error_Check.get() == 0:
                    GUI_canvas.delete(Input_Reconstruction_No_Files_Error_Canvas)
                    
                    if Input_Reconstruction_File_Name_Error_Check.get() == 1:
                        GUI_canvas.delete(Input_Folder_Error_Canvas)
                        GUI_canvas.delete(Input_Subfolder_Error_Canvas)
                        GUI_canvas.delete(Input_Reconstruction_Invalid_Files_Error_Canvas)
                        GUI_canvas.delete(Input_Reconstruction_No_Files_Error_Canvas)
                        GUI_canvas.delete(Input_Reconstruction_File_Type_Error_Canvas)
                    if Input_Reconstruction_File_Name_Error_Check.get() == 0:
                        GUI_canvas.delete(Input_Reconstruction_File_Name_Error_Canvas)
                            
                        if Input_Reconstruction_File_Type_Error_Check.get() == 0:
                            GUI_canvas.delete(Input_Reconstruction_File_Type_Error_Canvas)
                        if Input_Reconstruction_File_Type_Error_Check.get() == 1:
                            GUI_canvas.delete(Input_Folder_Error_Canvas)
                            GUI_canvas.delete(Input_Subfolder_Error_Canvas)
                            GUI_canvas.delete(Input_Reconstruction_Invalid_Files_Error_Canvas)
                            GUI_canvas.delete(Input_Reconstruction_No_Files_Error_Canvas)
                            GUI_canvas.delete(Input_Reconstruction_File_Name_Error_Canvas)
    
    if Input_Folder_Error_Check.get() == 0 and Input_Subfolder_Error_Check.get() == 0 and Input_Reconstruction_File_Name_Error_Check.get() == 0 and Input_Reconstruction_File_Type_Error_Check.get() == 0:
        GUI_canvas.delete(Input_Error_Label_Canvas)
    
    '''
        Check if the output directory exists
    '''
    
    if not isdir(Deriv_Output_Directory_Text.get()) or Deriv_Output_Directory_Text.get() == '(Required)':
        Errors_Found[1] = 1
    if isdir(Deriv_Output_Directory_Text.get()) and Deriv_Output_Directory_Text.get() != '(Required)':
            GUI_canvas.delete(Output_Error_Label_Canvas)
            GUI_canvas.delete(Output_Directory_Folder_Error_Canvas)
    
    '''
        Verify the x derivative entry contains only non-negative numbers
    '''
    
    try:
        np.array(Deriv_x_Value.get()).astype(int)>=0
    except ValueError:
        Deriv_x_check.set(1)
        Errors_Found[2] = 1
    else:
        Deriv_x_check.set(0)
        
    try:
        np.array(Deriv_y_Value.get()).astype(int)>=0
    except ValueError:
        Deriv_y_check.set(1)
        Errors_Found[2] = 1
    else:
        Deriv_y_check.set(0)
        
    try:
        np.array(Deriv_z_Value.get()).astype(int)>=0
    except ValueError:
        Deriv_z_check.set(1)
        Errors_Found[2] = 1
    else:
        Deriv_z_check.set(0)
        
    if Deriv_x_check.get() == 1 or Deriv_y_check.get() == 1 or Deriv_z_check.get() == 1:
        Errors_Found[2] = 1
        GUI_canvas.delete(Deriv_Summation_Error_Message_Canvas)
        GUI_canvas.delete(Deriv_Positive_Error_Message_Canvas)
        
    if Deriv_x_check.get() == 0 and Deriv_y_check.get() == 0 and Deriv_z_check.get() == 0:
        GUI_canvas.delete(Deriv_Incorrect_Characters_Error_Message_Canvas)
        dx,dy,dz = np.array(Deriv_x_Value.get()).astype(int),np.array(Deriv_y_Value.get()).astype(int),np.array(Deriv_z_Value.get()).astype(int)
        if dx + dy + dz < 0:
            Errors_Found[2] = 1
            GUI_canvas.delete(Deriv_Summation_Error_Message_Canvas)
            Deriv_Summation_Error_Message_Canvas = GUI_canvas.create_window(Derive_Error_Message_Horizontal.get(),Start_Button_Spacing.get(),window=Deriv_Summation_Error_Message)
        if dx + dy + dz == 0:
            Errors_Found[2] = 1
            GUI_canvas.delete(Deriv_Positive_Error_Message_Canvas)
        if dx + dy + dz > 0:
            GUI_canvas.delete(Deriv_Summation_Error_Message_Canvas)
            GUI_canvas.delete(Deriv_Positive_Error_Message_Canvas)
            GUI_canvas.delete(Deriv_Error_Symbol_Canvas)
    if np.count_nonzero(Errors_Found==1) == 0:
        GUI_canvas.delete(Overall_Error_Message_Canvas)
        Save_Option_Window()
        
def Deriv_Output_Directory():
    Deriv_Output_Directory_Text.set('')
    Deriv_Output_Directory_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Deriv_Output_Directory_Text_Entry.insert(END,Deriv_Output_Directory_Chosen)
    if Deriv_Output_Directory_Text.get() == '':
        Deriv_Output_Directory_Text.set('(Required)')
def Input_Directory():
    Input_Directory_Text.set('')
    Input_Direction_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Input_Directory_Text_Entry.insert(END,Input_Direction_Chosen)
    if Input_Directory_Text.get() == '':
        Input_Directory_Text.set('(Required)')

def Save_Option_Window():
    save_choices = Tk()
    save_canvas = Canvas(save_choices)
    save_canvas.pack()
    
    def Save_As_Hyperstack():
        Save_As_Hyperstack_Check.set(1)
        Save_As_Singles_Check.set(0)
        Close_And_Run()
    
    def Save_As_Singles():
        Save_As_Hyperstack_Check.set(0)
        Save_As_Singles_Check.set(1)
        Close_And_Run()
    
    def Close_And_Run():
        save_choices.destroy()
        Derivative_Start(Input_Directory_Text.get(),Deriv_Output_Directory_Text.get(),np.array([np.array(Deriv_x_Value.get()).astype(int),np.array(Deriv_y_Value.get()).astype(int),np.array(Deriv_z_Value.get()).astype(int)]))
        
    
    Save_Options_Label = Label(save_canvas,text='Save derivative tifs as a hyperstack or individual files?')
    Save_Options_Label_Canvas = save_canvas.create_window(150,28,window=Save_Options_Label)
    Save_As_Hyperstack_Button = Button(save_choices,text='Save as hyperstack',command=Save_As_Hyperstack)
    Save_As_Hyperstack_Button_Canvas = save_canvas.create_window(75,56,window=Save_As_Hyperstack_Button)
    Save_As_Singles_Button = Button(save_choices,text='Save individual tifs',command=Save_As_Singles)
    Save_As_Singles_Button_Canvas = save_canvas.create_window(225,56,window=Save_As_Singles_Button)
    
    save_choices.title('Save Options')
    w = 300 # width for the Tk save_choices
    h = 100 # height for the Tk save_choices
    ws = save_choices.winfo_screenwidth() # width of the screen
    hs = save_choices.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    save_choices.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    
if __name__ == '__main__':
    GUI = Tk()
    
    myframe = Frame(GUI)
    myframe.pack(fill=BOTH, expand=YES)
    GUI_canvas = Canvas(myframe, relief = 'raised')
    GUI_canvas.pack(fill=BOTH, expand=YES)
    
    '''
        Variables initialized to be used in the python graphical user interface (GUI) script.
    '''
    
    Input_Directory_Text = StringVar()
    Deriv_Output_Directory_Text = StringVar()
    Save_As_Hyperstack_Check = IntVar()
    Save_As_Singles_Check = IntVar()
    Deriv_x_Value = StringVar()
    Deriv_y_Value = StringVar()
    Deriv_z_Value = StringVar()
    Input_Folder_Error_Check = IntVar()
    Input_Subfolder_Error_Check = IntVar()
    Input_Reconstruction_File_Name_Error_Check = IntVar()
    Input_Reconstruction_File_Type_Error_Check = IntVar()
    Input_Reconstruction_No_Files_Error_Check = IntVar()
    Input_Reconstruction_Invalid_Files_Error_Check = IntVar()
    Error_Check_Output = IntVar()
    Error_Check_Deriv = IntVar()
    Deriv_x_check = IntVar()
    Deriv_y_check = IntVar()
    Deriv_z_check = IntVar()
    
    '''
        Variables are pre-set to not be blank, to pre-set the values for continued use uncomment out the second of each line by deleting the pound symbol (#).  Then fill in your directory variables with the input/output path and the output variables with the desired names.
    '''
    
    Input_Directory_Text.set('(Required)')
    #Input_Directory_Text.set('')
    Deriv_Output_Directory_Text.set('(Required)')
    #Deriv_Output_Directory_Text.set('')
    Deriv_x_Value.set('0')
    #Deriv_x_Value.set('')
    Deriv_y_Value.set('0')
    #Deriv_y_Value.set('')
    Deriv_z_Value.set('1')
    #Deriv_z_Value.set('')
    
    '''
        Labels initialized for use in the GUI, these display the text on the GUI_canvas.
    '''
    
    Introduction_Message = Label(GUI,text='Select the folder with your reconstructions for input and the output for where the deriv stacks will be placed.')
    Deriv_x_Label = Label(GUI,text='Order of dx:')
    Deriv_y_Label = Label(GUI,text='Order of dy:')
    Deriv_z_Label = Label(GUI,text='Order of dz:')
    
    '''
        Error messages/symbols
    '''
    
    Overall_Error_Message = Label(GUI,text='Missing Correct Inputs(*), Please Correct And Try Again')
    Input_Error_Symbol = Label(GUI,text='*')
    Input_Folder_Error = Label(GUI,text='Reconstruction Directory Is Not A Valid Directory')
    Input_Subfolder_Error = Label(GUI,text='Reconstruction Directory Does Not Contain Valid Folders')
    Input_Reconstruction_File_Name_Error = Label(GUI,text='Reconstruction Directory Contains Invalid File Names')
    Input_Reconstruction_File_Type_Error = Label(GUI,text='Reconstruction Directory Contains Invalid File Types')
    Input_Reconstruction_No_Files_Error = Label(GUI,text='Reconstruction Directory Contains No Files')
    Input_Reconstruction_Invalid_Files_Error = Label(GUI,text='Reconstruction Directory Contains Invalid Files')
    Deriv_Error_Symbol = Label(GUI,text='*')
    Deriv_Incorrect_Characters_Error_Message = Label(GUI,text='Deriv Order Must Be Numbers Only')
    Deriv_Positive_Error_Message = Label(GUI,text='Non-Negative Integers Only (>=0)')
    Output_Folder_Error_Symbol = Label(GUI,text='*')
    Output_Folder_Error_Message = Label(GUI,text='Deriv Output Is Not A Valid Directory')
    Deriv_Summation_Error_Message = Label(GUI,text='Sum Of Orders Must Be Greater Than Zero')
    
    
    '''
        Buttons initialized for use in the GUI, these display the text on the GUI_canvas.
    '''
    
    Input_Directory_Button = Button(GUI,text='Select Reconstruction Input Directory',command=Input_Directory,width=29)
    Deriv_Output_Directory_Button = Button(GUI,text='Select Derivative Output Directory',command=Deriv_Output_Directory,width=29)
    Start_Button = Button(GUI,text='Take Derivative',command=Error_Check)
    
    '''
       Entries initialized for use in the GUI, these are populated by the variables to display what folders are being used and names for output files.
    '''
    Deriv_Entry_Width = 3
    if platform.system() == 'Windows':
        Directory_Entry_Width = 90
    if platform.system() == 'Darwin':
        Directory_Entry_Width = 90
    if platform.system() == 'Linux':
        Directory_Entry_Width = 90
    
    Input_Directory_Text_Entry = Entry(GUI,textvariable=Input_Directory_Text,width=Directory_Entry_Width)
    Deriv_Output_Directory_Text_Entry = Entry(GUI,textvariable=Deriv_Output_Directory_Text,width=Directory_Entry_Width)
    Deriv_x_Entry = Entry(GUI,textvariable=Deriv_x_Value,width=Deriv_Entry_Width)
    Deriv_y_Entry = Entry(GUI,textvariable=Deriv_y_Value,width=Deriv_Entry_Width)
    Deriv_z_Entry = Entry(GUI,textvariable=Deriv_z_Value,width=Deriv_Entry_Width)
    
    '''
        The placement of each component in the vertical direction is determined by a spacing of 28 units, each next set is given a value of 28 units below the previous one.  This allows for a smooth increase should sections need to be added or removed.
    '''
    
    gap,Intro_Spacing,Overall_Error_Spacing,Input_Spacing,Input_Error_Spacing,Output_Spacing,Output_Error_Spacing,Deriv_Order_Spacing,Start_Button_Spacing = IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()
    
    gap.set(28)
    Intro_Spacing.set(.25*gap.get())
    Overall_Error_Spacing.set((Intro_Spacing.get()/gap.get()+1)*gap.get())
    Input_Spacing.set((Overall_Error_Spacing.get()/gap.get()+1)*gap.get())
    Input_Error_Spacing.set((Input_Spacing.get()/gap.get()+1)*gap.get())
    Output_Spacing.set((Input_Error_Spacing.get()/gap.get()+1)*gap.get())
    Output_Error_Spacing.set((Output_Spacing.get()/gap.get()+1)*gap.get())
    Deriv_Order_Spacing.set((Output_Error_Spacing.get()/gap.get()+1)*gap.get())
    Start_Button_Spacing.set((Deriv_Order_Spacing.get()/gap.get()+1)*gap.get())
    
    Center_Messages_Horizontal,Input_Output_Button_Horizontal,Input_Output_Entry_Horizontal,Input_Output_Error_Symbol_Horizontal,Deriv_x_Horizontal,Deriv_y_Horizontal,Deriv_z_Horizontal,Deriv_x_Entry_Horizontal,Deriv_y_Entry_Horizontal,Deriv_z_Entry_Horizontal,Deriv_Error_Symbol_Horizontal,Derive_Error_Message_Horizontal = IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()
    
    if platform.system() == 'Windows':
        Center_Messages_Horizontal.set(425)
        Input_Output_Button_Horizontal.set(150)
        Input_Output_Entry_Horizontal.set(532)
        Input_Output_Error_Symbol_Horizontal.set(25)
        Deriv_Error_Symbol_Horizontal.set(240)
        Deriv_x_Horizontal.set(Deriv_Error_Symbol_Horizontal.get()+55)
        Deriv_x_Entry_Horizontal.set(Deriv_x_Horizontal.get()+50)
        Deriv_y_Horizontal.set(Deriv_x_Entry_Horizontal.get()+50)
        Deriv_y_Entry_Horizontal.set(Deriv_y_Horizontal.get()+50)
        Deriv_z_Horizontal.set(Deriv_y_Entry_Horizontal.get()+50)
        Deriv_z_Entry_Horizontal.set(Deriv_z_Horizontal.get()+50)
        Derive_Error_Message_Horizontal.set(Deriv_z_Entry_Horizontal.get()+135)
        
    if platform.system() == 'Darwin':
        Center_Messages_Horizontal.set(425)
        Input_Output_Button_Horizontal.set(150)
        Input_Output_Entry_Horizontal.set(532)
        Input_Output_Error_Symbol_Horizontal.set(25)
        Deriv_Error_Symbol_Horizontal.set(240)
        Deriv_x_Horizontal.set(Deriv_Error_Symbol_Horizontal.get()+55)
        Deriv_x_Entry_Horizontal.set(Deriv_x_Horizontal.get()+50)
        Deriv_y_Horizontal.set(Deriv_x_Entry_Horizontal.get()+50)
        Deriv_y_Entry_Horizontal.set(Deriv_y_Horizontal.get()+50)
        Deriv_z_Horizontal.set(Deriv_y_Entry_Horizontal.get()+50)
        Deriv_z_Entry_Horizontal.set(Deriv_z_Horizontal.get()+50)
        Derive_Error_Message_Horizontal.set(Deriv_z_Entry_Horizontal.get()+135)
        
    if platform.system() == 'Linux':
        Center_Messages_Horizontal.set(425)
        Input_Output_Button_Horizontal.set(150)
        Input_Output_Entry_Horizontal.set(532)
        Input_Output_Error_Symbol_Horizontal.set(25)
        Deriv_Error_Symbol_Horizontal.set(240)
        Deriv_x_Horizontal.set(Deriv_Error_Symbol_Horizontal.get()+55)
        Deriv_x_Entry_Horizontal.set(Deriv_x_Horizontal.get()+50)
        Deriv_y_Horizontal.set(Deriv_x_Entry_Horizontal.get()+50)
        Deriv_y_Entry_Horizontal.set(Deriv_y_Horizontal.get()+50)
        Deriv_z_Horizontal.set(Deriv_y_Entry_Horizontal.get()+50)
        Deriv_z_Entry_Horizontal.set(Deriv_z_Horizontal.get()+50)
        Derive_Error_Message_Horizontal.set(Deriv_z_Entry_Horizontal.get()+135)
    
    
    Introduction_Message_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Intro_Spacing.get(),window=Introduction_Message)
    Input_Directory_Button_Canvas = GUI_canvas.create_window(Input_Output_Button_Horizontal.get(),Input_Spacing.get(),window=Input_Directory_Button)
    Input_Directory_Text_Entry_Canvas = GUI_canvas.create_window(Input_Output_Entry_Horizontal.get(),Input_Spacing.get(),window=Input_Directory_Text_Entry)
    Deriv_Output_Directory_Button_Canvas = GUI_canvas.create_window(Input_Output_Button_Horizontal.get(),Output_Spacing.get(),window=Deriv_Output_Directory_Button)
    Deriv_Output_Directory_Text_Entry_Canvas = GUI_canvas.create_window(Input_Output_Entry_Horizontal.get(),Output_Spacing.get(),window=Deriv_Output_Directory_Text_Entry)
    Deriv_x_Label_Canvas = GUI_canvas.create_window(Deriv_x_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_x_Label)
    Deriv_x_Entry_Canvas = GUI_canvas.create_window(Deriv_x_Entry_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_x_Entry)
    Deriv_y_Label_Canvas = GUI_canvas.create_window(Deriv_y_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_y_Label)
    Deriv_y_Entry_Canvas = GUI_canvas.create_window(Deriv_y_Entry_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_y_Entry)
    Deriv_z_Label_Canvas = GUI_canvas.create_window(Deriv_z_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_z_Label)
    Deriv_z_Entry_Canvas = GUI_canvas.create_window(Deriv_z_Entry_Horizontal.get(),Deriv_Order_Spacing.get(),window=Deriv_z_Entry)
    Start_Button_Canvas = GUI_canvas.create_window(Center_Messages_Horizontal.get(),Start_Button_Spacing.get(),window=Start_Button)
    
    
    
    w = Center_Messages_Horizontal.get()*2 # width for the Tk GUI
    h = (Start_Button_Spacing.get()/gap.get()+1)*gap.get() # height for the Tk root
    ws = GUI.winfo_screenwidth() # width of the screen
    hs = GUI.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    GUI.geometry('%dx%d+%d+%d' % (w, h, x, y))
    GUI.title("Derivative")
    GUI.mainloop()