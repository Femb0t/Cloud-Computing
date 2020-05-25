pt1 - mapper.py, reducer.py
pt1 output - mapOut.txt, reduceOut.txt ;output when running locally
	     part1-output ;hadoop output folder

pt2 - mapper1.py, reducer1.py
pt2 output - map2Out.txt, reduce2Out.txt, reduce2OutPt2.txt ;output when running locally
	     crimeData-output2 ;hadoop output folder
             crimeData-2tasks ;hadoop output folder for running with 2 tasks 

$HADOOP_PREFIX/bin/hadoop fs -rmr /user/cc/crimeData-output2

$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/contrib/streaming/hadoop-streaming-*.jar \
-input /user/cc/crimeData/input.csv \
-output /user/cc/crimeData-output2 \
-file /home/cc/mapper.py \
-mapper /home/cc/mapper.py \
-file /home/cc/reducer.py \
-reducer /home/cc/reducer.py

$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/contrib/streaming/hadoop-streaming-*.jar \
-input /user/cc/crimeData/input.csv \
-output /user/cc/crimeData-output2 \
-file /home/cc/mapper1.py \
-mapper /home/cc/mapper1.py \
-file /home/cc/reducer1.py \
-reducer /home/cc/reducer1.py

2 tasks

$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/contrib/streaming/hadoop-streaming-*.jar \
-D mapred.reduce.tasks=2 \
-input /user/cc/crimeData/input.csv \
-output /user/cc/crimeData-output2 \
-file /home/cc/mapper1.py \
-mapper /home/cc/mapper1.py \
-file /home/cc/reducer1.py \
-reducer /home/cc/reducer1.py

copy to main dir
$HADOOP_PREFIX/bin/hadoop fs -get /user/cc/crimeData-output2 ~/