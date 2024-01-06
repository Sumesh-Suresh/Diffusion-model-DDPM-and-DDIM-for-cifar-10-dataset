## **Forward process equation:**

1. Diffusion rate $\beta_t \in$ [0,1]
2. From the diffusion rate find $\alpha_t$ and $\bar{\alpha_t}$
$$\alpha_t = 1 - \beta_t, \bar{\alpha_t} = \prod_{i=1}^t \alpha_i$$
3. We can find the noisy latents at a timestep $t$ from the original image from the equation:
 $$x_t = \sqrt{\bar{\alpha_t}}x_0 + \sqrt{1 - \bar{\alpha_t}}\epsilon$$

