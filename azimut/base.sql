INSERT INTO reports.auth_group (id,name) VALUES
	 (5,'АЗИМУТ'),
	 (4,'КУСКОВО'),
	 (3,'НOВОМОСКОВСКИЙ'),
	 (1,'РИК'),
	 (2,'ФЭ');

INSERT INTO reports.auth_user (password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES
	 ('pbkdf2_sha256$600000$jWGmGcFxitizV9XUlbJQEI$Oibz3z9rqJoowSVaCLQVF3KV8uK0hIyzJPwpBq3zLhY=','2023-11-06 09:09:56',1,'admin_azimut','','','admin@admin.ru',1,1,'2023-10-23 13:10:32'),
	 ('pbkdf2_sha256$600000$ai2Vt6TKSRtORdbIcnfhHM$wHRcagT78OIzzd+YWVak5dSPcuJ99Y7dYxMX3OMaAqc=','2023-11-05 10:11:02.874890',0,'fin','','','',0,1,'2023-10-31 14:26:58'),
	 ('pbkdf2_sha256$600000$yM06jid6W5Eu31iuFtn3uR$9PU+Ubwrdm+pWqjtU+c12UlZtCnXZzlRdcxb6980HyM=','2023-11-04 18:54:10.803039',0,'kuskovo','','','',0,1,'2023-10-31 14:32:00'),
	 ('pbkdf2_sha256$600000$V6u56A6I51PtoRDoSspQAh$PZgk7KZAP+K05Fmu9/vVIbKnjk/+TZ2STiTB023yZJk=','2023-11-04 18:53:40',0,'nvmos','','','',0,1,'2023-10-31 14:33:08'),
	 ('pbkdf2_sha256$600000$gwE4xEg5S1K8A0bsOHOa4t$Kh8DsfkTOKU6mwt9H8bS9l/kF/aoCZCl+jNo9hdA+HA=','2023-11-06 09:14:54.076620',0,'azimut_person','','','',0,1,'2023-11-01 15:27:06'),
	 ('pbkdf2_sha256$600000$yLWUTQjCDiPwvMrkYWkQ0r$1DSoEBSVMmD7pGXZ+StDYC/ZnKRmjtU8tO8KAUAaygQ=',NULL,0,'rik','','','',0,1,'2023-11-06 09:10:47');

INSERT INTO reports.reports_object (name) VALUES
	 ('1'),
	 ('2'),
	 ('3'),
	 ('4'),
	 ('5'),
	 ('Кусково'),
	 ('Новомосковский');

INSERT INTO reports.auth_user_groups (user_id,group_id) VALUES
	 (1,5),
	 (2,2),
	 (3,4),
	 (4,3),
	 (5,5),
	 (6,1);

INSERT INTO reports.reports_objectgroup (fee,group_id,object_id) VALUES
	 (30.00,4,6),
	 (33.00,3,7),
	 (16.83,1,1),
	 (16.83,1,2),
	 (16.83,1,3),
	 (16.83,1,4),
	 (16.83,1,5),
	 (16.17,2,1),
	 (16.17,2,2),
	 (16.17,2,3);
INSERT INTO reports.reports_objectgroup (fee,group_id,object_id) VALUES
	 (16.17,2,4),
	 (16.17,2,5),
	 (0.00,5,1),
	 (0.00,5,2),
	 (0.00,5,3),
	 (0.00,5,4),
	 (0.00,5,5),
	 (0.00,5,6),
	 (0.00,5,7);
