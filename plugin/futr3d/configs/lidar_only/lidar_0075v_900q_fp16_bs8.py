_base_ = ['./lidar_0075v_900q.py']
fp16 = dict(loss_scale='dynamic')
data = dict(samples_per_gpu=8)