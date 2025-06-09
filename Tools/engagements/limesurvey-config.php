<?php

if (!defined('BASEPATH')) {
    exit('No direct script access allowed');
}

return array(
    'components' => array(
        'db' => array(
            'connectionString' => 'pgsql:host=limesurvey_db;port=5432;dbname=limesurvey;',
            'username' => 'limesurvey_user',
            'password' => 'limesurvey_password',
            'charset' => 'utf8',
            'tablePrefix' => 'lime_',
            'emulatePrepare' => true,
        ),
        'session' => array(
            'class' => 'application.core.web.DbHttpSession',
            'connectionID' => 'db',
            'sessionTableName' => '{{sessions}}',
            'autoCreateSessionTable' => false,
        ),
    ),
    'config' => array(
        'rootdir' => '/var/www/html',
        'sitename' => 'Ledger Security Assessment Survey Platform',
        'defaultuser' => 'admin',
        'defaultpass' => 'admin123',
        'databasetype' => 'pgsql',
        'databasehost' => 'limesurvey_db',
        'databaseport' => '5432',
        'databasename' => 'limesurvey',
        'databaseuser' => 'limesurvey_user',
        'databasepass' => 'limesurvey_password',
        'databasetableprefix' => 'lime_',
        'publicurl' => 'http://localhost:8080/',
        'tempdir' => '/var/www/html/tmp',
        'uploaddir' => '/var/www/html/upload',
        'debug' => 0,
        'debugsql' => 0,
    )
); 