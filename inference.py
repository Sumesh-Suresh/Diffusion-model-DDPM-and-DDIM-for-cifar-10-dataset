import argparse
import os
import torch

from model import DiffusionModel
from unet import Unet
from torchvision.utils import save_image
from cleanfid import fid as cleanfid

@torch.no_grad()
def get_fid(gen, dataset_name, dataset_resolution, z_dimension, batch_size, num_gen):
    # diffusion model given z
    # The output must be in the range [0, 255]!
    z_shape = (batch_size,gen.channels,dataset_resolution,dataset_resolution)
   
    def get_fn(z):
        images = gen.sample_given_z(z,z_shape)
        gen_image = torch.clamp((images-images.min())/(images.max()-images.min())*255,0,255)

        return gen_image

    score = cleanfid.compute_fid(
        gen= get_fn,
        dataset_name=dataset_name,
        dataset_res=dataset_resolution,
        num_gen=num_gen,
        z_dim=z_dimension,
        batch_size=batch_size,
        verbose=True,
        dataset_split="train",
    )
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diffusion Model Inference')
    parser.add_argument('--ckpt', required=True, type=str, help="Pretrained checkpoint")
    parser.add_argument('--num-images', default=100, type=int, help="Number of images per iteration")
    parser.add_argument('--image-size', default=32, type=int, help="Image size to generate")
    parser.add_argument('--sampling-method', choices=['ddpm', 'ddim'])
    parser.add_argument('--ddim-timesteps', type=int, default=25, help="Number of timesteps to sample for DDIM")
    parser.add_argument('--ddim-eta', type=int, default=1, help="Eta for DDIM")
    parser.add_argument('--compute-fid', action="store_true")
    args = parser.parse_args()

    prefix = f"data_{args.sampling_method}/"
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    sampling_timesteps = args.ddim_timesteps if args.sampling_method == "ddim" else None

    model = Unet(
        dim=64,
        dim_mults=(1, 2, 4, 8)
    ).cuda()
    diffusion = DiffusionModel(
        model,
        timesteps=1000,   # number of timesteps
        sampling_timesteps=sampling_timesteps,
        ddim_sampling_eta=args.ddim_eta,
    ).cuda()

    img_shape = (args.num_images, diffusion.channels, args.image_size, args.image_size)

    # load pre-trained weight
    ckpt = torch.load(args.ckpt)
    model.load_state_dict(ckpt["model_state_dict"])

    with torch.no_grad():
        # run inference
        model.eval()
        if args.sampling_method == "ddpm":
            generated_samples = diffusion.sample(img_shape)
        elif args.sampling_method == "ddim":
            generated_samples = diffusion.sample(img_shape)
        save_image(
            generated_samples.data.float(),
            prefix + f"samples_{args.sampling_method}.png",
            nrow=10,
        )
        if args.compute_fid:
            # NOTE: This will take a very long time to run even though 10K samples are used.
            score = get_fid(diffusion, "cifar10", 32, 32*32*3, batch_size=256, num_gen=10_000)
            print("FID: ", score)
