# import torch

# img_ckpt = torch.load('work_dirs/vovnet_trainval/epoch_24.pth')
# state_dict1 = img_ckpt['state_dict']

# pts_ckpt = torch.load('work_dirs/co_dab_lidar_0075v_900q_trainval/epoch_20.pth')
# state_dict2 = pts_ckpt['state_dict']
# # pts_head in camera checkpoint will be overwrite by lidar checkpoint
# state_dict1.update(state_dict2)

# merged_state_dict = state_dict1

# save_checkpoint = {'state_dict':merged_state_dict }

# torch.save(save_checkpoint, 'checkpoint/lidar_vov_trainval.pth')
# === 以上内容为原始代码，以下为修改后内容 ===
# === 融合detr3d_res101与lidar_0075v_900q权重，融合后的权重需要调用spconv1_spconv2.py进行转换 ===
# import torch
# img_ckpt = torch.load('work_dirs/detr3d_res101_gridmask/epoch_24.pth')
# state_dict1 = img_ckpt['state_dict']
# pts_ckpt = torch.load('work_dirs/lidar_0075v_900q/epoch_20.pth')
# state_dict2 = pts_ckpt['state_dict']
# state_dict1.update(state_dict2)
# merged_state_dict = state_dict1
# save_checkpoint = {'state_dict':merged_state_dict }
# torch.save(save_checkpoint, 'checkpoint/lidar_0075_cam_res101.pth')
# === 融合detr3d_vovnet与lidar_0075v_900q权重，融合后的权重需要调用spconv1_spconv2.py进行转换 ===
import torch
img_ckpt = torch.load('work_dirs/detr3d_vovnet_gridmask/epoch_24.pth')
state_dict1 = img_ckpt['state_dict']
pts_ckpt = torch.load('work_dirs/lidar_0075v_900q/epoch_20.pth')
state_dict2 = pts_ckpt['state_dict']
state_dict1.update(state_dict2)
merged_state_dict = state_dict1
save_checkpoint = {'state_dict':merged_state_dict }
torch.save(save_checkpoint, 'checkpoint/lidar_0075_cam_vovnet.pth')