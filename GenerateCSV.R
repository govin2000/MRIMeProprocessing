
setwd('/Users/gopoudel/Documents/Personal/MRIMe/webdata/script')
indatadir<-'../FreeSurferData/'
outdatadir<-'../csvdata/'


sdate<-'2022_03_14'
sid<-'pid_006_PM'


outputfile<-paste(outdatadir, sdate, "_", sid,".csv", sep="")

map<-read.csv('labelmap.csv')

aseg<-read.csv(paste(indatadir,sid, '_aseg.txt', sep = ""), sep='\t')
lhaparc<-read.csv(paste(indatadir,sid, '_lh_aparc.txt', sep = ""), sep='\t')
rhaparc<-read.csv(paste(indatadir,sid, '_rh_aparc.txt', sep = ""), sep='\t')

all_data<-cbind(aseg,lhaparc,rhaparc)
roi<-map$freesurfer_roi
roi_data<-all_data[roi]
colnames(roi_data)<-map$model_label
t_roi_data<-data.frame(t(roi_data))

write.csv(t(roi_data), outputfile) 

file_list<-list.files(path=outdatadir, pattern="*.csv", full.names = TRUE, recursive = FALSE)

dt_all<-c()
for (fn in file_list) {
  
  dt<-read.csv(fn)
  dt_all<-rbind(dt_all,dt[,2])
  
}

mean_dt<-colMeans(dt_all)

#Write relative data
for (fn in file_list) {
  
  dt<-read.csv(fn)
  rel<-dt[,2]/mean_dt
  dt_w<-cbind(dt[,1],dt[,2],rel)
  colnames(dt_w)<-c("label","absolute","relative")
  write.csv(dt_w,fn)
}


