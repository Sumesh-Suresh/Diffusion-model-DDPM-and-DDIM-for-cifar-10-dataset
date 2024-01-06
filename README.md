Forward process equation:


1. $q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha_t}} x_0, (1 - \alpha_t)\mathcal{I})$
(This is equation is derived after reparameterization)
2. $\alpha_t = 1 - \beta_t, \bar{\alpha_t} = \prod_{i=1}^t \alpha_i$
where $\beta_t$ lies between 0 and 1.
3. 

