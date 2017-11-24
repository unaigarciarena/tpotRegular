#!/bin/bash


#########################################
## Parametros que le pasamos al script ##
#########################################
# $1 fichero .jar a ejecutar
# $2 string con los parametros para el .jar
# $3 ficheros adicionales necesarios para
#    para ejecutar el .jar (ej. fichero 
#    .arff de datos, etc)
#########################################

#$ -S /bin/bash
#
#######################################
# Usar el directorio de trabajo actual
#######################################
#$ -cwd

# Tiempo de trabajo
#$ -l h_rt=2400:00:00

# juntar la salida estandar y de error en un solo fichero
#$ -j y
###########################
# usar colas indicadas
###########################

#$ -q 2014all.q,slow.q
#$ -t 1-30:1

#################################
#Nuestro directorio de scratch
##################################
# scratch en kalimero, i2Bask y ATC

PARAMS=(${@:1})

echo "Params: "${PARAMS[@]}

SEED=$SGE_TASK_ID
WORKDIR=$(pwd)
SCRT=/var/tmp/$USER/$JOB_ID-$SGE_TASK_ID

#crear directorio scratch
echo "mkdir -p $SCRT"
mkdir -p $SCRT



##########################################################################################
#creamos los subdirectorios donde queremos guardar los resultados (si no estan creados)
##########################################################################################
mkdir -p $WORKDIR/results
mkdir -p $SCRT/results

#######################################################
#Copiamos los archivos al directorio scratch.
#Usaremos cp -r para copiar tambien subdirectorios.
#Se puede pasar un tercer parametro en el que indicar
#ficheros adicionales a copiar
#######################################################
cp *.py  $SCRT             # We copy all the .py files in TPOT
echo "cp *.py  $SCRT"   
cp -r config  $SCRT        # Copy the whole directory with the operators
echo "cp -r config $SCRT"
cp -r builtins  $SCRT        # Copy the whole directory with the operators
echo "cp -r builtins $SCRT"
cp -r DB  $SCRT        # Copy the whole directory with the operators
echo "cp -r DB $SCRT"
#cp -r venv  $SCRT        # Copy the whole directory with the operators
#echo "cp -r venv $SCRT"


#Nos movemos de directorio
cd $SCRT
#########################
#Ejecutamos el programa
#########################

echo Host --> $HOSTNAME
echo Init Time: `date`

#source venv/bin/activate
echo "python3 $1 $SEED $2 $3 $4>  $SCRT/results/Output_tpotRegular_$2_$3_$4_$SEED"
      python3 $1 $SEED $2 $3 $4>  $SCRT/results/Output_tpotRegular_$2_$3_$4_$SEED
#deactivate

    
# Example of calling the program
# ./main_tpot.py seed dbfilename

mv $SCRT/results/* $WORKDIR/results/
cd ~/
rm -fR $SCRT
echo End  Time: `date`

# qstat -g C

