FROM lh1284577/django24:20180220
EXPOSE 22  
CMD [ "/etc/init.d/ssh","start" ]
