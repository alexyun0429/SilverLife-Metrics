/*
 * mysql
 * Version 1.0 22th of August, 2015
 * Author : Ajay Masi
 * Organisation : Shivy Inc.
 */
#include "Arduino.h"
#include "mysql.h"

int mysql_connect(char *host, char *user, char *pass, char *db){
	Serial.print("host=");
        Serial.println(host);
	Serial.print("user=");
        Serial.println(user);
	Serial.print("pass=");
        Serial.println(pass);
	Serial.print("db=");
        Serial.println(db);
        Serial.println("mysql_connect()");
	int x = Serial.read();
        if(x == '-')
        return 0;
        while( x <= 0){
         x = Serial.read();
         if(x == '-')
           return 0;
        }
    return x-48;
}

int mysql_connect(char *host, char *user, char *pass, char *db){
	Serial.print("is_mysql()");
	int x = Serial.read();
        if(x == '-')
        return 0;
        while( x <= 0){
         x = Serial.read();
         if(x == '-')
           return 0;
        }
    return x-48;
}

void mysql_close(){
	Serial.println("mysql_close()");
}
int mysql_query(char *query){
	Serial.print("query=");
        Serial.println(query);
	int x = Serial.read();
         if(x == '-' || x == '0')
        return 0;
        while( x <= 0){
         x = Serial.read();
         if(x == '-' || x == '0')
           return 0;
        }
    return x-12;
}

String mysql_result_query(String query, String field){
  String res = "";
  String q = query + "&field=" + field;
  Serial.println(q);
  res = Serial.readString();
  if(res == "-")
  return 0;
  while(res.length() <= 0){
  res = Serial.readString();  
  if(res == "-")
  return 0;
  }
  return res;
}