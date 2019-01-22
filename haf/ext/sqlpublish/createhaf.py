create_case = [ """
CREATE TABLE `case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ids_id` varchar(255) DEFAULT NULL,
  `run` int(255) DEFAULT NULL,
  `dependent` varchar(255) DEFAULT NULL,
  `bench_name` varchar(255) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `response_id` int(11) DEFAULT NULL,
  `expect_id` int(11) DEFAULT NULL,
  `sqlinfo_id` int(11) DEFAULT NULL,
  `type` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""
,
                '''
CREATE TABLE `case_expect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) DEFAULT NULL,
  `sql_check_func` varchar(255) DEFAULT NULL,
  `sql_response_result` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
                '''DROP TABLE IF EXISTS `case_ids`;
CREATE TABLE `case_ids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` int(11) DEFAULT NULL,
  `case_sub_id` int(11) DEFAULT NULL,
  `case_name` varchar(255) DEFAULT NULL,
  `case_api_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
'''
CREATE TABLE `case_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `header` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `method` varchar(255) DEFAULT NULL,
  `protocol` varchar(255) DEFAULT NULL,
  `host_port` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''

,
                '''
CREATE TABLE `case_response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `header` varchar(255) DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
                      '''
CREATE TABLE `case_sqlinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scripts_id` int(11) DEFAULT NULL,
  `config` varchar(255) DEFAULT NULL,
  `config_id` int(11) DEFAULT NULL,
  `check_list_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
                      '''
CREATE TABLE `case_sqlinfo_checklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
                                '''
CREATE TABLE `case_sqlinfo_config` (
  `id` int(11) NOT NULL,
  `host` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
                        '''
CREATE TABLE `case_sqlinfo_script` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
                             '''
CREATE TABLE `detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) DEFAULT NULL,
  `result_check_response` varchar(255) DEFAULT NULL,
  `result_check_sql_response` varchar(255) DEFAULT NULL,
  `run_error` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `log_dir` varchar(255) DEFAULT NULL,
  `runner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
'''
CREATE TABLE `main` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration_time` time DEFAULT NULL,
  `passed` int(255) DEFAULT NULL,
  `failed` int(255) DEFAULT NULL,
  `skip` int(255) DEFAULT NULL,
  `error` int(255) DEFAULT NULL,
  `suite_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;'''
,
 '''
CREATE TABLE `suite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `main_id` int(11) NOT NULL,
  `suite_name` varchar(255) NOT NULL
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
,
               '''
CREATE TABLE `summary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `passed` int(255) DEFAULT NULL,
  `failed` int(255) DEFAULT NULL,
  `skip` int(255) DEFAULT NULL,
  `error` int(255) DEFAULT NULL,
  `all` int(255) DEFAULT NULL,
  `base_url` varchar(255) DEFAULT NULL,
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration_time` int(11) DEFAULT NULL,
  `suite_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `suite_id` (`suite_id`),
  CONSTRAINT `suite_id` FOREIGN KEY (`suite_id`) REFERENCES `suite` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
]
