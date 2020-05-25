#code must first be copied to both master and slave (dos2unix if edited on windows)

#go to spark folder
cd /usr/local/spark-1.6.1-bin-hadoop1

#start master
./sbin/start-master.sh 

#start slave
./sbin/start-slaves.sh 

#optional: to see if master and slave have started
jps

#run the code (example is with extraCredit.py saved to the default root directory)
./bin/spark-submit --master spark://10.230.119.206:7077 ~/extraCredit.py

#make sure any changes are on both master and slave by copying the file
scp /home/cc/extraCredit.py 129.114.25.60: