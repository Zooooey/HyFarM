sudo rmdir /cgroup2/benchmarks/BFSLJTest_wtl
sudo mkdir /cgroup2/benchmarks/BFSLJTest_wtl
echo "mkdir"
sudo sh -c "echo '774564059' > /cgroup2/benchmarks/BFSLJTest_wtl/memory.high"

echo "add to cgroup procs"

sudo sh -c "echo $$  > /cgroup2/benchmarks/BFSLJTest_wtl/cgroup.procs"

VERTEX=4847571

echo "start BFS ${VERTEX}"
taskset -c 3 /usr/bin/time -v /home/wangjing/fargraph-server/test_gridgraph/bin/bin/pagerank /home/wangjing/fargraph-server/dataset/ortest-8/ 20 100000000
echo "done"
