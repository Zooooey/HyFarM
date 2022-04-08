gpu2   /home/wjing/hfm-workloads/

1. quicksort
cd /home/wjing/hfm-workloads/
/usr/bin/time -v ./quicksort/quicksort  2047
/usr/bin/time -v ./quicksort/quicksort  8096

2. ffmpeg 
cd /home/wjing/hfm-workloads/
rm /output/out*
/usr/bin/time -v  ./ffmpeg-4.4.1/ffmpeg -i input/duye.mkv output/out-duye.mkv
/usr/bin/time -v  ./ffmpeg-4.4.1/ffmpeg -i input/avengers.mkv output/out-avergers.mkv

3. fsdet
conda activate fsdet
cd /home/wjing/hfm-workloads/few-shot-object-detection

python3 -m demo.demo --config-file configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_1shot.yaml   --input ../input/bike.jpg --output output/ --opts MODEL.WEIGHTS fsdet://coco/tfa_cos_1shot/model_final.pth  MODEL.DEVICE cpu

python3 -m demo.demo --config-file configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_1shot.yaml   --video-input ../input/test2.mp4 --output output/ --opts MODEL.WEIGHTS fsdet://coco/tfa_cos_1shot/model_final.pth  MODEL.DEVICE cpu

4. ligra
cd /home/wangjing/ligra-master
##./utils/rMatGraph 10000000  inputs/rMat_10000000
./apps/BFS -s -r 1 inputs/rMat_10000000
./apps/BFS -s -r 1 inputs/rMat_40000000
./apps/PageRank -s -r 1 inputs/rMat_10000000
./apps/PageRank -s -r 1 inputs/rMat_40000000

5. gridgraph
cd  /home/wangjing/fargraph-client/test_gridgraph
./bin/bfs aaaGrid4 0 1
./bin/bfs ../dataset/twtest-8/ 0 1
./bin/pagerank ../dataset/twtest-8/ 2
./bin/pagerank ../dataset/twtest-8/ 20

6. tensorflow
cd /home/wjing/hfm-workloads/
./tf-inception.sh
./tf-resnet.sh
