## **Forward process equations:**

1. Diffusion rate $\beta_t \in$ [0,1]
2. From the diffusion rate find $\alpha_t$ and $\bar{\alpha_t}$
   $$\alpha_t = 1 - \beta_t, \bar{\alpha_t} = \prod_{i=1}^t \alpha_i$$
3. Given an input image $x_0$, the forward process sequentially applies a gaussian noise to the image, producing the following conditional distribution:
   $$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t\mathcal{I})$$
4. After reparameterization we get the equation with respect to $x_0$ instead of $x_{t-1}$
   $$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha_t}} x_0, (1 - \alpha_t)\mathcal{I})$$
5. We can find the noisy latents at a timestep $t$ from the original image from the equation:
   $$x_t = \sqrt{\bar{\alpha_t}}x_0 + \sqrt{1 - \bar{\alpha_t}}\epsilon$$
   where $\epsilon$ is pure noise image sampled from $\mathcal{N}(0,\mathcal{I})$  
   
## **Reverse Process equations**
We can get the denoised image by predicting the noise from the network
1. Noise predicted from the network:
   $$\epsilon_t = f(x_t, t)$$
2. Previous timestep image is calculated using the noise predicted by network:
   $$\hat{x_0} = \frac{1}{\sqrt{\bar{\alpha_t}}} (x_t - \sqrt{1 - \bar{\alpha_t}} \epsilon_t)$$
   By repeating this equation we can get the original image $x_0$. (NOTE: $\hat{x_0} represents the previous timestep image)

## Inference Using DDPM 
1. Initialize the $IMG$ as Z where Z is given by $$Z = \mathcal{N}(0,\mathcal{I})$$ 
NOW FOR EACH TIMESTEP:
2. Do the reverse process to find the Previous timestep image $\hat{x_0}$ and $\epsilon_t$
3. find the mean and variance of the distribution using the equations
   $$\tilde{\mu_t} = \frac{\sqrt{\alpha_t} (1 - \bar{\alpha_{t-1}})}{1 - \bar{\alpha_t}} x_t + \frac{\sqrt{\bar{\alpha_{t-1}}}\beta_t}{1 - \bar{\alpha_t}} \hat{x_0}$$
   $$\sigma_t^2 = \tilde{\beta_t} = \frac{1 - \bar\alpha_{t - 1}}{1 - \bar\alpha_t} \beta_t$$
4. update the $IMG$ (with previous image) with the equation:
   $$x_{t - 1} = \tilde{\mu}_t + \sigma_t z$$
   $$IMG = x_{t - 1}$$
5. REPEAT UNTILL $x_0$ IS FOUND AS $IMG$ AND RETURN  $IMG$
   
   

   
