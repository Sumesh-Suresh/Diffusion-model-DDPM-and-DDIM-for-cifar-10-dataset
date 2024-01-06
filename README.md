## **Forward process equation:**

1. Diffusion rate $\beta_t \in$ [0,1]
2. From the diffusion rate find $\alpha_t$ and $\bar{\alpha_t}$
   $$\alpha_t = 1 - \beta_t, \bar{\alpha_t} = \prod_{i=1}^t \alpha_i$$
3. Given an input image $x_0$, the forward process sequentially applies a gaussian noise to the image, producing the following conditional distribution:
   $$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t\mathcal{I})$$
4. After reparameterization we get the equation with respect to $x_0$ instead of $x_{t-1}$
   $$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha_t}} x_0, (1 - \alpha_t)\mathcal{I})$$
6. We can find the noisy latents at a timestep $t$ from the original image from the equation:
   $$x_t = \sqrt{\bar{\alpha_t}}x_0 + \sqrt{1 - \bar{\alpha_t}}\epsilon$$
   where $\epsilon$ is pure noise image sampled from $\mathcal{N}(0,\mathcal{I})$

