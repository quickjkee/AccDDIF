import subprocess
import shutil


def run(path_to_model, n_steps):

    print('===============================================================================================================================')
    print(f'===================GENERATION STARTED using {path_to_model}===================')
    subprocess.call(f"CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7 torchrun --standalone --nproc_per_node=7 edm/generate.py --outdir=fid-tmp --seeds=100000-149999 --subdirs \
        --network={path_to_model} --steps={n_steps}", shell=True)


    print('===================FID CALCULATION===================')
    print('====================================')
    print('Final FID')
    subprocess.call(f"CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7 torchrun --standalone --nproc_per_node=7 edm/fid.py calc --images=fid-tmp/final \
        --ref=$INPUT_PATH/ffhq-64x64.npz \
        --ref_inc=edm/inception-2015-12-05.pkl", shell=True)
    print('====================================')

    for i in range(n_steps):
        print('====================================')
        print(f'x0_{i} FID')
        subprocess.call(f"CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7 torchrun --standalone --nproc_per_node=7 edm/fid.py calc --images=fid-tmp/x0_{i} \
            --ref=$INPUT_PATH/ffhq-64x64.npz \
            --ref_inc=edm/inception-2015-12-05.pkl", shell=True)
        print('====================================')
    print(
        '===============================================================================================================================')

    shutil.rmtree('fid-tmp')