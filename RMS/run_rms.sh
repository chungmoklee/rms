docker run \
	-p 5984:5984 \
	-p 8083:8083 \
	-p 8086:8086 \
	-p 51324:51324 \
	-p 6379:6379 \
	-v /Users/cmlee/Documents/DockerWorkspace/web_server:/web_server \
	-v /Users/cmlee/Documents/DockerWorkspace/logs:/usr/local/var/log \
	--name rms_server \
	--rm \
	-it rms1 supervisord