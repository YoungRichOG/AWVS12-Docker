# AWVS12-Docker
Docker&amp;AWVS批量部署


- dockfile、acunetix_trial.sh.zip、patch_awvs放置同一目录

- docker build -t awvs .

- docker run --privileged=true -p 1111:1111-it -d awvs "/sbin/init"

- 进入到docker容器内执行命令：mv patch_awvs mv patch_awvs /home/acunetix/.acunetix_trial/v_190325161/scanner/  
  cd /home/acunetix/.acunetix_trial/v_190325161/scanner/  
  ./patch_awvs  
  chattr +i /home/acunetix/.acunetix_trial/data/license/license_info.json  
  systemctl stop acunetix_trial.service  
  vim /home/acunetix/.acunetix_trial/wvs.ini 修改监听端口 server.port=1111  
  systemctl start acunetix_trial.service  
  
- awvs.py记得修改ip、port、apikey

- 在awvs.py同目录下放置url.txt，内放批量域名

附件:
https://file-1256911118.cos.ap-beijing.myqcloud.com/acunetix_trial.sh.zip
