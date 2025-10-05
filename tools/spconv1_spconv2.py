import torch
import re

def convert_spconv_weights(checkpoint_path, output_path):
    """将 spconv 1.x 的权重转换为 spconv 2.0 格式"""
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    if 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint
    converted_state_dict = {}
    for key, weight in state_dict.items():
        if 'pts_middle_encoder' in key and 'weight' in key and len(weight.shape) == 5:
            converted_weight = weight.permute(1,2,3,4,0).contiguous()
            converted_state_dict[key] = converted_weight
            print(f"已转换 {key}: {weight.shape} -> {converted_weight.shape}")
        else:
            converted_state_dict[key] = weight
    if 'state_dict' in checkpoint:
        checkpoint['state_dict'] = converted_state_dict
        torch.save(checkpoint, output_path)
    else:
        torch.save(converted_state_dict, output_path)
    print(f"转换后的检查点已保存至 {output_path}")

convert_spconv_weights('checkpoint/lidar_0075_cam_res101.pth', 'checkpoint/lidar_0075_cam_res101_spconv2.pth')
