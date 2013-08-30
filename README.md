
===================

paralell inparanoid
AKA
parapy

===================

Parapy is a multiprocessing wrapper of Inparanoid software.
The parallelization of Inparanoid is useful when there are a lot of genomes, therefore launching inparanoid over all the combinations would require too much time.

===================

To work, it needs:
  - a directory with Inparanoid scripts (all the scripts required by inparanoid.pl to work)
  - a directory with all the genomes
  - python and all the modules in the script

===================

Parapy will create a Job Queue, enqueueing Inparanoid jobs for all the Genome pairs.
For each Consumer (process), a directory will be created (if not existent), and the inparanoid scripts are copied into it.
The consumer is fed with a job from the queue, then the sequences of correspondent genome pair are copied into the consumer directory.
Inparanoid runs, then the outputs are copied into the main directory (directory where is present parapy.py).

===================


  
