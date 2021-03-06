# Dark Matter (DM)

## Introduction

The problem of the DM in the universe, together with the explanation of dark energy, is still one of the major unsolved problems in cosmology, astrophysics and particle physics. Its identity links studies of the universe at both the largest and smallest observable scales. The DM problem, historically termed as the missing matter problem, was proposed by Fritz Zwicky in 1933, when his research on the Coma galaxy cluster inferred the existence of an anomaly. The virial theorem allows the calculation of galaxy masses making use of gravitational attraction. Zwicky calculated the theoretical galaxy cluster mass using the rotational velocity of luminous matter, and observed a discrepancy with the measured galaxy cluster mass. For the coming years various DM evidences were found, all of them based on gravitational interactions. However, given the universality of gravity, these evidences give very little information about the nature of DM.

The Planck mission's final data release (2018) showed that the dark energy density in the universe is Ω_λ ≈ 0.68, while matter density is Ω_m h^2 ≈ 0.32, from which around 85% is non-baryonic. None of the Standard Model particles is a good DM candidate; most of them are unstable, with lifetimes far shorter than the age of the universe, and the rest contribute to the baryonic energy density Ω_b, which is too small to be considered as a possibility. A vast majority of the scientific community believes that the evidence for DM requires particles beyond the Standard Model. Neutralinos, gravitinos, sterile neutrinos, axions and other particles related to hidden dark sectors, such as dark photons, are some of the researched candidates. Lately non-fundamental particles such as SIMPS (strongly interacting massive particles), and macroscopic objects such as primordial black holes, have also been proposed as DM candidates. Nonetheless, a minor part of the community does not believe in DM; they believe that the theory of gravitation is not complete, and work with alternative theories of gravity, such as Modified Newtonian dynamics (MOND).

Three strategies are followed for DM detection: accelerators, direct and indirect detection:

<p align="center">
<img src="https://github.com/aritzLizoain/CNN-Image-segmentation/blob/master/Images/Example_Images/DM_Detection_Methods.jpg" width="450"/>
</p>

*Sketch of different types of search strategies for DM detection. Digital Image. Virdee, T. S. "Beyond the standard model of particle physics". (Royal Society, 2016). [Link](https://royalsocietypublishing.org/doi/10.1098/rsta.2015.0259).*


## DAMIC/DAMIC-M

In this study the direct search strategy is followed. It is a huge endeavor to develop experiments able to directly investigate the particle nature of DM. These experiments aim to identify recoils produced by the scattering between the theoretical DM particles and a detector's target nuclei or electron. Specifically in this research, the silicon of the CCDs is used as a target.

<p align="center">
<img src="https://github.com/aritzLizoain/CNN-Image-segmentation/blob/master/Images/Example_Images/DM_particle_and_detector_scattering.png" width="500"/>
</p>

*Nuclear recoil produced by the scattering between a DM particle and a detector's Si nucleus. Digital image. Aguilar-Arevalo, A. et al. "Measurement of radioactive contamination in the CCD’s of the DAMIC experiment". (Journal of Physics, 2015). [Link](https://arxiv.org/pdf/1506.02562.pdf).*

This kind of experiments are very sensitive to any radiation background, either from the construction material or cosmogenic. Moreover, the collision signals are expected to be rare and low (keV scale and below). In order to screen out the radiation background, the material is thoroughly assayed. In addition, carrying out the measurements in a subterranean location, inside a mountain or a mine, shielded from cosmic-rays induced events, is key to achieve sensitivity to DM particle detection.

Previously calibrated and tested 675 μm-thick (approx. 15g each) CCDs are located inside an electroformed copper box, used for screening purposes. The 36MP CCDs have a very low radiation background (0.1/event/kg/day/keV) and a resolution better than 1e- by means of the skipper readout system. The operating temperature can range between 135-140K and a maximum of 240K. An array of 50 skipper CCDs will constitute the future DAMIC-M experiment located in the Laboratoire Souterrain de Mondane facility (France), which is still finalizing its design and is scheduled to be installed by the end of 2023. Nevertheless, the collaboration has been studying this technology approximately since 2012 and data has been taken from the DAMIC experiment located at SNOLAB (Canada). The data from DAMIC is the one that has been used in this project.

CCD images contain a high-resolution two-dimensional projection on the XY plane of the charge deposits in the active volume of the device. The DAMIC data has been acquired with two different readout configurations: 1X1 and 1X100. The first one is the standard CCD readout, reading each pixel individually. On the second one instead, columns of 100 pixel rows are read individually. The image readout times are 24h and 8h, respectively for the 1X1 and 1X100 setups. Immediately after taking the image, a "blank" image is acquired, whose exposure is only a few seconds. Since the occurrence of a physical event during each readout mode is <5% and <0.1% (respectively for 1X1 and 1X100), most blank images contain only the image noise. The total exposure time presents a statistically consistent white noise distribution. 

Different ionizing particles in a CCD include: straight track-shaped cosmic ray muons, large drop-shaped alpha particles, "worm"-shaped straggling electrons, and low-energy candidates, characterized by small round clusters.

<p align="center">
<img src="https://github.com/aritzLizoain/CNN-Image-segmentation/blob/master/Images/Example_Images/DAMIC_CCD_image_and_signatures_of_ionizing_particles.jpeg" width="400"/>
</p>

*Signatures of different ionizing particles in a CCD (processed image). Adapted Digital image. Aguilar-Arevalo, A. et al. "Measurement of radioactive contamination in the CCD’s of the DAMIC experiment". (Journal of Physics, 2015). [Link](https://arxiv.org/pdf/1506.02562.pdf).*

Furthermore, the ionizing particles need to be distinguished from noise signals such as hot pixels (i.e. pixels which look much brighter than they should), glowing and any other issue with the pixels. The major research problem is the difficulty involved in correctly masking out the background noise; signals from ionizing particles are almost at the same energy level as the background. In order to face the challenge of discriminating the different ionizing particles from the background noise, machine learning is proposed as a solution.

The goal of this project is to implement an innovative deep learning application able to extract all the information from the detector images. An automated quality monitoring system is sought with the purpose of identifying the main defects associated to the detector. Four main categories are discriminated on each image: background, glowing, hot pixels and pixel clusters. The ML algorithm implemented on the images performs a behavior generalization seeking to uncover the signal of each category. Thus, the output shows all the practical information at a glance; an ideal segmented image is displayed making each category clearly distinguishable. As a result, pixel clusters can be differentiated, leading to further research. 