# sudo rmdir /cgroup2/benchmarks/BFSLJTest_wtl
# sudo mkdir /cgroup2/benchmarks/BFSLJTest_wtl
sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"
sudo rmdir /sys/fs/cgroup/memory/farmemory
sudo mkdir /sys/fs/cgroup/memory/farmemory
# echo "mkdir"
# sudo sh -c "echo '100' > /cgroup2/benchmarks/BFSLJTest_wtl/memory.high"
sudo sh -c "echo -1 > /sys/fs/cgroup/memory/farmemory/memory.limit_in_bytes"
echo "add to cgroup procs"

sudo sh -c "echo $$  > /sys/fs/cgroup/memory/farmemory/cgroup.procs"

# VERTEX=4847571

# echo "start BFS ${VERTEX}"
# taskset -c 3 /usr/bin/time -v /home/wjing/hfm-workloads/quicksort/quicksort 2047
/usr/bin/time -v /home/wjing/hfm-workloads/tensorflow/tf-resnet.sh
echo "done"
