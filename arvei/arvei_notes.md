Computer Architecture Department							R. Tous
Universitat Politecnica de Catalunya. BarcelonaTech (UPC)                                                                       
                                                              
															  
															  
					Arvei Notes

1. Information about the cluster:

Cluster features (nodes, queues, etc.): 

	https://www.ac.upc.edu/app/wiki/serveis-tic/Clusters/Users/arvei

Howto:

	https://www.ac.upc.edu/app/wiki/serveis-tic/Clusters/Users/FuncionamentGeneral

More:

	https://www.ac.upc.edu/app/wiki/serveis-tic/Clusters/Users

2. Excuting long jobs (up to 60 hours):

	qsub -l big ...

3. Problems installing lxml

Initially I managed to install lxml==4.2.1 but I don't know how. Maybe an update in arvei changed the environment. Two dependencies seem to be wrong:

which xml2-config
which xslt-config

I solved the first one with:

	CFLAGS=-I/usr/include/libxml2 pip install lxml

But not the second one. Finally y downloaded the wheel:

wget --no-check-certificate https://www.silx.org/pub/wheelhouse/old/lxml-3.4.4-cp27-none-linux_x86_64.whl
