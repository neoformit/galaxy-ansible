# Debugging Galaxy ITs server

> Followed
[tutorial](https://training.galaxyproject.org/training-material/topics/admin/tutorials/interactive-tools/tutorial.html)
through to the end. Listed ITs are exposed in the Galaxy UI and run without
explicit error, but go into infinite loading/polling.

- [x] `galaxy-gie-proxy` service is running ok
- [x] `journalctl` - logs show container pull and run without error
- [x] `docker ps` - shows container running
- [x] Add `gie_proxy_verbose: true` to Ansible conf
- [x] `curl` docker container to check port
      - *Doesn't seem to work* but unsure whether it should
- [x] Update `gie_proxy_*` variables to match [usegalaxy.eu](https://galaxy.ansible.com/usegalaxy_eu/gie_proxy) example
- [x] Nuke `/srv/galaxy` dir and rerun playbook

- [ ] Check `interactivetools_map.sqlite` for port mapping entry

---

### Log output

> Prettified for readability

**Docker container pull and launch**
```
Jul 23 01:37:53 cam-gx-dev uwsgi[309675]: [ $? -ne 0 ] && docker pull shiltemann/ethercalc-galaxy-ie:17.05 > /dev/null 2>&1
Jul 23 01:37:53 cam-gx-dev uwsgi[309675]:
    docker run
      -e "GALAXY_SLOTS=$GALAXY_SLOTS"
      -e "HOME=$HOME"
      -e "_GALAXY_JOB_HOME_DIR=$_GALAXY_JOB_HOME_DIR"
      -e "_GALAXY_JOB_TMP_DIR=$_GALAXY_JOB_TMP_DIR"
      -e "TMPDIR=$TMPDIR"
      -e "TMP=$TMP"
      -e "TEMP=$TEMP"
      -p 8000
      --name 2510effbbd2b4d9fbd43d57c0ff62051
      -v /srv/galaxy/server:/srv/galaxy/server:ro
      -v /srv/galaxy/server/tools/interactive:/srv/galaxy/server/tools/interactive:ro
      -v /srv/galaxy/jobs/000/69:/srv/galaxy/jobs/000/69:ro
      -v /srv/galaxy/jobs/000/69/outputs:/srv/galaxy/jobs/000/69/outputs:rw
      -v /srv/galaxy/jobs/000/69/configs:/srv/galaxy/jobs/000/69/configs:rw
      -v /srv/galaxy/jobs/000/69/working:/srv/galaxy/jobs/000/69/working:rw
      -v /data:/data:rw
      -v /srv/galaxy/var/tool-data:/srv/galaxy/var/tool-data:ro
      -v /srv/galaxy/var/tool-data:/srv/galaxy/var/tool-data:ro
      -v "$_GALAXY_JOB_TMP_DIR:$_GALAXY_JOB_TMP_DIR:rw"
      -w /srv/galaxy/jobs/000/69/working
      --net bridge
      --rm shiltemann/ethercalc-galaxy-ie:17.05
      /bin/sh /srv/galaxy/jobs/000/69/tool_script.sh > ../outputs/tool_stdout 2> ../outputs/tool_stderr; return_code=$?; cd '/srv/galaxy/jobs/000/69';
```

```
Jul 23 01:37:55 cam-gx-dev systemd[1]:
    var-lib-docker-overlay2-0e08cee8a783501ab57754245c97bbbbd5d2f0b9704e4501c2d6ffcb58b80a41\x2dinit-merged.mount: Succeeded.
Jul 23 01:37:55 cam-gx-dev systemd[276200]:
    var-lib-docker-overlay2-0e08cee8a783501ab57754245c97bbbbd5d2f0b9704e4501c2d6ffcb58b80a41\x2dinit-merged.mount: Succeeded.
Jul 23 01:37:55 cam-gx-dev systemd[276200]:
    var-lib-docker-overlay2-0e08cee8a783501ab57754245c97bbbbd5d2f0b9704e4501c2d6ffcb58b80a41-merged.mount: Succeeded.
Jul 23 01:37:55 cam-gx-dev systemd[1]:
    var-lib-docker-overlay2-0e08cee8a783501ab57754245c97bbbbd5d2f0b9704e4501c2d6ffcb58b80a41-merged.mount: Succeeded.
```

**Networking warning etc that might be an issue?**
```
Jul 23 01:37:55 cam-gx-dev kernel: docker0: port 1(veth05140c9) entered blocking state
Jul 23 01:37:55 cam-gx-dev kernel: docker0: port 1(veth05140c9) entered disabled state
Jul 23 01:37:55 cam-gx-dev kernel: device veth05140c9 entered promiscuous mode
Jul 23 01:37:55 cam-gx-dev systemd-networkd[246789]: veth05140c9: Link UP
Jul 23 01:37:55 cam-gx-dev networkd-dispatcher[511]: WARNING:Unknown index 10 seen, reloading interface list
Jul 23 01:37:55 cam-gx-dev systemd-udevd[332516]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Jul 23 01:37:55 cam-gx-dev systemd-udevd[332516]: Using default interface naming scheme 'v245'.
Jul 23 01:37:55 cam-gx-dev systemd-udevd[332516]: veth1f0d1af: Could not generate persistent MAC: No data available
Jul 23 01:37:55 cam-gx-dev systemd-udevd[332517]: ethtool: autonegotiation is unset or enabled, the speed and duplex are not writable.
Jul 23 01:37:55 cam-gx-dev systemd-udevd[332517]: Using default interface naming scheme 'v245'.
Jul 23 01:37:55 cam-gx-dev systemd-udevd[332517]: veth05140c9: Could not generate persistent MAC: No data available
```

**But then it seems to get over that**
```
Jul 23 01:37:55 cam-gx-dev containerd[209915]: time="2021-07-23T01:37:55.541722362Z" level=info msg="starting signal loop" namespace=moby path=/run/containerd/io.containerd.runtime.v2.task/moby/fe8ab50947d4c315caf8027103b7dec29fa31071bb74ba0c62c306a659210b7e pid=332561
Jul 23 01:37:55 cam-gx-dev kernel: eth0: renamed from veth1f0d1af
Jul 23 01:37:55 cam-gx-dev systemd-networkd[246789]: veth05140c9: Gained carrier
Jul 23 01:37:55 cam-gx-dev systemd-networkd[246789]: docker0: Gained carrier
Jul 23 01:37:55 cam-gx-dev kernel: IPv6: ADDRCONF(NETDEV_CHANGE): veth05140c9: link becomes ready
Jul 23 01:37:55 cam-gx-dev kernel: docker0: port 1(veth05140c9) entered blocking state
Jul 23 01:37:55 cam-gx-dev kernel: docker0: port 1(veth05140c9) entered forwarding state
```

**Docker container found by galaxy**
```
Jul 23 01:37:56 cam-gx-dev uwsgi[309675]:
 galaxy.jobs DEBUG 2021-07-23 01:37:56,116 [p:309675,w:0,m:1]
  [LocalRunner.work_thread-0] found container runtime {
    '8000': {
      'tool_port': 8000,
      'host': '45.113.234.221',
      'port': 49156,
      'protocol': 'tcp'
    }
  }
```

**Now we just go into infinite polling**
```
Jul 23 01:37:57 cam-gx-dev uwsgi[309672]: 125.168.246.82 - - [23/Jul/2021:01:37:57 +0000] "GET /api/histories/5752094d537323e0/contents?order=hid&v=dev&q=update_time-ge&q=deleted&q=purged&qv=2021-07-23T01%3A37%3A53.000Z&qv=False&qv=False HTTP/1.1" 200 - "https://cam-gx-dev.gvl.org.au/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"

...

```
