#!/bin/bash
printf "POST /upload HTTP/1.1\r\nContent-Type: application/sdadasdax-www-form-urlencoded\r\nuid=123\%26x=234\%26z=345" | nc localhost 5000
