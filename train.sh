!/bin/bash
# Must launch with qsub -S /bin/bash ./noise.sh
#!/bin/sh
### Directivas para el gestor de colas (modificar los valores NAMEOFJOB y USERNAME, y mantener la opción "-S")
# Cambiar el nombre del trabajo
#$ -N NAMEOFJOB
# Especificar un shell
#$ -S /bin/sh
# Enviame un correo cuando empiece el trabajo y cuando acabe...
#$ -m be
# ... a esta dirección de correo
#$ -M nobody@ac.upc.edu

CSCRATCH=/scratch/nas/4/`whoami`
DATA=data.$JOB_ID

### Crear zona de datos local y transferir datos
#mkdir $DATA
#rsync $CSCRATCH/exSimul/data $DATA
# La otra opción es que la aplicación lea de $CSCRATCH

### Ejecutar
CURRENT_ENVIRONMENT=`ls -d /scratch/nas/4/rtous`/convnetquake
source $CURRENT_ENVIRONMENT/bin/activate
cd /scratch/nas/4/rtous/ConvNetQuake/
export PYTHONPATH=.
./bin/train --dataset data/6_clusters/train2 --checkpoint_dir output/convnetquake --n_clusters 6
### Copiar salida (comprimida)
#gzip -c $DATA/output-$1-$2 > $CSCRATCH/out/output-$1-$2.gz

### Borrar zona datos local
rm -rf $DATA