
# Goal:

**1) Modify existing GAN model to improve the quality of the output image**

- used DCGAN(Deep Convolutional GAN) to generate images of people that look like celebrities using Celeb-A Faces dataset
- Modified the size of latent vector, feature map(ngf) and the number of training epochs to reduce discriminator loss


I modified values in the inputs section:
-- Changed value of nz from 100 to 200
-- Changed number of training epochs to 10
