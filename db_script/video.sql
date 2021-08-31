INSERT INTO `teacher` VALUES (1,now(),now(),0,'西蓝花','主任','是一个优秀的讲师','/media/111.jpg'),
(2,now(),now(),0,'九牧村','院长','德高望重，气宇轩昂','/media/head.jpg');


INSERT INTO `course_category` (name ,update_time,is_delete,create_time) VALUES
('python基础',now(),0,now()),
('java',now(),0,now()),
('web前端',now(),0,now());

INSERT INTO `course` VALUES
(1,now(),now(),0,'集美大桥','http://me7tbcb2hrmacnc0gsw.exp.bcevod.com/mda-me7vzh6039ivwar6/mda-me7vzh6039ivwar6.jpg','http://me7tbcb2hrmacnc0gsw.exp.bcevod.com/mda-me7vzh6039ivwar6/mda-me7vzh6039ivwar6.m3u8','这里是课程视频的简介','大纲1,2,3',3,2),
(2,now(),now(),0,'朋友','http://me7tbcb2hrmacnc0gsw.exp.bcevod.com/mda-me7vsah14hrunsxf/mda-me7vsah14hrunsxf.jpg','http://me7tbcb2hrmacnc0gsw.exp.bcevod.com/mda-me7vsah14hrunsxf/mda-me7vsah14hrunsxf.m3u8','这里是课程视频的简介','大纲1,2,3',1,1);