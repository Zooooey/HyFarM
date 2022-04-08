conda activate fsdet
cd /home/wjing/hfm-workloads/few-shot-object-detection

python3 -m demo.demo --config-file configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_1shot.yaml   --input ../input/bike.jpg --output output/ --opts MODEL.WEIGHTS fsdet://coco/tfa_cos_1shot/model_final.pth  MODEL.DEVICE cpu

python3 -m demo.demo --config-file configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_1shot.yaml   --video-input ../input/test2.mp4 --output output/ --opts MODEL.WEIGHTS fsdet://coco/tfa_cos_1shot/model_final.pth  MODEL.DEVICE cpu
