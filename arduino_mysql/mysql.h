/*
 * mysql
 * Version 1.0 22th of August, 2015
 * Author : Ajay Masi
 * Organisation : Shivy Inc.
 */
#ifndef mysql_h
#define mysql_h

int mysql_connect(char *, char *, char *, char *);
void mysql_close();
int is_mysql();
int mysql_query(char *);
char *mysql_result_query(char *, char *);


#endif